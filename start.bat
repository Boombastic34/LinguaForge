@echo off
title LinguaForge
cd /d "%~dp0"
echo ==========================================
echo   LinguaForge - kuznia Twojego angielskiego
echo ==========================================
where python >nul 2>nul
if errorlevel 1 (
  echo [BLAD] Nie znaleziono Pythona. Zainstaluj go z https://www.python.org/downloads/
  echo Podczas instalacji zaznacz "Add Python to PATH"!
  pause
  exit /b
)
echo Sprawdzam biblioteki...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
echo Uruchamiam serwer... (przegladarka otworzy sie sama)
python main.py
pause
