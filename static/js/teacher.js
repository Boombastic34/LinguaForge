// Panel nauczyciela: uczniowie → profil / prace (arkusze) / kreator programów 2.0
async function viewTeacher() {
  clearMain();
  const main = document.querySelector("main");
  const { students } = await API.get("/api/teacher/students");
  main.append(hero("🧑‍🏫", "Panel nauczyciela", "Profil ucznia, arkusze prac i kreator programów", "gold",
    `${students.length} uczniów`));
  const card = el("div", { class: "card" });
  if (!students.length) card.append(el("p", { class: "muted" }, "Brak uczniów. Załóż konto ucznia na ekranie logowania."));
  const tbl = el("table", { class: "table" },
    el("tr", {}, el("th", {}, "Uczeń"), el("th", {}, "Poziom"), el("th", {}, "Cel"),
      el("th", {}, "XP"), el("th", {}, "Seria"), el("th", {}, "Ostatnio"), el("th", {}, "")));
  students.forEach(s => tbl.append(el("tr", {},
    el("td", {}, el("b", {}, s.username)),
    el("td", {}, s.level || (s.placement_done ? "?" : "przed testem")),
    el("td", {}, s.target || "—"), el("td", {}, String(s.xp)), el("td", {}, s.streak + " dni"),
    el("td", {}, s.last_active || "—"),
    el("td", {},
      el("button", { class: "btn mini", onclick: () => viewStudentDetail(s.username) }, "👁 Profil"), " ",
      el("button", { class: "btn mini", onclick: () => viewWorksheets(s.username) }, "📄 Prace"), " ",
      el("button", { class: "btn mini", onclick: () => viewStudentWritings(s.username) }, "✍️ Wypracowania"), " ",
      el("button", { class: "btn mini ok", onclick: () => viewProgramBuilder(s.username) }, "🛠 Program")))));
  card.append(tbl);
  main.append(card);
  main.append(el("div", { class: "card" },
    el("h3", {}, "🗂 Baza treści"),
    el("p", { class: "muted" }, "Dodaj słówka, zdania i dyktanda GLOBALNIE — zapisują się do plików w folderze data/ i są od razu widoczne dla wszystkich uczniów."),
    el("button", { class: "btn primary", onclick: viewContentEditor }, "✏️ Otwórz edytor treści")));
}

