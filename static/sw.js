// Service worker — wymagany przez Chrome do instalacji aplikacji na telefonie.
// Trzyma w pamięci podręcznej tylko powłokę (style, skrypty, ikony);
// dane i odpowiedzi z API nigdy nie są cache'owane.
const SHELL = "lf-shell-v1";
const FILES = ["/", "/manifest.json", "/icons/icon-192.png", "/icons/icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(FILES)).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== SHELL).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.pathname.startsWith("/api/")) return;  // dane zawsze z serwera
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request).then(r => r || caches.match("/")))
  );
});
