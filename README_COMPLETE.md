# 🚗 Auto Servis Pro - Kompletna Aplikacija

## 📱 Pregled

**Auto Servis Pro** je kompletna aplikacija za upravljanje auto servisom sa:
- ✅ **Desktop aplikacija** (Windows/Linux) - Tkinter GUI
- ✅ **Web interfejs** (Browser) - Responzivni HTML/CSS/JS
- 🔄 **API Server** (REST API za mobilne appove)
- 📦 **Buildovi za iOS i Android** (u pripremi)
- 🔍 **Napredna pretraga** - Pretraži sve entitete
- 🚙 **Tipovi vozila** - 12 predefinisanih + custom tipovi
- 📊 **30+ Default servisa** - Detaljni opisi na ijekavici

---

## 🚀 Brzo Pokretanje

### 1⃣ Desktop + Web (BEZ Flask-a)

```bash
# Otvori terminal u folderu projekta
cd C:\Users\admin11\Desktop\obd_full-scanner-repair

# Pokreni sve odjednom
.\START_APP.bat
```

**Šta se pokreće:**
- 🖥️ **Desktop App** - Tkinter GUI aplikacija
- 🌐 **Web Interface** - http://localhost:8000
- ⚠️ **API Server** - Preskočen (Flask nije instaliran)

**Login opcije:**
- **Admin:** `admin` / `admin123`
- **Test User:** `user` / `user123`

---

## 🎯 Funkcionalnosti

### Desktop Aplikacija
- ✅ Login/Registracija korisnika
- ✅ **Admin Panel:**
  - 📅 **Termini** - Kreiranje, uređivanje, brisanje, pretraga
  - 👥 **Korisnici** - Upravljanje korisnicima, pretraga po imenu/emailu
  - 🔧 **Usluge** - 30+ default servisa, cjene, trajanje, kategorije
  - 🚙 **Tipovi vozila** - 12 default + mogućnost kreiranja custom tipova
  - 🔔 **Notifikacije** - Slanje poruka korisnicima, broadcast
  - ⚙️ **Postavke** - SSH, Cloud backup, Printer
  - 📊 **Izvještaji** - Dnevni, mjesečni
  - 🔍 **Pretraga** - Napredna pretraga svih entiteta
- ✅ **User Panel:**
  - 📝 **Rezervacija termina** - Odaberi uslugu i datum
  - 📋 **Moji termini** - Pregled i upravljanje terminima
  - 🔔 **Notifikacije** - Primaj poruke od servisa
  - 🚗 **Vozila** - Dodaj vozila po tipu
  - 👤 **Profil** - Uredi svoje podatke

### 🚙 Tipovi Vozila (Default)

1. **Osobno vozilo** 🚗 - Standardni automobili sa 4-5 sjedišta
2. **SUV / Terenac** 🚙 - Sportsko-terenska vozila
3. **Kombi / Karavan** 🚐 - Vozila sa produženim prtljažnikom
4. **Pick-up** 🛻 - Teretna vozila sa otvorenim sandukom
5. **Kamion** 🚚 - Teška teretna vozila
6. **Motocikl** 🏍️ - Dvotočkaša - motori, skuteri, kvadovi
7. **Prikolica** 🚜 - Priključna vozila bez sopstvenog pogona
8. **Van / Dostavno** 🚐 - Komercijalna vozila za dostavu
9. **Sportsko vozilo** 🏎️ - Visokoperformansni automobili
10. **Luksuzno vozilo** 💎 - Premium vozila visokog cjenovnog ranga
11. **Hibrid / Električno** ⚡ - Ekološka vozila
12. **Oldtimer / Klasik** 🕰️ - Istorijska vozila starija od 30 godina

**➕ Mogućnost kreiranja custom tipova vozila**

### 🔧 Default Usluge (30+ Servisa)

#### Održavanje
- **Redovan servis - Mali** (80 KM, 60 min) - Zamjena ulja i filtera, provjera svih tekućnosti
- **Redovan servis - Veliki** (150 KM, 120 min) - Kompletno održavanje sa dijagnostikom
- **Zamjena ulja i filtera** (60 KM, 40 min) - Sintetsko ulje prema specifikacijama

#### Dijagnostika
- **Dijagnostika motora** (50 KM, 60 min) - Kompjuterska dijagnostika svih sistema

#### Kočioni Sistem
- **Zamjena kočionih pločica - prednje** (120 KM, 90 min)
- **Zamjena kočionih pločica - zadnje** (100 KM, 100 min)
- **Zamjena kočionih diskova** (250 KM, 150 min) - Sa pločicama

#### Klima
- **Punjenje klima uređaja** (70 KM, 75 min) - R134a ili R1234yf gas
- **Servis klima uređaja - kompletno** (150 KM, 140 min) - Sa dezinfekcijom ozonom

