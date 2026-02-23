# 🚀 QUICK START - Auto Servis Pro Builds

## 🪟 WINDOWS (Ovaj Računar)

```batch
.\BUILD_WINDOWS_QUICK.bat
```

**Output**: `output\windows\AutoServisPro.exe` ✅

**Distribucija**: Samo kopiraj `.exe` fajl bilo gdje

---

## 📱 ANDROID (Potreban WSL/Linux)

### Setup (jednom)

```bash
# 1. Instaliraj WSL (PowerShell kao Admin)
wsl --install
# Restartuj računar

# 2. U WSL terminalu
cd ~
cp -r /mnt/c/Users/admin11/Desktop/obd_full-scanner-repair autoservispro
cd autoservispro

# 3. Instaliraj dependencies
sudo apt-get update
sudo apt-get install -y python3-pip build-essential git zip unzip openjdk-17-jdk
pip3 install buildozer cython==0.29.36
```

### Build

```bash
# Prva kompilacija (30-60 min - skida Android SDK)
buildozer android debug

# Sljedeće kompilacije (5-10 min)
buildozer android debug
```

**Output**: `bin/autoservispro-2.0-debug.apk` 📱

**Kopiraj na Windows**:
```bash
cp bin/autoservispro-2.0-debug.apk /mnt/c/Users/admin11/Downloads/
```

**Instalacija na telefon**:
1. Kopiraj APK na telefon
2. Settings → Security → Unknown Sources → Enable
3. Otvori APK → Install

---

## 🍎 iOS (Potreban macOS)

### Setup (jednom)

```bash
# 1. Instaliraj alate
xcode-select --install
brew install python@3.11
pip3 install kivy-ios

# 2. Kopiraj projekat na macOS
cd ~/Documents
cp -r /putanja/do/projekta autoservispro
cd autoservispro

# 3. Build toolchain (1-2 sata)
toolchain build python3 kivy sqlite3 pillow
```

### Build

```bash
# Kreiraj Xcode projekat
toolchain create AutoServisPro main_mobile.py

# Otvori u Xcode
open AutoServisPro-ios/AutoServisPro.xcodeproj

# U Xcode:
# 1. Signing & Capabilities → Selektuj Team
# 2. Play (▶️) za test
# 3. Product → Archive za IPA
```

**Output**: `.ipa` fajl preko Xcode Organizer 🍎

---

## 📚 DETALJI

- **Windows**: [BUILD_GUIDE.md](BUILD_GUIDE.md)
- **Android**: [BUILD_ANDROID_INSTRUKCIJE.md](BUILD_ANDROID_INSTRUKCIJE.md)
- **iOS**: [BUILD_IOS_INSTRUKCIJE.md](BUILD_IOS_INSTRUKCIJE.md)

---

## 🎯 DEFAULT KORISNICI

```
Admin: admin / admin123
User:  user / user123
```

---

**Pro tip**: Windows build radi ODMAH na ovom računaru! ✅
