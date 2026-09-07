"""Run the whole pipeline in order. Safe to re-run.

  1. extract_units.py      source-artifacts/*.html -> units/*.html
  2. apply_retrofit.py     add tracked-thread data-root spans (retrofit-tags.json)
  3. extract_legends.py    backfill translit/gloss into data/units.json
  4. scan_occurrences.py   -> data/occurrences.json
  5. verify_occurrences.py independent re-derivation + colour checks
"""

import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["extract_units.py", "apply_retrofit.py", "extract_legends.py",
         "scan_occurrences.py", "verify_occurrences.py"]


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
