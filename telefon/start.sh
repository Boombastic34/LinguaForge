#!/data/data/com.termux/files/usr/bin/bash
# LinguaForge — uruchomienie na telefonie (Termux) z ochroną przed usypianiem
cd "$(dirname "$0")/.."

# 1) blokada uśpienia procesora — bez tego Android zatrzymuje serwer po wyjściu z Termuksa
termux-wake-lock 2>/dev/null && echo "[OK] Blokada uśpienia włączona" \
  || echo "[!] Brak Termux:API — zainstaluj aplikacje Termux:API, aby serwer nie zasypiał"

# 2) stałe powiadomienie = Android traktuje Termux jak aplikację pierwszoplanowa
termux-notification --id linguaforge --ongoing \
  --title "LinguaForge działa" \
  --content "Dotknij, aby wrócić do nauki • http://127.0.0.1:8177" 2>/dev/null

echo
echo "=============================================="
echo "  LinguaForge dziala w tle."
echo "  Otworz w przegladarce:  http://127.0.0.1:8177"
echo "  Mozesz zminimalizowac Termux (przycisk HOME)."
echo "  Zatrzymanie: wroc tutaj i nacisnij Ctrl+C."
echo "=============================================="
echo

cleanup() {
  termux-notification-remove linguaforge 2>/dev/null
  termux-wake-unlock 2>/dev/null
  echo "LinguaForge zatrzymana."
}
trap cleanup EXIT INT TERM

python main.py
