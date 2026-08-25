#!/data/data/com.termux/files/usr/bin/bash
# Uruchomienie w tle — serwer dziala nawet po zamknieciu okna Termuksa.
cd "$(dirname "$0")/.."
termux-wake-lock 2>/dev/null
termux-notification --id linguaforge --ongoing \
  --title "LinguaForge działa" \
  --content "http://127.0.0.1:8177 • dotknij, aby wrócić do nauki" 2>/dev/null
mkdir -p logs
nohup python main.py > logs/serwer.log 2>&1 &
echo $! > logs/serwer.pid
sleep 2
echo "=============================================="
echo "  LinguaForge uruchomiona w tle (PID $(cat logs/serwer.pid))."
echo "  Otworz:  http://127.0.0.1:8177"
echo "  Zatrzymanie:  bash telefon/stop.sh"
echo "=============================================="
