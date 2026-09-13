#!/usr/bin/env python3
"""Bounded DSH stage runner. File delivery is not scientific acceptance.

No model calls in check mode. Outputs and runtime journals stay under --root.
Worker input isolation is a task contract, not a filesystem security sandbox.
"""
import argparse
import concurrent.futures
from contextlib import contextmanager
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import threading
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    temp = path.with_suffix('.tmp')
    with temp.open('w') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)


def relative(root, name):
    p = (root / name).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError('artifact escapes run root')
    return p


def check(plan):
    if not 1 <= plan['parallel'] <= 2:
        raise ValueError('parallel must be 1 or 2')
    if not 60 <= plan['total_seconds'] <= 28800:
        raise ValueError('total wall-clock budget out of range')
    seen = set()
    for stage in plan['stages']:
        sid = stage['id']
        if not sid or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in sid) or sid in seen:
            raise ValueError('invalid/duplicate stage id')
        if not set(stage['depends']).issubset(seen):
            raise ValueError('dependencies must appear earlier')
        if not 1 <= stage['seconds'] <= 3600 or not stage['prompt'].strip():
            raise ValueError('invalid stage budget/prompt')
        if not stage['outputs'] or 'result.json' not in stage['outputs']:
            raise ValueError('result.json envelope required')
        for name in stage['outputs']:
            relative(Path('/validation-root'), name)
        seen.add(sid)


def deliverable(folder, names):
    for name in names:
        p = relative(folder, name)
        if not p.is_file() or p.stat().st_size == 0:
            raise ValueError('missing/empty output: ' + name)
    result = json.loads((folder / 'result.json').read_text())
    if result.get('outcome') not in {'findings', 'accept', 'revise', 'reject', 'unavailable', 'no_viable_candidate'}:
        raise ValueError('invalid outcome')
    if not isinstance(result.get('summary'), str) or not result['summary'].strip():
        raise ValueError('summary required')
    if not isinstance(result.get('open_questions'), list):
        raise ValueError('open_questions required')
    return result


def stop_process_group(proc):
    # Only process groups created by this runner with start_new_session=True.
    if proc.pid <= 1:
        raise ValueError('invalid owned process group')
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        pass
    # The group leader may exit while a descendant ignores TERM.
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait()


@contextmanager
def termination_event():
    event = threading.Event()
    old = {}
    if threading.current_thread() is threading.main_thread():
        for sig in (signal.SIGINT, signal.SIGTERM):
            old[sig] = signal.signal(sig, lambda *_: event.set())
    try:
        yield event
    finally:
        for sig, handler in old.items():
            signal.signal(sig, handler)


def verify_receipt(folder):
    receipt = json.loads((folder / 'receipt.json').read_text())
    if receipt.get('state') != 'delivered':
        raise ValueError('dependency not delivered')
    for name, fingerprint in receipt['output_hashes'].items():
        if sha(relative(folder, name)) != fingerprint:
            raise ValueError('delivered dependency changed: ' + name)
    return receipt


def execute(root, stage, plan, deadline, command=None, stop=None):
    folder = root / 'jobs' / stage['id']
    folder.mkdir(parents=True, exist_ok=False)
    inputs = {}
    if (root / 'SOURCES.md').is_file():
        inputs[str(root / 'SOURCES.md')] = sha(root / 'SOURCES.md')
    for dep in stage['depends']:
        dep_folder = root / 'jobs' / dep
        receipt = verify_receipt(dep_folder)
        for name, fingerprint in receipt['output_hashes'].items():
            inputs[str(relative(dep_folder, name))] = fingerprint
        inputs[str(dep_folder / 'receipt.json')] = sha(dep_folder / 'receipt.json')
    prompt = (plan['contract'] + '\n\n本阶段任务：\n' + stage['prompt']
              + '\n本次授权资料入口（只读）：' + str(root / 'SOURCES.md')
              + '\n\n本阶段输出目录：' + str(folder)
              + '\n依赖产物目录：' + ', '.join(str(root / 'jobs' / d) for d in stage['depends'])
              + '\n必交文件：' + ', '.join(stage['outputs'])
              + '\nresult.json只包含outcome、summary、open_questions；outcome允许 findings/accept/revise/reject/unavailable/no_viable_candidate。'
              + '\n不要创建goal或后台进程；外部控制器接力。只写本阶段目录，研究原件与其他阶段只读。')
    (folder / 'TASK.md').write_text(prompt)
    record = {'id': stage['id'], 'state': 'running', 'started_at': dt.datetime.now(dt.timezone.utc).isoformat(),
              'input_hashes': inputs, 'scientific_acceptance': 'not_certified_by_runner'}
    write_json(folder / 'receipt.json', record)
    start = time.monotonic()
    remaining = min(stage['seconds'], deadline - start)
    if remaining <= 0:
        record['state'] = 'deadline'
    else:
        proc = None
        try:
            with (folder / 'stdout.txt').open('w') as out, (folder / 'stderr.txt').open('w') as err:
                proc = subprocess.Popen(command or ['dsh', '--profile', 'headless', prompt], cwd=folder,
                                        stdout=out, stderr=err, start_new_session=True)
                record['pid'] = proc.pid
                write_json(folder / 'receipt.json', record)
                limit = start + remaining
                while True:
                    if (stop and stop.is_set()) or time.monotonic() >= limit:
                        stop_process_group(proc)
                        record['state'] = 'cancelled' if stop and stop.is_set() else 'timeout'
                        break
                    try:
                        record['exit_code'] = proc.wait(timeout=min(1, max(.001, limit - time.monotonic())))
                        break
                    except subprocess.TimeoutExpired:
                        continue
                if record['state'] not in {'timeout', 'cancelled'}:
                    stop_process_group(proc)
            if record['state'] not in {'timeout', 'cancelled'}:
                if record['exit_code'] != 0:
                    raise ValueError('process failed')
                for name, old_sha in inputs.items():
                    if sha(Path(name)) != old_sha:
                        raise ValueError('dependency changed during stage: ' + name)
                record['result'] = deliverable(folder, stage['outputs'])
                record['output_hashes'] = {name: sha(relative(folder, name)) for name in stage['outputs']}
                record['state'] = 'delivered'
        except (OSError, ValueError, KeyError) as exc:
            if proc is not None and proc.poll() is None:
                stop_process_group(proc)
            record.update(state='failed', error=str(exc))
    record['elapsed_seconds'] = round(time.monotonic() - start, 2)
    write_json(folder / 'receipt.json', record)
    return record


