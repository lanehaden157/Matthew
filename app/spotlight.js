/* Per-verse asides, collapsed by default. Three kinds:
     .gloss              -> a light "note" (bare * marker, plain italic aside, no box)
     .compare            -> a "spotlight" (✦ chip, tinted panel with a header)
     aside.synoptic       -> a synoptic parallel: author-authored, already a
                             complete <aside class="synoptic"><h4>…</h4>…</aside>
                             (its own header text, one per parallel — not merged
                             under a shared header the way .compare is). This
                             script only hides it and adds its toggle chip.
   Runs on the freshly-loaded fragment; the fragments themselves are untouched. */

const STOP_SEL =
  "p.v, div.v, h3, section, header, .verses, .sectionhead, .panelhead, .movement, .ring, .structure, table";

export function enhanceSpotlights(root) {
  let count = 0;

  for (const verse of root.querySelectorAll("p.v, div.v")) {
    const glosses = [];
    const compares = [];
    const synoptics = [];
    let n = verse.nextElementSibling;
    while (n && !n.matches(STOP_SEL)) {
      const next = n.nextElementSibling;
      if (n.matches(".gloss")) glosses.push(n);
      else if (n.matches(".compare")) compares.push(n);
      else if (n.matches("aside.synoptic")) synoptics.push(n);
      else if (glosses.length || compares.length || synoptics.length) break;
      n = next;
    }
    if (!glosses.length && !compares.length && !synoptics.length) continue;

    // insertion point after the verse; keep spotlight below note if both exist
    let after = verse;
    if (glosses.length) after = mount(verse, after, "note", glosses);
    if (compares.length) mount(verse, after, "spot", compares);
    synoptics.forEach((box) => mountReady(verse, box));
    count += glosses.length + compares.length + synoptics.length;
  }

  if (count) addAllControl(root);
  return count;
}

const KIND = {
  note: { cls: "verse-note", tag: "div", head: null,
          btnCls: "note-toggle", sym: "*", aria: "notes" },
  spot: { cls: "spotlight", tag: "aside", head: "✦ Rendering",
          btnCls: "spot-toggle", sym: "✦", aria: "spotlight" },
};

function mount(verse, insertAfter, kind, items) {
  const K = KIND[kind];
  const box = document.createElement(K.tag);
  box.className = K.cls;
  box.hidden = true;
  if (K.head) {
    const h = document.createElement("div");
    h.className = "spot-head";
    h.textContent = K.head;
    box.append(h);
  }
  items.forEach((el, i) => {
    if (i && kind === "spot") box.append(divider());
    box.append(el);
  });
  insertAfter.after(box);

  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = K.btnCls;
  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-label",
    `Show ${K.aria} for this verse${items.length > 1 ? ` (${items.length})` : ""}`);
  btn.textContent = K.sym;
  btn.addEventListener("click", (e) => { e.stopPropagation(); setOpen(box, btn, box.hidden); });
  verse.append(" ", btn);
  box._btn = btn;
  return box;
}

function mountReady(verse, box) {
  box.hidden = true;
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "spot-toggle syn-toggle";
  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-label", "Show synoptic parallel for this verse");
  btn.textContent = "✦";
  btn.addEventListener("click", (e) => { e.stopPropagation(); setOpen(box, btn, box.hidden); });
  verse.append(" ", btn);
  box._btn = btn;
  return box;
}

function setOpen(box, btn, open) {
  box.hidden = !open;
  btn.setAttribute("aria-expanded", String(open));
  btn.classList.toggle("is-open", open);
}

function divider() {
  const d = document.createElement("div");
  d.className = "spot-div";
  return d;
}

function boxes(root) {
  return [...root.querySelectorAll(".verse-note, .spotlight, .synoptic")];
}

function addAllControl(root) {
  const article = root.querySelector("article.unit") || root;
  const firstVerse = article.querySelector("p.v, div.v");
  if (!firstVerse) return;

  // the article-level element that is or contains the first verse
  let anchor = firstVerse;
  while (anchor.parentElement && anchor.parentElement !== article) {
    anchor = anchor.parentElement;
  }
  // if a section heading sits right above it, put the bar above that instead,
  // so the control always lands just under the structural blocks
  const prev = anchor.previousElementSibling;
  if (prev && prev.matches("h2.secthead, h3.pericope, h3.panel, h3.movement, .sectionhead")) {
    anchor = prev;
  }

  const bar = document.createElement("div");
  bar.className = "spot-controls";
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "spot-all";
  const relabel = () => {
    const anyClosed = boxes(root).some((b) => b.hidden);
    btn.textContent = anyClosed ? "✦ Show all notes" : "Hide all notes";
    btn.dataset.mode = anyClosed ? "show" : "hide";
  };
  btn.addEventListener("click", () => {
    const open = btn.dataset.mode === "show";
    boxes(root).forEach((b) => setOpen(b, b._btn, open));
    relabel();
  });
  relabel();
  bar.append(btn);
  anchor.before(bar);
}

/* print / PDF: open everything so nothing is lost on paper */
if (typeof window !== "undefined") {
  window.addEventListener("beforeprint", () => {
    document.querySelectorAll(".verse-note, .spotlight, .synoptic").forEach((b) => {
      b._wasHidden = b.hidden;
      b.hidden = false;
    });
  });
  window.addEventListener("afterprint", () => {
    document.querySelectorAll(".verse-note, .spotlight, .synoptic").forEach((b) => {
      if (b._wasHidden) b.hidden = true;
    });
  });
}
