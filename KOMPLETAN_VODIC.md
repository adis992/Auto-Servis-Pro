# 🚗 Auto Servis Pro - Kompletan Web + Desktop Sistem

Profesionalni sistem za upravljanje auto servisom sa web panelom i desktop aplikacijom.

## ✨ Glavne Karakteristike

### 👥 Za Korisnike
- ✅ Registracija i prijava
- ✅ Dodavanje i upravljanje vozilima
- ✅ Kreiranje servisnih narudžbi
- ✅ Pregled dostupnih usluga
- ✅ Notifikacije o stanju narudžbi
- ✅ Upravljanje profilom

### ⚙️ Za Administratore
- ✅ Upravljanje uslugama (Add/Edit/Delete)
- ✅ Pregled svih narudžbi
- ✅ Statistika i izvještaji
- ✅ Upravljanje korisnicima
- ✅ Broadcast notifikacija

## 🏗️ Arhitektura Projekta

```
Auto Servis Pro/
├── narudzbe/
│   ├── api_server.py       # Flask REST API (port 7000)
│   ├── database.py         # SQLite database layer
│   ├── main.py             # Main app
│   ├── web/
│   │   └── index.html      # Web panel (responsive UI)
│   └── autoservice.db      # SQLite database
├── docs/
│   └── index.html          # GitHub Pages
├── main_mobile.py          # Kivy mobile app
└── README.md
```

## 🚀 Početak Rada

### Zahtjevi
- Python 3.8+
- Flask & CORS enabled
- SQLite3
- Git

### 1️⃣ Instalacija

```bash
# Kloniraj repo
git clone https://github.com/adis992/Auto-Servis-Pro.git
cd Auto-Servis-Pro

# Kreiraj virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows

# Instaliraj dependencies
pip install -r requirements.txt
```

### 2️⃣ Pokreni API Server

```bash
cd narudzbe
python api_server.py
```

Server će biti dostupan na: **http://localhost:7000**

### 3️⃣ Otvori Web Panel

**Online verzija (GitHub Pages):**
- 🌍 https://adis992.github.io/Auto-Servis-Pro/

**Lokalno:**
- Otvori `narudzbe/web/index.html` ili `docs/index.html` u browser-u

## 🔐 Demo Računi

| Username | Lozinka  | Uloga      |
|----------|----------|------------|
| admin    | admin123 | 👑 Admin   |
| user     | user123  | 👤 Korisnik|

## 📡 API Endpointi

### Autentifikacija
```
POST /api/auth/login
POST /api/auth/register
```

### Vozila
```
GET /api/vehicles              # Moja vozila
POST /api/vehicles             # Dodaj vozilo
DELETE /api/vehicles/<id>      # Obriši vozilo
```

### Narudžbe
```
GET /api/appointments          # Sve narudžbe
POST /api/appointments         # Kreiraj narudžbu
PUT /api/appointments/<id>     # Ažuriraj narudžbu
DELETE /api/appointments/<id>  # Otkaži narudžbu
```

### Usluge
```
GET /api/services              # Sve usluge
POST /api/services             # Dodaj uslugu (admin)
PUT /api/services/<id>         # Ažuriraj uslugu (admin)
DELETE /api/services/<id>      # Obriši uslugu (admin)
```

### Notifikacije
```
GET /api/notifications         # Moje notifikacije
PUT /api/notifications/<id>/read  # Označi kao pročitano
POST /api/notifications/broadcast # Broadcast (admin)
```

## 🎨 Funkcionalnosti Web Panela

### 📊 Dashboard
- Statistika: Vozila, Narudžbe, Notifikacije
- Quick access do glavnih sekcija

### 🚗 Vozila
- **Dodaj novo vozilo:**
  - Marka, Model, Godište
  - VIN, Registarska tablica
  - Boja, Vrsta motora, Kilometraža
  - Napomene

- **Pregled vozila:**
  - Brz pregled svih vozila
  - Mogućnost brisanja

### 📅 Narudžbe
- **Kreiraj narudžbu:**
  - Odaberi vozilo
  - Odaberi uslugu
  - Postavi datum i vrijeme
  - Dodaj napomene

- **Pregled narudžbi:**
  - Status narudžbe (Scheduled/Completed/Cancelled)
  - Cijena i datum
  - Mogućnost otkazivanja

