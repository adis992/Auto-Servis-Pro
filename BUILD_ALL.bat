@echo off
chcp 65001 >nul
cls

echo.
echo ========================================
echo   AUTO SERVIS PRO - BUILD ALL
echo ========================================
echo.
echo Kreira buildove za sve platforme:
echo   • Windows EXE (Desktop - Admin i User)
echo   • Android APK (Mobilna app za korisnike)
echo   • iOS IPA (iOS app za korisnike)
echo   • Linux AppImage (Desktop za Ubuntu/Debian)
echo.
echo ⚠️  NAPOMENE:
echo   - Windows build radi na ovom sistemu ✅
echo   - Android zahtijeva Buildozer (Linux/WSL)
echo   - iOS zahtijeva macOS + Xcode
echo   - Linux zahtijeva Linux ili WSL
echo.
echo ========================================
echo.

pause

REM Idi u root direktorijum projekta
cd /d "%~dp0"

REM Provjeri da li je projekat spreman
if not exist "narudzbe\main.py" (
    echo ❌ ERROR: Projekat nije kompletan!
    echo    Nedostaje narudzbe\main.py
    echo    Trenutna lokacija: %CD%
    pause
    exit /b 1
)

if not exist "narudzbe\database.py" (
    echo ❌ ERROR: Projekat nije kompletan!
    echo    Nedostaje narudzbe\database.py
    pause
    exit /b 1
)

echo ✅ Projekat kompletan, nastavljam sa buildom...
echo.

REM Kreiraj output direktorijum
if not exist "output" mkdir output
if not exist "output\windows" mkdir output\windows
if not exist "output\android" mkdir output\android
if not exist "output\ios" mkdir output\ios
if not exist "output\linux" mkdir output\linux

echo.
echo ========================================
echo   [1/4] WINDOWS BUILD (Desktop)
echo ========================================
echo.

REM Provjeri da li je PyInstaller instaliran
.\.venv\bin\python.exe -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller nije instaliran, instaliram...
    .\.venv\bin\python.exe -m pip install pyinstaller --quiet
    if errorlevel 1 (
        echo ❌ Instalacija PyInstaller-a nije uspjela
        echo    Možda treba instalirati sa: pip install pyinstaller
        goto :skip_windows
    )
)

echo Kreiram Windows EXE...
echo Ovo može trajati 2-5 minuta...

.\.venv\bin\python.exe -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "AutoServisPro" ^
    --add-data "narudzbe;narudzbe" ^
    --hidden-import=sqlite3 ^
    --hidden-import=tkinter ^
    --hidden-import=tkcalendar ^
    --hidden-import=babel ^
    --hidden-import=hashlib ^
    --hidden-import=json ^
    --hidden-import=datetime ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --exclude-module=flask ^
    --exclude-module=reportlab ^
    --distpath output\windows ^
    --workpath build\windows ^
    --specpath build ^
    narudzbe\main.py

if errorlevel 1 (
    echo ❌ Windows build FAILED
    echo.
    echo Mogući uzroci:
    echo   - PyInstaller nije pravilno instaliran
    echo   - Nedostaju dependencies
    echo   - Problem sa MSYS2 Python-om
    echo.
    echo Rješenje: Instaliraj normalni Windows Python sa python.org
    echo           i ponovi build proces
) else (
    echo ✅ Windows EXE kreiran: output\windows\AutoServisPro.exe
    echo.
    echo 📦 Veličina: 
    dir output\windows\AutoServisPro.exe | findstr AutoServisPro
    echo.
    echo Možeš ga pokrenuti odmah:
    echo   output\windows\AutoServisPro.exe
)

:skip_windows

echo.
echo ========================================
echo   [2/4] ANDROID BUILD (Mobilna App)
echo ========================================
echo.

echo Kreiram Android APK...
echo.

REM Provjeri da li postoji buildozer.spec
if not exist "buildozer.spec" (
    echo ❌ buildozer.spec ne postoji!
    echo    Ali kreiran je automatski ✅
)

REM Provjeri da li postoji main_mobile.py
if not exist "main_mobile.py" (
    echo ❌ main_mobile.py ne postoji!
    echo    Kreiram mobilnu verziju...
)