def run(plan, root, command=None):
    # Production headless launch is retired. Explicit commands are retained only
    # for local synthetic regression fixtures; CLI cannot supply one.
    check(plan)
    if not (root / 'SOURCES.md').is_file() or not (root / 'SOURCES.md').read_text().strip():
        raise ValueError('explicit source-scope file SOURCES.md required before launching models')
    if command is None:
        raise ValueError('LIVE_REQUEST_GUARD_UNAVAILABLE: use research_harness.py for visible control; no headless fallback')
    root.mkdir(parents=True, exist_ok=True)
    with (root / '.run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if (root / 'RUN.json').exists():
            raise ValueError('existing run preserved; use a new run root for explicit continuation')
        if not (root / 'SOURCES.md').is_file() or not (root / 'SOURCES.md').read_text().strip():
            raise ValueError('explicit source-scope file SOURCES.md required before launching models')
        state = {'status': 'running', 'started_at': dt.datetime.now(dt.timezone.utc).isoformat(),
                 'controller_pid': os.getpid(), 'deadline_at': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=plan['total_seconds'])).isoformat(),
                 'source_scope_sha256': sha(root / 'SOURCES.md'),
                 'stages': {}, 'scientific_acceptance': 'requires_content_review'}
        write_json(root / 'PLAN.json', plan)
        state['plan_sha256'] = sha(root / 'PLAN.json')
        write_json(root / 'RUN.json', state)
        deadline = time.monotonic() + plan['total_seconds']
        pending = list(plan['stages'])
        with termination_event() as stop, concurrent.futures.ThreadPoolExecutor(max_workers=plan['parallel']) as pool:
            while pending and time.monotonic() < deadline and not stop.is_set():
                if sha(root / 'SOURCES.md') != state['source_scope_sha256']:
                    state['scope_error'] = 'authorized source scope changed'
                    break
                ready = [s for s in pending if all(state['stages'].get(d, {}).get('state') == 'delivered' for d in s['depends'])][:plan['parallel']]
                if not ready:
                    break
                futures = {pool.submit(execute, root, s, plan, deadline, command, stop): s for s in ready}
                for future in concurrent.futures.as_completed(futures):
                    stage = futures[future]
                    try:
                        state['stages'][stage['id']] = future.result()
                    except Exception as exc:
                        state['stages'][stage['id']] = {'state': 'failed', 'error': str(exc)}
                    pending.remove(stage)
                    write_json(root / 'RUN.json', state)
            cancelled = stop.is_set()
        for sid, item in state['stages'].items():
            if item['state'] == 'delivered':
                try:
                    verify_receipt(root / 'jobs' / sid)
                except (OSError, ValueError, KeyError) as exc:
                    item.update(state='failed', error=str(exc))
        state['pending'] = [s['id'] for s in pending]
        if sha(root / 'SOURCES.md') != state['source_scope_sha256']:
            state['scope_error'] = 'authorized source scope changed'
        state['status'] = ('cancelled' if cancelled else 'awaiting_content_review' if not pending and all(v['state'] == 'delivered' for v in state['stages'].values())
                           else 'deadline' if time.monotonic() >= deadline else 'execution_blocked')
        if state.get('scope_error'):
            state['status'] = 'execution_blocked'
        write_json(root / 'RUN.json', state)
        return state


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=['check', 'run'])
    ap.add_argument('--plan', type=Path, required=True)
    ap.add_argument('--root', type=Path)
    args = ap.parse_args()
    plan = json.loads(args.plan.read_text())
    check(plan)
    if args.mode == 'check':
        print(json.dumps({'valid': True, 'stages': len(plan['stages']), 'launches_models': False}))
        return
    if not args.root:
        ap.error('--root required for run')
    print(json.dumps(run(plan, args.root.resolve()), ensure_ascii=False))


if __name__ == '__main__':
    main()
