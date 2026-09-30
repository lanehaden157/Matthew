/* Interlinear reading mode: the Greek of each verse word by word under it.
   Transliterated word, MorphGNT lexicon gloss, parsing. Each word links to
   search for its lemma.

   Adapted from bible-core web/app/reader.js (@25efd85): passageRange,
   indexVerses, findVerse, mountInterlinear and unmountInterlinear. What
   changed and why is in docs/interlinear-pilot.md. The book-specific parts
   (data folder, link format, book name) are options, so this can move
   back to core.

   Data (built by pipeline/build_words.py, fetched lazily, cached per page):
     data/words/<ch>.json  {"c", "verses": {"1": [{"w", "t", "l", "m"}]}}
     data/lemmas.json      {"lemmas": {"<id>": {"t", "g", "n", "refs"}}}

   Glosses identify the word for the reader. They are never the study's
   rendering, and the key line says so. No native script: the data carries
   none. */

const DEFAULTS = {
  data: new URL("../data/", import.meta.url),
  lemmaHref: (id) => `#/search/${encodeURIComponent(id)}`,
  book: "the book",
};

const cache = new Map();
function getJSON(base, p) {
  const url = new URL(p, base).href;
  if (!cache.has(url)) {
    cache.set(url, fetch(url).then((r) => (r.ok ? r.json() : null)).catch(() => null));
  }
  return cache.get(url);
}
export const loadLemmas = (opts = {}) =>
  getJSON(opts.data || DEFAULTS.data, "lemmas.json").then((d) => d?.lemmas || {});
const loadChapter = (base, c) => getJSON(base, `words/${c}.json`).then((d) => d?.verses || {});

/* ------------------------------------------------------------ references */

const RANGE_RE = /(\d+):(\d+)\s*[–-]\s*(?:(\d+):)?(\d+)/;

/* [lo, hi] as [c, v] pairs from "Matthew 9:35–11:1" or "Matthew 5:1-48" */
export function passageRange(passage) {
  const m = RANGE_RE.exec(passage || "");
  if (!m) {
    const one = /(\d+):(\d+)/.exec(passage || "");
    return one ? [[+one[1], +one[2]], [+one[1], +one[2]]] : null;
  }
  return [[+m[1], +m[2]], [+(m[3] || m[1]), +m[4]]];
}

const cmp = (a, b) => a[0] - b[0] || a[1] - b[1];

export function unitForRef(c, v, units) {
  return units.find((u) => {
    const r = passageRange(u.passage);
    return r && cmp(r[0], [c, v]) <= 0 && cmp([c, v], r[1]) <= 0;
  }) || null;
}

/* Stamp every verse block with data-ref="C:V". Fragments carry bare verse
   numbers, so the chapter starts at the unit's passage and rolls over: an
   explicit "11:1" resets it, a bare number that goes backwards moves to the
   next chapter. */
export function indexVerses(root, unit) {
  const r = passageRange(unit.passage);
  let ch = r ? r[0][0] : 1, prev = null;
  for (const el of root.querySelectorAll("p.v, div.v")) {
    const t = el.querySelector(".n")?.textContent.trim() || "";
    const m = /^(?:(\d+):)?(\d+)$/.exec(t);
    if (!m) continue;
    const v = +m[2];
    if (m[1]) { ch = +m[1]; prev = null; }
    else if (prev !== null && v < prev) ch += 1;
    prev = v;
    el.dataset.ref = `${ch}:${v}`;
  }
}

/* "5:3" -> that verse; a verse with no block of its own (6:10 sits inside
   the Lord's Prayer block) -> its interlinear box if mounted, else the
   closest verse before it */
export function findVerse(root, anchor) {
  const cv = /^(\d+):(\d+)$/.exec(anchor);
  if (!cv) return null;
  const want = [+cv[1], +cv[2]];
  const exact = root.querySelector(`.v[data-ref="${anchor}"], .il-gap[data-ref="${anchor}"]`);
  if (exact) return exact;
  let best = null;
  for (const el of root.querySelectorAll(".v[data-ref]")) {
    if (cmp(el.dataset.ref.split(":").map(Number), want) <= 0) best = el;
  }
  return best;
}

/* ------------------------------------------------------------ interlinear */

