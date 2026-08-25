// Widok logowania / rejestracji
function viewAuth() {
  const app = document.getElementById("app");
  app.innerHTML = "";
  let mode = "login";

  const user = el("input", { type: "text", id: "u", placeholder: "np. marek" });
  const pass = el("input", { type: "password", id: "p", placeholder: "hasło" });
  const btn = el("button", { class: "btn mt", style: "width:100%" }, "Zaloguj się");
  const info = el("p", { class: "muted mt center" }, "");

  const tabL = el("button", { class: "btn sm" }, "Logowanie");
  const tabR = el("button", { class: "btn sm ghost" }, "Nowe konto");
  function setMode(m) {
    mode = m;
    tabL.className = "btn sm" + (m === "login" ? "" : " ghost");
    tabR.className = "btn sm" + (m === "register" ? "" : " ghost");
    btn.textContent = m === "login" ? "Zaloguj się" : "Załóż konto i zacznij";
  }
  tabL.onclick = () => setMode("login");
  tabR.onclick = () => setMode("register");

  async function go() {
    try {
      const tok = await API.post("/api/" + mode, { username: user.value, password: pass.value });
      API.setAuth(tok);
      location.hash = tok.role === "teacher" ? "#teacher" : "#dashboard";
      boot();
    } catch (e) { info.textContent = e.message; info.style.color = "var(--red)"; }
  }
  btn.onclick = go;
  pass.addEventListener("keydown", e => { if (e.key === "Enter") go(); });

  app.append(el("div", { class: "auth-wrap" },
    el("div", { class: "card ember auth-card" },
      el("div", { class: "auth-hero brand" }, "Lingua", el("span", {}, "Forge")),
      el("p", { class: "muted mb" }, "Kuźnia Twojego angielskiego. Ucz się mądrze, nie długo."),
      el("div", { class: "tabbtns" }, tabL, tabR),
      el("label", {}, "Nazwa użytkownika"), user,
      el("label", {}, "Hasło"), pass,
      btn, info,
      el("p", { class: "muted mt", style: "font-size:.75rem" },
        "Konto nauczyciela: login „nauczyciel”, hasło „nauczyciel”."))));
}
