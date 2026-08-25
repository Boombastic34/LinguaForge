// Baza wiedzy: teoria (co to, kiedy, formuła, sygnały, przykłady, błędy) + sprawdzian opisowy PL
async function viewKnowledge() {
  clearMain();
  const main = document.querySelector("main");
  const d = await API.get("/api/knowledge");
  main.append(hero("📖", "Baza wiedzy", "Teoria jak od nauczyciela: co to, kiedy używać, wzór, przykłady — i sprawdzian z rozumienia", "indigo",
    `${d.articles.length} tematów`));
  for (const cat of d.categories) {
    const card = el("div", { class: "card" }, el("h3", {}, `${cat.emoji} ${cat.name}`));
    const grid = el("div", { class: "kb-grid stagger" });
    d.articles.filter(a => a.cat === cat.id).forEach((a, i) => {
      grid.append(el("div", { class: "topic-card", style: `animation-delay:${i * 50}ms`, onclick: () => viewKbArticle(a.id) },
        el("div", { class: "topic-lvl" }, a.level),
        el("b", {}, a.name),
        el("div", { class: "muted small" }, a.what),
        a.n_quiz ? el("div", { class: "small", style: "margin-top:6px;color:#4c5fd5" }, `📝 sprawdzian: ${a.n_quiz} pytań opisowych`) : null));
    });
    card.append(grid);
    main.append(card);
  }
}

async function viewKbArticle(aid) {
  clearMain();
  const main = document.querySelector("main");
  const a = await API.get("/api/knowledge/" + aid);
  main.append(hero("📖", a.name, a.what, "indigo", a.level));
  main.append(el("button", { class: "btn ghost", onclick: viewKnowledge }, "← Baza wiedzy"));
  const box = el("div", { class: "card" });
  main.append(box);

  const sec = (title, node) => box.append(el("div", { class: "kb-sec" }, el("h4", {}, title), node));

  const whenUl = el("ul", {});
  a.when.forEach(w => whenUl.append(el("li", {}, w)));
  sec("Kiedy używać?", whenUl);

  const form = el("div", { class: "kb-form" });
  if (a.form.plus && a.form.plus !== "—") form.append(el("div", {}, "➕ Twierdzenie: " + a.form.plus));
  if (a.form.minus && a.form.minus !== "—") form.append(el("div", {}, "➖ Przeczenie: " + a.form.minus));
  if (a.form.question && a.form.question !== "—") form.append(el("div", {}, "❓ Pytanie: " + a.form.question));
  sec("Formuła (wzór)", form);

  if (a.signals && a.signals.length) {
    const sig = el("div", { class: "kb-sig" });
    a.signals.forEach(s => sig.append(el("span", { class: "chip" }, s), " "));
    sec("Słowa-sygnały", sig);
  }

  const exs = el("div", {});
  a.examples.forEach(([en, pl]) => exs.append(el("div", { class: "kb-ex" },
    el("div", { class: "en" }, el("b", {}, en), " ",
      el("button", { class: "mini-tts", onclick: () => speak(en) }, "🔊")),
    el("div", { class: "muted" }, pl))));
  sec("Przykłady", exs);

  const mis = el("div", {});
  a.mistakes.forEach(x => mis.append(el("div", { class: "kb-mistake" }, "⚠ " + x)));
  sec("Typowe błędy Polaków", mis);

  if (a.quiz && a.quiz.length)
    box.append(el("button", { class: "btn primary", style: "margin-top:10px", onclick: () => runKbQuiz(a) },
      `📝 Sprawdź, czy rozumiesz (${a.quiz.length} pytań opisowych)`));
}

function runKbQuiz(a) {
  clearMain();
  const main = document.querySelector("main");
  main.append(hero("📝", "Sprawdzian z rozumienia: " + a.name,
    "Odpowiadasz PO POLSKU, własnymi słowami — liczy się sens, nie formułka", "gold",
    `${a.quiz.length} pytań`));
  const box = el("div", { class: "card" });
  main.append(box);
  let i = 0, total = 0, t0 = 0;

  function next() {
    if (i >= a.quiz.length) return finish();
    const q = a.quiz[i];
    t0 = Date.now();
    box.innerHTML = "";
    box.append(
      el("div", { class: "pl-top" },
        el("span", { class: "badge" }, `Pytanie ${i + 1}/${a.quiz.length}`),
        el("div", { class: "progress" }, el("div", { class: "progress-fill", style: `width:${Math.round(i / a.quiz.length * 100)}%` }))),
      el("div", { class: "qtext" }, q.q),
      el("div", { class: "muted small" }, "Napisz 1–3 zdania po polsku."));
    const ta = el("textarea", { class: "input", placeholder: "Twoja odpowiedź po polsku…" });
    const send = el("button", { class: "btn ok", onclick: check }, "Sprawdź");
    box.append(ta, send);
    ta.focus();

    async function check() {
      box.querySelectorAll("button,textarea").forEach(b => b.disabled = true);
      const r = await API.post("/api/knowledge/check", { article: a.id, q_idx: i, answer: ta.value, rt: Date.now() - t0 });
      total += r.score;
      if (r.correct && r.xp) xpPop(r.xp);
      box.innerHTML = "";
      box.append(feedbackPanel({
        correct: r.correct,
        your: ta.value,
        answer: `${Math.round(r.score * 100)}% sensu trafione`,
        pl: null,
        explain: r.msg,
        extraHtml: `<div class="fb-explain">📘 Wzorcowa odpowiedź: <b>${r.model}</b></div>`,
        onNext: () => { i++; next(); },
      }));
    }
  }

  function finish() {
    const pct = Math.round(100 * total / a.quiz.length);
    if (pct >= 60) confetti();
    box.innerHTML = "";
    box.append(el("h3", {}, pct >= 60 ? "🎉 Rozumiesz ten temat!" : "Warto wrócić do teorii"),
      el("p", {}, `Wynik: ${pct}% sensu.` + (pct < 60 ? " Przeczytaj artykuł jeszcze raz i spróbuj ponownie." : "")),
      el("div", { class: "fb-btns" },
        el("button", { class: "btn primary", onclick: () => viewKbArticle(a.id) }, "← Do artykułu"),
        el("button", { class: "btn ghost", onclick: viewKnowledge }, "Baza wiedzy")));
  }
  next();
}
