@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║  AUTO SERVIS PRO - QUICK WINDOWS EXE BUILD                        ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

REM Provjeri Python
echo [√] Provjeravam Python...
if exist ".venv\bin\python.exe" (
    echo     ✅ MSYS2 Python: .venv\bin\python.exe
    set PY=.venv\bin\python.exe
) else (
    if exist ".venv\Scripts\python.exe" (
        echo     ✅ Windows Python: .venv\Scripts\python.exe
        set PY=.venv\Scripts\python.exe
    ) else (
        echo     ❌ Virtual environment ne postoji!
        echo.
        echo     Pokreni prvo: .\install.bat
        pause
        exit /b 1
    )
)


echo.
echo [√] Provjeravam PyInstaller...
!PY! -m pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo     ⚙️  Instaliram PyInstaller (ovo može trajati malo)...
    !PY! -m pip install pyinstaller --quiet
    echo     ✅ PyInstaller instaliran
) else (
    echo     ✅ PyInstaller je već instaliran
)

echo.
echo [√] Kreiram Windows EXE...
echo.
echo ⏳ Kompajliranje u toku... Ovo može trajati 2-5 minuta...
echo.

REM Kreiraj output folder
if not exist "output\windows" mkdir output\windows
if not exist "build" mkdir build

REM Pokreni PyInstaller (sa ili bez ikone - ne smeta ako ne postoji)
!PY! -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "AutoServisPro" ^
    --add-data "narudzbe;narudzbe" ^
    --hidden-import=sqlite3 ^
    --hidden-import=tkinter ^
    --hidden-import=tkcalendar ^
    --hidden-import=babel.numbers ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --distpath output\windows ^
    --workpath build\windows ^
    --specpath build ^
    --clean ^
    --noconfirm ^
    narudzbe\main.py

if errorlevel 1 (
    echo.
    echo ❌ BUILD FAILED!
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
    echo    4. Pokreni ponovo: .\BUILD_WINDOWS_QUICK.bat
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

REM Prikaži veličinu fajla
if exist "output\windows\AutoServisPro.exe" (
    echo 📊 Informacije:
    dir output\windows\AutoServisPro.exe | findstr /C:"AutoServisPro.exe"
    echo.
)

echo ┌───────────────────────────────────────────────────────────────────┐
echo │ 🚀 TESTIRANJE APLIKACIJE                                          │
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
echo │ 💾 DISTRIBUCIJA SA POSTOJEĆOM BAZOM                                │
echo └───────────────────────────────────────────────────────────────────┘
echo.
echo    Ako želiš da distribuiraš sa već popunjenom bazom:
echo    - Kopiraj: autoservice.db u isti folder kao AutoServisPro.exe
echo.

echo ┌───────────────────────────────────────────────────────────────────┐
echo │ 🎯 DEFAULT KORISNICI                                               │
echo └───────────────────────────────────────────────────────────────────┘
echo.
echo    👤 Admin: admin / admin123
echo    👤 User:  user / user123
echo.

pause
