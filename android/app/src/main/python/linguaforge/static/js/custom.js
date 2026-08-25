// Własne fiszki użytkownika
async function viewCustom() {
  const m = clearMain();
  const en = el("input", { type: "text", placeholder: "np. reach the target" });
  const pl = el("input", { type: "text", placeholder: "np. osiągnąć cel/normę" });
  const ex = el("input", { type: "text", placeholder: "np. We reached the target before 2 p.m." });
  const hint = el("input", { type: "text", placeholder: "np. skojarzenie, wymowa…" });
  const lvl = levelSelect("A2", "clvl");

  const form = el("div", { class: "card ember" },
    el("div", { class: "eyebrow" }, "Własne fiszki"),
    el("p", { class: "muted" }, "Usłyszałeś coś w pracy? Dodaj — słowo wejdzie do systemu powtórek FSRS jak każde inne."),
    el("label", {}, "Po angielsku *"), en,
    el("label", {}, "Po polsku *"), pl,
    el("label", {}, "Przykładowe zdanie"), ex,
    el("label", {}, "Podpowiedź / skojarzenie"), hint,
    el("label", {}, "Poziom"), lvl,
    el("button", { class: "btn mt", onclick: add }, "Dodaj fiszkę"));

  const listCard = el("div", { class: "card" }, el("div", { class: "eyebrow" }, "Twoje fiszki"));
  const tbl = el("table", {});
  listCard.append(tbl);

  async function refresh() {
    const d = await API.get("/api/cards/custom");
    tbl.innerHTML = "";
    tbl.append(el("tr", {}, el("th", {}, "EN"), el("th", {}, "PL"), el("th", {}, "Poziom"), el("th", {}, "Źródło")));
    for (const it of d.items.slice().reverse())
      tbl.append(el("tr", {},
        el("td", {}, el("b", {}, it.en)), el("td", {}, it.pl),
        el("td", {}, it.level || "—"),
        el("td", {}, it.from_teacher ? "👨‍🏫 nauczyciel" : "ja")));
    if (d.items.length === 0)
      tbl.append(el("tr", {}, el("td", { colspan: 4, class: "muted" }, "Jeszcze pusto — dodaj pierwszą fiszkę powyżej.")));
  }

  async function add() {
    if (!en.value.trim() || !pl.value.trim()) return toast("Wypełnij oba pola językowe", true);
    await API.post("/api/cards/custom", { en: en.value, pl: pl.value, example: ex.value,
      hint: hint.value, level: lvl.value });
    toast("Fiszka dodana do Twojej talii ✔");
    en.value = pl.value = ex.value = hint.value = "";
    refresh();
  }

  m.append(form, listCard);
  refresh();
}