// ---------- Edytor treści (zapis do plików danych) ----------
async function viewContentEditor() {
  clearMain();
  const main = document.querySelector("main");
  main.append(hero("🗂", "Baza treści", "Nowe pozycje trafiają do plików w data/ z automatycznym numerem [nr]", "gold"));
  main.append(el("button", { class: "btn ghost", onclick: viewTeacher }, "← Panel nauczyciela"));
  const box = el("div", { class: "card" });
  main.append(box);

  const kindSel = el("select", {},
    el("option", { value: "word" }, "Słówko (fiszka)"),
    el("option", { value: "sentence" }, "Zdanie do tłumaczenia PL→EN"),
    el("option", { value: "dictation" }, "Dyktando (słuchanie)"));
  const form = el("div", {});
  box.append(el("div", { class: "set-row" }, "Typ treści: ", kindSel), form);
  const log = el("div", { class: "card" }, el("h4", {}, "Dodane w tej sesji"));
  const logList = el("div", {});
  log.append(logList);
  main.append(log);
  kindSel.onchange = renderForm;

  const THEMES = [["zwierzeta","Zwierzęta"],["jedzenie","Jedzenie"],["dom","Dom"],["transport","Transport"],
    ["cialo","Ciało i zdrowie"],["rodzina","Rodzina"],["ubrania","Ubrania"],["miasto","Miasto"],
    ["natura","Natura"],["uczucia","Uczucia"],["liczebniki","Liczebniki"],["kalendarz","Kalendarz"],
    ["kolory","Kolory"],["czasowniki","Czasowniki"],["praca","Praca / magazyn"],["inne","Inne"]];

  function lvlSel() {
    const s = el("select", {});
    ["A1","A2","B1","B2","C1"].forEach(L => s.append(el("option", { value: L }, L)));
    return s;
  }

  async function send(kind, payload, label) {
    try {
      const r = await API.post("/api/teacher/content", { kind, ...payload });
      toast(`Zapisano do ${r.file} jako [${r.nr}] ✔`);
      logList.append(el("div", { class: "bank-row" },
        el("span", { class: "badge nr-badge" }, "[" + r.nr + "]"),
        el("span", { class: "task-label" }, label),
        el("span", { class: "muted small" }, r.file)));
    } catch (e) { toast("Błąd zapisu", true); }
  }

  function renderForm() {
    form.innerHTML = "";
    const k = kindSel.value;
    if (k === "word") {
      const en = el("input", { class: "input", placeholder: "Słowo po angielsku, np. hammer" });
      const pl = el("input", { class: "input", placeholder: "Znaczenie po polsku, np. młotek" });
      const ex = el("input", { class: "input", placeholder: "Przykładowe zdanie (opcjonalnie)" });
      const th = el("select", {});
      THEMES.forEach(([v, n]) => th.append(el("option", { value: v }, n)));
      const lv = lvlSel();
      form.append(en, pl, ex,
        el("div", { class: "set-row" }, "Kategoria: ", th, " Poziom: ", lv),
        el("p", { class: "muted small" }, "Kategoria jest ważna — to na jej podstawie aplikacja wykrywa braki ucznia."),
        el("button", { class: "btn ok", onclick: () => {
          if (!en.value.trim() || !pl.value.trim()) return toast("Uzupełnij EN i PL", true);
          send("word", { en: en.value, pl: pl.value, example: ex.value, theme: th.value, level: lv.value },
               `${en.value} — ${pl.value}`);
          en.value = pl.value = ex.value = "";
          en.focus();
        } }, "💾 Zapisz do bazy"));
    } else if (k === "sentence") {
      const pl = el("input", { class: "input", placeholder: "Zdanie po polsku" });
      const en = el("input", { class: "input", placeholder: "Wzorcowe tłumaczenie EN" });
      const kw = el("input", { class: "input", placeholder: "Słowa kluczowe (przecinki; warianty przez |) — puste = automat" });
      const tn = el("input", { class: "input short", placeholder: "Nazwa czasu" });
      const lv = lvlSel();
      form.append(pl, en, kw, el("div", { class: "set-row" }, "Czas: ", tn, " Poziom: ", lv),
        el("button", { class: "btn ok", onclick: () => {
          if (!pl.value.trim() || !en.value.trim()) return toast("Uzupełnij PL i EN", true);
          send("sentence", { pl: pl.value, en: en.value, keywords: kw.value, tense_name: tn.value, level: lv.value },
               `${pl.value} → ${en.value}`);
          pl.value = en.value = kw.value = "";
          pl.focus();
        } }, "💾 Zapisz do bazy"));
    } else {
      const en = el("input", { class: "input", placeholder: "Zdanie EN (uczeń usłyszy głosem)" });
      const pl = el("input", { class: "input", placeholder: "Tłumaczenie PL" });
      const lv = lvlSel();
      form.append(en, pl, el("div", { class: "set-row" }, "Poziom: ", lv,
        el("button", { class: "btn mini", onclick: () => en.value && speak(en.value) }, "🔊 Posłuchaj")),
        el("button", { class: "btn ok", onclick: () => {
          if (!en.value.trim()) return toast("Wpisz zdanie EN", true);
          send("dictation", { en: en.value, pl: pl.value, level: lv.value }, en.value);
          en.value = pl.value = "";
          en.focus();
        } }, "💾 Zapisz do bazy"));
    }
  }
  renderForm();
}

