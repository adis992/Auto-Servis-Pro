# 🍎 iOS BUILD - Kompletne Instrukcije

## Preduslovi

iOS buildovi **MORAJU** biti kreirani na **macOS** sa instaliranim **Xcode**.
Windows i Linux **NE PODRŽAVAJU** iOS build proces.

**Potrebno**:
- macOS računar (MacBook, iMac, Mac Mini, Mac Studio)
- Xcode 14+ (besplatno iz App Store)
- Apple Developer Account ($99/godišnje za distribuciju)
- Homebrew package manager

---

## Korak 1: Instaliraj Xcode i Command Line Tools

### Instalacija Xcode

```bash
# Preuzmi iz App Store:
# https://apps.apple.com/app/xcode/id497799835

# Ili preko xcode-select:
xcode-select --install

# Prihvati licencu
sudo xcodebuild -license accept
```

**NAPOMENA**: Xcode zauzima **~12-15 GB** disk prostora.

---

## Korak 2: Instaliraj Homebrew

```bash
# Instaliraj Homebrew (macOS package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Provjeri instalaciju
brew --version
```

---

## Korak 3: Instaliraj Python i Zavisnosti

```bash
# Instaliraj Python 3
brew install python@3.11

# Provjeri verziju
python3 --version

# Instaliraj pip ako nije instaliran
python3 -m ensurepip --upgrade
```

---

## Korak 4: Kopiraj Projekat na macOS

**Metoda 1: USB ili External Drive**

```bash
# Kopiraj projekat folder sa USB-a
cd ~/Documents
mkdir AutoServisPro
cp -r /Volumes/USB_DRIVE/obd_full-scanner-repair/* ~/Documents/AutoServisPro/
cd ~/Documents/AutoServisPro
```

**Metoda 2: Cloud (Google Drive, Dropbox, iCloud)**

```bash
# Ako si sinhronizovao preko cloud-a
cd ~/Google\ Drive/AutoServisPro
# ili
cd ~/Dropbox/AutoServisPro
```

**Metoda 3: Git (ako imaš repo)**

```bash
git clone https://github.com/tvoj-username/autoservispro.git
cd autoservispro
```

---

## Korak 5: Instaliraj Kivy-iOS

```bash
# Instaliraj kivy-ios toolchain
pip3 install kivy-ios

# Provjeri instalaciju
toolchain --version
```

---

## Korak 6: Build Dependencies (DUGO TRAJE - 1-2 sata)

**NAPOMENA**: Ovo se radi SAMO JEDNOM i traje 1-2 sata.

```bash
cd ~/Documents/AutoServisPro

# Build Python3 za iOS
toolchain build python3

# Build Kivy framework
toolchain build kivy

# Build SQLite3
toolchain build sqlite3

# Build Pillow (za slike)
toolchain build pillow

# Build sve odjednom (alternativa)
toolchain build python3 kivy sqlite3 pillow
```

**Napomena o greškama**:
- Ako se build zaustavi sa greškom, često pomoći ponovna pokušaja: `toolchain build <package>`
- Neke greške su normalne u build procesu - toolchain će ih riješiti automatski

---

## Korak 7: Kreiraj Xcode Projekat

```bash
# Kreiraj iOS projekat sa main_mobile.py kao entrypoint
toolchain create AutoServisPro ~/Documents/AutoServisPro/main_mobile.py

# Ovo kreira folder: AutoServisPro-ios/
```

**Struktura kreiranog projekta**:
```
AutoServisPro-ios/
├── AutoServisPro.xcodeproj       # Xcode projekat fajl
├── app/                           # Python fajlovi
│   └── main_mobile.py
└── Frameworks/                    # iOS frameworki
    ├── SDL2.framework
    ├── libpython.a
    └── ...
```

---

## Korak 8: Otvori u Xcode

```bash
# Otvori Xcode projekat
open AutoServisPro-ios/AutoServisPro.xcodeproj
```

---

## Korak 9: Konfiguriši Projekat u Xcode

### 9.1 General Settings

1. Klikni na projekat u lijevom sidebar-u (AutoServisPro)
2. U **General** tabu:
   - **Display Name**: Auto Servis Pro
   - **Bundle Identifier**: `com.autoservis.autoservispro`
   - **Version**: 2.0
   - **Build**: 1

