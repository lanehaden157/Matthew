/* Spotlight — collapse the per-verse asides (.gloss, .compare) into one
   click-to-open panel per verse, so the translation reads clean by default.
   Runs on the freshly-loaded fragment; the fragments themselves are untouched. */

const ASIDE_SEL = ".gloss, .compare";
const STOP_SEL = "p.v, div.v, h3, section, header, .verses, .sectionhead, .panelhead, .movement, .ring, .structure, table";

export function enhanceSpotlights(root) {
  const verses = [...root.querySelectorAll("p.v, div.v")];
  let total = 0;

  for (const verse of verses) {
    const items = [];
    let n = verse.nextElementSibling;
    while (n && !n.matches(STOP_SEL)) {
      const next = n.nextElementSibling;
      if (n.matches(ASIDE_SEL)) items.push(n);
      else if (items.length) break;      // a non-aside broke the run
      n = next;
    }
    if (!items.length) continue;
    total += items.length;

    const panel = document.createElement("aside");
    panel.className = "spotlight";
    panel.hidden = true;
    const head = document.createElement("div");
    head.className = "spot-head";
    head.textContent = "Spotlight";
    panel.append(head);
    items.forEach((el, i) => {
      if (i) panel.append(divider());
      panel.append(el);                  // move the node in, as-is
    });
    verse.after(panel);

    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "spot-toggle";
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-label", `Show note for this verse (${items.length})`);
    btn.textContent = "✦";
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      setOpen(panel, btn, panel.hidden);
    });
    verse.append(" ", btn);
    panel._btn = btn;
  }

  if (total) addAllControl(root);
  return total;
}

function setOpen(panel, btn, open) {
  panel.hidden = !open;
  btn.setAttribute("aria-expanded", String(open));
  btn.classList.toggle("is-open", open);
}

function divider() {
  const d = document.createElement("div");
  d.className = "spot-div";
  return d;
}

function addAllControl(root) {
  const anchor = root.querySelector(".verses") ||
    root.querySelector("p.v, div.v")?.parentElement;
  if (!anchor) return;
  const bar = document.createElement("div");
  bar.className = "spot-controls";
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "spot-all";
  const label = () => {
    const anyClosed = [...root.querySelectorAll(".spotlight")].some((p) => p.hidden);
    btn.textContent = anyClosed ? "✦ Show all notes" : "Hide all notes";
    btn.dataset.mode = anyClosed ? "show" : "hide";
  };
  btn.addEventListener("click", () => {
    const open = btn.dataset.mode === "show";
    root.querySelectorAll(".spotlight").forEach((p) => setOpen(p, p._btn, open));
    label();
  });
  label();
  bar.append(btn);
  anchor.before(bar);
}

/* print / PDF: open everything so nothing is lost on paper */
if (typeof window !== "undefined") {
  window.addEventListener("beforeprint", () => {
    document.querySelectorAll(".spotlight").forEach((p) => {
      p._wasHidden = p.hidden;
      p.hidden = false;
    });
  });
  window.addEventListener("afterprint", () => {
    document.querySelectorAll(".spotlight").forEach((p) => {
      if (p._wasHidden) p.hidden = true;
    });
  });
}
