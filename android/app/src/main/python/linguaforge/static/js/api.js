// Warstwa komunikacji z serwerem
const API = {
  token: localStorage.getItem("lf_token") || "",
  user: JSON.parse(localStorage.getItem("lf_user") || "null"),

  setAuth(tok) {
    this.token = tok.token; this.user = { username: tok.username, role: tok.role };
    localStorage.setItem("lf_token", this.token);
    localStorage.setItem("lf_user", JSON.stringify(this.user));
  },
  logout() {
    this.token = ""; this.user = null;
    localStorage.removeItem("lf_token"); localStorage.removeItem("lf_user");
    location.hash = ""; location.reload();
  },
  online: true,
  async call(path, method = "GET", body = null, timeout = 12000) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeout);
    let res;
    try {
      res = await fetch(path, {
        method,
        headers: { "Content-Type": "application/json", "x-token": this.token },
        body: body ? JSON.stringify(body) : null,
        signal: ctrl.signal,
      });
    } catch (e) {
      clearTimeout(timer);
      this.online = false;
      if (typeof serverDown === "function") serverDown();
      throw new Error("Brak połączenia z aplikacją — sprawdź, czy serwer działa.");
    }
    clearTimeout(timer);
    this.online = true;
    if (typeof serverUp === "function") serverUp();
    if (res.status === 401) { this.logout(); throw new Error("Sesja wygasła"); }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || data.detail || "Błąd serwera");
    return data;
  },
  get(p) { return this.call(p); },
  post(p, b) { return this.call(p, "POST", b || {}); },
  async download(path) {
    const res = await fetch(path, { headers: { "x-token": this.token } });
    if (!res.ok) { toast("Błąd pobierania", true); return; }
    const blob = await res.blob();
    const cd = res.headers.get("Content-Disposition") || "";
    const m = cd.match(/filename=([^;]+)/);
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = m ? m[1].trim() : "eksport";
    a.click();
    URL.revokeObjectURL(a.href);
  },
};