### 9.2 Signing & Capabilities

1. Klikni **Signing & Capabilities** tab
2. **Automatically manage signing**: ✓ (chekirati)
3. **Team**: Izaberi svoj Apple Developer Team
   - Ako nemaš team, moraš kreirati Apple Developer Account ($99/godišnje)
   - Za testiranje na vlastitom uređaju, možeš koristiti Free Provisioning (ograničeno na 7 dana)

### 9.3 Deployment Info

1. **Deployment Target**: iOS 13.0 ili viši
2. **Devices**: iPhone i iPad (Universal)
3. **Supported Orientations**:
   - ✓ Portrait
   - (opciono) Landscape

---

## Korak 10: Dodaj App Permissions (Info.plist)

1. U Xcode, otvori `AutoServisPro-ios/Info.plist`
2. Dodaj potrebne permisije (Right-click → Add Row):

```xml
<key>NSPhotoLibraryUsageDescription</key>
<string>Auto Servis treba pristup fotografijama za slike vozila</string>

<key>NSCameraUsageDescription</key>
<string>Auto Servis treba pristup kameri za fotografisanje vozila</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>Auto Servis koristi lokaciju za pronalaženje servisa</string>
```

---

## Korak 11: Build & Test na Simulator

### Pokreni Simulator

1. U Xcode, gore lijevo izaberi **Destination** (target uređaj)
2. Izaberi simulator, npr: **iPhone 14 Pro**
3. Klikni **Play** dugme (▶️) ili pritisnuti **Cmd + R**

**Prvi build može trajati 5-10 minuta.**

### Provjeri logove

Ako se app ne pokrene, provjeri logove:
1. **View** → **Debug Area** → **Show Debug Area**
2. Pogledaj console output za greške

---

## Korak 12: Test na Pravom iPhone/iPad Uređaju

### 12.1 Povezi Uređaj

1. Povezi iPhone/iPad preko USB-a
2. Unlock uređaj
3. Prihvati "Trust This Computer"

### 12.2 Selektuj Uređaj u Xcode

1. U Xcode, gore lijevo izaberi **tvoj uređaj** (npr: "John's iPhone")
2. Klikni **Play** (▶️)

### 12.3 Trust Developer na Uređaju

Ako se app ne pokrene:
1. Na iPhone: **Settings** → **General** → **VPN & Device Management**
2. Klikni na svoj Developer Account
3. Klikni **Trust "[Your Name]"**

---

## Korak 13: Kreiraj IPA Fajl (Za Distribuciju)

### Metoda 1: Archive u Xcode

1. U Xcode: **Product** → **Archive**
   - Ovo može trajati 5-15 minuta
2. Xcode Organizer će se otvoriti sa listom arhiva
3. Izaberi najnoviju arhivu
4. Klikni **Distribute App**

### Izaberi Opciju Distribucije

**Ad Hoc** (za testiranje na specifičnim uređajima):
- Izaberi **Ad Hoc**
- Next → Exportuj IPA
- Instaliraj preko Xcode ili Apple Configurator

**Development** (za sopstveno testiranje):
- Izaberi **Development**
- Next → Exportuj IPA

**App Store** (za objavu na App Store):
- Izaberi **App Store Connect**
- Next → Upload

---

## Korak 14: Instaliraj IPA na iPhone

### Metoda 1: Xcode (Najjednostavnije)

1. Povezi iPhone preko USB-a
2. **Window** → **Devices and Simulators**
3. Izaberi svoj uređaj
4. Drag & Drop IPA fajl na uređaj
5. App će se instalirati automatski

### Metoda 2: Apple Configurator 2

1. Preuzmi Apple Configurator 2 iz App Store
2. Povezi iPhone
3. Drag & Drop IPA na uređaj

### Metoda 3: TestFlight (Beta Testing)

1. Upload na App Store Connect
2. Dodaj testera preko email-a
3. Tester preuzme TestFlight app
4. Instalira app preko TestFlight-a

---

## Korak 15: Publish na App Store (Opciono)

### 15.1 App Store Connect Setup

1. Idi na: https://appstoreconnect.apple.com
2. Klikni **My Apps** → **+** → **New App**
3. Popuni informacije:
   - **Platform**: iOS
   - **Name**: Auto Servis Pro
   - **Primary Language**: Croatian / Serbian
   - **Bundle ID**: com.autoservis.autoservispro
   - **SKU**: AUTOSERVISPRO2024

