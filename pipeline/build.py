"""Re-derive everything downstream of the committed fragments. Safe to re-run.

  1. apply_retrofit.py     fragment edits from retrofit-tags.json (idempotent:
                           strip_span / text / *_word / unwrap / retag / add)
  2. refresh_meta.py       regenerate each built fragment's unit-meta block
  3. scan_occurrences.py   -> data/occurrences.json
  4. verify_occurrences.py independent re-derivation + colour checks
  5. threads_digest.py     data/threads.json -> threads-digest.md
  advisory:
  6. audit_thread_coverage.py  Greek vs. fragments — thread tag-coverage gaps
                               in built units (never fails the build)

units/*.html are the source of truth here — this script never regenerates them
from source-artifacts/. extract_units.py did that once (Phase 1) and now lives
only as a library port_artifact.py imports; running it again would drop every
post-extract direct edit (pericope headings, synoptic boxes, chiasm cuts).

Adding a NEW unit is `port_artifact.py NN`, not this.

(extract_legends.py was a one-time backfill of translit/gloss into units.json —
units.json is hand-maintained now. Run it manually only to re-seed from scratch.)
"""

import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["apply_retrofit.py", "refresh_meta.py", "scan_occurrences.py",
         "verify_occurrences.py", "threads_digest.py"]
ADVISORY = ["audit_thread_coverage.py"]  # run, show output, never fail the build


def main():
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for s in STEPS:
        print(f"\n=== {s} ===")
        r = subprocess.run([sys.executable, os.path.join(HERE, s)], env=env)
        if r.returncode != 0:
            print(f"\nFAILED at {s}")
            sys.exit(r.returncode)
    for s in ADVISORY:
        print(f"\n=== {s} (advisory) ===")
        subprocess.run([sys.executable, os.path.join(HERE, s), "--check"], env=env)
    print("\nbuild ok")


if __name__ == "__main__":
    main()
