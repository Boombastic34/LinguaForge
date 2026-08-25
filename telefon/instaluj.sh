#!/data/data/com.termux/files/usr/bin/bash
# LinguaForge — instalacja na telefonie (Termux). Uruchom raz: bash instaluj.sh
set -e
echo "=============================================="
echo "  LinguaForge — instalacja na telefonie"
echo "=============================================="
echo
echo "[1/4] Aktualizuję pakiety Termuksa..."
pkg update -y && pkg upgrade -y

echo
echo "[2/4] Instaluję Pythona i narzędzia..."
pkg install -y python rust binutils build-essential libjpeg-turbo freetype

echo
echo "[3/4] Instaluję biblioteki aplikacji (to potrwa kilka minut)..."
python -m pip install --upgrade pip wheel setuptools
# najpierw próba szybka (gotowe paczki), potem awaryjnie budowanie ze źródeł
# zestaw bez modułów kompilowanych — instaluje się na telefonie bez Rusta
pip install -r telefon/requirements_telefon.txt
# reportlab jest opcjonalny (katalog PDF); brak nie przeszkadza w nauce
pip install reportlab || echo "(pominięto reportlab — katalog PDF będzie w formacie HTML)"

echo
echo "[4/4] Nadaję dostęp do plików..."
termux-setup-storage || true

echo
echo "=============================================="
echo "  GOTOWE. Uruchamiaj aplikację poleceniem:"
echo "     bash start.sh"
echo "=============================================="
