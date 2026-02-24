# 🔧 AUTO SERVIS PRO - Sistem za rezervaciju termina

Kompletan desktop sistem za upravljanje auto servisom sa:
- Desktop aplikacija (tkinter)
- REST API server (Flask)
- Notification sistem
- Cloud/Server SSH konfiguracija
- PDF printing sa printer postavkama
- Multi-platform builds (Windows/Linux/Android/iOS)

## 📦 INSTALACIJA

### Windows
```cmd
install.bat
```

### Linux/Mac
```bash
chmod +x install.sh
./install.sh
```

## 🚀 POKRETANJE

### Desktop App
```cmd
cd narudzbe
python main.py
```

### API Server
```cmd
cd narudzbe
python api_server.py
```

### Sve odjednom
```bash
bash run_all.sh
```

## 🌐 WEB API

API Server: `http://localhost:5000`

Endpoints:
- `/api/health` - Health check
- `/api/auth/login` - Login
- `/api/auth/register` - Registracija
- `/api/services` - Usluge
- `/api/appointments` - Termini
- `/api/notifications` - Notifikacije

## 🔔 NOTIFICATION SISTEM

Admin može slati notifikacije korisnicima:
- Info poruke
- Promjene termina
- Potvrde
- Broadcast svim korisnicima

## 📱 BUILD-OVI

### Windows EXE
```cmd
build_windows.bat
```

### Linux AppImage
```bash
bash build_linux.sh
```

### Android APK
```bash
bash build_android.sh
```

### iOS IPA
```bash
bash build_ios.sh
```

### Sve platforme
```bash
bash build_all.sh
```

Build fajlovi: `output/`

## 📊 STRUKTURA

```
obd_full-scanner-repair/
├── narudzbe/
│   ├── main.py          # Desktop app
│   ├── database.py       # SQLite baza
│   ├── api_server.py     # REST API
│   ├── pdf_printer.py    # PDF generisanje
│   └── autoservis.db     # SQLite fajl
├── output/               # Build fajlovi
├── logs/                 # API i Desktop logovi
├── .venv/                # Virtual environment
├── requirements.txt      # Dependencies
├── install.bat/sh        # Instalacija
├── build_*.sh/bat        # Build skripte
└── run_all.sh            # Quick start
```

## 👤 DEMO NALOZI

- **Admin**: admin / admin123
- **User**: user / user123

## 🛠️ TEHNOLOGIJE

- Python 3.12
- tkinter (GUI)
- SQLite3 (database)
- Flask (API)
- reportlab (PDF)
- PyInstaller (builds)
- Kivy/Buildozer (Android)
- Kivy-iOS (iOS)

## ☁️ CLOUD SETTINGS

Admin panel ima SSH konfiguraciju za cloud deployment.

## 📄 PDF PRINTING

Konfiguriši printer u postavkama:
- Auto-print opcija
- Izbor printera
- Test print

---

**Auto Servis Pro** © 2026
