@echo off
chcp 65001 >nul
cls
echo.
echo ============================================
echo    AUTO SERVIS PRO - QUICK START
echo ============================================
echo.

cd /d "%~dp0"

REM Proveri Flask
echo [1/4] Provera dependencies...
.\.venv\bin\python.exe -c "import flask" 2>nul
if errorlevel 1 (
    echo ! Flask nije instaliran - API server neće raditi
    set SKIP_API=1
) else (
    echo ✓ Flask OK
    set SKIP_API=0
)

REM Pokreni API server u background (ako je Flask instaliran)
if "%SKIP_API%"=="0" (
    echo [2/4] Pokretanje API servera...
    start /B .\.venv\bin\python.exe narudzbe\api_server.py
    timeout /t 2 /nobreak >nul
    echo ✓ API Server pokrenut na http://localhost:7000
) else (
    echo [2/4] API server preskočen
)

REM Pokreni Web Server (uvek radi, bez Flask zavisnosti)
echo [3/4] Pokretanje Web interfejsa...
start /B .\.venv\bin\python.exe narudzbe\web_server.py
timeout /t 2 /nobreak >nul
echo ✓ Web interfejs pokrenut na http://localhost:8000

REM Pokreni Desktop App
echo [4/4] Pokretanje Desktop aplikacije...
start .\.venv\bin\python.exe narudzbe\main.py
timeout /t 1 /nobreak >nul
echo ✓ Desktop App pokrenut

echo.
echo ============================================
echo    SISTEM POKRENUT!
echo ============================================
echo.
echo Desktop App: Prozor otvoren ✅
echo Web Interface: http://localhost:8000 ✅
if "%SKIP_API%"=="0" (
    echo API Server: http://localhost:7000 ✅
) else (
    echo API Server: NIJE INSTALIRAN ⚠️
)
echo.
echo Login: admin / admin123
echo.
echo 🌐 Otvori u browseru: http://localhost:8000
echo.