const HEADING_SEL = "h2, h3, .sectionhead, .panelhead, .movement, .spot-controls";

/* Mount word boxes under every indexed verse of root (call indexVerses
   first). Verses the fragment has no block for, like 6:10–13 inside the
   prayer block, get labelled boxes just before the next verse. Returns once
   the chapter files have loaded; a later unmount cancels a pending mount. */
export async function mountInterlinear(root, unit, opts = {}) {
  const o = { ...DEFAULTS, ...opts };
  if (root.querySelector(".il")) return;
  const gen = (root._ilGen = (root._ilGen || 0) + 1);
  const verses = [...root.querySelectorAll(".v[data-ref]")];
  const refs = verses.map((el) => el.dataset.ref.split(":").map(Number));
  const chapters = [...new Set(refs.map((r) => r[0]))];
  const [lemmas, ...chs] = await Promise.all([loadLemmas(o), ...chapters.map((c) => loadChapter(o.data, c))]);
  if (root._ilGen !== gen || root.querySelector(".il")) return;
  const byCh = new Map(chapters.map((c, i) => [c, chs[i]]));
  const words = (c, v) => byCh.get(c)?.[String(v)];

  verses.forEach((el, i) => {
    const [c, v] = refs[i];
    if (i > 0) {
      const gap = between(refs[i - 1], refs[i], byCh);
      const at = gapAnchor(el);
      for (const [gc, gv] of gap) {
        const ws = words(gc, gv);
        if (ws?.length) at.before(box(ws, gc, gv, lemmas, o, true));
      }
    }
    const ws = words(c, v);
    if (ws?.length) el.after(box(ws, c, v, lemmas, o, false));
  });

  if (!root.querySelector(".il-key")) {
    const key = document.createElement("p");
    key.className = "il-key";
    key.textContent = "Interlinear: the Greek transliterated, a lexicon gloss (it identifies " +
      "the word; it isn't this study's translation) and the grammar. Tap a word to find " +
      `every place its lemma occurs in ${o.book}.`;
    keyAnchor(root)?.before(key);
  }
}

export function unmountInterlinear(root) {
  root._ilGen = (root._ilGen || 0) + 1;
  root.querySelectorAll(".il, .il-key").forEach((e) => e.remove());
}

function box(ws, c, v, lemmas, o, gap) {
  const el = document.createElement("div");
  el.className = gap ? "il il-gap" : "il";
  el.setAttribute("aria-label", `Interlinear, ${c}:${v}`);
  if (gap) el.dataset.ref = `${c}:${v}`;
  el.innerHTML = (gap ? `<span class="il-ref">${c}:${v}</span>` : "") + ws.map((w) => {
    const lem = lemmas[w.l] || {};
    const title = [lem.g && `Gloss: ${lem.g}`, w.m, lem.n && `${lem.n}× in ${o.book}`]
      .filter(Boolean).join(" · ");
    return `<a class="il-w" href="${esc(o.lemmaHref(w.l))}" title="${esc(title)}">` +
      `<i>${esc(w.t)}</i><b>${esc(lem.g || "—")}</b><small>${esc(w.m)}</small></a>`;
  }).join("");
  return el;
}

/* the verses strictly between two refs that the chapter data has */
function between(a, b, byCh) {
  const out = [];
  for (let c = a[0]; c <= b[0]; c++) {
    const vs = Object.keys(byCh.get(c) || {}).map(Number).sort((x, y) => x - y);
    for (const v of vs) {
      if (cmp([c, v], a) > 0 && cmp([c, v], b) < 0) out.push([c, v]);
    }
  }
  return out;
}

/* before the next verse, but above any heading that opens it */
function gapAnchor(verse) {
  let at = verse;
  while (at.previousElementSibling?.matches(HEADING_SEL)) at = at.previousElementSibling;
  return at;
}

/* above the first verse (and the heading or notes bar over it) */
function keyAnchor(root) {
  const article = root.querySelector("article.unit") || root;
  const bar = article.querySelector(".spot-controls");
  if (bar) return bar;
  let at = article.querySelector(".v[data-ref]");
  if (!at) return null;
  while (at.parentElement && at.parentElement !== article) at = at.parentElement;
  return gapAnchor(at);
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}
