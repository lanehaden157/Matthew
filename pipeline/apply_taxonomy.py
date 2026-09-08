"""One-shot: apply the root/motif taxonomy to data/units.json.
Re-runnable (idempotent-ish). Not part of build.py — units.json is hand-kept now.
"""
import json
import os

P = os.path.join(os.path.dirname(__file__), "..", "data", "units.json")
d = json.load(open(P, encoding="utf-8"))
U = {u["n"]: u for u in d["units"] if u.get("built")}


def R(n):
    return U[n]["roots"]


def relabel(n, root, translit, gloss, kind="root", members=None):
    e = R(n).get(root)
    if e is None:
        return
    if isinstance(e, str):
        e = {"color": e}
        R(n)[root] = e
    e["translit"], e["gloss"], e["kind"] = translit, gloss, kind
    e.pop("members", None)
    if members:
        e["members"] = members


def add(n, root, color, translit, gloss, kind="root"):
    R(n)[root] = {"color": color, "translit": translit, "gloss": gloss, "kind": kind}


def rm(n, root):
    R(n).pop(root, None)


# default kind
for u in U.values():
    for e in u["roots"].values():
        if isinstance(e, dict):
            e.setdefault("kind", "root")

# family trims
for n in (1, 2, 3, 4):
    relabel(n, "beget", "gennaō · genesis", "beget (γεν-)")
for n in (1, 2, 3):
    relabel(n, "dream", "onar", "dream")
for n in (1, 3):
    relabel(n, "save", "sōzō", "save")
relabel(3, "immerse", "baptizō · baptisma", "immerse (βαπτ-)")
relabel(3, "repent", "metanoeō · metanoia", "repent (μετανο-)")
relabel(3, "son", "huios", "Son")
relabel(6, "hidden", "kryptos · kryphaios", "hidden (κρυπτ-)")
relabel(6, "treasure", "thēsauros · thēsaurizō", "treasure (θησαυρ-)")
relabel(6, "seek", "zēteō · epizēteō", "seek (ζητ-)")
relabel(7, "judge", "krinō · krima", "judge (κρι-)")
relabel(7, "measure", "metron · metreō", "measure (μετρ-)")
relabel(7, "eye", "ophthalmos", "eye")
relabel(8, "faith", "pistis · pisteuō", "trust (πιστ-)")
relabel(5, "whole", "holos", "whole")

# splits
for n in (1, 3):
    relabel(n, "name", "onoma", "name")
    relabel(n, "david", "Dauid", "David")
    add(n, "call", "#9c2f8f", "kaleō", "call")
relabel(3, "test", "peirazō", "test")
add(3, "slanderer", "#4a1c2a", "diabolos", "the slanderer")
relabel(4, "dark", "skotia", "darkness")
add(4, "shadow", "#6b7280", "skia", "shadow")
relabel(7, "way", "hodos", "road / way")
add(7, "gate", "#8a5a9c", "pylē", "gate")

# motifs
relabel(5, "said", "ēkousate / errethē", '"you heard / it was said"', "motif",
        [{"translit": "ēkousate", "gloss": "you heard"},
         {"translit": "errethē", "gloss": "it was said"}])
relabel(6, "wage", "misthos / apechō / apodidōmi", "the reward economy", "motif",
        [{"translit": "misthos", "gloss": "wage / reward"},
         {"translit": "apechō", "gloss": "have in full"},
         {"translit": "apodidōmi", "gloss": "pay back"}])
relabel(6, "seen", "theaomai / phainō / aphanizō / blepō", "seen / unseen", "motif",
        [{"translit": "theaomai", "gloss": "be gazed at"},
         {"translit": "phainō", "gloss": "appear"},
         {"translit": "aphanizō", "gloss": "make vanish"},
         {"translit": "blepō", "gloss": "see"}])

# 'with' is now the emmanuel thread
rm(1, "with")
rm(3, "with")

json.dump(d, open(P, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(P, "a").write("\n")
print("units.json taxonomy applied")
