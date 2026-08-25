@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Kopiuje kod aplikacji do projektu Androida...
set DST=app\src\main\python\linguaforge
if exist "%DST%" rmdir /s /q "%DST%"
mkdir "%DST%"
xcopy /E /I /Y "..\core" "%DST%\core" >nul
xcopy /E /I /Y "..\data" "%DST%\data" >nul
xcopy /E /I /Y "..\static" "%DST%\static" >nul
copy /Y "..\main.py" "%DST%\main.py" >nul
echo Gotowe: %DST%
pause
