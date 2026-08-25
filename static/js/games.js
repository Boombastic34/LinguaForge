// Mini-gra: dopasuj pary EN-PL na czas
async function viewGames() {
  const m = clearMain();
  const d = await API.get("/api/game/pairs");
  const start = Date.now();
  let sel = null, left = d.pairs.length;

  const tiles = [];
  d.pairs.forEach((p, i) => {
    tiles.push({ txt: p.en, key: i }, { txt: p.pl, key: i });
  });
  tiles.sort(() => Math.random() - .5);

  const grid = el("div", { class: "pairs-grid" });
  const timer = el("span", { class: "badge" }, "0.0 s");
  const iv = setInterval(() => timer.textContent = ((Date.now() - start) / 1000).toFixed(1) + " s", 100);

  tiles.forEach(t => {
    const b = el("button", { class: "pair-tile" }, t.txt);
    b.onclick = () => {
      if (sel === b) return;
      if (!sel) { sel = b; b.classList.add("sel"); b.dataset.key = t.key; return; }
      if (Number(sel.dataset.key) === t.key) {
        sel.classList.remove("sel"); sel.classList.add("done"); b.classList.add("done");
        sel = null; left--;
        if (!left) finish();
      } else {
        b.classList.add("wrong"); sel.classList.add("wrong");
        const s = sel; sel = null;
        setTimeout(() => { b.classList.remove("wrong"); s.classList.remove("wrong", "sel"); }, 350);
      }
    };
    b.dataset.key = t.key;
    grid.append(b);
  });

  async function finish() {
    clearInterval(iv);
    const ms = Date.now() - start;
    confetti();
    const xp = ms < 20000 ? 12 : (ms < 40000 ? 8 : 5);
    await API.post("/api/game/result", { game: "pairs", ms, xp });
    toast(`🏁 Czas: ${(ms / 1000).toFixed(1)} s · +${xp} XP`);
    setTimeout(viewGames, 1600);
  }

  m.append(el("div", { class: "card gold" },
    el("div", { class: "row", style: "justify-content:space-between" },
      el("div", { class: "eyebrow" }, "Gra · pary na czas"), timer),
    el("p", { class: "muted mb" }, "Połącz słowo angielskie z polskim znaczeniem. Gra korzysta z Twoich słówek z fiszek."),
    grid));
}
