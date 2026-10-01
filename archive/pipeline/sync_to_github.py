"""Keep project-side/synced/ current on GitHub, so the Claude.ai project's
GitHub-connector "sync" source always reflects the latest chat-side docs with
no manual re-pasting.

Copies each file in check_project_sync.TRACKED_FILES into
project-side/synced/<basename> (a flat, deliberately duplicated mirror --
see project-side/README.md), commits only if something actually changed, and
pushes to origin/main. Safe to run anytime: it's a no-op when nothing changed.

Unlike Joshua, Matthew does NOT run this from a scheduled task. build.py calls
it as its last step, so the mirror refreshes exactly when the data it mirrors
does, and the history stays readable (platform-design-review.md A10/H9).

build.py runs it with --copy-only, so the mirror refreshes in the working tree
alongside the change that caused it and lands in the SAME commit. Nothing here
commits or pushes on its own unless you ask it to.

Usage:
    python pipeline/sync_to_github.py              # copy, commit, push
    python pipeline/sync_to_github.py --copy-only  # copy into synced/, nothing else
    python pipeline/sync_to_github.py --no-push    # copy and commit only
    python pipeline/sync_to_github.py --dry-run    # say what would change
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_project_sync import ROOT, TRACKED_FILES  # noqa: E402

SYNCED_DIR = ROOT / "project-side" / "synced"


def run(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=True)


def main() -> int:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    copy_only = "--copy-only" in args
    push = "--no-push" not in args and not dry_run and not copy_only

    SYNCED_DIR.mkdir(parents=True, exist_ok=True)

    missing = []
    for rel in TRACKED_FILES:
        src = ROOT / rel
        if not src.exists():
            missing.append(rel)
            continue
        if not dry_run:
            shutil.copyfile(src, SYNCED_DIR / Path(rel).name)

    if missing:
        print("MISSING on disk (skipped):")
        for rel in missing:
            print(f"  - {rel}")

    if dry_run:
        for rel in TRACKED_FILES:
            src, dst = ROOT / rel, SYNCED_DIR / Path(rel).name
            if not src.exists():
                continue
            if not dst.exists():
                print(f"  would add:    {dst.relative_to(ROOT)}")
            elif src.read_bytes() != dst.read_bytes():
                print(f"  would update: {dst.relative_to(ROOT)}")
        return 0

    if copy_only:
        status = run("git", "status", "--porcelain", "--", str(SYNCED_DIR))
        changed = [line[3:] for line in status.stdout.splitlines()]
        if changed:
            print("project-side mirror refreshed (uncommitted — commit it with "
                  "the change that caused it):")
            for c in changed:
                print(f"  - {c}")
        else:
            print("project-side mirror: already up to date.")
        return 0

    status = run("git", "status", "--porcelain", "--", str(SYNCED_DIR))
    if not status.stdout.strip():
        print("project-side sync: already up to date.")
        return 0

    changed = [line[3:] for line in status.stdout.splitlines()]
    run("git", "add", "--", str(SYNCED_DIR))
    message = "Sync project-side docs\n\n" + "\n".join(f"- {c}" for c in changed)
    run("git", "commit", "-m", message)
    if push:
        run("git", "push")

    print("project-side sync: " + ("synced and pushed:" if push else "committed (not pushed):"))
    for c in changed:
        print(f"  - {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
