// Gramatyka: tematy + trening mieszany
async function viewGrammar() {
  clearMain();
  const main = document.querySelector("main");
  const { topics } = await API.get("/api/grammar/topics");
  const totalEx = topics.reduce((s, t) => s + t.n_ex, 0);
  main.append(hero("📐", "Gramatyka", "Pojedyncze tematy albo trening mieszany — jak w prawdziwym języku", "indigo",
    `${topics.length} tematów · ${totalEx} ćwiczeń`));

  // trening mieszany
  const mix = el("div", { class: "card" });
  mix.append(el("h3", {}, "🔀 Trening mieszany"),
    el("p", { class: "muted" }, "Zaznacz tematy — ćwiczenia zostaną wymieszane. To najskuteczniejsza forma nauki (interleaving): musisz sam rozpoznać, która reguła pasuje."));
  const checks = el("div", { class: "mix-checks" });
  const chosen = new Set();
  topics.forEach(t => {
    const lab = el("label", { class: "chip chip-check" },
      el("input", { type: "checkbox", onchange: e => { e.target.checked ? chosen.add(t.id) : chosen.delete(t.id); } }),
      ` ${t.name} (${t.n_ex})`);
    checks.append(lab);
  });
  mix.append(checks,
    el("button", { class: "btn primary", onclick: () => startMixed([...chosen]) }, "▶ Start (10 pytań)"),
    " ",
    el("button", { class: "btn ghost", onclick: () => startMixed([]) }, "🎲 Wszystkie tematy"));
  main.append(mix);

  const grid = el("div", { class: "topic-grid stagger" });
  topics.forEach((t, i) => {
    const m = t.mastery;
    grid.append(el("div", { class: "topic-card", style: `animation-delay:${i * 50}ms`, onclick: () => viewTopic(t.id) },
      el("div", { class: "topic-lvl" }, t.level),
      el("b", {}, t.name),
      el("div", { class: "muted small" }, `${t.n_ex} ćwiczeń`),
      el("div", { class: "mastery-bar" },
        el("div", { class: "mastery-fill", style: `width:${m ?? 0}%` })),
      el("div", { class: "muted small" }, m != null ? `opanowanie ${Math.round(m)}%` : "jeszcze nie ćwiczone")));
  });
  main.append(el("div", { class: "card" }, el("h3", {}, "📚 Tematy"), grid));
}

async function viewTopic(tid) {
  clearMain();
  const main = document.querySelector("main");
  const t = await API.get("/api/grammar/topic/" + tid);
  main.append(hero("📐", t.name, "Najpierw teoria, potem praktyka", "indigo", `${t.total_ex} ćwiczeń w temacie`));
  const box = el("div", { class: "card" });
  main.append(box);
  box.append(el("div", { class: "theory", html: t.theory }));
  box.append(sizePicker({
    title: "Ile ćwiczeń z tego tematu?", pool: t.total_ex, unit: "ćwiczeń", suggested: 8,
    onStart: n => {
      const all = t.exercises.map(e => ({ ...e, topic: tid }));
      runExercises(box, n === "all" ? all : all.slice(0, n), () => viewGrammar());
    },
  }));
}

async function startMixed(topicIds) {
  const main = document.querySelector("main");
  clearMain();
  main.append(hero("🔀", "Trening mieszany", "Czasy i tematy wymieszane — rozpoznaj, co pasuje", "indigo"));
  const box = el("div", { class: "card" });
  main.append(box);
  const probe = await API.post("/api/grammar/mixed", { topics: topicIds, n: 1 });
  box.append(sizePicker({
    title: "Ile pytań w treningu mieszanym?", pool: probe.pool_size, unit: "ćwiczeń", suggested: 10,
    onStart: async n => {
      const { exercises } = await API.post("/api/grammar/mixed",
        { topics: topicIds, n: n === "all" ? probe.pool_size : n });
      box.innerHTML = "";
      runExercises(box, exercises, () => viewGrammar(), true);
    },
  }));
}

function runExercises(box, list, onDone, showTopic = false) {
  let i = 0, good = 0, t0 = 0;
  enterFocus({ title: "📐 Gramatyka", subtitle: `${list.length} ćwiczeń`, theme: "indigo",
    onExit: () => { exitFocus(); onDone(); } });
  next();
  function next() {
    if (i >= list.length) return finish();
    const ex = list[i];
    t0 = Date.now();
    box.innerHTML = "";
    focusProgress(i, list.length, `poprawnych: ${good}`);
    box.append(el("div", { class: "pl-top" },
      showTopic && ex.topic_name ? el("span", { class: "badge" }, ex.topic_name) : null,
      el("span", { class: "muted", style: "margin-left:auto" }, `${i + 1}/${list.length}`)),
      el("div", { class: "qtext" }, ex.text));
    if (ex.type === "choice") {
      const opts = el("div", { class: "options stagger" });
      ex.options.forEach((o, j) => opts.append(
        el("button", { class: "option", style: `animation-delay:${j * 60}ms`, onclick: () => submit(ex, j) }, o)));
      box.append(opts, el("button", { class: "btn ghost", onclick: () => submit(ex, -1) }, "🤷 Nie wiem"));
    } else {
      if (ex.type === "order" && ex.words) box.append(el("div", { class: "wordbank" },
        ...ex.words.map(w => el("span", { class: "chip" }, w))));
      const inp = el("input", { class: "input", autocomplete: "off", placeholder: "Twoja odpowiedź…" });
      const send = el("button", { class: "btn ok" }, "Sprawdź");
      send.onclick = () => submit(ex, inp.value.trim());
      inp.onkeydown = e => { if (e.key === "Enter") send.click(); };
      box.append(inp, el("div", { class: "fb-btns" }, send,
        el("button", { class: "btn ghost", onclick: () => submit(ex, "") }, "🤷 Nie wiem")));
      inp.focus();
    }
  }
  async function submit(ex, val) {
    box.querySelectorAll("button,input").forEach(b => b.disabled = true);
    const r = await API.post("/api/grammar/answer", { topic: ex.topic, ex: ex.id, answer: val, rt: Date.now() - t0 });
    if (r.correct) { good++; if (r.xp) xpPop(r.xp); }
    box.innerHTML = "";
    box.append(feedbackPanel({
      correct: r.correct, your: r.your, answer: r.answer, pl: r.pl, en: r.en, explain: r.explain,
      rule: r.rule, ruleTitle: r.topic_name,
      askKnown: r.correct && ex.type === "choice",
      onNext: (guessed) => {
        if (guessed) API.post("/api/grammar/guessed", { topic: ex.topic });
        i++; next();
      },
    }));
  }
  function finish() {
    exitFocus();
    box.innerHTML = "";
    if (good / list.length >= 0.8) confetti();
    box.append(el("h3", {}, "Koniec serii"),
      el("p", {}, `Wynik: ${good}/${list.length}`),
      el("button", { class: "btn primary", onclick: onDone }, "← Powrót"));
  }
}
