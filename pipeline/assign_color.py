"""Pick a colour for a new root, instead of guessing one and finding out later.

The palette is dense enough that a colour chosen by eye will usually collide
with something -- when `shake` was added it landed dE00 1.68 from `cross`, which
is below the just-noticeable difference, and no check caught it for eleven
units. This does the search that a person cannot do by eye.

    python pipeline/assign_color.py <root>
        Propose colours for a NEW root. Avoids: every chrome accent, and every
        root that would share a unit with it. With no co-occurrence information
        it assumes the new root could appear anywhere, which is the safe
        assumption for a thread.

    python pipeline/assign_color.py <root> --unit 12
        The root is being added to unit 12. Avoids the chrome accents and only
        the roots already in that unit (plus any unit the root is already in),
        which is a much weaker constraint and finds better colours. Use this
        for a LOCAL root -- the per-unit rule is the only one that binds it.

    python pipeline/assign_color.py <root> --recolour
        The root already has a colour and you want a better one. Same as the
        first form but excludes the root's own current colour from `avoid`.

    python pipeline/assign_color.py --audit
        No proposal -- just report how much room is left: the tightest
        co-occurring pairs, and the per-unit headroom in each built unit.

Options: --hue N restricts the search near one hue; -n N changes how many
proposals are printed (default 6).
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import palette as P  # noqa: E402


def avoid_for(root, unit=None, recolour=False):
    """{label: hex} the new colour has to stay away from."""
    colors = P.all_colors()
    avoid = {f"--{k}": v for k, v in P.reserved().items()}

    if unit is not None:
        slug = f"unit-{int(unit):02d}"
        occ = P.load("occurrences.json")
        peers = set(occ.get(slug, {}))
        # plus wherever this root already appears
        for other_slug, roots in occ.items():
            if root in roots:
                peers |= set(roots)
        peers.discard(root)
    else:
        peers = set(colors) - {root}

    for r in sorted(peers):
        if r in colors:
            avoid[r] = colors[r]["color"]
    if not recolour and root in colors:
        avoid[root] = colors[root]["color"]
    return avoid


def audit():
    colors = P.all_colors()
    occ = P.load("occurrences.json")
    co = P.cooccurring_pairs(occ)

    print(f"{len(colors)} roots carry a colour; {len(co)} pairs co-occur in a "
          f"built unit ({100 * len(co) / (len(colors) * (len(colors) - 1) / 2):.0f}% "
          f"of all pairs).\n")

    print("Tightest CO-OCCURRING pairs (these are the hard constraint):")
    rows = []
    for a, b in co:
        if a in colors and b in colors:
            rows.append((P.de2000(colors[a]["color"], colors[b]["color"]), a, b))
    rows.sort()
    for d, a, b in rows[:8]:
        print(f"  dE00 {d:5.2f}  {a} / {b}")

    print("\nPer-unit headroom -- roots on the page, and the closest two:")
    for slug in sorted(occ):
        rs = [r for r in occ[slug] if r in colors]
        worst = None
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                d = P.de2000(colors[rs[i]]["color"], colors[rs[j]]["color"])
                if worst is None or d < worst[0]:
                    worst = (d, rs[i], rs[j])
        if worst:
            print(f"  {slug}  {len(rs):2} roots   tightest dE00 {worst[0]:5.2f}  "
                  f"({worst[1]} / {worst[2]})")

    print("\nThe per-unit number is the one that matters. A unit stays readable "
          "while its\ntightest pair is comfortably above the ~2.3 "
          "just-noticeable difference; the\nbook-wide count can keep growing "
          "as long as new roots land in units that have room.")


def main():
    args = [a for a in sys.argv[1:]]
    if "--audit" in args:
        audit()
        return 0
    if not args or args[0].startswith("-"):
        print(__doc__)
        return 2

    root = args[0]
    unit = None
    hue = None
    n = 6
    recolour = "--recolour" in args
    for flag, cast in (("--unit", int), ("--hue", int), ("-n", int)):
        if flag in args:
            val = cast(args[args.index(flag) + 1])
            if flag == "--unit":
                unit = val
            elif flag == "--hue":
                hue = val
            else:
                n = val

    avoid = avoid_for(root, unit=unit, recolour=recolour)
    scope = (f"unit {unit} and wherever '{root}' already appears"
             if unit is not None else "every root in the book")
    print(f"Proposing a colour for '{root}', clear of the chrome accents and "
          f"{scope}\n({len(avoid)} colours to avoid; "
          f"needs dE00 >= {P.CO_OCCUR_DE00}, dE76 >= {P.CO_OCCUR_DE76}, "
          f"contrast >= {P.CONTRAST_MIN}:1 on {P.background()}).\n")

    picks = P.propose(avoid, n=n, prefer_hue=hue)
    if not picks:
        print("Nothing clears the thresholds. Either narrow the scope with "
              "--unit, or this\nroot needs to share a colour with something it "
              "never co-occurs with -- pick from\nthe audit's least-tight pairs "
              "by hand and record why.")
        return 1
    for hx, d00, d76, near in picks:
        print(f"  {hx}   dE00 {d00:5.2f}  dE76 {d76:5.2f}   nearest: {near}")
    print("\nFirst one is the most separated. Paste it into data/threads.json "
          "(global) or\nthe unit's roots map in data/units.json (local), then "
          "run pipeline/build.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
