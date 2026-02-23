# 🚀 AUTO SERVIS PRO - BUILD INSTRUKCIJE

Kompletne instrukcije za kreiranje instalabilnih fajlova za sve platforme.

---

## 📋 PREGLED

| Platforma | Tip Fajla | Gdje Build-ovati | Trajanje | Veličina |
|-----------|-----------|------------------|----------|----------|
| **Windows** | `.exe` | Windows | 2-5 min | ~30-50 MB |
| **Android** | `.apk` | Linux/WSL | 30-60 min (prvi put), 5-10 min (sljedeći) | ~20-30 MB |
| **iOS** | `.ipa` | macOS + Xcode | 1-2 sata (prvi put), 5-10 min (sljedeći) | ~15-25 MB |

---

## 🪟 WINDOWS BUILD (EXE)

### ✅ Brza Metoda

```batch
.\BUILD_WINDOWS_QUICK.bat
```

**Output**: `output\windows\AutoServisPro.exe`

### 📋 Manuelna Metoda

```batch
# 1. Provjeri Python environment
.venv\bin\python.exe --version

# 2. Instaliraj PyInstaller
.venv\bin\python.exe -m pip install pyinstaller

# 3. Build
.venv\bin\python.exe -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "AutoServisPro" ^
    --add-data "narudzbe;narudzbe" ^
    --distpath output\windows ^
    narudzbe\main.py
```

### 📦 Distribucija

- Kopiraj `AutoServisPro.exe` bilo gdje
- Ne zahtijeva instalaciju Python-a
- Sve dependencies su uključene
- Baza se kreira automatski pri prvom pokretanju

### 💾 Distribucija sa Bazom

Ako želiš da distribuiraš sa popunjenom bazom:
```batch
# Kopiraj zajedno:
AutoServisPro.exe
autoservice.db
```

---

## 📱 ANDROID BUILD (APK)

### ⚠️ VAŽNO

Android buildovi **MORAJU** biti kreirani na **Linux** ili **WSL**.

### ✅ Preporučena Metoda: WSL (Windows Subsystem for Linux)

#### Korak 1: Instaliraj WSL

```powershell
# U PowerShell-u kao Administrator
wsl --install

# Restartuj računar
```

#### Korak 2: Kopiraj Projekat u WSL

```bash
# U WSL terminalu
cd ~
cp -r /mnt/c/Users/admin11/Desktop/obd_full-scanner-repair autoservispro
cd autoservispro
```

#### Korak 3: Instaliraj Zavisnosti (jednom)

```bash
# Update sistema
sudo apt-get update

# Instaliraj sve potrebno
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    zip \
    unzip \
    openjdk-17-jdk

# Instaliraj Buildozer
pip3 install buildozer cython==0.29.36
```

#### Korak 4: Build APK

```bash
# Prva kompilacija (30-60 minuta - skida Android SDK/NDK)
buildozer android debug

# Sljedeće kompilacije (5-10 minuta)
buildozer android debug
```

**Output**: `bin/autoservispro-2.0-debug.apk`

#### Korak 5: Kopiraj na Windows

```bash
# Kopiraj APK u Windows Downloads
cp bin/autoservispro-2.0-debug.apk /mnt/c/Users/admin11/Downloads/
```

#### Korak 6: Instaliraj na Telefon

**Metoda 1: USB + ADB**

```bash
# Instaliraj ADB
sudo apt-get install -y adb

# Omogući USB Debugging na telefonu
# Settings → About → Build Number (tap 7x) → Developer Options → USB Debugging

# Povezi telefon i instaliraj
adb install -r bin/autoservispro-2.0-debug.apk
```

**Metoda 2: Manual Transfer**

1. Kopiraj APK na telefon (Email, Drive, USB)
2. Settings → Security → Unknown Sources → Enable
3. Otvori APK na telefonu → Install

### 📄 Detaljne Instrukcije

Sve detalje, troubleshooting i release build instrukcije vidi u:

📖 **[BUILD_ANDROID_INSTRUKCIJE.md](BUILD_ANDROID_INSTRUKCIJE.md)**

---

## 🍎 iOS BUILD (IPA)

### ⚠️ VAŽNO

iOS buildovi **MORAJU** biti kreirani na **macOS** sa **Xcode**.

### ✅ Preduslovi

- macOS računar
- Xcode 14+ (App Store)
- Apple Developer Account ($99/godišnje za distribuciju)

### 📋 Koraci

#### Korak 1: Instaliraj Alate

```bash
# Command Line Tools
xcode-select --install

# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python i Kivy-iOS
brew install python@3.11
pip3 install kivy-ios
```

#### Korak 2: Kopiraj Projekat

```bash
# Kopiraj na macOS (USB, Cloud, Git)
cd ~/Documents
cp -r /putanja/do/projekta autoservispro
cd autoservispro
```

#### Korak 3: Build Toolchain (jednom, 1-2 sata)

```bash
# Build iOS dependencies
toolchain build python3 kivy sqlite3 pillow
```

#### Korak 4: Kreiraj Xcode Projekat

```bash
# Kreiraj iOS projekat
toolchain create AutoServisPro main_mobile.py

# Otvori u Xcode
open AutoServisPro-ios/AutoServisPro.xcodeproj
```

#### Korak 5: Konfiguriši i Build

1. **U Xcode**:
   - Signing & Capabilities → Selektuj Team
   - General → Bundle ID: `com.autoservis.autoservispro`
2. **Test na Simulator**:
   - Izaberi iPhone simulator gore → Klikni Play (▶️)
3. **Archive za IPA**:
   - Product → Archive
   - Distribute App → Ad Hoc / App Store

#### Korak 6: Instaliraj na iPhone