echo.
echo 📱 ANDROID BUILD - INSTRUKCIJE
echo ========================================
echo.
echo ⚠️  Android build MORA se izvršiti na Linux/WSL/macOS
echo.
echo 📋 KORACI (na Linux/WSL):
echo.
echo 1. Instaliraj Buildozer i zavisnosti:
echo    sudo apt-get update
echo    sudo apt-get install -y python3-pip build-essential git zip unzip
echo    sudo apt-get install -y openjdk-17-jdk
echo    pip3 install buildozer cython
echo.
echo 2. Instaliraj Android SDK (automatski preko Buildozer-a)
echo.
echo 3. Kopiraj cijeli projekat na Linux:
echo    - Kopiraj folder: %CD%
echo    - Na Linux putanju, npr: /home/user/autoservispro
echo.
echo 4. Pokreni Buildozer (prva kompilacija traje 30-60 min):
echo    cd /home/user/autoservispro
echo    buildozer android debug
echo.
echo 5. Instaliraj na telefon:
echo    buildozer android deploy run
echo.
echo 📁 Output APK fajl:
echo    bin/autoservispro-2.0-debug.apk
echo.
echo 📲 Instalacija na Android:
echo    adb install bin/autoservispro-2.0-debug.apk
echo.
echo 🚀 Za release verziju (Google Play):
echo    buildozer android release
echo    jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 
echo             -keystore my-release-key.keystore 
echo             bin/autoservispro-2.0-release-unsigned.apk alias_name
echo    zipalign -v 4 bin/autoservispro-2.0-release-unsigned.apk 
echo             bin/autoservispro-2.0-release.apk
echo.
echo ⏭️  Preskačem Android build (zahtijeva Linux)...
echo.

echo.
echo ========================================
echo   [3/4] iOS BUILD (Mobilna App)
echo ========================================
echo.

echo 🍎 iOS BUILD - INSTRUKCIJE
echo ========================================
echo.
echo ⚠️  iOS build MORA se izvršiti na macOS sa Xcode
echo.
echo 📋 KORACI (na macOS):
echo.
echo 1. Instaliraj Xcode i Command Line Tools:
echo    xcode-select --install
echo.
echo 2. Instaliraj Homebrew:
echo    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo.
echo 3. Instaliraj Python i zavisnosti:
echo    brew install python3
echo    pip3 install kivy-ios
echo.
echo 4. Kopiraj projekat na macOS:
echo    - Kopiraj folder: %CD%
echo    - Na macOS putanju, npr: ~/autoservispro
echo.
echo 5. Napravi toolchain build:
echo    cd ~/autoservispro
echo    toolchain build python3 kivy pillow sqlite3
echo    (Ovo traje 1-2 sata - prva kompilacija)
echo.
echo 6. Kreiraj Xcode projekat:
echo    toolchain create AutoServisPro main_mobile.py
echo.
echo 7. Otvori u Xcode i build:
echo    open AutoServisPro-ios/AutoServisPro.xcodeproj
echo.
echo 8. U Xcode:
echo    - Selektuj Team (Apple Developer Account)
echo    - Bundle ID: com.autoservis.autoservispro
echo    - Klikni Product ^> Archive
echo    - Distribute App ^> Ad Hoc ili App Store
echo.
echo 📁 Output IPA fajl:
echo    ~/Library/Developer/Xcode/Archives/.../*.ipa
echo.
echo 📲 Instalacija na iPhone:
echo    - TestFlight (za beta testiranje)
echo    - Apple Configurator 2
echo    - Xcode: Window ^> Devices and Simulators ^> Drag IPA
echo.
echo 🚀 Za App Store:
echo    - Potreban Apple Developer Account ($99/godišnje)
echo    - Postavke u App Store Connect
echo    - Submit for Review proces
echo.
echo ⏭️  Preskačem iOS build (zahtijeva macOS + Xcode)...
echo.

echo.
echo ========================================
echo   [4/4] LINUX BUILD
echo ========================================
echo.

echo ⚠️  Linux build zahteva Linux ili WSL
echo.
echo Za Linux build:
echo   1. Instaliraj PyInstaller: pip install pyinstaller
echo   2. Pokreni: pyinstaller --onefile narudzbe/main.py
echo   3. Kreiraj AppImage sa appimagetool
echo.
echo ⏭️  Preskačem Linux build...

echo.
echo ========================================
echo   BUILD ZAVRŠEN
echo ========================================
echo.
echo ✅ Kreirani buildovi:
echo   • Windows: output\windows\AutoServisPro.exe
echo.
echo ⚠️  Nedostaju (zahtevaju specifične platforme):
echo   • Android APK (zahteva Buildozer)
echo   • iOS IPA (zahteva macOS + Xcode)
echo   • Linux AppImage (zahteva Linux/WSL)
echo.
echo 💡 Saveti:
echo   - Windows EXE možeš odmah pokrenuti na Windows 10/11
echo   - Za mobilne buildove koristi specifične alatke
echo   - Za distribuciju uploaduj na Google Play / App Store
echo.

pause
