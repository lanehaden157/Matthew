/* Matthew Study — tab router + footnote interactions.
   Plain ES module, no build step. Paths are relative so it works from a GitHub
   Pages subpath. */

const UNITS_URL = new URL("../data/units.json", import.meta.url);

const content = document.getElementById("content");
const unitNav = document.getElementById("unit-nav");
const pager = document.getElementById("unit-pager");
const navToggle = document.getElementById("nav-toggle");
const navToggleCtx = document.getElementById("nav-toggle-ctx");

let manifest = null;

init();

async function init() {
  try {
    manifest = await (await fetch(UNITS_URL)).json();
  } catch (e) {
    content.innerHTML = `<p class="missing">Could not load <code>data/units.json</code>.</p>`;
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
    const url = new URL(`../units/${unit.slug}.html`, import.meta.url);
    html = await (await fetch(url)).text();
  } catch (e) {
    content.innerHTML = `<p class="missing">Could not load <code>units/${unit.slug}.html</code>.</p>`;
    return;
  }

  content.innerHTML = html;
  injectPalette(unit);
  wireFootnotes();
  buildPager(unit);
  document.title = `Unit ${unit.n} · ${unit.title} — Matthew Study`;

  if (anchor) {
    const el = document.getElementById(anchor);
    if (el) { el.scrollIntoView(); flash(el); }
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

/* --------------------------------------------------------- per-unit palette */

function injectPalette(unit) {
  document.getElementById("unit-palette")?.remove();
  if (!unit.roots) return;
  const rules = Object.entries(unit.roots)
    .map(([root, hex]) =>
      `.unit[data-unit="${unit.n}"] [data-root="${cssEsc(root)}"]{color:${hex}}` +
      `\n.unit[data-unit="${unit.n}"] .swatch[style*="--c-${cssEsc(root)}"]{background:${hex}!important}`)
    .join("\n");
  const style = document.createElement("style");
  style.id = "unit-palette";
  style.textContent = rules;
  document.head.appendChild(style);
}

/* --------------------------------------------------- footnote jump + return */

function wireFootnotes() {
  let origin = null; // the <sup> a reader jumped from

  content.querySelectorAll("sup.en a[href^='#']").forEach((a) => {
    const id = a.getAttribute("href").slice(1);
    a.addEventListener("click", (e) => {
      e.preventDefault();
      const note = document.getElementById(id);
      if (!note) return;
      const sup = a.closest("sup.en");

      // second click on the same ref, while the note is roughly in view -> go back
      if (origin === sup && inView(note)) { returnToOrigin(); return; }

      origin = sup;
      ensureBackLink(note);
      note.scrollIntoView({ block: "center" });
      flash(note);
    });
  });

  function ensureBackLink(note) {
    let back = note.querySelector(".note-back");
    if (!back) {
      back = document.createElement("a");
      back.className = "note-back";
      back.href = "#";
      back.textContent = "↩ back";
      note.appendChild(document.createTextNode(" "));
      note.appendChild(back);
    }
    back.onclick = (e) => { e.preventDefault(); returnToOrigin(); };
  }

  function returnToOrigin() {
    if (!origin) return;
    origin.scrollIntoView({ block: "center" });
    const verse = origin.closest(".v") || origin;
    flash(verse);
    origin = null;
  }
}

function inView(el) {
  const r = el.getBoundingClientRect();
  return r.top < window.innerHeight * 0.9 && r.bottom > window.innerHeight * 0.1;
}

function flash(el) {
  el.classList.remove("flash");
  void el.offsetWidth; // restart the animation
  el.classList.add("flash");
  el.addEventListener("animationend", () => el.classList.remove("flash"), { once: true });
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
function cssEsc(s) { return s.replace(/[^a-zA-Z0-9_-]/g, "\\$&"); }
