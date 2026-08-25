@echo off
chcp 65001 >nul
title LinguaForge - tryb telefonu
cd /d "%~dp0"
echo ==========================================
echo   LinguaForge - dostep z telefonu
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
echo.
echo Za chwile zobaczysz adres do wpisania w telefonie.
echo Telefon musi byc w tej samej sieci Wi-Fi co ten komputer.
echo Przy pierwszym uruchomieniu Windows moze zapytac o dostep do sieci
echo - zaznacz "Sieci prywatne" i kliknij "Zezwol na dostep".
echo.
set LF_LAN=1
python main.py
pause
