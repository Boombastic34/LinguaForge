#!/bin/bash
# Kopiuje kod aplikacji do projektu Androida (uruchom przed budowaniem APK).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$(dirname "$HERE")"
DST="$HERE/app/src/main/python/linguaforge"
rm -rf "$DST"
mkdir -p "$DST"
cp -r "$SRC/main.py" "$SRC/core" "$SRC/data" "$SRC/static" "$DST/"
rm -rf "$DST/data/_kopie" "$DST"/**/__pycache__ 2>/dev/null || true
echo "Skopiowano kod aplikacji do: $DST"
