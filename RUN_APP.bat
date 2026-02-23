@echo off
REM ================================================================
REM   AUTO SERVIS PRO - QUICK START
REM   Pokrece Desktop App + API Server odjednom
REM ================================================================

title Auto Servis Pro - Launcher
color 0A

echo ============================================
echo   AUTO SERVIS PRO - QUICK START
echo ============================================
echo.

REM Provjeri venv
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment ne postoji!
    echo Pokrenite prvo: install.bat
    pause
    exit /b 1
)

echo [1/3] Pokretanje API servera na port 7000...
start "Auto Servis API" /MIN cmd /c ".venv\Scripts\python.exe narudzbe\api_server.py"
timeout /t 3 /nobreak >nul

echo [2/3] Pokretanje Desktop aplikacije...
cd narudzbe
start "Auto Servis Desktop" ..\\.venv\Scripts\python.exe main.py
cd ..

timeout /t 2 /nobreak >nul

echo [3/3] Otvaranje web interfacea...
start http://localhost:7000

echo.
echo ============================================
echo   SISTEM POKRENUT!
echo ============================================
echo.
echo   Desktop App: Prozor se otvorio
echo   API Server:  http://localhost:7000
echo   Web Access:  Provjeri browser
echo.
echo   Za zatvaranje: Zatvori prozore ili Ctrl+C
echo.
echo ============================================
echo.

pause
