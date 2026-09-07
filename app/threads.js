/* Two-tier colour resolution + data-driven legend.
   Global tier: data/threads.json (a tracked root's colour is identical in every
   unit). Local tier: data/units.json roots {color,translit,gloss}. */

const bust = (u) => { const x = new URL(u); x.searchParams.set("v", Date.now()); return x; };
const THREADS_URL = new URL("../data/threads.json", import.meta.url);
const OCC_URL = new URL("../data/occurrences.json", import.meta.url);

let _threads = null; // { byRoot: Map, list: [] }
let _occ = null;

export async function loadThreadData() {
  if (!_threads) {
    const [t, o] = await Promise.all([
      fetch(bust(THREADS_URL)).then((r) => r.json()),
      fetch(bust(OCC_URL)).then((r) => r.json()).catch(() => ({})),
    ]);
    _threads = { list: t.threads, byRoot: new Map(t.threads.map((x) => [x.root, x])) };
    _occ = o;
  }
  return _threads;
}

/** root -> { color, translit, gloss, threadId|null, status, count } for one unit */
export function resolveUnit(unit) {
  const out = new Map();
  const local = unit.roots || {};
  const counts = (_occ && _occ[unit.slug]) || {};
  const names = new Set([...Object.keys(local), ...Object.keys(counts)]);
  for (const root of names) {
    const th = _threads.byRoot.get(root);
    const lc = local[root];
    const localMeta = typeof lc === "string" ? { color: lc } : lc || {};
    out.set(root, {
      color: th ? th.color : localMeta.color || null,
      translit: (th && th.translit) || localMeta.translit || root,
      gloss: (th && th.gloss) || localMeta.gloss || "",
      threadId: th ? th.id : null,
      status: th ? th.status : null,
      count: (counts[root] && counts[root].count) || 0,
    });
  }
  return out;
}

/** Inject `.unit[data-unit=N] [data-root=x]{color}` + legend swatch colours. */
export function injectPalette(unit, resolved) {
  document.getElementById("unit-palette")?.remove();
  const rules = [];
  for (const [root, m] of resolved) {
    if (!m.color) continue;
    const sel = `.unit[data-unit="${unit.n}"]`;
    rules.push(`${sel} [data-root="${cssEsc(root)}"]{color:${m.color}}`);
    rules.push(`${sel} .swatch[style*="--c-${cssEsc(root)}"]{background:${m.color}!important}`);
  }
  const s = document.createElement("style");
  s.id = "unit-palette";
  s.textContent = rules.join("\n");
  document.head.appendChild(s);
}

/** Rebuild the unit's colour-key list from data. */
export function rebuildLegend(contentEl, resolved) {
  const legend = contentEl.querySelector("section.legend, section.block.legend");
  if (!legend) return;
  const ul = legend.querySelector("ul");
  if (!ul) return;

  const rows = [...resolved.entries()]
    .filter(([, m]) => m.color && m.count > 0)
    .sort((a, b) =>
      (b[1].threadId ? 1 : 0) - (a[1].threadId ? 1 : 0) || b[1].count - a[1].count);

  ul.innerHTML = rows.map(([root, m]) => {
    const pill = m.threadId
      ? ` <span class="tag tag-thread" title="tracked cross-unit thread — same colour everywhere">thread${m.status === "closed" ? " · closed" : ""}</span>`
      : "";
    const n = m.count > 1 ? ` <span class="tag">${m.count}×</span>` : "";
    return `<li><span class="swatch" style="background:${m.color}"></span>` +
      `<span class="r" data-root="${escAttr(root)}">${esc(m.translit)}</span>` +
      `${m.gloss ? " — " + esc(m.gloss) : ""}${pill}${n}</li>`;
  }).join("");

  let cap = legend.querySelector(".cap");
  if (!cap) {
    cap = document.createElement("p");
    cap.className = "cap";
    legend.querySelector("h2")?.after(cap);
  }
  const nThreads = rows.filter(([, m]) => m.threadId).length;
  cap.textContent = nThreads
    ? `${rows.length} roots tracked in this unit — ${nThreads} are cross-unit threads (same colour book-wide).`
    : `${rows.length} roots tracked in this unit.`;
}

function esc(s) { return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])); }
function escAttr(s) { return String(s).replace(/"/g, "&quot;"); }
function cssEsc(s) { return s.replace(/[^a-zA-Z0-9_-]/g, "\\$&"); }
