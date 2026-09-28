"""Re-derive everything downstream of the committed fragments. Safe to re-run.

Phase E (moving pipeline/ onto bible-core) is swapping these steps for core
commands one at a time; see PLAN.md / the phase E PR for what's proven and
what's still blocked. Steps still on the old pipeline script are marked below.

  1. apply_retrofit.py       fragment edits from retrofit-tags.json (idempotent:
                             strip_span / text / *_word / unwrap / retag / add)
                             STILL PIPELINE: core's `retrofit` engine supports
                             every op, but core's own retrofit/retrofit-tags.json
                             is missing most of pipeline/retrofit-tags.json's
                             entries (strip_span, untag_word, retag_word, unwrap,
                             and all but 11 of 230 `add` entries) -- a hand-authored
                             data migration for Lane to review, not a code swap.
  2. `biblecore refresh`     regenerate each built fragment's unit-meta block
  3. `biblecore scan`        -> data/occurrences.json
  4. `biblecore verify-occurrences`  independent re-derivation + colour checks
  5. `biblecore digest`      data/threads.json -> threads-digest.md
  6. sync_to_github.py       refresh project-side/synced/ (--copy-only: it never
                             commits or pushes from here; the refreshed mirror is
                             meant to go in the same commit as the change that
                             caused it).
                             STILL PIPELINE: core's `sync` always commits+pushes
                             on its own; it has no copy-only mode yet.
  advisory:
  7. `biblecore audit`       Greek vs. fragments -- thread tag-coverage gaps
                             in built units (never fails the build)
  8. `biblecore leads`       canon-leads/canon-leads-unit-NN.md for built
                             units from 13 on + the next one: the intertext
                             pass's reading list (requires pipeline/corpus/,
                             see fetch_corpus.py; never fails the build)

units/*.html are the source of truth here — this script never regenerates them
from source-artifacts/. extract_units.py did that once (Phase 1) and now lives
only as a library port_artifact.py imports; running it again would drop every
post-extract direct edit (pericope headings, synoptic boxes, chiasm cuts).

Adding a NEW unit is `port_artifact.py NN`, not this (phase E: `biblecore port`
can't take over yet either -- it rejects unit-13's `descriptor` meta key, which
core doesn't recognize; see the phase E PR).

pipeline/scan_occurrences.py and pipeline/verify_occurrences.py still exist
because port_artifact.py's own post-port pipeline (run_retrofit_and_scan())
shells out to them by filename; they're no longer called from here.
"""

import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STEPS = ["apply_retrofit.py", "refresh", "scan", "verify-occurrences", "digest"]
STEP_ARGS = {"sync_to_github.py": ["--copy-only"]}
STEPS.append("sync_to_github.py")
ADVISORY = ["audit", "leads"]  # run, show output, never fail the build
CORE_COMMANDS = {"refresh", "scan", "verify-occurrences", "digest", "audit", "leads"}


def run(cmd, args, env):
    if cmd in CORE_COMMANDS:
        return subprocess.run([sys.executable, "-m", "biblecore", cmd] + args,
                               cwd=ROOT, env=env)
    return subprocess.run([sys.executable, os.path.join(HERE, cmd)] + args, env=env)


def main():
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for s in STEPS:
        print(f"\n=== {s} ===")
        r = run(s, STEP_ARGS.get(s, []), env)
        if r.returncode != 0:
            print(f"\nFAILED at {s}")
            sys.exit(r.returncode)
    for s in ADVISORY:
        print(f"\n=== {s} (advisory) ===")
        run(s, [], env)
    print("\nbuild ok")


if __name__ == "__main__":
    main()