### 🔧 Usluge
- **30+ usluga dostupno:**
  - Održavanje (Redovan servis, Zamjena ulja...)
  - Kočioni sistem
  - Klima uređaj
  - Ovjesen
  - Gume
  - Električni sistem
  - Motor
  - I mnogo više!

- **Svaka usluga sadrži:**
  - Detaljni opis
  - Cijena
  - Trajanje u minutama
  - Kategorija

### 🔔 Notifikacije
- Prikaz svih notifikacija
- Status (Pročitana/Nepročitana)
- Filtriranje po tipu

### 👤 Profil
- **Pregled podataka:**
  - Username, Email
  - Puno ime, Telefon
  - Uloga i datum registracije

- **Sigurnost:**
  - Promjena lozinke

### ⚙️ Admin Panel
- **Upravljanje Uslugama:**
  - Dodaj novu uslugu
  - Pregled svih usluga
  - Brisanje usluga

- **Statistika:**
  - Ukupno korisnika
  - Ukupno narudžbi

## 🗄️ Baza Podataka

### Tabele
- **users:** Korisnici sistema
- **services:** Dostupne usluge
- **vehicles:** Vozila korisnika
- **appointments:** Servisne narudžbe
- **notifications:** Obaveštenja
- **vehicle_types:** Tipovi vozila (sistem)
- **settings:** Konfiguracija

## 🔄 Workflow

### Za Korisnike:
1. Registriraj se ili prijavi
2. Dodaj svoje vozilo(a)
3. Odaberi uslugu iz kataloga
4. Kreiraj narudžbu za željeni datum
5. Čekaj potvrdu i obaveštenja

### Za Admina:
1. Logujem se kao admin
2. Vidim sve narudžbe
3. Mogu dodati nove usluge
4. Pregledam statistiku
5. Upravljam sistemom

## 🌐 GitHub Pages Setup

Web panel je automatski dostupan na GitHub Pages!

**URL:** https://adis992.github.io/Auto-Servis-Pro/

**Konfiguracija:**
- Source: `main` branch
- Folder: `/docs`
- Index: `index.html`

## 📱 Dostupnost

- ✅ Desktop (Web Browser)
- ✅ Mobile Responsive
- ✅ Tablet Friendly
- ✅ Offline Demo (Demo računi)

## 🔒 Sigurnost

- ✅ SHA-256 heširanje lozinki
- ✅ JWT-like token autentifikacija
- ✅ CORS omogućen
- ✅ Role-based pristup (User/Admin)
- ✅ Validacija na backend-u

## 📊 Statistika Projekta

- **30+ usluge** sa detaljnim opisima
- **12 tipova vozila** predefinisano
- **6 sekcija** u web panelu
- **8+ API endpointa** dostupno
- **Responsive UI** za sve uređaje

## 🐛 Troubleshooting

### Problem: "API server nije dostupan"
**Rješenje:**
```bash
cd narudzbe
python api_server.py
```
Provjeri da je port 7000 slobodan.

### Problem: Vozila se ne učitavaju
**Rješenje:**
- Provjeri da si se prijavio
- Osvježi stranicu (F5)
- Provjeri browser console za greške

### Problem: Baza podataka je prazna
**Rješenje:**
- Delete `autoservice.db`
- Ponovno pokreni API
- Database će se automatski kreirati sa default podacima

## 📝 Logovanje

Sve akcije se logiraju u bazu podataka:
- Prijave (last_login timestamp)
- Kreirane narudžbe (created_at)
- Ažuriranja (updated_at)
- Završeni servisi (completed_at)

## 🎯 Buduće Mogućnosti

- [ ] Email notifikacije
- [ ] SMS obaveštenja
- [ ] Integacija sa platnom Gateway-om
- [ ] Mobile app sa Kivy
- [ ] Real-time status updates (WebSocket)
- [ ] Booking calendar view
- [ ] Receipt/Invoice PDF
- [ ] Advanced reporting

## 🤝 Doprinosi

Svaki doprinos je dobrodošao! Slobodno:
1. Fork repo
2. Kreiraj feature branch
3. Commitaj promjene
4. Push i otvori Pull Request

## 📄 Licenca

MIT License - Slobodno koristi ovaj projekt!

## 📞 Kontakt

Za pitanja ili probleme, otvori GitHub Issue ili kontaktiraj maintajnera.

---

**Verzija:** 2.0  
**Zadnji update:** Februar 2026  
**Status:** ✅ Aktivno održavanje
