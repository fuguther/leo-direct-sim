#!/usr/bin/env python3
"""Local Harness control adapter. No prompt admission without a request-level guard.

Transport implements the installed Harness RPC envelope, not a private database
writer. Authentication is supplied by the caller; secrets never enter journals.
"""
import argparse
from contextlib import contextmanager
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import time
import urllib.request
from urllib.parse import urlsplit
import uuid


class Blocked(RuntimeError):
    pass


def atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def fingerprint(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_authorization(root, plan, now=None):
    root = Path(root)
    auth = json.loads((root / 'AUTHORIZATION.json').read_text())
    now = now or dt.datetime.now(dt.timezone.utc)
    expiry = dt.datetime.fromisoformat(auth['expires_at'])
    if expiry.tzinfo is None or now >= expiry:
        raise Blocked('authorization expired or timezone missing')
    for key in ('provider', 'model', 'destination', 'project_cwd'):
        if not auth.get(key) or auth[key] != plan.get(key):
            raise Blocked('authorization mismatch: ' + key)
    if auth['model'] != 'z-ai/glm-5.3-flash' or auth['destination'] != 'https://api.commandcode.ai/provider/v1':
        raise Blocked('route outside current user authorization')
    budget = auth.get('budget_fen')
    if type(budget) is not int or not 0 < budget <= 1000:
        raise Blocked('budget must be positive integer fen, at most 1000')
    if plan.get('budget_fen') != budget:
        raise Blocked('plan budget differs from authorization')
    if auth.get('source_scope_sha256') != fingerprint(root / 'SOURCES.md'):
        raise Blocked('source scope mismatch')
    if auth.get('plan_sha256') != fingerprint(root / 'PLAN.json'):
        raise Blocked('plan mismatch')
    return auth


class Budget:
    """Durable conservative reservations. Lost responses stay fully charged.

    This ledger is not a provider hook. Live admission stays blocked until an
    actual request boundary can reserve the maximum charge including retries.
    """
    def __init__(self, path, limit_fen):
        if type(limit_fen) is not int or not 0 < limit_fen <= 1000:
            raise Blocked('invalid budget')
        self.path = str(path)
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS meta (id INTEGER PRIMARY KEY, ceiling INTEGER)')
            db.execute('INSERT OR IGNORE INTO meta VALUES (1, ?)', (limit_fen,))
            if db.execute('SELECT ceiling FROM meta WHERE id=1').fetchone()[0] != limit_fen:
                raise Blocked('cannot change existing budget')
            db.execute('CREATE TABLE IF NOT EXISTS calls (id TEXT PRIMARY KEY, reserved INTEGER, actual INTEGER)')
            db.execute('CREATE TABLE IF NOT EXISTS faults (reason TEXT NOT NULL)')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        try:
            with db:
                yield db
        finally:
            db.close()

    def reserve(self, request_id, maximum_fen):
        if type(maximum_fen) is not int or maximum_fen <= 0:
            raise Blocked('positive maximum request charge required')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT 1 FROM faults').fetchone():
                raise Blocked('budget frozen after accounting fault')
            if db.execute('SELECT 1 FROM calls WHERE id=?', (request_id,)).fetchone():
                raise Blocked('request already admitted; reconcile, do not resend')
            used = db.execute('SELECT COALESCE(SUM(COALESCE(actual,reserved)),0) FROM calls').fetchone()[0]
            ceiling = db.execute('SELECT ceiling FROM meta').fetchone()[0]
            if used + maximum_fen > ceiling:
                raise Blocked('budget exhausted')
            db.execute('INSERT INTO calls VALUES (?,?,NULL)', (request_id, maximum_fen))

    def settle(self, request_id, actual_fen):
        if type(actual_fen) is not int or actual_fen < 0:
            raise Blocked('invalid actual charge')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT reserved,actual FROM calls WHERE id=?', (request_id,)).fetchone()
            if row is None:
                raise Blocked('unknown request')
            if row[1] is not None:
                if row[1] != actual_fen:
                    raise Blocked('conflicting settlement')
                return
            if actual_fen > row[0]:
                db.execute('UPDATE calls SET actual=? WHERE id=?', (actual_fen, request_id))
                db.execute('INSERT INTO faults VALUES (?)', ('provider charge exceeded reserved bound',))
                db.commit()  # Preserve the overrun even when raising; freeze future calls.
                raise Blocked('provider charge exceeded reserved bound; investigate')
            db.execute('UPDATE calls SET actual=? WHERE id=?', (actual_fen, request_id))


class Harness:
    def __init__(self, base='http://127.0.0.1:3080', cookie=None):
        u = urlsplit(base)
        if u.scheme != 'http' or u.hostname not in ('127.0.0.1', 'localhost', '::1') or u.path not in ('', '/') or u.query or u.fragment or u.username:
            raise Blocked('Harness must be a local origin')
        self.base = base.rstrip('/')
        self.cookie = cookie

    def rpc(self, method, payload):
        if method not in {'session/list', 'session/page', 'session/create', 'session/rename', 'session/cancel', 'workspace/list'}:
            raise Blocked('RPC not admitted by control-only adapter')
        rid = str(uuid.uuid4())
        body = json.dumps(dict(type='client-request', rpcId=rid, method=method, payload=payload)).encode()
        headers = {'Content-Type': 'application/json'}
        if self.cookie:
            headers['Cookie'] = self.cookie
        request = urllib.request.Request(self.base + '/api/' + method, body, headers)
        # Never follow a redirect carrying the local authentication cookie.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        try:
            with urllib.request.build_opener(NoRedirect).open(request, timeout=10) as response:
                data = json.load(response)
        except Exception as exc:
            raise Blocked('Harness RPC unavailable: ' + type(exc).__name__) from None
        if data.get('rpcId') != rid or data.get('type') != 'server-response':
            raise Blocked('invalid Harness response envelope')
        result = data.get('result', {})
        if not result.get('ok'):
            raise Blocked('Harness rejected RPC: ' + str(result.get('error', {}).get('code', 'unknown')))
        return result.get('value')

    def snapshot(self, sid):
        """Read a bounded native follow snapshot; never invent a history cursor."""
        try:
            import websocket
        except ImportError:
            raise Blocked('websocket-client required for Harness history') from None
        stream_id = str(uuid.uuid4())
        socket = None
        try:
            socket = websocket.create_connection(
                self.base.replace('http://', 'ws://', 1) + '/api/remote.mux',
                cookie=self.cookie, origin=self.base, timeout=10)
            socket.send(json.dumps(dict(type='open', streamId=stream_id,
                endpoint='session/follow', payload=dict(
                    address=dict(kind='session', sessionId=sid), maxMessages=1))))
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                socket.settimeout(max(.01, deadline - time.monotonic()))
                frame = json.loads(socket.recv())
                if frame.get('streamId') != stream_id:
                    continue
                value = frame.get('value', {})
                if frame.get('type') == 'item' and value.get('type') == 'snapshot':
                    cursor = value.get('cursor')
                    if type(cursor) is not int or cursor < 0:
                        raise Blocked('invalid history snapshot cursor')
                    return value
                if frame.get('type') in ('error', 'end'):
                    raise Blocked('history stream ended without snapshot')
            raise Blocked('history snapshot timeout')
        except Blocked:
            raise
        except Exception as exc:
            raise Blocked('Harness history unavailable: ' + type(exc).__name__) from None
        finally:
            if socket is not None:
                socket.close()

    def visible(self, sid, cwd):
        rows = self.rpc('session/list', {})['items']
        row = next((r for r in rows if r['sessionId'] == sid), None)
        if row is None or row.get('cwd') != cwd:
            raise Blocked('session absent from list or wrong project')
        snapshot = self.snapshot(sid)
        page = self.rpc('session/page', {
            'address': {'kind': 'session', 'sessionId': sid},
            'throughSeq': snapshot['cursor'], 'maxMessages': 1})
        if not isinstance(page, dict) or not isinstance(page.get('records'), list):
            raise Blocked('invalid Harness history page')
        return row

    def admit_prompt(self, *args, **kwargs):
        raise Blocked('LIVE_REQUEST_GUARD_UNAVAILABLE: no verified per-request cost/route hook; no model call sent')


def reconcile(root, client):
    state = json.loads((Path(root) / 'VISIBLE-RUN.json').read_text())
    return {sid: client.visible(sid, state['project_cwd']) for sid in state['sessions']}


def cancel(root, client):
    path = Path(root) / 'VISIBLE-RUN.json'
    state = json.loads(path.read_text())
    state['status'] = 'cancel_requested'
    atomic(path, state)  # Persist stop before attempting any remote operation.
    errors = []
    for sid in state['sessions']:
        try:
            client.rpc('session/cancel', {'sessionId': sid})
        except Blocked:
            errors.append(sid)
    state['status'] = 'cancel_unconfirmed' if errors else 'cancel_requested'
    state['cancel_unconfirmed'] = errors
    atomic(path, state)
    return state


def prepare(root, client):
    root = Path(root)
    plan = json.loads((root / 'PLAN.json').read_text())
    validate_authorization(root, plan)
    path = root / 'VISIBLE-RUN.json'
    if path.exists():
        raise Blocked('existing run: use reconcile; never automatically resend')
    # O_EXCL prevents two controllers from claiming a run. Crash leaves it for
    # explicit reconciliation; it is not silently recycled.
    fd = os.open(root / '.visible-owner', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(fd)
    ids = {str(uuid.uuid4()): label for label in ['controller'] + [s['id'] for s in plan['stages']]}
    state = dict(status='preparing', project_cwd=plan['project_cwd'], sessions=ids,
                 authorization_sha256=fingerprint(root / 'AUTHORIZATION.json'),
                 plan_sha256=fingerprint(root / 'PLAN.json'), scientific_acceptance='requires_content_review')
    atomic(path, state)
    try:
        for sid, label in ids.items():
            validate_authorization(root, plan)
            if fingerprint(root / 'AUTHORIZATION.json') != state['authorization_sha256']:
                raise Blocked('authorization changed during preparation')
            client.rpc('session/create', {'sessionId': sid, 'cwd': plan['project_cwd']})
            client.rpc('session/rename', {'sessionId': sid, 'title': 'Research ' + root.name + ' / ' + label})
            client.visible(sid, plan['project_cwd'])
        state['status'] = 'prepared_control_only'
    except Exception:
        state['status'] = 'execution_blocked'
        atomic(path, state)
        raise
    atomic(path, state)
    return state


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['probe', 'prepare', 'reconcile', 'cancel'])
    p.add_argument('--root', type=Path)
    p.add_argument('--base', default='http://127.0.0.1:3080')
    args = p.parse_args()
    client = Harness(args.base, os.environ.get('RESEARCH_HARNESS_COOKIE'))
    if args.mode == 'probe':
        result = {'session_count': len(client.rpc('session/list', {})['items']),
                  'live_admission': 'blocked_pending_request_guard'}
    else:
        if not args.root:
            p.error('--root required')
        result = {'prepare': prepare, 'reconcile': reconcile, 'cancel': cancel}[args.mode](args.root, client)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