**Metoda 1: Xcode**
1. Window → Devices and Simulators
2. Drag & Drop IPA na uređaj

**Metoda 2: TestFlight**
1. Upload na App Store Connect
2. Dodaj testera preko email-a
3. Instaliraj preko TestFlight app-a

### 📄 Detaljne Instrukcije

Sve detalje, Xcode setup, App Store submission vidi u:

📖 **[BUILD_IOS_INSTRUKCIJE.md](BUILD_IOS_INSTRUKCIJE.md)**

---

## 🎯 BRZI START (Sve Platforme)

### Windows (na Windows računaru)

```batch
.\BUILD_WINDOWS_QUICK.bat
```

### Android (na WSL/Linux)

```bash
# Jednom: Instalacija (10-20 min)
sudo apt-get update && sudo apt-get install -y python3-pip build-essential git zip unzip openjdk-17-jdk
pip3 install buildozer cython==0.29.36

# Build (prvi put 30-60 min, sljedeći 5-10 min)
buildozer android debug

# Kopiraj na Windows
cp bin/autoservispro-2.0-debug.apk /mnt/c/Users/admin11/Downloads/
```

### iOS (na macOS)

```bash
# Jednom: Instalacija (1-2 sata)
xcode-select --install
brew install python@3.11
pip3 install kivy-ios
toolchain build python3 kivy sqlite3 pillow

# Build (5-10 min)
toolchain create AutoServisPro main_mobile.py
open AutoServisPro-ios/AutoServisPro.xcodeproj
# U Xcode: Play (▶️) ili Archive
```

---

## 📦 DISTRIBUCIJA

### Windows EXE

**Desktop Aplikacija**
- Jednostavno kopiraj `.exe` fajl
- Ne zahtijeva instalaciju
- Radi na Windows 10/11

### Android APK

**Debug APK** (za testiranje)
- Direktna instalacija na telefon
- Enable "Unknown Sources"

**Release APK** (za distribuciju)
- Potpisani APK za širu distribuciju
- Google Play Store upload

### iOS IPA

**Ad Hoc** (za testiranje)
- Instalacija preko Xcode ili Apple Configurator
- Ograničen broj uređaja (100)

**App Store** (za javnu distribuciju)
- Potreban Apple Developer Account ($99/godišnje)
- Review proces 1-7 dana

---

## 🔧 TROUBLESHOOTING

### Windows Build Fails

```batch
# Problem: PyInstaller ne radi sa MSYS2 Python
# Rješenje: Instaliraj normalni Windows Python

# 1. Preuzmi sa python.org (Python 3.11 ili 3.12)
# 2. Kreiraj novi venv:
python -m venv venv

# 3. Instaliraj dependencies:
venv\Scripts\pip install tkinter tkcalendar babel pyinstaller

# 4. Build ponovo:
venv\Scripts\python -m PyInstaller ...
```

### Android Build Fails

```bash
# Problem: Buildozer not found
# Rješenje:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Problem: Java not found
# Rješenje:
sudo apt-get install openjdk-17-jdk

# Problem: Permission denied
# Rješenje:
chmod -R +x ~/.buildozer
```

### iOS Build Fails

```bash
# Problem: No Xcode found
# Rješenje:
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer

# Problem: Provisioning profile error
# Rješenje:
rm -rf ~/Library/Developer/Xcode/DerivedData
# Restartuj Xcode
```

---

## 🧪 TESTIRANJE

### Default Korisnici

Svi build-ovi dolaze sa ovim korisnicima:

```
👤 Admin:
   Username: admin
   Password: admin123
   Email: admin@autoservis.com

👤 Test User:
   Username: user
   Password: user123
   Email: user@test.com
```

### Test Scenarios

1. **Login** → Admin/User credentials
2. **Kreiranje Termina** → Odaberi vozilo, uslugu, datum
3. **Dodavanje Vozila** → Unesi registraciju, marku, model
4. **Pretraga** → Pretraži termine, korisnike, usluge
5. **Profil** → Izmijeni korisničke podatke

---

## 📊 COMPARISON

| Feature | Windows EXE | Android APK | iOS IPA |
|---------|-------------|-------------|---------|
| **Backend** | Tkinter | Kivy | Kivy |
| **Database** | SQLite (local) | SQLite (local) | SQLite (local) |
| **Build Time** | 2-5 min | 30-60 min (first), 5-10 min | 1-2h (first), 5-10 min |
| **Build Platform** | Windows | Linux/WSL | macOS |
| **Distribucija** | Copy `.exe` | Install APK | TestFlight / App Store |
| **Cost** | Free | Free | $99/year (for App Store) |

---

## 📞 PODRŠKA

- **GitHub Issues**: [link ako imaš repo]
- **Email**: [tvoj email]
- **Documentation**:
  - Android: [BUILD_ANDROID_INSTRUKCIJE.md](BUILD_ANDROID_INSTRUKCIJE.md)
  - iOS: [BUILD_IOS_INSTRUKCIJE.md](BUILD_IOS_INSTRUKCIJE.md)

---

## 📝 CHANGELOG

### v2.0 (Latest)
- ✅ 30 servisa sa ijekavica opisima
- ✅ 12 tipova vozila (sistemski + custom)
- ✅ Napredna pretraga za sve entitete
- ✅ 2 default korisnika (admin + test)
- ✅ Mobile app support (Android + iOS)
- ✅ Build sistema za sve platforme

---

## 🎉 ZAKLJUČAK

**Windows Build** → Najbrži i najjednostavniji ✅

**Android Build** → Zahtijeva WSL ali radi odlično 📱

**iOS Build** → Zahtijeva macOS ali professional rezultat 🍎

---

**Happy Building! 🚀**
