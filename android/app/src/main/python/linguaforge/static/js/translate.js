// Tłumaczenia zdań z oceną czasu gramatycznego
async function viewTranslate() {
  clearMain();
  const main = document.querySelector("main");
  const stats = await API.get("/api/content/stats");
  main.append(hero("🌐", "Tłumaczenia", "Przetłumacz zdanie — system ocenia słowa I użyty czas", "teal",
    `${stats.translations} zdań w bazie`));
  const box = el("div", { class: "card" });
  main.append(box);
  let t0 = 0;

  async function next() {
    box.innerHTML = "";
    const it = await API.get("/api/translate/next");
    t0 = Date.now();
    if (it.locked_domains && it.locked_domains.length)
      box.append(el("div", { class: "lockinfo" },
        `🔒 Dziedzina „${it.locked_domains.join(", ")}” odblokuje się, gdy poznasz ~25% jej słówek na fiszkach (nauka etapami).`));
    box.append(
      el("span", { class: "badge" }, `${it.level}${it.tense_name ? " · " + it.tense_name : ""}`),
      el("div", { class: "qtext" }, "„" + it.pl + "”"));
    const inp = el("input", { class: "input", placeholder: "Tłumaczenie po angielsku…", autocomplete: "off" });
    const send = el("button", { class: "btn ok" }, "Sprawdź");
    send.onclick = () => check(it, inp.value.trim());
    inp.onkeydown = e => { if (e.key === "Enter") send.click(); };
    box.append(inp, send);
    inp.focus();
  }

  async function check(it, val) {
    box.querySelectorAll("button,input").forEach(b => b.disabled = true);
    const { result, xp } = await API.post("/api/translate/check", { id: it.id, answer: val, rt: Date.now() - t0 });
    const ok = result.score >= 0.7;
    if (ok && xp) xpPop(xp);
    box.innerHTML = "";
    box.append(feedbackPanel({
      correct: ok, your: val, answer: result.ref, pl: it.pl, tts: result.ref,
      en: result.ref,
      explain: result.feedback + (result.hint && !result.tense_ok ? "" : (result.hint ? " " + result.hint : "")),
      onNext: next,
    }));
    box.append(el("div", { class: "muted small" }, `Trafność: ${Math.round(result.score * 100)}%`));
  }
  next();
}
