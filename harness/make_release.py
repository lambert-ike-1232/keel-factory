#!/usr/bin/env python3
"""Cut a versioned KEEL FACTORY release, and prove it before calling it done.

    python3 "$KEEL/harness/make_release.py"

Releases the version named in VERSION. It refuses unless the master is a git
repository on branch main (MANUAL's upgrade pulls main, so a release cut on another
branch would not reach a machine that upgrades that way) with a clean working tree,
RELEASES.md has a "## v<version>" section, and no release folder for that version exists
yet. It checks all of this before it writes anything. Then it:

1. tags HEAD v<version> (annotated), unless that tag already points at HEAD;
2. writes ../KEEL-FACTORY-releases/v<version>/ next to the master, containing:
   - KEEL-FACTORY-v<version>.bundle — the whole repository in one file, history and
     tags included. It is the safe way to carry the master on an exFAT drive, which
     would otherwise drop file permissions;
   - KEEL-FACTORY-v<version>.tar.gz — the tagged files, for restoring without git;
   - MANUAL-v<version>.md — the manual, readable straight off the drive;
   - README-FIRST.txt — how to restore onto the local disk, checksums first;
   - SHA256SUMS — checksums of everything above;
3. proves the release: clones the bundle into a temporary folder, checks the tag,
   checks the archive holds every tracked file, runs every self-test from the clone,
   and runs check_kit.py there, so the plugin and the Codex skill set are well formed.

It exits 0 only when every proof passes. Standard library only, plus git.
Self-test: test_make_release.py, beside this file.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

MASTER = Path(__file__).resolve().parent.parent
RELEASE_BRANCH = "main"
SELF_TESTS = [
    "harness/hooks/test_data_boundary_guard.py",
    "harness/hooks/test_keel_hook.py",
    "harness/test_link_kit.py",
    "harness/test_install_guard.py",
    "harness/test_install_plugin.py",
    "harness/test_check_kit.py",
    "harness/test_make_release.py",
    "keel/skills/crew/scripts/test_check_lanes.py",
]


def git(*args: str, cwd: Path = MASTER) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def current_branch(cwd: Path = MASTER) -> str:
    """The branch HEAD is on, or "" when HEAD is detached."""
    result = subprocess.run(["git", "symbolic-ref", "--quiet", "--short", "HEAD"], cwd=cwd,
                            capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def refuse(message: str) -> int:
    print(f"refused: {message}")
    return 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    if shutil.which("git") is None:
        return refuse("git is not installed")
    try:
        git("rev-parse", "--is-inside-work-tree")
    except subprocess.CalledProcessError:
        return refuse(f"{MASTER} is not a git repository")
    branch = current_branch()
    if branch != RELEASE_BRANCH:
        where = f"HEAD is on {branch}" if branch else "HEAD is detached"
        return refuse(f"releases are cut from {RELEASE_BRANCH}, and {where}; merge into "
                      f"{RELEASE_BRANCH}, check it out, then run this again")
    if git("status", "--porcelain"):
        return refuse("the working tree has uncommitted changes; commit them first")
    version = (MASTER / "VERSION").read_text().strip()
    tag = f"v{version}"
    if f"## {tag}" not in (MASTER / "RELEASES.md").read_text():
        return refuse(f"RELEASES.md has no '## {tag}' section; write the release notes first")
    out = MASTER.parent / "KEEL-FACTORY-releases" / tag
    if out.exists():
        return refuse(f"{out} already exists; a release is never overwritten, so bump VERSION")

    head = git("rev-parse", "HEAD")
    existing = git("tag", "--list", tag)
    if existing and git("rev-list", "-n", "1", tag) != head:
        return refuse(f"tag {tag} already exists on another commit; bump VERSION")
    if not existing:
        git("tag", "-a", tag, "-m", f"KEEL FACTORY {tag}")

    out.mkdir(parents=True)
    bundle = out / f"KEEL-FACTORY-{tag}.bundle"
    archive = out / f"KEEL-FACTORY-{tag}.tar.gz"
    manual = out / f"MANUAL-{tag}.md"
    readme = out / "README-FIRST.txt"
    git("bundle", "create", str(bundle), "--all")
    git("archive", "--format=tar.gz", "--prefix=KEEL-FACTORY/", "-o", str(archive), tag)
    manual.write_text(git("show", f"{tag}:MANUAL.md") + "\n")
    readme.write_text(
        f"KEEL FACTORY {tag}\n\n"
        "Restore the master onto this machine's own disk. Run every command below from this\n"
        "folder (cd into it first). ~/GitProjects/KEEL-FACTORY is an example: use your own\n"
        "local path, never the drive.\n\n"
        "First, check the files (every line must say OK):\n\n"
        "    shasum -a 256 -c SHA256SUMS\n\n"
        "Then restore with git:\n\n"
        f"    git clone --branch {RELEASE_BRANCH} \"$PWD/{bundle.name}\" ~/GitProjects/KEEL-FACTORY\n"
        f"    git -C ~/GitProjects/KEEL-FACTORY describe --tags     (must print {tag})\n\n"
        "Without git (makes ~/GitProjects/KEEL-FACTORY/ and writes nothing on the drive):\n\n"
        f"    mkdir -p ~/GitProjects && tar -xzf {archive.name} -C ~/GitProjects\n\n"
        f"Then follow section 3 of {manual.name}, \"Setting up a machine\".\n")
    files = [bundle, archive, manual, readme]
    (out / "SHA256SUMS").write_text("".join(f"{sha256(f)}  {f.name}\n" for f in files))

    failures = []
    git("bundle", "verify", str(bundle))
    tracked = len(git("ls-tree", "-r", "--name-only", tag).splitlines())
    with tarfile.open(archive) as tar:
        in_archive = sum(1 for member in tar.getmembers() if member.isfile())
    if in_archive != tracked:
        failures.append(f"archive holds {in_archive} files, the tag tracks {tracked}")
    with tempfile.TemporaryDirectory(prefix="keel-release-check-") as tmp:
        clone = Path(tmp) / "KEEL-FACTORY"
        git("clone", "--quiet", str(bundle), str(clone), cwd=Path(tmp))
        git("checkout", "--quiet", tag, cwd=clone)
        if git("describe", "--tags", "--exact-match", cwd=clone) != tag:
            failures.append("the clone is not at the release tag")
        for test in SELF_TESTS:
            path = clone / test
            result = subprocess.run([sys.executable, "-B", path.name], cwd=path.parent,
                                    capture_output=True, text=True)
            status = "OK" if result.returncode == 0 else "FAILED"
            print(f"  self-test from the fresh clone: {test}: {status}")
            if result.returncode != 0:
                failures.append(f"{test} failed in the clone")
        result = subprocess.run([sys.executable, "-B", str(clone / "harness" / "check_kit.py")],
                                capture_output=True, text=True)
        print(f"  kit check from the fresh clone: {'OK' if result.returncode == 0 else 'FAILED'}")
        if result.returncode != 0:
            failures.append("check_kit.py found problems in the clone:\n" + result.stdout)

    if failures:
        print(f"release {tag} written to {out} but NOT proven:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"release {tag} proven: {tracked} tracked files, bundle verified, every self-test passed from a fresh clone")
    print(f"  {out}")
    for path in files + [out / "SHA256SUMS"]:
        print(f"    {path.name}  ({path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
