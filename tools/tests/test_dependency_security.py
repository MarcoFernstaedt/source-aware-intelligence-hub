import os
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _audit_command() -> str:
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    marker = "      - name: Python dependency advisory audit\n"
    step = workflow.split(marker, maxsplit=1)[1].split("      - name:", maxsplit=1)[0]
    return next(line.removeprefix("        run: ") for line in step.splitlines() if "run:" in line)


def test_ci_audits_the_exported_uv_lock_with_a_locked_tool() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    command = _audit_command()

    assert "pip-audit==2.10.1" in pyproject["dependency-groups"]["dev"]
    assert 'requirements_file="$(mktemp)"' in command
    assert "uv export --locked --no-hashes --format requirements-txt" in command
    assert '--output-file "$requirements_file"' in command
    assert 'uv run pip-audit --strict --requirement "$requirements_file"' in command
    assert "<(" not in command


def test_ci_does_not_audit_when_dependency_export_fails(tmp_path: Path) -> None:
    audit_marker = tmp_path / "audit-ran"
    fake_uv = tmp_path / "uv"
    fake_uv.write_text(
        f'#!/bin/sh\nif [ "$1" = export ]; then exit 42; fi\ntouch {audit_marker!s}\nexit 0\n',
        encoding="utf-8",
    )
    fake_uv.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = f"{tmp_path}:{env['PATH']}"

    result = subprocess.run(["bash", "-c", _audit_command()], env=env, check=False)

    assert result.returncode == 42
    assert not audit_marker.exists()
