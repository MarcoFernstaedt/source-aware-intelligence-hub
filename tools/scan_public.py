from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

_TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".lock",
    ".md",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
_EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "node_modules",
}
_PATTERNS = {
    "absolute-path": re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+/"),
    "email": re.compile(
        r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![A-Za-z0-9.-])"
    ),
    "private-ip": re.compile(
        r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
    ),
    "credential-shape": re.compile(
        r"(?i)(?:api.?key|access.?token|client.?secret|password)\s*[:=]\s*['\"][A-Za-z0-9_./+-]{12,}['\"]"
    ),
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


@dataclass(frozen=True)
class Finding:
    detector: str
    path: str
    summary: str


def _is_sensitive_filename(path: Path) -> bool:
    name = path.name.lower()
    return (
        name == ".env"
        or (name.startswith(".env.") and name != ".env.example")
        or name in {".npmrc", ".pypirc", "credentials.json", "id_ed25519", "id_rsa"}
    )


def _is_public_commit_email(value: str) -> bool:
    normalized = value.strip().lower()
    return normalized.endswith("@users.noreply.github.com") or normalized.endswith(
        "@noreply.github.com"
    )


def _scan_text(text: str, label: str) -> list[Finding]:
    findings: list[Finding] = []
    for detector, pattern in _PATTERNS.items():
        count = len(pattern.findall(text))
        if count:
            findings.append(Finding(detector, label, f"{detector}: {count} match(es)"))
    return findings


def scan_paths(paths: list[Path], root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(paths):
        if any(part in _EXCLUDED_PARTS for part in path.relative_to(root).parts):
            continue
        label = str(path.relative_to(root)) if path.is_relative_to(root) else path.name
        if path.is_symlink():
            findings.append(Finding("symlink", label, "symlink: 1 match(es)"))
            continue
        if _is_sensitive_filename(path):
            findings.append(Finding("sensitive-filename", label, "sensitive-filename: 1 match(es)"))
            continue
        if path.suffix not in _TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        findings.extend(_scan_text(text, label))
    return findings


def current_findings(root: Path) -> list[Finding]:
    return scan_paths([path for path in root.rglob("*") if path.is_file()], root)


def history_findings(root: Path) -> list[Finding]:
    commits = subprocess.run(
        ["git", "rev-list", "--all"], cwd=root, check=True, text=True, capture_output=True
    ).stdout.splitlines()
    findings: list[Finding] = []
    seen: set[tuple[str, str, str]] = set()
    for commit in commits:
        identities = subprocess.run(
            ["git", "show", "-s", "--format=%ae%n%ce", commit],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.splitlines()
        direct_identity_count = sum(
            bool(identity.strip()) and not _is_public_commit_email(identity)
            for identity in identities
        )
        if direct_identity_count:
            findings.append(
                Finding(
                    "commit-email",
                    commit[:12],
                    f"commit-email: {direct_identity_count} match(es)",
                )
            )
        message = subprocess.run(
            ["git", "show", "-s", "--format=%B", commit],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        findings.extend(_scan_text(message, f"{commit[:12]}:commit-message"))
        entries = subprocess.run(
            ["git", "ls-tree", "-r", commit],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.splitlines()
        for entry in entries:
            metadata, path = entry.split("\t", 1)
            mode, _kind, object_id = metadata.split()
            key = (commit, path, object_id)
            candidate_path = Path(path)
            if key in seen:
                continue
            seen.add(key)
            if mode == "120000":
                findings.append(Finding("symlink", f"{commit[:12]}:{path}", "symlink: 1 match(es)"))
                continue
            if _is_sensitive_filename(candidate_path):
                findings.append(
                    Finding(
                        "sensitive-filename",
                        f"{commit[:12]}:{path}",
                        "sensitive-filename: 1 match(es)",
                    )
                )
                continue
            if candidate_path.suffix not in _TEXT_SUFFIXES:
                continue
            raw = subprocess.run(
                ["git", "cat-file", "blob", object_id], cwd=root, check=True, capture_output=True
            ).stdout
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue
            findings.extend(_scan_text(text, f"{commit[:12]}:{path}"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed public content scanner")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--history", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    findings = history_findings(root) if args.history else current_findings(root)
    for finding in findings:
        print(f"{finding.detector}\t{finding.path}\t{finding.summary}")
    print(f"scan_mode={'history' if args.history else 'current'} findings={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
