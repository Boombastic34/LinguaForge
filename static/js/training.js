// Mój trening — własny program nauki z wybranych kategorii
async function viewTraining() {
  clearMain();
  const main = document.querySelector("main");
  const o = await API.get("/api/training/options");
  main.append(hero("🛠", "Mój trening",
    "Zbuduj własny zestaw: wybierz rodzaje ćwiczeń i zakres materiału", "indigo",
    `${o.kinds.length} rodzajów ćwiczeń`));

  const box = el("div", { class: "card" });
  main.append(box);

  const kinds = new Set(["vocab_recognise", "vocab_produce"]);
  const themes = new Set();
  const topics = new Set();
  const levels = new Set();

  // --- rodzaje ćwiczeń
  box.append(el("h3", {}, "1. Czego chcesz trenować?"));
  const kindGrid = el("div", { class: "kind-grid" });
  o.kinds.forEach(k => {
    const cell = el("div", { class: "kind-cell" + (kinds.has(k.id) ? " on" : ""), onclick: () => {
      if (kinds.has(k.id)) { kinds.delete(k.id); cell.classList.remove("on"); }
      else { kinds.add(k.id); cell.classList.add("on"); }
    } }, el("b", {}, k.name));
    kindGrid.append(cell);
  });
  box.append(kindGrid);

  // --- zakres słownictwa
  box.append(el("h3", {}, "2. Zakres słownictwa (opcjonalnie)"),
    el("p", { class: "muted small" }, "Nic nie zaznaczasz = cała baza. Zaznacz kategorie, jeśli chcesz trenować konkretny obszar."));
  const themeWrap = el("div", { class: "mix-checks" });
  o.themes.forEach(t => themeWrap.append(el("label", { class: "chip chip-check" },
    el("input", { type: "checkbox", onchange: e => e.target.checked ? themes.add(t.id) : themes.delete(t.id) }),
    ` ${t.name} (${t.n})`)));
  box.append(themeWrap);

  // --- zakres gramatyki / teorii
  box.append(el("h3", {}, "3. Zakres gramatyki i teorii (opcjonalnie)"));
  const topicWrap = el("div", { class: "mix-checks" });
  o.topics.forEach(t => topicWrap.append(el("label", { class: "chip chip-check" },
    el("input", { type: "checkbox", onchange: e => e.target.checked ? topics.add(t.id) : topics.delete(t.id) }),
    ` ${t.name} (${t.n})`)));
  o.articles.forEach(a => topicWrap.append(el("label", { class: "chip chip-check" },
    el("input", { type: "checkbox", onchange: e => e.target.checked ? topics.add(a.id) : topics.delete(a.id) }),
    ` 📖 ${a.name}`)));
  box.append(topicWrap);

  // --- poziom i długość
  box.append(el("h3", {}, "4. Poziom i długość"));
  const lvlWrap = el("div", { class: "mix-checks" });
  o.levels.forEach(L => lvlWrap.append(el("label", { class: "chip chip-check" },
    el("input", { type: "checkbox", onchange: e => e.target.checked ? levels.add(L) : levels.delete(L) }), " " + L)));
  const nInp = el("input", { class: "input short", type: "number", value: 12, min: 4, max: 40 });
  const nameInp = el("input", { class: "input", placeholder: "Nazwa treningu (opcjonalnie), np. Powtórka przed zmianą" });
  box.append(lvlWrap, el("div", { class: "set-row" }, "Liczba zadań: ", nInp), nameInp);

  box.append(el("div", { class: "fb-btns" },
    el("button", { class: "btn primary big", onclick: start }, "▶ Zbuduj i zacznij trening"),
    el("button", { class: "btn ghost", onclick: () => {
      kinds.clear(); ["vocab_produce", "grammar", "translate", "dictation"].forEach(k => kinds.add(k));
      kindGrid.querySelectorAll(".kind-cell").forEach((c, i) =>
        c.classList.toggle("on", kinds.has(o.kinds[i].id)));
      toast("Ustawiono zestaw mieszany");
    } }, "🎲 Zestaw mieszany")));

  async function start() {
    if (!kinds.size) return toast("Zaznacz przynajmniej jeden rodzaj ćwiczeń", true);
    try {
      const data = await API.post("/api/training/build", {
        kinds: [...kinds], themes: [...themes], topics: [...topics],
        levels: [...levels], n: +nInp.value, name: nameInp.value,
      });
      runBuiltSession(data);
    } catch (e) {
      toast("Nie udało się złożyć treningu — zmień zakres", true);
    }
  }
}

// odtwarza gotową sesję (bez ponownego pobierania z serwera)
function runBuiltSession(data) {
  clearMain();
  const main = document.querySelector("main");
  main.append(hero("🛠", data.link.name, "Twój własny zestaw", "indigo", `${(data.tasks || []).length} zadań`));
  const box = el("div", { class: "card" });
  main.append(box);
  runTaskList(box, data.tasks, "custom", () => viewTraining());
}
