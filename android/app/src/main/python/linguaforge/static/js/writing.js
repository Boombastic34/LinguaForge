// Pisanie — dłuższe wypowiedzi z oceną w trzech osiach
async function viewWriting() {
  clearMain();
  const main = document.querySelector("main");
  const { tasks } = await API.get("/api/writing");
  main.append(hero("✍️", "Pisanie", "Napisz kilka zdań — ocenię kompletność, długość i poprawność", "teal",
    `${tasks.length} zadań`));
  const card = el("div", { class: "card" });
  const list = el("div", { class: "chapter-list stagger" });
  tasks.forEach((t, i) => list.append(el("div", {
    class: "chapter" + (t.best != null ? " ch-done" : ""), style: `animation-delay:${i * 60}ms`,
    onclick: () => runWriting(t.id),
  },
    el("div", { class: "ch-status" }, t.emoji),
    el("div", { class: "ch-body" },
      el("b", {}, t.title),
      el("div", { class: "muted small" }, t.brief),
      el("div", { class: "small counters" },
        `poziom ${t.level} · min. ${t.min_words} słów · ${t.elements.length} wymaganych elementów` +
        (t.best != null ? ` · najlepszy wynik ${Math.round(t.best * 100)}%` : ""))))));
  card.append(list);
  main.append(card);
}

async function runWriting(wid) {
  clearMain();
  const main = document.querySelector("main");
  const t = await API.get("/api/writing/" + wid);
  main.append(hero(t.emoji || "✍️", t.title, t.brief, "teal", `poziom ${t.level}`));
  const box = el("div", { class: "card" });
  main.append(box);
  enterFocus({ title: "✍️ " + t.title, subtitle: "praca pisemna", theme: "teal",
    onExit: () => viewWriting() });

  const checklist = el("div", { class: "check-list" });
  (t.must_pl || []).forEach(x => checklist.append(el("div", { class: "check-item" }, "○ " + x)));
  const counter = el("span", { class: "wc-counter" }, "0 słów");
  const ta = el("textarea", { class: "input write-area", placeholder: "Pisz po angielsku…" });
  ta.oninput = () => {
    const n = (ta.value.match(/[A-Za-z']+/g) || []).length;
    counter.textContent = `${n} słów`;
    counter.className = "wc-counter " + (n >= t.min_words ? "wc-ok" : (n >= t.min_words * 0.6 ? "wc-mid" : ""));
  };

  box.append(
    el("div", { class: "write-brief" },
      el("b", {}, "Co ma się znaleźć w tekście:"), checklist,
      t.tense_hint ? el("div", { class: "fb-rule" }, el("b", {}, "📏 Podpowiedź: "), t.tense_hint) : null),
    el("div", { class: "pl-top" }, el("span", { class: "muted small" }, `minimum ${t.min_words} słów`), counter),
    ta,
    el("div", { class: "fb-btns" },
      el("button", { class: "btn primary big", onclick: check }, "📤 Sprawdź moją pracę"),
      el("button", { class: "btn ghost", onclick: viewWriting }, "← Lista zadań")));
  ta.focus();

  async function check() {
    if ((ta.value.match(/[A-Za-z']+/g) || []).length < 8)
      return toast("Napisz przynajmniej kilka zdań", true);
    const r = await API.post("/api/writing/check", { id: wid, text: ta.value });
    exitFocus();
    if (r.xp && r.state === "good") xpPop(r.xp);
    if (r.state === "good") confetti();
    clearMain();
    const m2 = document.querySelector("main");
    m2.append(hero(t.emoji || "✍️", "Ocena: " + t.title,
      r.label, r.state === "good" ? "teal" : (r.state === "partial" ? "gold" : "ember"),
      `${Math.round(r.score * 100)}%`));
    const res = el("div", { class: "card" });

    res.append(el("div", { class: "axis-row" },
      axis("📋 Kompletność", r.completeness, "czy zawarłeś wymagane elementy"),
      axis("📏 Długość", r.length_ratio, `${r.words} słów, ${r.sentences} zdań`),
      axis("✅ Poprawność", r.correctness, "błędy językowe i styl")));

    if (r.hit.length) {
      res.append(el("h4", {}, "Masz w tekście:"));
      r.hit.forEach(x => res.append(el("div", { class: "check-item done" }, "✔ " + x)));
    }
    if (r.missed.length) {
      res.append(el("h4", {}, "Brakuje:"));
      r.missed.forEach(x => res.append(el("div", { class: "check-item miss" }, "✘ " + x)));
    }
    if (r.issues.length) {
      res.append(el("h4", {}, "Uwagi językowe:"));
      r.issues.forEach(x => res.append(el("div", { class: "kb-mistake" }, "⚠ " + x)));
    }
    res.append(el("h4", {}, "Twój tekst:"),
      el("div", { class: "write-your" }, ta.value),
      el("details", { class: "path-sec" },
        el("summary", {}, "📘 Zobacz przykładową wypowiedź wzorcową"),
        el("div", { class: "kb-ex" },
          el("div", { class: "en" }, r.model, " ",
            el("button", { class: "mini-tts", onclick: () => speak(r.model) }, "🔊")))),
      el("div", { class: "fb-btns", style: "margin-top:12px" },
        el("button", { class: "btn primary", onclick: () => runWriting(wid) }, "🔁 Popraw i wyślij ponownie"),
        el("button", { class: "btn ghost", onclick: viewWriting }, "← Lista zadań")));
    m2.append(res);
  }

  function axis(name, val, sub) {
    const pct = Math.round(val * 100);
    const cls = pct >= 75 ? "gap-ok" : (pct >= 45 ? "gap-mid" : "gap-bad");
    return el("div", { class: "axis-cell " + cls },
      el("div", { class: "axis-val" }, pct + "%"),
      el("div", { class: "axis-name" }, name),
      el("div", { class: "axis-sub" }, sub));
  }
}
