/* Concordance search — type a transliterated root or an English gloss, get
   every tagged occurrence across the built units with a context snippet,
   then every Greek lemma in the book that matches (data/lemmas.json), with
   all its references.

   #/search/<query> pre-fills and runs the query (the interlinear's words link
   here with their lemma id); plain #/search restores the last one. */

import { getOccurrences, getThreadFor, resolveUnit } from "./threads.js?v=38";
import { loadLemmas, unitForRef } from "./interlinear.js?v=40";

const KEY = "matthew.search.q";

export function renderSearch(container, units, query = null) {
  if (query !== null) {
    try { sessionStorage.setItem(KEY, query); } catch (e) { /* private mode */ }
  }
  let q0 = query;
  if (q0 === null) {
    try { q0 = sessionStorage.getItem(KEY) || ""; } catch (e) { q0 = ""; }
  }
  container.innerHTML = `
    <div class="search-view">
      <h1>Concordance</h1>
      <p class="search-hint">Type a transliterated root (<i>aphiēmi</i>, or just <i>aphiemi</i>)
        or an English gloss (<i>forgive</i>). Searches the tagged roots in every built unit,
        then every Greek word in Matthew.</p>
      <input id="search-input" type="search" autocomplete="off" spellcheck="false"
        placeholder="root or gloss…" value="${escAttr(q0)}">
      <div id="search-results" class="search-results"></div>
    </div>`;

  const input = container.querySelector("#search-input");
  const out = container.querySelector("#search-results");
  const index = buildIndex(units);

  let lemmas = null;
  loadLemmas().then((l) => { lemmas = l; run(); });

  let t;
  const run = () => {
    const q = input.value.trim();
    try { sessionStorage.setItem(KEY, q); } catch (e) { /* private mode */ }
    const want = q ? `#/search/${encodeURIComponent(q)}` : "#/search";
    if (location.hash.startsWith("#/search") && location.hash !== want) history.replaceState(null, "", want);
    // a query that is exactly a lemma id (what the interlinear links with)
    // shows that word first, above the tracked roots (Lane, 2026-09-30)
    const own = lemmas?.[q] ? lemmaBlock("Greek word", [[q, lemmas[q]]], 0, units, true) : "";
    // one letter is too broad to search past that (ē, ō)
    if (q.length < 2) { out.innerHTML = own; return; }
    const html = own + results(q, index, units) + (lemmas ? lemmaResults(q, lemmas, units) : "");
    out.innerHTML = html || (lemmas ? `<p class="search-empty">Nothing matches “${esc(q)}”.</p>` : "");
  };
  input.addEventListener("input", () => { clearTimeout(t); t = setTimeout(run, 120); });
  input.focus();
  run();
}

/* root -> { meta, translit, gloss, thread, units:[{unit, hits}] } over built units */
function buildIndex(units) {
  const occ = getOccurrences();
  const byN = new Map(units.map((u) => [u.n, u]));
  const idx = new Map();

  for (const [slug, roots] of Object.entries(occ)) {
    const n = Number(slug.split("-")[1]);
    const unit = byN.get(n);
    if (!unit || !unit.built) continue;
    const resolved = resolveUnit(unit);
    for (const [root, data] of Object.entries(roots)) {
      if (!data.hits || !data.hits.length) continue;
      let e = idx.get(root);
      if (!e) {
        const m = resolved.get(root) || {};
        e = {
          root,
          color: m.color || null,
          translit: m.translit || root,
          gloss: m.gloss || "",
          thread: getThreadFor(root),
          units: [],
          total: 0,
        };
        idx.set(root, e);
      }
      e.units.push({ unit, hits: data.hits });
      e.total += data.hits.length;
    }
  }
  return idx;
}

function results(query, idx, units) {
  const q = fold(query);
  const matches = [...idx.values()].filter((e) =>
    fold(e.translit).includes(q) || fold(e.gloss).includes(q) || e.root.includes(q));

  if (!matches.length) return "";

  matches.sort((a, b) => (b.thread ? 1 : 0) - (a.thread ? 1 : 0) || b.total - a.total);

  return matches.map((e) => {
    const units_ = e.units
      .sort((a, b) => a.unit.n - b.unit.n)
      .map((u) => `
        <div class="sr-unit">
          <a class="sr-unit-h" href="#/${u.unit.slug}">Unit ${u.unit.n} · ${esc(u.unit.title)}</a>
          <ul>${u.hits.map((h) => `
            <li><a href="#/${u.unit.slug}${h.v ? "/v" + h.v : ""}">
              ${h.v ? `<span class="sr-v">v.${h.v}</span> ` : ""}${esc(h.pre)}<b>${esc(h.hit)}</b>${esc(h.post)}</a></li>`).join("")}
          </ul>
        </div>`).join("");
    return `
      <section class="sr-root">
        <h3>
          ${e.color ? `<span class="swatch" style="background:${e.color}"></span>` : ""}
          <i>${esc(e.translit)}</i>${e.gloss ? ` — ${esc(e.gloss)}` : ""}
          ${e.thread ? `<span class="sr-tag">thread${e.thread.status === "closed" ? " · closed" : ""}</span>` : ""}
          <span class="sr-n">${e.total}</span>
        </h3>
        ${units_}
      </section>`;
  }).join("");
}

/* ---- Greek words (every lemma, tracked or not), after core's sr-lemma ----
   Matches the transliterated lemma or (from three letters) the gloss; exact
   transliterations first, then by frequency. A lemma whose id is exactly the
   query is left out: run() already put it at the top. */
function lemmaResults(query, lemmas, units) {
  const f = fold(query);
  const hits = Object.entries(lemmas).filter(([k, e]) =>
    k !== query && (fold(e.t).includes(f) || (f.length > 2 && fold(e.g).includes(f))));
  if (!hits.length) return "";
  hits.sort((a, b) => (fold(b[1].t) === f) - (fold(a[1].t) === f) || b[1].n - a[1].n);
  const shown = hits.slice(0, 12);
  return lemmaBlock(lemmas[query] ? "Other Greek words in Matthew" : "Greek words in Matthew",
    shown, hits.length - shown.length, units, hits.length === 1 && !lemmas[query]);
}

function lemmaBlock(title, shown, more, units, open) {
  return `<section class="sr-block"><h3>${title}</h3>` + shown.map(([k, e]) => `
    <details class="sr-lemma"${open ? " open" : ""}>
      <summary><i>${esc(e.t)}</i> — ${esc(e.g)} <span class="sr-n">${e.n}×${k !== e.t ? ` · lemma ${esc(k)}` : ""}</span></summary>
      <p class="sr-refs">${e.refs.map((r) => refLink(r, units)).join(" ")}</p>
    </details>`).join("") +
    (more > 0 ? `<p class="search-empty">${more} more; narrow the search.</p>` : "") +
    `</section>`;
}

/* linked where the unit is built, dimmed where it isn't */
function refLink(ref, units) {
  const [c, v] = ref.split(":").map(Number);
  const u = unitForRef(c, v, units);
  return u?.built ? `<a href="#/${u.slug}/${ref}">${ref}</a>` : `<span class="sr-unbuilt">${ref}</span>`;
}

/* fold diacritics so "aphiemi" matches "aphiēmi", "hoba" matches "ḥoba" */
function fold(s) {
  return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
}
function esc(s) { return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])); }
function escAttr(s) { return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
