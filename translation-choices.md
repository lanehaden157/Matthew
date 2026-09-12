# Translation Choices

A working glossary of deliberate English renderings for this study's own
translation — built from `data/threads.json` and `data/units.json` and
**audited against the verse text of units 1–11** (2026-09-12), plus register
decisions that aren't tracked as coloured `data-root` spans at all. **Not** a
list of every English word in the fragments — just the ones where the choice
was made on purpose and is worth carrying forward consistently.

Verse refs below are Matthew chapter:verse.

## How to use this file (for the Claude.ai research project)

Before rendering a Greek word in a new unit's translation, check this file
for a prior decision and match it. If a different rendering genuinely fits
better in a specific verse, use it — but say so explicitly in the artifact
(a note, or flagged in the thread-delta), rather than silently drifting.
Lane reviews the flag and decides whether it's a one-off exception or a
correction that should update this file everywhere.

Claude Code keeps this file current as part of its normal workflow — any
session that changes a rendering updates the relevant row/bullet and the Log
section below in the same turn, without being asked separately. It's still
hand-maintained prose, not generated from the fragments, so if a unit's
actual text and this file ever disagree, the unit is more likely right;
flag the mismatch rather than trusting the file blindly.

## Tracked colour-thread words (global — same colour in every unit)

Thread id, transliteration, the rendering(s) actually used, and why. Threads
marked `(phrase)` are tracked by fixed phrase rather than lexical stem. A few
of these words genuinely **drift with context** by Lane's standing call
(mercy, righteous) — that's noted, not a bug.

