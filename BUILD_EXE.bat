@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║  AUTO SERVIS PRO - WINDOWS EXE BUILD                              ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

REM Provjeri Python
echo [1/4] Provjeravam Python...
if not exist ".venv\bin\python.exe" (
    echo     ❌ Virtual environment ne postoji!
    echo.
    echo     Pokreni prvo: .\install.bat
    pause
    exit /b 1
)
echo     ✅ Python: .venv\bin\python.exe

echo.
echo [2/4] Provjeravam PyInstaller...
.venv\bin\python.exe -m pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo     ⚙️  Instaliram PyInstaller...
    .venv\bin\python.exe -m pip install pyinstaller --quiet
    if errorlevel 1 (
        echo     ❌ Instalacija PyInstaller-a nije uspjela
        pause
        exit /b 1
    )
    echo     ✅ PyInstaller instaliran
) else (
    echo     ✅ PyInstaller je već instaliran
)

echo.
echo [3/4] Kreiram output foldere...
if not exist "output\windows" mkdir output\windows
if not exist "build" mkdir build
echo     ✅ Folderi kreirani

echo.
echo [4/4] Kreiram Windows EXE...
echo.
echo ⏳ PyInstaller u toku... Ovo može trajati 2-5 minuta...
echo.

.venv\bin\python.exe -m PyInstaller --onefile --windowed --name "AutoServisPro" --add-data "narudzbe;narudzbe" --hidden-import=sqlite3 --hidden-import=tkinter --hidden-import=tkcalendar --hidden-import=babel.numbers --exclude-module=matplotlib --exclude-module=numpy --exclude-module=pandas --distpath output\windows --workpath build\windows --specpath build --clean --noconfirm narudzbe\main.py

if errorlevel 1 (
    echo.
    echo ╔═══════════════════════════════════════════════════════════════════╗
    echo ║  ❌ BUILD FAILED!                                                 ║
    echo ╚═══════════════════════════════════════════════════════════════════╝
    echo.
    echo 🔍 Mogući problemi:
    echo    - PyInstaller nije pravilno instaliran
    echo    - MSYS2 Python problem (koristi normalni Windows Python)
    echo    - Nedostaju neki dependencies
    echo.
    echo 🔧 Rješenja:
    echo    1. Instaliraj normalni Windows Python sa python.org (3.11 ili 3.12)
    echo    2. Kreiraj novu venv: python -m venv venv
    echo    3. Instaliraj: pip install tkinter tkcalendar babel pyinstaller
    echo    4. Pokreni ponovo
    echo.
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║  ✅ USPJEŠNO! Windows EXE kreiran                                 ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

echo 📁 Lokacija:
echo    output\windows\AutoServisPro.exe
echo.

if exist "output\windows\AutoServisPro.exe" (
    echo 📊 Informacije:
    dir output\windows\AutoServisPro.exe | findstr /C:"AutoServisPro.exe"
    echo.
)

echo ┌───────────────────────────────────────────────────────────────────┐
echo │ 🚀 TESTIRANJE                                                      │
echo └───────────────────────────────────────────────────────────────────┘
echo.
echo    output\windows\AutoServisPro.exe
echo.

echo ┌───────────────────────────────────────────────────────────────────┐
echo │ 📦 DISTRIBUCIJA                                                    │
echo └───────────────────────────────────────────────────────────────────┘
echo.
echo    ✓ Kopiraj AutoServisPro.exe bilo gdje
echo    ✓ Ne zahtijeva instalaciju Python-a
echo    ✓ Sve dependencies su uključene
echo    ✓ Baza se kreira automatski pri prvom pokretanju
echo.

echo ┌───────────────────────────────────────────────────────────────────┐
echo │ 🎯 DEFAULT KORISNICI                                               │
echo └───────────────────────────────────────────────────────────────────┘
echo.
echo    👤 Admin: admin / admin123
echo    👤 User:  user / user123
echo.

pause
