/* Matthew Study — tab router + footnote interactions.
   Plain ES module, no build step. Paths are relative so it works from a GitHub
   Pages subpath. */

import { loadThreadData, resolveUnit, injectPalette, rebuildLegend } from "./threads.js?v=6";

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
  const set = (open) => {
    unitNav.hidden = !open;
    navToggle.setAttribute("aria-expanded", String(open));
  };
  navToggle.addEventListener("click", () => set(unitNav.hidden));
  unitNav.addEventListener("click", (e) => {
    if (e.target.closest(".unit-chip:not(.unbuilt)")) set(false);
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") set(false); });
}

/* ----------------------------------------------------------------- unit nav */

function buildUnitNav() {
  const byMovement = new Map();
  for (const u of manifest.units) {
    if (!byMovement.has(u.movement)) byMovement.set(u.movement, []);
    byMovement.get(u.movement).push(u);
  }
  const frag = document.createDocumentFragment();
  for (const m of manifest.movements) {
    const label = document.createElement("div");
    label.className = "movement-label";
    label.textContent = `Movement ${roman(m.id)} · ${m.label}`;
    frag.appendChild(label);

    const grid = document.createElement("div");
    grid.className = "unit-grid";
    for (const u of byMovement.get(m.id) || []) {
      const a = document.createElement("a");
      a.className = "unit-chip" + (u.built ? "" : " unbuilt");
      a.dataset.slug = u.slug;
      if (u.built) a.href = `#/${u.slug}`;
      a.innerHTML =
        `<span class="n">${u.n}</span>${escapeHtml(u.title)}` +
        `<span class="passage">${escapeHtml(u.passage)}${u.built ? "" : " · not yet built"}</span>`;
      grid.appendChild(a);
    }
    frag.appendChild(grid);
  }
  unitNav.innerHTML = "";
  unitNav.appendChild(frag);
}

/* ------------------------------------------------------------------- router */

function route() {
  const hash = location.hash.replace(/^#\/?/, "");
  const [slug, anchor] = hash.split("/");
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
  const resolved = resolveUnit(unit);
  injectPalette(unit, resolved);
  rebuildLegend(content, resolved);
  wireFootnotes();
  buildPager(unit);
  document.title = `Unit ${unit.n} · ${unit.title} — Matthew Study`;

  if (anchor) {
    const el = document.getElementById(anchor);
    if (el) requestAnimationFrame(() => jumpTo(el));
  } else {
    content.scrollIntoView({ block: "start" });
  }
}

function markCurrent(slug) {
  let cur = null;
  for (const a of unitNav.querySelectorAll(".unit-chip")) {
    if (a.dataset.slug === slug) { a.setAttribute("aria-current", "page"); cur = a; }
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
    b.textContent = "↩ back to the text";
    b.addEventListener("click", (e) => { e.preventDefault(); back(id); });
    note.append(" ", b);
  }

  function back(id) {
    const sup = origin.get(id);
    if (!sup) return;
    jumpTo(sup.closest(".v") || sup, sup);
    origin.delete(id);
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

let _flashed = null;
function flash(el) {
  if (_flashed === el) return;
  _flashed = el;
  el.classList.remove("flash");
  void el.offsetWidth;
  el.classList.add("flash");
  el.addEventListener("animationend", () => {
    el.classList.remove("flash");
    if (_flashed === el) _flashed = null;
  }, { once: true });
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
