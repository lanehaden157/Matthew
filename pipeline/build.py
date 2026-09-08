"""Run the whole pipeline in order. Safe to re-run.

  1. extract_units.py      source-artifacts/*.html -> units/*.html
  2. apply_retrofit.py     tag edits from retrofit-tags.json
  3. refresh_meta.py       regenerate each built fragment's unit-meta block
  4. scan_occurrences.py   -> data/occurrences.json
  5. verify_occurrences.py independent re-derivation + colour checks
  6. threads_digest.py     data/threads.json -> threads-digest.md

Adding a NEW unit is not this script — use `port_artifact.py NN` for that.
This is the re-derive-everything-from-source pass for the units already built.

(extract_legends.py was a one-time backfill of translit/gloss into units.json
from the artifacts' hand legends — units.json is hand-maintained now, so it's
no longer in the chain. run it manually only to re-seed from scratch.)
"""

import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["extract_units.py", "apply_retrofit.py", "refresh_meta.py",
         "scan_occurrences.py", "verify_occurrences.py", "threads_digest.py"]


def main():
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for s in STEPS:
        print(f"\n=== {s} ===")
        r = subprocess.run([sys.executable, os.path.join(HERE, s)], env=env)
        if r.returncode != 0:
            print(f"\nFAILED at {s}")
            sys.exit(r.returncode)
    print("\nbuild ok")


if __name__ == "__main__":
    main()
