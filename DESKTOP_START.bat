@echo off
title AUTO SERVIS PRO - DESKTOP APP
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║       🖥️  AUTO SERVIS PRO - WINDOWS DESKTOP APP           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Pokretanje aplikacije...
echo.

cd /d "%~dp0"

REM Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [GRESKA] Virtual environment ne postoji!
    echo Pokrenite install.bat prvo.
    pause
    exit /b 1
)

REM Start desktop app
cd narudzbe
python main.py

if errorlevel 1 (
    echo.
    echo [GRESKA] Aplikacija se nije pokrenula!
    echo.
    pause
)
