from pathlib import Path


RUNNER = (Path(__file__).resolve().parents[2]
          / "scripts" / "remote" / "run-remote.sh")


def _heredoc_body(script: str, assignment: str) -> str:
    marker = f"{assignment}=$(cat <<EOF\n"
    start = script.index(marker) + len(marker)
    end = script.index("\nEOF\n)", start)
    return script[start:end]


def test_remote_prepare_uses_the_activated_formal_environment():
    remote_command = _heredoc_body(
        RUNNER.read_text(encoding="utf-8"), "remote_command")

    activation = remote_command.index("$REMOTE_ENV_ACTIVATE")
    prepare = remote_command.index(
        "$q_python scripts/remote/remote_job.py $q_prepare_args")

    assert activation < prepare