async function viewStudentDetail(username) {
  clearMain();
  const main = document.querySelector("main");
  const d = await API.get("/api/teacher/student/" + username);
  main.append(hero("👁", "Uczeń: " + username,
    `Poziom ${d.profile.level || "?"} · ${d.profile.xp} XP · fiszki: ${d.cards_total} (utrwalone ${d.mature})`, "gold"));
  main.append(el("button", { class: "btn ghost", onclick: viewTeacher }, "← Lista uczniów"));

  const row = el("div", { class: "grid2" });
  const skc = el("div", { class: "card" }, el("h3", {}, "Umiejętności"));
  const names = { vocab: "Słownictwo", grammar: "Gramatyka", reading: "Czytanie", listening: "Słuchanie", writing: "Pisanie" };
  for (const [k, label] of Object.entries(names)) skc.append(skillBar(label, d.skills[k], d.cefr[k]));
  const gt = d.skills.grammar_topics || {};
  if (Object.keys(gt).length) {
    skc.append(el("h4", {}, "Tematy gramatyczne"));
    for (const [t, v] of Object.entries(gt)) skc.append(skillBar(t, v, Math.round(v) + "%"));
  }
  row.append(skc);

  const right = el("div", { class: "card" }, el("h3", {}, "Lekcje i sprawdziany"));
  if (d.lessons) right.append(el("p", {}, `Rozdziały zaliczone: ${d.lessons.chapters_done}/${d.lessons.chapters_total}`));
  const ex = d.exams || {};
  if (Object.keys(ex).length)
    for (const [uid, e] of Object.entries(ex))
      right.append(el("p", {}, `Sprawdzian ${uid}: ${e.pct}% — ocena ${e.grade} (${e.grade_name}), ${e.date}`));
  else right.append(el("p", { class: "muted" }, "Jeszcze bez sprawdzianu."));
  right.append(el("h3", {}, "Błędy wg typu"));
  const errs = Object.entries(d.errors).sort((a, b) => b[1].count - a[1].count).slice(0, 8);
  if (!errs.length) right.append(el("p", { class: "muted" }, "Brak zebranych błędów."));
  errs.forEach(([type, e]) => right.append(el("div", { class: "err-row" },
    el("b", {}, type), ` ×${e.count} `, el("span", { class: "muted small" },
      (e.examples.slice(-2).map(x => x.ctx).join(" | ") || "")))));
  if (d.leeches.length) {
    right.append(el("h3", {}, "Uparte słówka"));
    d.leeches.forEach(l => right.append(el("div", {}, `${l.en} — ${l.pl} (${l.lapses} wpadek)`)));
  }
  row.append(right);
  main.append(row);
  main.append(el("div", { class: "card" },
    el("button", { class: "btn ghost", onclick: () => API.download(`/api/teacher/export/${username}?fmt=csv`) }, "⬇ Eksport CSV"),
    " ",
    el("button", { class: "btn ghost", onclick: () => API.download(`/api/teacher/export/${username}?fmt=json`) }, "⬇ Eksport JSON")));
}

