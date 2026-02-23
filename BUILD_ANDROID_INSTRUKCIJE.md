# 📱 ANDROID BUILD - Kompletne Instrukcije

## Preduslovi

Android buildovi **MORAJU** biti kreirani na **Linux** ili **WSL** (Windows Subsystem for Linux).
Windows direktno **NE PODRŽAVA** Android build proces.

---

## Opcija 1: WSL (Windows Subsystem for Linux) - PREPORUČENO

### Korak 1: Instaliraj WSL

```powershell
# U PowerShell-u kao Administrator:
wsl --install

# Restartuj računar
# Nakon restarta, otvori WSL terminal
```

### Korak 2: Kopiraj Projekat u WSL

```bash
# U WSL terminalu:
cd ~
mkdir autoservispro
```

```powershell
# U Windows PowerShell-u:
# Kopiraj cijeli projekat u WSL
cp -r "C:\Users\admin11\Desktop\obd_full-scanner-repair\*" \\wsl$\Ubuntu\home\<your-username>\autoservispro\
```

Ili jednostavno:
```bash
# U WSL:
cp -r /mnt/c/Users/admin11/Desktop/obd_full-scanner-repair/* ~/autoservispro/
cd ~/autoservispro
```

### Korak 3: Instaliraj Zavisnosti (WSL)

```bash
# Update sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instaliraj build alate
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    ccache \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev

# Instaliraj Buildozer i Cython
pip3 install --upgrade pip
pip3 install buildozer
pip3 install cython==0.29.36
```

### Korak 4: Inicijalizuj Buildozer (Prva kompilacija - 30-60 minuta)

```bash
cd ~/autoservispro

# Prva kompilacija će skinuti Android SDK/NDK (velika količina podataka)
# Ovo MORA biti urađeno samo jednom
buildozer android debug

# Ako se desi greška sa permissions:
chmod +x ~/.buildozer -R
```

**NAPOMENA**: Prva kompilacija traje **30-60 minuta** i preuzima **~3-4 GB** podataka (Android SDK, NDK, Python za Android).

### Korak 5: Kreiraj APK

```bash
# Nakon uspješnog initialnog build-a, svaki naredi build je brži (5-10 min)
buildozer android debug

# APK će biti u:
# bin/autoservispro-2.0-debug.apk
```

### Korak 6: Kopiraj APK na Windows

```bash
# Kopiraj APK iz WSL u Windows Downloads folder
cp bin/autoservispro-2.0-debug.apk /mnt/c/Users/admin11/Downloads/

# Ili samo prikaži putanju
echo "APK lokacija: $(realpath bin/autoservispro-2.0-debug.apk)"
```

### Korak 7: Instaliraj na Android Telefon

**Metoda 1: Preko USB (ADB)**

```bash
# Instaliraj ADB tools
sudo apt-get install -y adb

# Omogući USB Debugging na telefonu:
# Settings → About Phone → Tap "Build Number" 7x → Developer Options → USB Debugging

# Povezi telefon preko USB-a

# Provjeri da li je telefon prepoznat
adb devices

# Instaliraj APK
adb install -r bin/autoservispro-2.0-debug.apk

# Ili direktno pokreni:
buildozer android deploy run
```

**Metoda 2: Prenos fajla (Manual)**

1. Kopiraj `autoservispro-2.0-debug.apk` na telefon (Email, Google Drive, USB)
2. Na telefonu: Omogući "Install from Unknown Sources"
   - Settings → Security → Unknown Sources → Enable
3. Otvori APK fajl na telefonu
4. Klikni "Install"

---

## Opcija 2: Native Linux (Ubuntu/Debian)

Ako imaš Linux računar, koraci su isti kao WSL **OSIM** kopiranja fajlova:

```bash
# Kopiraj projekat (ako je na eksternom disku ili USB-u)
cd ~
mkdir autoservispro
cp -r /putanja/do/projekta/* ~/autoservispro/
cd ~/autoservispro

# Nastavi sa koracima 3-7 iz WSL sekcije
```

---

## Opcija 3: Docker (Napredni)

```bash
# Koristi Docker sa Android build okruženjem (brže, izolovanije)
docker pull buildozer/buildozer

# Pokreni build
docker run --rm -v "$(pwd)":/app buildozer/buildozer android debug
```

---

## Česti Problemi i Rješenja

### Problem 1: "Command 'buildozer' not found"

