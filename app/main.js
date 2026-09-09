/* Matthew Study — tab router + footnote interactions.
   Plain ES module, no build step. Paths are relative so it works from a GitHub
   Pages subpath. */

import { loadThreadData, resolveUnit, injectPalette, rebuildLegend, wireRoots } from "./threads.js?v=31";
import { enhanceSpotlights } from "./spotlight.js?v=31";
import { renderSearch } from "./search.js?v=31";

const UNITS_URL = new URL("../data/units.json", import.meta.url);

// always revalidate — a no-build static site changes the moment files are pushed
// no build step: always fetch the current file, never a cached copy
const bust = (u) => { const x = new URL(u); x.searchParams.set("v", Date.now()); return x; };

const content = document.getElementById("content");
const unitNav = document.getElementById("unit-nav");
const pager = document.getElementById("unit-pager");
const navToggle = document.getElementById("nav-toggle");
const navToggleCtx = document.getElementById("nav-toggle-ctx");

let manifest = null;

init();

async function init() {
  try {
    [manifest] = await Promise.all([
      fetch(bust(UNITS_URL)).then((r) => r.json()),
      loadThreadData(),
    ]);
  } catch (e) {
    content.innerHTML = `<p class="missing">Could not load site data (<code>data/*.json</code>).</p>`;
    return;
  }
  buildUnitNav();
  wireNavToggle();
  window.addEventListener("hashchange", route);
  route();
}