### 15.2 App Information

- **Category**: Business / Productivity
- **Subtitle**: Rezervacija servisa vozila
- **Description**: (detaljan opis na ijekavici)
- **Keywords**: auto servis, vozilo, rezervacija, termin
- **Support URL**: (tvoj website ili email)
- **Privacy Policy URL**: (obavezno!)

### 15.3 Screenshots

Potrebni screenshot-ovi za različite veličine:
- iPhone 6.7" (iPhone 14 Pro Max)
- iPhone 6.5" (iPhone 11 Pro Max)
- iPhone 5.5" (iPhone 8 Plus)
- iPad Pro 12.9"

**Alat za generisanje screenshot-ova**: Simulator → Cmd + S

### 15.4 Upload Build

1. U Xcode: **Product** → **Archive**
2. **Distribute App** → **App Store Connect**
3. Next → Upload
4. Čekaj 10-30 minuta za processing

### 15.5 Submit for Review

1. U App Store Connect, izaberi build
2. Popuni **Export Compliance** informacije
3. Klikni **Submit for Review**

**Review proces traje 1-7 dana.**

---

## Česti Problemi i Rješenja

### Problem 1: "No Xcode installation found"

```bash
# Rješenje: Postavi Xcode path
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

### Problem 2: "Team is not available"

- **Rješenje**: Dodaj Apple ID u Xcode
  1. **Xcode** → **Preferences** → **Accounts**
  2. Klikni **+** → Dodaj Apple ID
  3. Refresh i selektuj team

### Problem 3: "Provisioning profile error"

```bash
# Očisti derived data
rm -rf ~/Library/Developer/Xcode/DerivedData

# Otvori Xcode ponovo
```

### Problem 4: "Python module not found"

```bash
# Rebuild toolchain
toolchain build python3 --clean
toolchain build kivy --clean
```

### Problem 5: "Signing certificate expired"

1. **Xcode** → **Preferences** → **Accounts**
2. Izaberi account → **Manage Certificates**
3. Obriši stari certificate
4. Klikni **+** → **iOS Development**

---

## Automatizacija (Opciono)

Kreiraj `BUILD_IOS.sh`:

```bash
#!/bin/bash
echo "🍎 Auto Servis Pro - iOS Build"
echo "================================"
echo

cd ~/Documents/AutoServisPro

echo "[1/3] Kreiram Xcode projekat..."
toolchain create AutoServisPro main_mobile.py

echo "[2/3] Otvaram u Xcode..."
open AutoServisPro-ios/AutoServisPro.xcodeproj

echo
echo "✅ Gotovo!"
echo "📱 Sada u Xcode:"
echo "   1. Izaberi Team"
echo "   2. Klikni Play (▶️) za test"
echo "   3. Product → Archive za IPA"
```

Pokreni:
```bash
chmod +x BUILD_IOS.sh
./BUILD_IOS.sh
```

---

## Brzi Start (TL;DR)

```bash
# Instaliraj sve
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.11
pip3 install kivy-ios

# Build toolchain (1-2 sata - samo jednom)
cd ~/Documents/AutoServisPro
toolchain build python3 kivy sqlite3 pillow

# Kreiraj Xcode projekat
toolchain create AutoServisPro main_mobile.py

# Otvori u Xcode
open AutoServisPro-ios/AutoServisPro.xcodeproj

# U Xcode: Izaberi Team → Klikni Play (▶️)
```

---

## Dodatni Resursi

- **Kivy iOS Docs**: https://kivy.org/doc/stable/guide/packaging-ios.html
- **Xcode Help**: https://developer.apple.com/documentation/xcode
- **App Store Guidelines**: https://developer.apple.com/app-store/review/guidelines/
- **TestFlight**: https://developer.apple.com/testflight/

---

## Troškovi

- **Apple Developer Account**: $99/godišnje (obavezno za App Store)
- **Free Provisioning**: Besplatno (7 dana validnosti, samo za testiranje)
- **Xcode**: Besplatno
- **Kivy-iOS**: Besplatno (Open Source)

---

**Napomena**: Prvi build može trajati 1-2 sata zbog kompilacije svih dependency-ja.
Nakon toga, svaki build je **5-10 minuta**.
