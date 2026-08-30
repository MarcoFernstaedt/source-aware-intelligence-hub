import subprocess
from pathlib import Path

from tools.scan_public import current_findings, history_findings, scan_paths


def test_scanner_detects_forbidden_canaries_without_echoing_values(tmp_path: Path) -> None:
    candidate = tmp_path / "canary.txt"
    candidate.write_text(
        "contact admin" + "@" + "example.test and read " + "/" + "home/demo/private.db",
        encoding="utf-8",
    )

    findings = scan_paths([candidate], root=tmp_path)

    assert {finding.detector for finding in findings} == {"email", "absolute-path"}
    assert all("example.test" not in finding.summary for finding in findings)
    assert all("/home/" not in finding.summary for finding in findings)


def test_scanner_accepts_clean_synthetic_text(tmp_path: Path) -> None:
    candidate = tmp_path / "clean.txt"
    candidate.write_text("Fictional Atlas Workshop status is scheduled.", encoding="utf-8")
    assert scan_paths([candidate], root=tmp_path) == []


def test_current_scanner_includes_generated_build_output(tmp_path: Path) -> None:
    bundle = tmp_path / "frontend" / "dist" / "assets" / "app.js"
    bundle.parent.mkdir(parents=True)
    bundle.write_text("const contact = 'build" + "@" + "example.test'", encoding="utf-8")

    findings = current_findings(tmp_path)

    assert [(finding.detector, finding.path) for finding in findings] == [
        ("email", "frontend/dist/assets/app.js")
    ]


def test_current_scanner_rejects_sensitive_filenames(tmp_path: Path) -> None:
    candidate = tmp_path / ".env.production"
    candidate.write_text("intentionally empty", encoding="utf-8")

    findings = current_findings(tmp_path)

    assert [(finding.detector, finding.path) for finding in findings] == [
        ("sensitive-filename", ".env.production")
    ]


def test_current_scanner_rejects_symlinks_without_following_them(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("clean", encoding="utf-8")
    link = tmp_path / "public-link.txt"
    link.symlink_to(outside)

    findings = current_findings(tmp_path)

    assert [(finding.detector, finding.path) for finding in findings] == [
        ("symlink", "public-link.txt")
    ]


def test_history_scanner_rejects_direct_commit_identity_without_printing_it(
    tmp_path: Path,
) -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=tmp_path, check=True, capture_output=True)
    candidate = tmp_path / "README.md"
    candidate.write_text("clean", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    identity = "builder" + "@" + "example.test"
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Fixture Builder",
            "-c",
            f"user.email={identity}",
            "commit",
            "-m",
            "fixture",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    findings = history_findings(tmp_path)

    assert any(finding.detector == "commit-email" for finding in findings)
    assert all(identity not in finding.summary for finding in findings)


def test_history_scanner_checks_commit_messages(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-b", "main"], cwd=tmp_path, check=True, capture_output=True)
    candidate = tmp_path / "README.md"
    candidate.write_text("clean", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    private_path = "/" + "home/demo/private.db"
    noreply_identity = "1+fixture" + "@" + "users.noreply.github.com"
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Fixture Builder",
            "-c",
            f"user.email={noreply_identity}",
            "commit",
            "-m",
            f"remove {private_path}",
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    findings = history_findings(tmp_path)

    assert any(finding.detector == "absolute-path" for finding in findings)
    assert all(private_path not in finding.summary for finding in findings)