function wireNavToggle() {
  const backdrop = document.getElementById("nav-backdrop");
  const set = (open) => {
    unitNav.hidden = !open;
    backdrop.hidden = !open;
    navToggle.setAttribute("aria-expanded", String(open));
    if (open) unitNav.scrollTop = 0;
  };
  navToggle.addEventListener("click", () => set(unitNav.hidden));
  backdrop.addEventListener("click", () => set(false));
  unitNav.addEventListener("click", (e) => {
    if (e.target.closest("a.unit-chip, a.bm-tick")) set(false);
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") set(false); });
}

/* ----------------------------------------------------------------- unit nav */

function discourseOf(n) {
  return (manifest.discourses || []).find((d) => d.units.includes(n)) || null;
}

function chip(u) {
  const d = discourseOf(u.n);
  const a = document.createElement("a");
  a.className = "unit-chip" + (u.built ? "" : " unbuilt") + (d ? " in-disc" : "");
  a.dataset.slug = u.slug;
  if (u.built) a.href = `#/${u.slug}`;
  if (d) a.title = `Discourse ${roman(d.n)} — ${d.label}`;
  a.innerHTML =
    (d ? `<span class="disc-mark" aria-hidden="true">◆&nbsp;${roman(d.n)}</span>` : "") +
    `<span class="n">${u.n}</span>${escapeHtml(u.title)}` +
    `<span class="passage">${escapeHtml(u.passage)}${u.built ? "" : " · not yet built"}</span>`;
  return a;
}

function unitsByMovement() {
  const m = new Map();
  for (const u of manifest.units) {
    if (!m.has(u.movement)) m.set(u.movement, []);
    m.get(u.movement).push(u);
  }
  return m;
}

/* A map of the whole book: 28 ticks grouped into the 3 movements, with the
   5 discourses drawn as brackets spanning the units they cover. */
function buildBookMap() {
  const by = unitsByMovement();
  const wrap = document.createElement("div");
  wrap.className = "book-map";

  const scroller = document.createElement("div");
  scroller.className = "bm-scroll";
  const row = document.createElement("div");
  row.className = "bm-row";

  for (const m of manifest.movements) {
    const us = by.get(m.id) || [];
    if (!us.length) continue;
    const cols = `repeat(${us.length}, minmax(0, 1fr))`;

    const grp = document.createElement("div");
    grp.className = "bm-mv";
    grp.style.flex = String(us.length);

    const lab = document.createElement("div");
    lab.className = "bm-mv-label";
    lab.innerHTML = `<i></i><b>${roman(m.id)}</b><i></i>`;
    lab.title = `Movement ${roman(m.id)} — ${m.label}`;
    grp.appendChild(lab);

    const ticks = document.createElement("div");
    ticks.className = "bm-ticks";
    ticks.style.gridTemplateColumns = cols;
    for (const u of us) {
      const t = document.createElement(u.built ? "a" : "span");
      t.className = "bm-tick" + (u.built ? "" : " unbuilt") + (discourseOf(u.n) ? " in-disc" : "");
      t.dataset.slug = u.slug;
      t.textContent = u.n;
      t.title = `Unit ${u.n} · ${u.title} · ${u.passage}${u.built ? "" : " (not yet built)"}`;
      if (u.built) t.href = `#/${u.slug}`;
      ticks.appendChild(t);
    }
    grp.appendChild(ticks);

    const brs = document.createElement("div");
    brs.className = "bm-brackets";
    brs.style.gridTemplateColumns = cols;
    const first = us[0].n;
    for (const d of manifest.discourses || []) {
      const inHere = d.units.filter((n) => us.some((u) => u.n === n));
      if (!inHere.length) continue;
      const a = Math.min(...inHere) - first + 1;
      const b = Math.max(...inHere) - first + 2;
      const el = document.createElement("div");
      el.className = "bm-disc";
      el.style.gridColumn = `${a} / ${b}`;
      el.innerHTML = `<span class="bm-disc-bar"></span>` +
        `<span class="bm-disc-label">◆&nbsp;${roman(d.n)}</span>`;
      el.title = `Discourse ${roman(d.n)} — ${d.label} (Units ${d.units.join(", ")})`;
      brs.appendChild(el);
    }
    grp.appendChild(brs);
    row.appendChild(grp);
  }

  scroller.appendChild(row);
  wrap.appendChild(scroller);

  const key = document.createElement("div");
  key.className = "bm-key";
  key.innerHTML =
    `<div class="bm-key-row"><span class="bm-key-h">Movements</span><span class="bm-key-items">` +
      manifest.movements.map((m) =>
        `<span class="bm-key-item"><b>${roman(m.id)}</b> ${escapeHtml(m.label)}</span>`).join("") +
    `</span></div>` +
    `<div class="bm-key-row disc"><span class="bm-key-h">Discourses</span><span class="bm-key-items">` +
      (manifest.discourses || []).map((d) =>
        `<span class="bm-key-item"><b>◆&nbsp;${roman(d.n)}</b> ${escapeHtml(d.label)}</span>`).join("") +
    `</span></div>`;
  wrap.appendChild(key);
  return wrap;
}

function buildUnitNav() {
  const by = unitsByMovement();
  const frag = document.createDocumentFragment();
  frag.appendChild(buildBookMap());

  for (const m of manifest.movements) {
    const label = document.createElement("div");
    label.className = "movement-label";
    label.textContent = `Movement ${roman(m.id)} · ${m.label}`;
    frag.appendChild(label);

    const grid = document.createElement("div");
    grid.className = "unit-grid";
    for (const u of by.get(m.id) || []) grid.appendChild(chip(u));
    frag.appendChild(grid);
  }
  unitNav.innerHTML = "";
  unitNav.appendChild(frag);
}

/* ------------------------------------------------------------------- router */

function route() {
  const hash = location.hash.replace(/^#\/?/, "");
  const [slug, anchor] = hash.split("/");

  const searchLink = document.querySelector('.topbar-link[href="#/search"]');
  if (searchLink) {
    if (slug === "search") searchLink.setAttribute("aria-current", "page");
    else searchLink.removeAttribute("aria-current");
  }

  if (slug === "search") {
    markCurrent(null);
    pager.innerHTML = "";
    document.title = "Concordance — Matthew Study";
    renderSearch(content, manifest.units);
    content.scrollIntoView({ block: "start" });
    return;
  }

  const unit = manifest.units.find((u) => u.slug === slug && u.built);
  if (!unit) {
    const first = manifest.units.find((u) => u.built);
    if (first && !slug) { location.replace(`#/${first.slug}`); return; }
    content.innerHTML = `<p class="missing">Unit not found. Pick one above.</p>`;
    markCurrent(null);
    pager.innerHTML = "";
    return;
  }
  loadUnit(unit, anchor);
}

async function loadUnit(unit, anchor) {
  markCurrent(unit.slug);
  content.innerHTML = `<p class="loading">Loading ${escapeHtml(unit.title)}…</p>`;

  let html;
  try {
    const url = bust(new URL(`../units/${unit.slug}.html`, import.meta.url));
    html = await (await fetch(url)).text();
  } catch (e) {
    content.innerHTML = `<p class="missing">Could not load <code>units/${unit.slug}.html</code>.</p>`;
    return;
  }

  content.innerHTML = html;
  renderPlacement(content, unit);
  hoistStructureBlocks(content);
  normalizeSectionHeadings(content);
  const resolved = resolveUnit(unit);
  injectPalette(unit, resolved);
  rebuildLegend(content, resolved);
  enhanceSpotlights(content);
  wireRoots(content, unit, manifest.units);
  wireFootnotes();
  buildPager(unit);
  document.title = `Unit ${unit.n} · ${unit.title} — Matthew Study`;

  if (anchor) {
    const vm = anchor.match(/^v(\d+)$/);
    const el = vm
      ? [...content.querySelectorAll(".v")].find((v) => v.querySelector(".n")?.textContent.trim() === vm[1])
      : document.getElementById(anchor);
    if (el) requestAnimationFrame(() => jumpTo(el));
    else content.scrollIntoView({ block: "start" });
  } else {
    content.scrollIntoView({ block: "start" });
  }
}

/* Move every structural block (rings/chiasms, comparison tables, itineraries)
   to the top of the unit, just under the colour key, keeping their authored
   order. The research fragments drop these wherever they fall in the prose;
   the site always shows them first, before the translation. */
function hoistStructureBlocks(root) {
  const article = root.querySelector("article.unit") || root;
  const anchor =
    article.querySelector("section.block.legend") ||
    article.querySelector("header.mast");
  if (!anchor || !anchor.parentNode) return;
  let ref = anchor;
  for (const b of article.querySelectorAll("section.block")) {
    if (b.classList.contains("legend")) continue;
    ref.after(b); // re-parents b to sit right after ref, in document order
    ref = b;
  }
}

/* One section-heading form site-wide: <h3 class="pericope">Title <span>· range</span></h3>
   (Unit 8's shape). Older fragments used div.sectionhead / div.panelhead /
   h3.panel / h3.movement / h2.secthead — normalise them all here, and wrap a
   trailing verse range in the <span> if the author didn't. Catches any future
   drift too. */
function normalizeSectionHeadings(root) {
  const article = root.querySelector("article.unit") || root;
  const LEGACY =
    "h2.secthead, h2.sectionhead, h3.panel, h3.movement, .sectionhead, .panelhead";
  for (const h of [...article.querySelectorAll(LEGACY)]) {
    if (h.matches("h3.pericope")) continue;
    const h3 = document.createElement("h3");
    h3.className = "pericope";
    h3.innerHTML = h.innerHTML;
    h.replaceWith(h3);
  }
  const SEP = "(?:\\s|&nbsp;|\\u00a0)*";
  const RANGE = "((?:\\d+:\\d+)(?:\\s*[\\u2013-]\\s*(?:\\d+:)?\\d+)?)";
  const tail = new RegExp(SEP + "[·\\u2013\\u2014-]" + SEP + RANGE + "\\s*$");
  for (const h of article.querySelectorAll("h3.pericope")) {
    if (h.querySelector("span")) continue; // already Title <span>· range</span>
    let s = h.innerHTML.replace(/^\s*(?:Panel|Movement|Part)\s+[\w']+\s*[·|]\s*/i, "");
    h.innerHTML = s.replace(tail, " <span>· $1</span>");
  }
}

function renderPlacement(root, unit) {
  const mast = root.querySelector("header.mast");
  if (!mast) return;
  const mv = manifest.movements.find((m) => m.id === unit.movement);
  const d = discourseOf(unit.n);
  let txt = mv ? `Movement ${roman(mv.id)} · ${mv.label}` : "";
  if (d) {
    const pos = d.units.length > 1
      ? ` (${d.units.indexOf(unit.n) + 1} of ${d.units.length})`
      : "";
    txt += `${txt ? " — " : ""}◆ Discourse ${roman(d.n)}: ${d.label}${pos}`;
  }
  if (!txt) return;
  const el = document.createElement("div");
  el.className = "unit-place";
  el.textContent = txt;
  mast.appendChild(el);
}

function markCurrent(slug) {
  for (const a of unitNav.querySelectorAll(".unit-chip, .bm-tick")) {
    if (a.dataset.slug === slug) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  }
  const u = manifest.units.find((x) => x.slug === slug);
  navToggleCtx.textContent = u ? `· Unit ${u.n} of ${manifest.unit_count}` : "";
}

/* --------------------------------------------------- footnote jump + return */

function wireFootnotes() {
  const origin = new Map(); // note id -> the <sup> the reader jumped from

  content.querySelectorAll("sup.en a[href*='#']").forEach((a) => {
    const id = a.getAttribute("href").split("#").pop();
    a.addEventListener("click", (e) => {
      e.preventDefault();
      const note = document.getElementById(id);
      if (!note) return;
      const sup = a.closest("sup.en");
      // click the same ref again while the note is on screen -> jump back
      if (origin.get(id) === sup && inView(note)) { back(id); return; }
      origin.set(id, sup);
      addBackLink(note, id);
      jumpTo(note);
    });
  });

  function addBackLink(note, id) {
    if (note.querySelector(".note-back")) return;
    const b = document.createElement("a");
    b.className = "note-back";
    b.href = "#";
    b.textContent = "↩ back";
    b.addEventListener("click", (e) => { e.preventDefault(); back(id); });
    note.append(" ", b);
  }

  function back(id) {
    const sup = origin.get(id);
    origin.delete(id);
    document.getElementById(id)?.querySelector(".note-back")?.remove();
    if (!sup) return;
    jumpTo(sup.closest(".v") || sup, sup);
  }
}

function jumpTo(el, flashEl) {
  const reduce = prefersReducedMotion();
  el.scrollIntoView({ block: "center", behavior: reduce ? "auto" : "smooth" });
  const target = flashEl || el;
  if (reduce) { flash(target); return; }
  // fire the highlight once the smooth scroll has settled (or after a cap)
  let last = null, still = 0, fired = false, start = performance.now();
  const done = () => { if (!fired) { fired = true; flash(target); } };
  const tick = () => {
    if (fired) return;
    const y = window.scrollY;
    still = y === last ? still + 1 : 0;
    last = y;
    if (still > 2 || performance.now() - start > 700) done();
    else requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function flash(el) {
  clearTimeout(el._flashT);
  el.classList.remove("flash");
  void el.offsetWidth; // restart the animation
  el.classList.add("flash");
  el._flashT = setTimeout(() => el.classList.remove("flash"), 2100);
}

function inView(el) {
  const r = el.getBoundingClientRect();
  return r.top < window.innerHeight * 0.9 && r.bottom > window.innerHeight * 0.1;
}

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/* -------------------------------------------------------------- prev / next */

function buildPager(unit) {
  const built = manifest.units.filter((u) => u.built);
  const i = built.findIndex((u) => u.slug === unit.slug);
  const prev = built[i - 1];
  const next = built[i + 1];
  pager.innerHTML =
    (prev ? link(prev, "prev", "← Previous") : "<span></span>") +
    (next ? link(next, "next", "Next →") : "<span></span>");

  function link(u, cls, dir) {
    return `<a class="${cls}" href="#/${u.slug}">` +
      `<span class="dir">${dir}</span>Unit ${u.n} · ${escapeHtml(u.title)}</a>`;
  }
}

/* ------------------------------------------------------------------- utils */

function roman(n) { return ["", "I", "II", "III", "IV", "V"][n] || String(n); }
function escapeHtml(s) { return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