```bash
# Rješenje: Dodaj Python bin u PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Problem 2: "Java not found"

```bash
# Instalira Java JDK
sudo apt-get install openjdk-17-jdk

# Postavi JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc
```

### Problem 3: "Permission denied"

```bash
# Daj permissions Buildozer folderu
chmod -R +x ~/.buildozer
chmod +x ~/.local/bin/buildozer
```

### Problem 4: "Cython version mismatch"

```bash
# Instaliraj tačnu verziju Cython-a
pip3 uninstall cython
pip3 install cython==0.29.36
```

### Problem 5: "Out of space"

```bash
# Buildozer može zauzeti 5-10 GB
# Očisti stare buildove:
buildozer android clean

# Očisti potpuno:
rm -rf ~/.buildozer
```

---

## Release Build (Za Google Play)

### Korak 1: Kreiraj Keystore

```bash
keytool -genkey -v -keystore autoservis-release.keystore -alias autoservis -keyalg RSA -keysize 2048 -validity 10000

# Čuvaj keystore fajl i lozinku SIGURNO!
```

### Korak 2: Build Release APK

```bash
buildozer android release
```

### Korak 3: Potpiši APK

```bash
jarsigner -verbose \
    -sigalg SHA256withRSA \
    -digestalg SHA-256 \
    -keystore autoservis-release.keystore \
    bin/autoservispro-2.0-release-unsigned.apk \
    autoservis
```

### Korak 4: Zipalign

```bash
# Preuzmi zipalign (dio Android build tools-a)
~/.buildozer/android/platform/android-sdk/build-tools/*/zipalign -v 4 \
    bin/autoservispro-2.0-release-unsigned.apk \
    bin/autoservispro-2.0-release.apk
```

### Korak 5: Provjeri potpis

```bash
jarsigner -verify -verbose -certs bin/autoservispro-2.0-release.apk
```

---

## Google Play Upload

1. **Google Play Console**: https://play.google.com/console
2. **Create App** → Popuni informacije
3. **Upload APK** ili **Android App Bundle (AAB)**
4. **Internal Testing** → Upload APK
5. **Review & Release**

**NAPOMENA**: Google Play naplaćuje **$25** jednom za developer account.

---

## Testiranje

```bash
# Logovi sa telefona u real-time
adb logcat -s "python:* AutoServisPro:*"

# Očisti app sa telefona
adb uninstall com.autoservis.autoservispro

# Reinstaliraj
adb install -r bin/autoservispro-2.0-debug.apk
```

---

## Automatizacija (Opciono)

Kreiraj `BUILD_ANDROID.sh` skriptu:

```bash
#!/bin/bash
echo "🤖 Auto Servis Pro - Android Build"
echo "===================================="
echo

cd ~/autoservispro

echo "[1/3] Čistim stare buildove..."
buildozer android clean

echo "[2/3] Kreiram novi APK..."
buildozer android debug

echo "[3/3] Kopiranje na Windows..."
cp bin/autoservispro-2.0-debug.apk /mnt/c/Users/admin11/Downloads/

echo
echo "✅ Gotovo!"
echo "📦 APK: C:\\Users\\admin11\\Downloads\\autoservispro-2.0-debug.apk"
```

Pokreni sa:
```bash
chmod +x BUILD_ANDROID.sh
./BUILD_ANDROID.sh
```

---

## Brzi Start (TL;DR)

```bash
# WSL: Instaliraj i pokreni
wsl --install
# Restartuj računar

# U WSL terminalu:
cd ~
cp -r /mnt/c/Users/admin11/Desktop/obd_full-scanner-repair autoservispro
cd autoservispro

# Instaliraj sve odjednom (može trajati 10-20 min)
sudo apt-get update && sudo apt-get install -y python3-pip build-essential git zip unzip openjdk-17-jdk && pip3 install buildozer cython==0.29.36

# Build (prva kompilacija 30-60 min, sljedeće 5-10 min)
buildozer android debug

# Kopiraj na Windows
cp bin/autoservispro-2.0-debug.apk /mnt/c/Users/admin11/Downloads/

# Install na telefon
adb install -r bin/autoservispro-2.0-debug.apk
```

---

## Podrška

- **Buildozer Docs**: https://buildozer.readthedocs.io/
- **Kivy Android Docs**: https://kivy.org/doc/stable/guide/android.html
- **Stack Overflow**: Tag `buildozer` ili `kivy-android`

---

**Napomena**: Kompletna build chain (SDK + NDK + Python for Android) zauzima **5-10 GB** disk prostora.