// ---------- Prace ucznia (arkusze jak sprawdzian) ----------
async function viewWorksheets(username) {
  clearMain();
  const main = document.querySelector("main");
  const { days } = await API.get("/api/teacher/worksheets/" + username);
  main.append(hero("📄", "Prace: " + username, "Każdy dzień to arkusz — pytania, odpowiedzi ucznia i poprawne", "gold",
    `${days.length} dni pracy`));
  main.append(el("button", { class: "btn ghost", onclick: viewTeacher }, "← Lista uczniów"));
  const card = el("div", { class: "card" });
  if (!days.length) card.append(el("p", { class: "muted" }, "Ten uczeń jeszcze nie rozwiązywał zadań."));
  const TYPE_PL = { card_review: "fiszki", grammar_answer: "gramatyka", translate: "tłumaczenia",
    dictation: "słuchanie", placement_answer: "test poziomujący", program_answer: "program",
    verb_review: "czasowniki", lesson_answer: "lekcje", lesson_exam: "sprawdzian" };
  days.forEach(day => {
    const pct = day.total ? Math.round(100 * day.correct / day.total) : 0;
    card.append(el("div", { class: "chapter", onclick: () => viewWorksheet(username, day.day) },
      el("div", { class: "ch-status" }, day.placement ? "🧭" : (day.exam ? "🎓" : "📄")),
      el("div", { class: "ch-body" },
        el("b", {}, day.day + (day.placement ? " · zawiera test poziomujący" : "") + (day.exam ? " · SPRAWDZIAN" : "")),
        el("div", { class: "muted small" },
          `${day.total} odpowiedzi · ${pct}% dobrych · ` +
          Object.entries(day.types).map(([t, n]) => `${TYPE_PL[t] || t}: ${n}`).join(", ")))));
  });
  main.append(card);

  async function viewWorksheet(user, day) {
    clearMain();
    main.append(hero("📄", `Arkusz ${user} — ${day}`, "Jak sprawdzian na biurku nauczyciela", "gold"));
    main.append(el("button", { class: "btn ghost", onclick: () => viewWorksheets(user) }, "← Lista prac"));
    const { rows } = await API.get(`/api/teacher/worksheet/${user}/${day}`);
    const c = el("div", { class: "card" });
    let onlyBad = false;
    const filterBtn = el("button", { class: "btn mini", onclick: () => { onlyBad = !onlyBad; renderRows(); filterBtn.textContent = onlyBad ? "Pokaż wszystko" : "Tylko błędy"; } }, "Tylko błędy");
    c.append(el("div", { style: "margin-bottom:8px" }, `${rows.length} odpowiedzi · `, filterBtn));
    const tbl = el("table", { class: "table worksheet" });
    c.append(tbl);
    function renderRows() {
      tbl.innerHTML = "";
      tbl.append(el("tr", {}, el("th", {}, "Godz."), el("th", {}, "Moduł"), el("th", {}, "Pytanie"),
        el("th", {}, "Odpowiedź ucznia"), el("th", {}, "Poprawna"), el("th", {}, "")));
      rows.filter(r => !onlyBad || r.correct === false).forEach(r => tbl.append(
        el("tr", { class: r.correct === false ? "row-bad" : "row-ok" },
          el("td", {}, (r.time || "").slice(0, 5)), el("td", {}, TYPE_PL[r.type] || r.type),
          el("td", {}, r.question || "—"), el("td", {}, String(r.your ?? "—")),
          el("td", {}, r.good || "—"),
          el("td", {}, (r.correct === false ? "✘" : "✔") + (r.extra ? " · " + r.extra : "")))));
    }
    renderRows();
    main.append(c);
  }
}

