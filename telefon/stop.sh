#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")/.."
if [ -f logs/serwer.pid ]; then
  kill "$(cat logs/serwer.pid)" 2>/dev/null && echo "Zatrzymano serwer."
  rm -f logs/serwer.pid
else
  pkill -f "python main.py" && echo "Zatrzymano serwer."
fi
termux-notification-remove linguaforge 2>/dev/null
termux-wake-unlock 2>/dev/null