#### Ovjes
- **Zamjena amortizera - komplet** (400 KM, 240 min)
- **Geometrija trap traka - 3D** (50 KM, 75 min)

#### Gume
- **Balansiranje guma - komplet** (30 KM, 45 min)
- **Sezonska zamjena guma** (40 KM, 60 min)
- **Vulkaniziranje** (25 KM, 45 min)

#### Motor
- **Zamjena zubatog remena** (350 KM, 360 min) - KRITIČNO VAŽNA USLUGA!
- **Zamjena svjećica** (80 KM, 75 min)
- **Zamjena EGR ventila** (180 KM, 120 min)
- **Zamjena turbine** (800 KM, 420 min)

#### Električni Sistem
- **Zamjena autolampi** (30 KM, 40 min)
- **Punjenje/zamjena akumulatora** (150 KM, 60 min)

#### Transmisija
- **Zamjena kvačila - komplet** (500 KM, 480 min)
- **Servis automatskog mjenjača** (200 KM, 180 min)

#### Auto Detailing
- **Detailing - unutrašnje pranje** (100 KM, 180 min)
- **Detailing - kompletno** (250 KM, 360 min) - Premium usluga!
- **Poliranje farova** (70 KM, 90 min)

#### Ostalo
- **Čišćenje DPF filtera** (200 KM, 240 min) - Dizel vozila
- **Zamjena izduvnog sistema** (200 KM, 180 min)
- **Zamjena letve volana** (450 KM, 300 min)

### 🔍 Napredna Pretraga

Desktop aplikacija podržava pretragu:
- **Termini** - Po registraciji, marki, modelu, statusu, korisniku
- **Korisnici** - Po imenu, emailu, usernameu, telefonu
- **Usluge** - Po nazivu, kategoriji, opisu
- **Vozila** - Po registraciji, marki, modelu, VIN broju

### Web Interfejs
- ✅ Responzivni dizajn
- ✅ Login/Registracija
- ✅ Dashboard
- ⚠️ Funkcije povezane sa API-jem (zahtijeva Flask)

### API Server (ako je Flask instaliran)
- `POST /api/auth/login` - Prijava
- `POST /api/auth/register` - Registracija
- `GET /api/appointments` - Lista termina
- `POST /api/appointments` - Kreiranje termina
- `GET /api/notifications` - Notifikacije
- `POST /api/notifications/broadcast` - Slanje poruka (admin)
- `GET /api/services` - Sve usluge
- `GET /api/vehicle-types` - Tipovi vozila
- ... i još 15+ endpointa

---

## 📁 Struktura Projekta

```
obd_full-scanner-repair/
├── narudzbe/
│   ├── main.py              # Desktop GUI aplikacija (2353 linija)
│   ├── api_server.py        # Flask REST API server (691 linija)
│   ├── database.py          # SQLite database layer (1000+ linija)
│   ├── pdf_printer.py       # PDF generator (disabled)
│   ├── web_server.py        # Simple HTTP server za web UI
│   └── web/
│       └── index.html       # Web interfejs
├── .venv/                   # Python virtual environment
├── START_APP.bat            # Pokreće sve (Desktop + Web)
├── BUILD_ALL.bat            # Kreira buildove za sve platforme
├── RUN_APP.ps1              # PowerShell launcher
├── install.bat              # Instalaciona skripta (broken sa MSYS2)
└── README_COMPLETE.md       # Ova dokumentacija
```

---

## 📦 Buildovi za Sve Platforme

### Windows EXE

```bash
.\BUILD_ALL.bat
```

**Output:** `output/windows/AutoServisPro.exe`

### Android APK

**Zahtevi:**
- Linux/macOS/WSL
- Buildozer: `pip install buildozer`
- Android SDK

```bash
buildozer android debug
```

### iOS IPA

**Zahtevi:**
- macOS
- Xcode
- Kivy-iOS: `pip install kivy-ios`

```bash
toolchain build kivy
toolchain create <app_name> <app_directory>
```

### Linux AppImage

**Zahtevi:**
- Linux ili WSL
- PyInstaller: `pip install pyinstaller`

```bash
pyinstaller --onefile narudzbe/main.py
# Zatim koristi appimagetool za kreiranje AppImage
```

---

## 🔧 Rešavanje Problema

### Problem 1: Flask se ne instalira

**Error:** `Building wheel for MarkupSafe failed`

**Uzrok:** MSYS2 Python nema C compiler

**Rešenje:**
1. Instaliraj normalni Windows Python sa python.org
2. Kreiraj novi venv: `py -m venv .venv`
3. Aktiviraj: `.venv\Scripts\activate`
4. Instaliraj: `pip install Flask flask-cors`

### Problem 2: Desktop app se ne pokreće

**Error:** `AttributeError: 'AutoServiceDB' object has no attribute 'login_user'`