| thread | Greek | rendering | note |
|---|---|---|---|
| acts-of-power | dynamis | acts of power (not "miracles") | New thread (2026-09-12). Opens 7:22 (the false claim); pays off 11:20–23 (Galilee's own unrepented evidence). Kept literal, countable, and plural — not the modern "miracle" category. |
| apo-tote | apo tote | "from then" (phrase) | Two hinges: 4:17 ("began to proclaim") / 16:21 ("began to show he must suffer"). |
| authority | exousia | authority | Runs 7:29 to 28:18. |
| build | oikodomeō | build | 7:24–26 → "I will build my assembly" (16:18). |
| call | kaleō | call; be called | 1:21–25, 2:15, 5:9, 9:13. Distinct from prefixed compounds (parakaleō "urge", proskaleomai "summon", ekklēsia "assembly") — separate words, not this thread. |
| clean | katharizō | cleanse | Promoted from unit-08's local palette (2026-09-12) when it recurred at 10:8. Opens 8:2–3, pays off 10:8 (one of the Twelve's four powers). |
| come-here | deute | "come here" (a summons) | 4:19, 11:28. |
| cross | stauros | cross | First at 10:38, well before any passion prediction. |
| emmanuel | meta (`data-root="with"`) | "with" — God-with-us | 1:23 "Emmanuel … with us [is] God" ↔ 28:20 "I am with y'all always." |
| evil | ponēros | evil; the evil one; evildoer | "evil one" 5:37, 6:13; "evildoer" 5:39; "evil" elsewhere. |
| faith | pistis · pisteuō | **trust** (not "faith" or "believe") | Noun and verb both. "Faith"/"believe" appear nowhere in the verse text — only in compare-table citations of other translations. |
| father | patēr | Father / father | Tagged at every occurrence, including the ordinary human sense (2:22, 4:21–22). "Father in the skies," not "heavenly Father" (5:48, 6:14, 6:26, 6:32 — fixed 2026-09-12; see sky/skies below). |
| fear | phobeō | fear; be afraid | 1:20, 2:22, 9:8; saturates 10:26–31; recurs at 14:27 and 28:5, 10. |
| fish | halieus | fishers | "fishers of men" (4:19). |
| follow | akoloutheō | follow | A discipleship keyword from Unit 4 on. |
| foolish | mōros · mōrainō | fool; made foolish; stupid | 5:13 salt "made foolish," 5:22 "Fool!", 7:26 "a stupid man" (the deliberate opposite of "shrewd" at 7:24 — Lane's call, keep). Returns 23:17; 25:2. |
| fringe | kraspedon | fringe | 9:20 — the tzitzit of Numbers 15:38. |
| fulfill | plēroō | "filled full" in the formula quotations; "fulfill" in speech | Formula-quotation instances are all now "filled full," unhyphenated: 1:22, 2:15, 2:17, 2:23, 4:14, 8:17 (2026-09-12 — was split between "fulfilled" and hyphenated "filled-full"). Jesus' own speech keeps "fulfill": 3:15, 5:17. **plērōma** (same family) is rendered contextually — "patch" at 9:16, tagged with this root. |
| gehenna | geenna | Gehenna (not "hell") | 5:22 "the Gehenna of fire," 5:29–30, 10:28. |
| generation | genea | generation | 1:17 (literal count) and 11:16 ("this generation," moral sense) — one colour, two senses, not conflated. (1:17 was briefly double-tagged beget+generation; fixed 2026-09-12 to generation alone.) |
| gentle | praus | **gentle** (not "meek") | 5:5, 11:29 — unified 2026-09-12; Jesus claims it of himself at 11:29. Lane's call: gentle everywhere, may still drift by context if a future verse asks for it. |
| good-news | euangelion | **good-news** (hyphenated) | 4:23, 9:35/10:35, 11:5 → 24:14 → 26:13. Hyphen kept throughout (2026-09-12) since it renders one Greek word. "Gospel" is not used in the verse text. |
| hand-over | paradidōmi | hand over | 4:12, 5:25, 10:4 (Judas introduced by it), 10:17–21, 11:27; governs the passion from 17:22 on. |
| immerse | baptizō · baptisma · baptistēs | **immerse / Immerser** (not "baptize" / "Baptist") | Promoted from unit-03's local palette (2026-09-12) when John's title recurred at 11:11–12 as "the Baptizer" — now "the Immerser" throughout. |
| kingdom | basileia | kingdom | "kingdom of the skies" (see sky/skies), not "kingdom of heaven." Plural "kingdoms of the world" 4:8. Distinct from basileus, "king." |
| law-prophets | ho nomos kai hoi prophētai | "the Law and the Prophets" (phrase) | 7:12; "the Law or the Prophets" 5:17; "the Prophets and the Law" 11:13 (follows the Greek word order there). Frames 5:17–7:12. |
| learn | mathētēs · manthanō | **learner** (not "disciple") | Noun "learner" from 5:1; the verb "learn" now also tagged (9:13, 11:29 — added 2026-09-12, was untagged). "Disciple" appears nowhere in the verse text. |
| light | phōs | light | 4:16 → 5:14, 6:22–23, 10:27. |
| little-faith | oligopistoi | "little-faiths" (phrase) | 6:30, 8:26 — Matthew's near-nickname for the learners. The one place "faith" survives, deliberately: a distinct word from `faith` (pistis), own colour. |
| lose | apollymi · apōleia | lose; destroy; perish; lost; ruin | "destroy" 2:13, 10:28; "we are being destroyed" 8:25; "perish" 5:29–30; "lost sheep" 10:6; "lose" 10:39, 42; "ruin" 7:13 (apōleia). |
| mercy | eleos · eleeō | **loyal-love** (Hosea 6:6 sense — hesed, covenant loyalty) | 5:7 fixed 2026-09-12 to match 9:13, 9:27 ("Blessed are the loyal-in-love, for they shall be shown loyal-love"). Lane's call: loyal-love is the standing choice but may drift by context if a specific verse calls for it. "Mercy-deed" (eleēmosynē, almsgiving, 6:2–4) is a different word sharing the root — left as its own contextual rendering, not forced to "loyal-love." |
| metanoia | metanoia · metanoeō | **turn** (not "repent") | Unified 2026-09-12: 3:2 "Turn!", 3:8/3:11 "turning" (unchanged), 4:17 "Turn" (was "Repent"), 11:20 "turn" and 11:21 "turned" (was "change/changed their minds"). |
| nations | ethnē | nations; Gentiles | "Galilee of the nations" (4:15), 6:32, 10:5, 10:18; "Gentiles" 5:47 → "all the nations" (28:19). |
| peace | eirēnē | peace | 5:9 "peacemakers" → 10:13, 10:34 ("not peace but a sword"). |
| raise | egeirō | raise; get up; rise; rouse | Spans the mundane and the resurrection sense: "raised from sleep" 1:24, "rising" 2:13–21, "get up" 9:5–7, "roused him" 8:25, "the dead are raised" 11:5, "has not arisen" 11:11. |
| release | aphiēmi | release; leave; let; permit | Not "forgive" — same verb for sins, a debt, a fever, nets, the dead: "release" 6:12–15, 8:15, 9:2–6; "leaving the nets" 4:20–22; "permit" 3:15; "let me" 7:4; "let him have" 5:40. The nouns "debts"/"debtors" at 6:12 (opheilēma, a different Greek root) were mistakenly tagged under this colour — untagged 2026-09-12. |
| righteous | dikaios · dikaiosynē · dikaioō | righteous(ness); just; right-doing; upright; in the right | Deliberate drift by context (Lane's call, 2026-09-12 — all of these read better than a flattened "righteousness" everywhere): "righteous" 1:19; "righteousness" 3:15, 5:6–20; "right-doing" 6:1, 6:33; "just" 5:45, 10:41; "upright" 9:13; "shown to be in the right" 11:19. |
| rock | petra | rock | Distinct from Petros, the name. 7:24–25 → 16:18. |
| save | sōzō | save | 1:21, 8:25, 9:21–22, 10:22. Carries the heal/rescue sense on purpose (9:21–22); not forced apart. |
| sea | thalassa | sea | Galilee geography (4:13–18) → chaos-and-authority stage (8:24–32). |
| seek | zēteō · epizēteō | seek; seek after | 2:13, 2:20 (Herod) → 6:32–33 → 7:7–8. |
| shake | seismos | shaking | 8:24 "a great shaking … in the sea" = the same word as the cross/tomb earthquakes. |
| sin | hamartia · hamartōlos | sins; sinners | 1:21 → 3:6 → 9:2–13 → 11:19 → 26:28. Pairs with `save` and `release`. (paraptōma at 6:14–15 is "false steps" — a different word, untracked.) |
| skandalon | skandalizō | trip up | 5:29–30 "trips you up", 11:6 "tripped up" → 26:31–33. |
| son-of-david | huios Dauid | "Son of David" (phrase) | 9:27 on, always tied to healing. |
| son-of-man | ho huios tou anthrōpou | "the Son of Man" (phrase) | Daniel 7:13–14. 8:20, 9:6, 10:23, 11:19 → trial → parousia. |
| spirit | pneuma | spirit / Spirit; Holy Spirit | 1:18–20, 3:11, 3:16, 4:1; "poor in the spirit" 5:3; "unclean spirits" 8:16, 10:1. |
| test | peirazō · ekpeirazō | test; tester; test out | 4:1 "tested", 4:3 "the tester", 4:7 "test out" (ekpeirazō), 6:13 "testing." "Tempt" is not used. |
| throw | ballō (+ compounds) | throw (out/down); cast out; pour; put; wrap | Broad, contextual: ekballō "throw out" 7:4–5, 8:12, 10:1, 10:8; periballō "wrapped" 6:29, 6:31; "pour" 9:17; "puts" 9:16. |
| torment | basanizō · basanos | torment | 4:24 → 8:6 ↔ 8:29 inclusio. |
| urge | parakaleō | urge; comfort | "urging" 8:5, 8:31, "urged" 8:34 — same verb bends from trust to rejection. Passive "comforted" 2:18, 5:4. |
| wage | misthos | **wage** (not "reward") | Unified 2026-09-12: 5:12 and 5:46 changed from "reward" to match 6:1–16, 10:41–42. |
| well-pleased | eudokeō · eudokia | delight; well-pleasing | 3:17 "in whom I delighted" → 11:26 "well-pleasing before you." |
| wise | phronimos | **shrewd** (not "wise") | 7:24, 10:16 → 24:45, 25:2. ("Wise and perceptive" at 11:25 is sophos — a different word, untracked.) |
| withdraw | anachōreō | withdraw; clear out | 2:12–22, 4:12 — Matthew's standing verb for tactical retreat. Imperative "clear out" 9:24. |
| worship | proskyneō | worship; bow low; kneel low | "worship" for the magi and the tester (2:2–11, 4:9–10); "bowing low" 8:2 and "knelt low" 9:18 for suppliants → 28:9, 17. |
| worthy | axios | worthy | 3:8 ("fruit worthy of the turning") → 10:10–38. |

## Unit-local words (consistent so far, not yet promoted to a global colour)

Same idea, smaller stage — these haven't recurred across enough units to
be tracked book-wide yet, but the rendering below is what's been used
where they've appeared.

| root | Greek | rendering | first seen |
|---|---|---|---|
| anxious → **promoted to a global thread 2026-09-12** | — | — | see table above |
| ask | aiteō | ask | unit-07 |
| beget | gennaō · genesis | beget, begot; genesis | unit-01 ("Book of the genesis" 1:1, "the genesis was thus" 1:18) |
| burden | phortion · phortizō | burden; burdened | unit-11 |
| child | paidion | the child | unit-02 |
| clean → **promoted to a global thread 2026-09-12** | — | — | see table above |
| dark | skotia · skotos | darkness; the dark | unit-04 |
| david | Dauid | David | unit-01 |
| deeds | ergon | deeds | unit-11 (11:2 ↔ 11:19 — both occurrences now tagged; 11:2's verse text was missing the tag until 2026-09-12) |
| do | poieō | do, make | unit-07 ("make fruit" 7:17–19) |
| dream | onar | dream | unit-01 |
| enter | eiserchomai | come in, come into | unit-07 |
| eye | ophthalmos | eye | unit-07 |
| fruit | karpos | fruit | unit-07 |
| gate | pylē | gate | unit-07 |
| harvest | therismos | harvest | unit-10 ("the Master of the harvest" 9:38) |
| hidden | kryptos · kryphaios | "the hidden place" | unit-06 |
| hide-reveal | kryptō · apokalyptō | hide / reveal | unit-11 |
| immerse → **promoted to a global thread 2026-09-12** | — | — | see table above |
| judge | krinō · krima | judge; verdict (krima) | unit-07 |
| king | basileus | king | unit-02 |
| measure | metron · metreō | measure; measure out / back | unit-07 |
| name | onoma | name | unit-01 |
| **proclaim** | kēryssō | **proclaim** (not "herald" or "preach") | unit-04 (3:1, 4:17, 4:23, 9:35, 10:7, 10:27, 11:1) — see note below |
| receive | dechomai | receive | unit-10 |
| reed | kalamos | reed | unit-11 |
| reproach | oneidizō | reproach | unit-11 |
| seen | theaomai | gaze at | unit-06 ("to be gazed at" 6:1; "go out … to gaze at" 11:7) |
| seize | harpazō · biazomai | is under assault; seize | unit-11 (11:12) |
| send-out | apostellō · apostolos | send (out); **emissaries** (the Twelve, 10:2) | unit-10 |
| shadow | skia | shadow | unit-04 |
| slanderer | diabolos | the slanderer | unit-03 (4:1–11) |
| son | huios | Son (of God) | unit-03 |
| touch | haptomai | take hold of; touch | unit-08 ("took hold of" 8:3, 8:15; "touched" 9:29) |
| treasure | thēsauros · thēsaurizō | treasure; treasure up | unit-06 |
| way | hodos | road | unit-07 ("the road that leads off" 7:13–14; "clear your road" 11:10) |
| whole | holos · teleios | whole | unit-05 ("whole body" 5:29–30; "be whole as … Father is whole" 5:48) |
| wilderness | erēmos | wilderness | unit-03 |
| yoke | zygos | yoke | unit-11 |

> **proclaim, not herald:** `data-root="proclaim"` had been introduced with
> the gloss "proclaim, herald," and the running-translation word had
> drifted to "herald" in several verses (3:1, 9:35, 10:7, 10:27, 11:1) before
> being corrected. "Proclaim" is the standing choice; "herald" survives only
> in commentary prose used descriptively (e.g. "the herald and the one
> heralded"), never as translation. "Preach" is likewise not used as
> translation (it appears only in commentary prose).

> **lepros, rendered literally:** "leprous" / "leprosy" (8:1–4), "lepers"
> (11:5), and — fixed 2026-09-12 — 10:8's "skin-diseased" is now "cleanse
> the leprous" to match. No euphemism; render the plain word.

> **synagōgē, two acceptable renderings:** "synagogues" (4:23) and
> "gathering-places" (9:35/10:35, 10:17) both stand — Lane's call: either
> English rendering beats transliterating "synagogue," and there's no need
> to force one everywhere.

## General style conventions (not colour-tracked at all)

Register and idiom decisions that apply across the whole translation,
regardless of which Greek word is in play.

- **y'all / y'all's** — the plural "you" (hymeis/hymin/hymas/hymōn), kept
  distinct from singular "you" throughout; possessive is "y'all's." Fixed
  2026-09-12: 11:17 "beat your chests" → "beat y'all's chests"; 11:29 "rest
  for your souls" → "rest for y'all's beings" (see life/being, below). A
  broad re-check of every other "your" in units 1–11 confirmed the rest are
  correctly singular (Jesus or the Law addressing one person, or the Lord's
  Prayer addressing God) — not errors, don't "fix" those.
- **life / being, not soul** — psychē (2:20, 6:25, 10:28, 10:39, and now
  11:29 "y'all's beings" — fixed 2026-09-12, was "your souls"). "Being" is
  used for the plural (11:29); "life" for the singular elsewhere.
- **sky/skies, not heaven(s)** — ouranos, including the adjective ouranios:
  "Father in the skies," not "heavenly Father" (fixed 2026-09-12 at 5:48,
  6:14, 6:26, 6:32). Applies everywhere: "kingdom of the skies," "birds of
  the sky." (Swept book-wide by `pipeline/wording_skies.py` for units 1–5;
  units 6+ were drafted with it already in place.)
- **Master, not Lord** — kyrios addressing Jesus or a human master ("Master,
  save" 8:25; "the Master of the harvest" 9:38; slave/master 6:24,
  10:24–25). **Yahweh** — kyrios standing for the divine name: "an angel of
  Yahweh" (1:20 etc.), OT quotations (3:3, 4:7, 4:10, 5:33), and Jesus'
  address "Father, Yahweh of the sky and the earth" (11:25). "Lord"/"LORD"
  does not appear in the verse text.
- **Anointed, not "Christ"** — christos, kept as a title rather than a
  surname: "Jesus Anointed" (1:1, 1:18), "the one called Anointed" (1:16),
  "the Anointed" (1:17, 2:4, and the 11:2 ring-diagram label, fixed
  2026-09-12 from "the Christ"), "the Anointed One" (11:2 verse text).
- **look, not behold** — idou. Units 1–2 said "behold" at five places (1:20,
  1:23, 2:1, 2:9, 2:13, 2:19); unified to "look" 2026-09-12 to match unit 3
  onward.
- **amen, not truly** — amēn as a transliterated oath-opener: "Amen I say to
  y'all" (5:18, 6:2, 10:15…), "Amen I tell y'all" (8:10, and 11:11 — fixed
  2026-09-12, was "Truly I tell y'all").
- **"pulled apart with care," not "anxious"** — merimnaō, now the rendering
  everywhere the verb appears, including 10:19 (fixed 2026-09-12, was "do
  not be anxious"), matching 6:25–34.
- **Immerser, not Baptist/Baptizer** — baptistēs, John's title (3:1, and now
  11:11–12, fixed 2026-09-12 — see the `immerse` thread above).
- **Adversary** — satanas, as a common noun-title ("Go away, Adversary!"
  4:10). Keep distinct from diabolos, "the slanderer."
- **wrenched in the gut, not "moved with compassion"** — splanchnizomai; a
  deliberately bodily, blunt phrase (9:36), not a tender one.
- **harassed, not harried** — eskylmenoi (9:36) — plainer diction, matches
  the study's register.
- **stage-actors, not hypocrites** — hypokritēs (6:2, 6:5, 6:16).
- **sham-prophets, not false prophets** — pseudoprophētēs (7:15).
- **demon; demon-possessed** — daimonion / daimonizomai (4:24 "demon-oppressed",
  8:16, 8:28–33, 9:32–34, 10:8, 11:18).
- **messenger vs. angel** — angelos is "angel" for heavenly beings (1:20,
  4:6, 4:11) and "messenger" for the Malachi quotation about John (11:10).
- **slave, not servant** — doulos (8:9, 10:24–25); "to slave for" (6:24).
- **trust, not faith/believe** — see `faith` in the global table above;
  called out again here because it's easy to slip back into "faith" from
  habit.

## Log

- 2026-09-11 — added `learn` (learner, not disciple) as a new global thread;
  fixed `fulfill` gap at 9:16; corrected `proclaim` (was drifting to
  "herald"); fixed `harried` → `harassed` and two missed `lord` → `master`
  instances in Unit 10.
- 2026-09-12 (audit) — full audit against units 1–11 verse text; rewrote
  rows to describe actual renderings; ~12 drifts surfaced under "Open calls"
  for Lane's ruling. No unit text changed in this pass.
- 2026-09-12 (rulings applied) — Lane ruled on every open call; changes made
  to units 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 and to data/threads.json:
  - **Wording fixed to match the standing choice:** metanoia → turn (3:2 kept,
    4:17/11:20/11:21 changed); mercy 5:7 → loyal-love; wage 5:12/5:46 → wage;
    gentle 5:5 → gentle; "Father in the skies" (5:48, 6:14, 6:26, 6:32, was
    "heavenly Father"); Immerser (11:11–12, was "Baptizer"); lepros 10:8 →
    "cleanse the leprous" (was "skin-diseased"); fulfill formula unified to
    "filled full" (1:22, 2:15, 2:17, 2:23, 4:14, 8:17); look (1:20, 1:23, 2:1,
    2:9, 2:13, 2:19, was "behold"); amen 11:11 (was "Truly"); "pulled apart
    with care" 10:19 (was "anxious"); good-news hyphenated everywhere (10:35,
    11:5); y'all's for plural possessive (11:17 chests, 11:29 beings, was
    "your … souls"); "the Anointed" in the unit-11 ring diagram (was "the
    Christ").
  - **Ruled to keep as intentional context-drift:** dikaios family (righteous
    /just/right-doing/upright/in the right); 7:26 "stupid" (not "foolish");
    synagōgē (both "synagogues" and "gathering-places" stand); mercy-deed
    (eleēmosynē) stays a separate rendering from loyal-love.
  - **New global thread:** acts-of-power (dynamis) — tagged at 7:22 and
    11:20–23, replacing untagged "miracles."
  - **Threads promoted from local to global** (recurred in a second unit):
    immerse (unit-03 → 11), anxious (unit-06 → 10), clean (unit-08 → 10).
  - **Tagging fixes:** untagged 6:12 "debts"/"debtors" (wrongly under
    `release`, a different Greek root); consolidated 1:17's four
    "generations" onto the `generation` root alone (was double-tagged
    beget+generation on the first one, `beget` alone on the rest); tagged
    the `learn` verb at 9:13 and 11:29 (was untagged); tagged `deeds` in
    11:2's and 11:19's verse text (was tagged only in the structure ring,
    not the running translation); updated three stale threads.json glosses
    (release, gehenna, learn).
  - Ran `pipeline/build.py` clean after every change (retrofit-tags.json's
    recorded literal text updated to match 6 reworded verses so replay stays
    idempotent; three new thread colours picked to clear the Lab-distance
    check against every other colour active in their units).