// ---------- Kreator programów 2.0 (dwupanelowy) ----------
async function viewProgramBuilder(username) {
  clearMain();
  const main = document.querySelector("main");
  main.append(hero("🛠", "Kreator programu dla: " + username,
    "Lewa strona: bank gotowych zadań i formularze. Prawa: budowany program.", "gold"));
  main.append(el("button", { class: "btn ghost", onclick: viewTeacher }, "← Lista uczniów"));

  const tasks = [];
  const wrap = el("div", { class: "builder" });
  const left = el("div", { class: "card builder-left" });
  const right = el("div", { class: "card builder-right" });
  wrap.append(left, right);
  main.append(wrap);

  // ------ PRAWA: program
  const title = el("input", { class: "input", placeholder: "Tytuł programu, np. Powtórka Present Perfect" });
  const note = el("input", { class: "input", placeholder: "Notatka dla ucznia (opcjonalnie)" });
  const deadline = el("input", { class: "input short", type: "date" });
  const list = el("div", { class: "task-list" });
  right.append(el("h3", {}, "📋 Program (0 zadań)"), title, note,
    el("div", { class: "set-row" }, "Termin: ", deadline), list,
    el("button", { class: "btn primary", style: "margin-top:8px", onclick: publish }, "📤 Przypisz uczniowi"),
    " ",
    el("button", { class: "btn ghost", onclick: preview }, "👁 Podgląd ucznia"));

  const TYPE_PL = { vocab: "fiszka", choice: "wybór", gap: "luka", translate: "tłumaczenie", dictation: "dyktando" };
  function redraw() {
    right.querySelector("h3").textContent = `📋 Program (${tasks.length} zadań)`;
    list.innerHTML = "";
    tasks.forEach((t, i) => {
      list.append(el("div", { class: "task-row" },
        el("span", { class: "badge" }, TYPE_PL[t.type] || t.type),
        el("span", { class: "task-label" }, taskLabel(t)),
        el("span", { class: "task-btns" },
          el("button", { class: "btn mini", onclick: () => { if (i > 0) { [tasks[i - 1], tasks[i]] = [tasks[i], tasks[i - 1]]; redraw(); } } }, "↑"),
          el("button", { class: "btn mini", onclick: () => { if (i < tasks.length - 1) { [tasks[i + 1], tasks[i]] = [tasks[i], tasks[i + 1]]; redraw(); } } }, "↓"),
          el("button", { class: "btn mini danger", onclick: () => { tasks.splice(i, 1); redraw(); } }, "✕"))));
    });
    if (!tasks.length) list.append(el("p", { class: "muted" }, "Dodaj zadania z banku po lewej albo stwórz własne."));
  }
  function taskLabel(t) {
    if (t.type === "vocab") return `${t.en} — ${t.pl}`;
    if (t.type === "translate") return "PL→EN: " + t.pl;
    if (t.type === "dictation") return "🎧 " + t.en;
    return (t.text || "").slice(0, 60);
  }
  redraw();

  function preview() {
    const w = el("div", { class: "modal-bg", onclick: e => { if (e.target === w) w.remove(); } });
    const m = el("div", { class: "modal card" });
    m.append(el("h3", {}, "👁 Tak zobaczy to uczeń"), el("b", {}, title.value || "Program nauki"),
      el("p", { class: "muted" }, note.value || ""), deadline.value ? el("p", {}, "Termin: " + deadline.value) : null);
    tasks.forEach((t, i) => {
      const q = el("div", { class: "exam-q" });
      if (t.type === "vocab") q.append(el("div", {}, `${i + 1}. Fiszka: ${t.pl} → ${t.en}`));
      else if (t.type === "choice") q.append(el("div", {}, `${i + 1}. ${t.text}`),
        el("div", { class: "muted small" }, "Opcje: " + t.options.join(" / ")));
      else if (t.type === "translate") q.append(el("div", {}, `${i + 1}. Przetłumacz: „${t.pl}”`));
      else if (t.type === "dictation") q.append(el("div", {}, `${i + 1}. Dyktando 🎧 (uczeń usłyszy zdanie)`));
      else q.append(el("div", {}, `${i + 1}. ${t.text}`));
      m.append(q);
    });
    m.append(el("button", { class: "btn primary", onclick: () => w.remove() }, "Zamknij"));
    w.append(m); document.body.append(w);
  }

  async function publish() {
    if (!tasks.length) { toast("Program jest pusty", true); return; }
    await API.post("/api/teacher/program", { student: username, title: title.value || "Program nauki",
      note: note.value, deadline: deadline.value, tasks });
    toast("Program przypisany ✔"); confetti(); viewTeacher();
  }

  // ------ LEWA: zakładki bank / własne
  const tabs = el("div", { class: "tabs" });
  const bankTab = el("button", { class: "tab active" }, "🏦 Bank zadań");
  const ownTab = el("button", { class: "tab" }, "✏️ Własne zadanie");
  tabs.append(bankTab, ownTab);
  const bankBox = el("div", {});
  const ownBox = el("div", { style: "display:none" });
  left.append(tabs, bankBox, ownBox);
  bankTab.onclick = () => { bankTab.classList.add("active"); ownTab.classList.remove("active"); bankBox.style.display = ""; ownBox.style.display = "none"; };
  ownTab.onclick = () => { ownTab.classList.add("active"); bankTab.classList.remove("active"); ownBox.style.display = ""; bankBox.style.display = "none"; };

  // bank
  const { bank } = await API.get("/api/teacher/bank");
  const search = el("input", { class: "input", placeholder: "Szukaj w banku…" });
  const kindSel = el("select", {},
    el("option", { value: "" }, "Wszystkie typy"),
    ...["vocab", "grammar", "translate", "dictation"].map(k =>
      el("option", { value: k }, { vocab: "Słówka", grammar: "Gramatyka", translate: "Tłumaczenia", dictation: "Dyktanda" }[k])));
  const lvlSel = el("select", {}, el("option", { value: "" }, "Każdy poziom"),
    ...["A1", "A2", "B1", "B2", "C1"].map(L => el("option", { value: L }, L)));
  const results = el("div", { class: "bank-list" });
  const info = el("div", { class: "muted small" });
  bankBox.append(el("div", { class: "bank-filters" }, search, kindSel, lvlSel), info, results);
  function renderBank() {
    const q = search.value.toLowerCase();
    const hits = bank.filter(b =>
      (!kindSel.value || b.kind === kindSel.value) &&
      (!lvlSel.value || b.level === lvlSel.value) &&
      (!q || b.label.toLowerCase().includes(q))).slice(0, 60);
    info.textContent = `Baza: ${bank.length} zadań · pokazano ${hits.length}`;
    results.innerHTML = "";
    hits.forEach(b => results.append(el("div", { class: "bank-row" },
      el("span", { class: "badge" }, b.level),
      el("span", { class: "task-label" }, b.label),
      el("button", { class: "btn mini ok", onclick: () => { tasks.push(JSON.parse(JSON.stringify(b.task))); redraw(); } }, "+ Dodaj"))));
  }
  search.oninput = renderBank; kindSel.onchange = renderBank; lvlSel.onchange = renderBank;
  renderBank();

  // własne zadania — porządne formularze
  const typeSel = el("select", {},
    ...Object.entries({ choice: "Pytanie z opcjami", gap: "Uzupełnij lukę", translate: "Tłumaczenie PL→EN", dictation: "Dyktando (TTS)", vocab: "Fiszka słówka" })
      .map(([v, n]) => el("option", { value: v }, n)));
  const formBox = el("div", {});
  ownBox.append(el("div", { class: "set-row" }, "Typ: ", typeSel), formBox);
  typeSel.onchange = renderForm;
  function renderForm() {
    formBox.innerHTML = "";
    const t = typeSel.value;
    if (t === "choice") {
      const q = el("input", { class: "input", placeholder: "Treść pytania, np. She ___ to work." });
      const opts = el("div", {});
      const optInputs = [];
      let correct = 0;
      function addOpt(v = "") {
        const idx = optInputs.length;
        const radio = el("input", { type: "radio", name: "correctOpt", ...(idx === 0 ? { checked: 1 } : {}), onchange: () => { correct = idx; } });
        const inp = el("input", { class: "input opt-inp", placeholder: "Opcja " + (idx + 1), value: v });
        optInputs.push(inp);
        opts.append(el("div", { class: "opt-row" }, radio, inp));
      }
      addOpt(); addOpt();
      formBox.append(q, el("div", { class: "muted small" }, "Zaznacz kropką poprawną odpowiedź:"), opts,
        el("button", { class: "btn mini", onclick: () => addOpt() }, "+ opcja"),
        el("input", { class: "input", id: "own-pl", placeholder: "Tłumaczenie PL (pokaże się w feedbacku)" }),
        el("button", { class: "btn ok", onclick: () => {
          const options = optInputs.map(i => i.value.trim()).filter(Boolean);
          if (!q.value.trim() || options.length < 2) { toast("Podaj pytanie i min. 2 opcje", true); return; }
          tasks.push({ type: "choice", text: q.value.trim(), options, answer: correct, pl: document.getElementById("own-pl").value });
          redraw(); toast("Dodano ✔");
        } }, "Dodaj do programu"));
    } else if (t === "gap") {
      const q = el("input", { class: "input", placeholder: "Zdanie z luką, np. He ___ (go) to work." });
      const acc = el("input", { class: "input", placeholder: "Akceptowane odpowiedzi (oddziel przecinkami), np. goes" });
      const pl = el("input", { class: "input", placeholder: "Tłumaczenie PL" });
      formBox.append(q, acc, pl, el("button", { class: "btn ok", onclick: () => {
        if (!q.value.trim() || !acc.value.trim()) { toast("Uzupełnij pola", true); return; }
        tasks.push({ type: "gap", text: q.value.trim(), accept: acc.value.split(",").map(s => s.trim()).filter(Boolean), pl: pl.value });
        redraw(); toast("Dodano ✔");
      } }, "Dodaj do programu"));
    } else if (t === "translate") {
      const pl = el("input", { class: "input", placeholder: "Zdanie po polsku" });
      const en = el("input", { class: "input", placeholder: "Wzorcowe tłumaczenie EN" });
      const kw = el("input", { class: "input", placeholder: "Słowa kluczowe (przecinki; warianty przez |), np. bought|purchased, shoes" });
      formBox.append(pl, en, kw, el("button", { class: "btn ok", onclick: () => {
        if (!pl.value.trim() || !en.value.trim()) { toast("Uzupełnij PL i EN", true); return; }
        const keywords = kw.value ? kw.value.split(",").map(g => g.split("|").map(s => s.trim()).filter(Boolean)) : en.value.toLowerCase().split(" ").filter(w => w.length > 3).map(w => [w]);
        tasks.push({ type: "translate", pl: pl.value.trim(), en_ref: en.value.trim(), keywords, tense_patterns: [], forbidden: [] });
        redraw(); toast("Dodano ✔");
      } }, "Dodaj do programu"));
    } else if (t === "dictation") {
      const en = el("input", { class: "input", placeholder: "Zdanie EN (uczeń usłyszy je głosem)" });
      const pl = el("input", { class: "input", placeholder: "Tłumaczenie PL (feedback)" });
      formBox.append(en, pl,
        el("button", { class: "btn mini", onclick: () => en.value && speak(en.value) }, "🔊 Posłuchaj"),
        el("button", { class: "btn ok", onclick: () => {
          if (!en.value.trim()) { toast("Wpisz zdanie EN", true); return; }
          tasks.push({ type: "dictation", en: en.value.trim(), pl: pl.value });
          redraw(); toast("Dodano ✔");
        } }, "Dodaj do programu"));
    } else {
      const en = el("input", { class: "input", placeholder: "Słowo EN" });
      const pl = el("input", { class: "input", placeholder: "Znaczenie PL" });
      const ex = el("input", { class: "input", placeholder: "Przykładowe zdanie (opcjonalnie)" });
      formBox.append(en, pl, ex, el("button", { class: "btn ok", onclick: () => {
        if (!en.value.trim() || !pl.value.trim()) { toast("Uzupełnij EN i PL", true); return; }
        tasks.push({ type: "vocab", en: en.value.trim(), pl: pl.value.trim(), example: ex.value });
        redraw(); toast("Dodano ✔");
      } }, "Dodaj do programu"));
    }
  }
  renderForm();
}


// ---------- Wypracowania ucznia ----------
async function viewStudentWritings(username) {
  clearMain();
  const main = document.querySelector("main");
  const { writings } = await API.get("/api/teacher/writings/" + username);
  main.append(hero("✍️", "Wypracowania: " + username,
    "Pełne teksty ucznia z oceną i wzorcem", "gold", `${writings.length} prac`));
  main.append(el("button", { class: "btn ghost", onclick: viewTeacher }, "← Lista uczniów"));
  const card = el("div", { class: "card" });
  if (!writings.length) card.append(el("p", { class: "muted" }, "Uczeń nie oddał jeszcze żadnej pracy pisemnej."));
  writings.forEach(w => card.append(el("div", { class: "feedback " + (w.score >= 0.65 ? "fb-good" : "fb-part"), style: "margin-bottom:12px" },
    el("div", { class: "fb-head" }, `${w.title} · ${Math.round((w.score || 0) * 100)}% · ${w.date || ""}`),
    el("div", { class: "write-your" }, w.text || "—"),
    w.model ? el("details", { class: "path-sec" }, el("summary", {}, "📘 Wzorzec"),
      el("div", { class: "kb-ex" }, w.model)) : null)));
  main.append(card);
}