**Rešenje:** ✅ ISPRAVLJENO - Koristi `verify_user` umesto `login_user`

### Problem 3: tkcalendar nije instaliran

**Error:** `ModuleNotFoundError: No module named 'tkcalendar'`

**Rešenje:**
```bash
.\.venv\bin\python.exe -m pip install tkcalendar
```

### Problem 4: Port 8000 zauzet

**Rešenje:**
```bash
# Pronađi proces
netstat -ano | findstr :8000

# Ugasi proces
taskkill /PID <PID> /F
```

---

## 🌐 Portovi

- **8000** - Web interfejs (http://localhost:8000)
- **7000** - API server (http://localhost:7000) - ako je Flask instaliran

---

## 🎨 UI Dizajn

### Desktop App
- **Tema:** Dark mode sa modernim bojama
- **Boje:** #2c3e50 (primary), #27ae60 (success), #e74c3c (danger)
- **Framework:** tkinter

### Web Interface
- **Tema:** Gradient purple/blue
- **Responzivan:** Da (mobile-friendly)
- **Framework:** Vanilla HTML/CSS/JS

---

## 📊 Baza Podataka

**SQLite3** - `autoservis.db`

**Tabele:**
- `users` - Korisnici (admin/user role) - **2 default usera**
- `services` - Usluge servisa - **30+ default servisa**
- `vehicles` - Vozila korisnika
- `vehicle_types` - Tipovi vozila - **12 default tipova + custom**
- `appointments` - Termini
- `notifications` - Notifikacije
- `settings` - Sistemske postavke

**Default Korisnici:**
- **Admin:** username=`admin`, password=`admin123`, email=`admin@autoservis.com`
- **Test User:** username=`user`, password=`user123`, email=`user@test.com`

**Default Tipovi Vozila:**
- 12 predefinisanih tipova (sistemski, ne mogu se obrisati)
- Korisnici mogu kreirati svoje custom tipove

**Default Usluge:**
- 30+ detaljno opisanih servisa
- Kategorije: Održavanje, Dijagnostika, Kočioni sistem, Klima, Ovjes, Gume, Motor, Električni sistem, Transmisija, Auto detailing, Ostalo
- Svi opisi na ijekavici

---

## 🔐 Bezbednost

- ✅ Password hashing (hashlib SHA256)
- ✅ Session tokeni za API
- ✅ Role-based access control (admin/user)
- ⚠️ CORS omogućen (samo za dev)
- ⚠️ Za produkciju dodaj HTTPS

---

## 🚧 U Razvoju

- [ ] PDF izvještaji (zahteva reportlab + C compiler)
- [ ] Android APK build
- [ ] iOS IPA build
- [ ] Linux AppImage build
- [ ] Email notifikacije
- [ ] SMS notifikacije
- [ ] Online plaćanje

---

## 📞 Podrška

**Problem sa instalacijom?**
1. Proveri Python verziju: `.\.venv\bin\python.exe --version`
2. Proveri dependencies: `.\.venv\bin\python.exe -m pip list`
3. Reinstaliraj venv: `Remove-Item .venv -Recurse -Force; python -m venv .venv`

---

## 📝 Licence

**Open Source** - Slobodno za upotrebu i modifikaciju

---

## 🎉 Status

✅ **Desktop App** - RADI!  
✅ **Web Interface** - RADI!  
✅ **30+ Default Servisa** - Detaljni opisi na ijekavici  
✅ **12 Tipova Vozila** - + Custom tipovi  
✅ **Napredna Pretraga** - Svi entiteti  
✅ **2 Default Usera** - admin + test user  
⚠️ **API Server** - Zahtijeva Flask (Python ne-MSYS2)  
🔄 **Android/iOS** - U pripremi  

**Poslednje ažuriranje:** Februar 2026

---

## 🆕 Novosti

### Verzija 2.0 (Februar 2026)

✅ **Dodato 30+ detaljnih servisa**  
- Svi opisi prevedeni na ijekavicu  
- Kategorisani po tipu usluge  
- Realni timingovi i cijene  

✅ **12 Default tipova vozila**  
- Mogućnost kreiranja custom tipova  
- Ikone za svaki tip  
- Sistemski tipovi zaštićeni od brisanja  

✅ **Napredna pretraga**  
- Pretraga termina po vozilu/korisniku  
- Pretraga korisnika po svim poljima  
- Pretraga usluga po kategoriji/nazivu  
- Pretraga vozila po registraciji/marki  

✅ **Default test user**  
- Username: `user`  
- Password: `user123`  
- Za testiranje aplikacije  

✅ **Grupisanje po kategorijama**  
- Usluge grupisane po tipovima  
- Vozila grupisana po tipovima  
- Termini grupisani po statusu  

✅ **Ijekavica**  
- Svi tekstovi na ijekavskom standardu  
- Profesionalni opisi servisa
