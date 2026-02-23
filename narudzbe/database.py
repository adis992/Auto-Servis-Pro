import sqlite3
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple


class AutoServiceDB:
    def __init__(self, db_path: str = "autoservice.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Create all necessary tables."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                phone TEXT,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                reset_token TEXT,
                reset_token_expiry TIMESTAMP
            )
        ''')

        # Services table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                duration_minutes INTEGER DEFAULT 60,
                category TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Vehicles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER,
                vin TEXT UNIQUE,
                license_plate TEXT,
                color TEXT,
                engine_type TEXT,
                mileage INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                vehicle_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                appointment_date TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                technician_notes TEXT,
                total_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (vehicle_id) REFERENCES vehicles (id),
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        ''')

        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                notification_type TEXT DEFAULT 'info',
                related_appointment_id INTEGER,
                is_read INTEGER DEFAULT 0,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (related_appointment_id) REFERENCES appointments (id)
            )
        ''')

        # Vehicle types table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                icon TEXT DEFAULT '🚗',
                created_by INTEGER,
                is_system INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

        # Create default data
        self._create_default_users()
        self._create_default_vehicle_types()
        self._create_default_services()

    def _create_default_users(self):
        """Kreiraj default admin i test korisnika."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        count = cursor.fetchone()['count']
        
        if count == 0:
            # Admin korisnik
            admin_hash = self._hash_password("admin123")
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, phone, role)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("admin", "admin@autoservis.com", admin_hash, "Administrator", "+381 60 123 4567", "admin"))
            
            # Test user korisnik
            user_hash = self._hash_password("user123")
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, phone, role)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("user", "user@test.com", user_hash, "Test Korisnik", "+381 65 987 6543", "user"))
            
            conn.commit()
        
        conn.close()
    
    def _create_default_vehicle_types(self):
        """Kreiraj default tipove vozila."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        vehicle_types = [
            ('Osobno vozilo', 'Standardni automobil sa 4-5 sjedišta', '🚗', 1),
            ('SUV / Terenac', 'Sportsko-terenska vozila sa povišenim gabaritima', '🚙', 1),
            ('Kombi / Karavan', 'Vozila sa produženim prtljažnikom', '🚐', 1),
            ('Pick-up', 'Teretna vozila sa otvorenim sandukom', '🛻', 1),
            ('Kamion', 'Teška teretna vozila', '🚚', 1),
            ('Motocikl', 'Dvotočkaša - motori, skuteri, kvadovi', '🏍️', 1),
            ('Prikolica', 'Priključna vozila bez sopstvenog pogona', '🚜', 1),
            ('Van / Dostavno', 'Komercijalna vozila za dostavu', '🚐', 1),
            ('Sportsko vozilo', 'Visokoperformansni automobili', '🏎️', 1),
            ('Luksuzno vozilo', 'Premium vozila visokog cjenovnog ranga', '💎', 1),
            ('Hibrid / Električno', 'Ekološka vozila na hibridni ili električni pogon', '⚡', 1),
            ('Oldtimer / Klasik', 'Istorijska vozila starija od 30 godina', '🕰️', 1)
        ]
        
        for vtype in vehicle_types:
            cursor.execute('''
                INSERT OR IGNORE INTO vehicle_types (name, description, icon, is_system)
                VALUES (?, ?, ?, ?)
            ''', vtype)
        
        conn.commit()
        conn.close()
    
    def _create_default_services(self):
        """Kreiraj default usluge sa detaljnim opisima."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM services")
        count = cursor.fetchone()['count']
        
        if count == 0:
            services = [
                ('Redovan servis - Mali', 'Zamjena motornog ulja i filtera ulja. Provjera nivoa svih tečnosti (servo, kočnice, rashladna, staklo). Vizuelna kontrola kočnica i sistema osvjetljenja. Pregled sistema za hlađenje. Reset servisnog indikatora. Ukupno trajanje: 45-60 minuta.', 80.00, 60, 'Održavanje'),
                ('Redovan servis - Veliki', 'Zamjena motornog ulja, filtera ulja, filtera vazduha, filtera kabine. Provjera i dopuna svih tečnosti. Kontrola kočionog sistema i diskova. Provjera sistema ovjesa i amortizera. Dijagnostika elektronike. Reset servisnih intervala. Ukupno trajanje: 90-120 minuta.', 150.00, 120, 'Održavanje'),
                ('Zamjena ulja i filtera', 'Ispuštanje starog motornog ulja, zamjena filtera ulja, punjenje sa novim sintetskim uljem prema specifikacijama proizvođača. Provjera nivoa ostalih tečnosti. Reset indikatora. Trajanje: 30-40 minuta.', 60.00, 40, 'Održavanje'),
                ('Dijagnostika motora', 'Kompjuterska dijagnostika svih sistema vozila pomoću profesionalnih dijagnostičkih uređaja. Očitavanje memorije grešaka iz svih kontrolnih jedinica. Provjera rada senzora i aktuatora. Ispis detaljnog izvještaja o stanju. Trajanje: 45-60 minuta.', 50.00, 60, 'Dijagnostika'),
                ('Zamjena kočionih pločica - prednje', 'Demontaža točkova, zamjena kočionih pločica sa novim originalnim ili aftermarket pločicama. Čišćenje kočionih čeljusti i podmazivanje klizača. Provjera debljine diskova. Kontrolna vožnja. Trajanje: 60-90 minuta.', 120.00, 90, 'Kočioni sistem'),
                ('Zamjena kočionih pločica - zadnje', 'Demontaža točkova, zamjena zadnjih kočionih pločica ili pakni (kod bubanj kočnica). Čišćenje mehanizma, podmazivanje. Podešavanje ručne kočnice. Provjera hidrauličkog sistema. Trajanje: 75-100 minuta.', 100.00, 100, 'Kočioni sistem'),
                ('Zamjena kočionih diskova', 'Demontaža točkova i stare kočione opreme. Montaža novih kočionih diskova i pločica. Centriranje i provjera. Test kočenja na vožnji. Uključuje prednje ili zadnje diskove sa pločicama. Trajanje: 120-150 minuta.', 250.00, 150, 'Kočioni sistem'),
                ('Punjenje klima uređaja', 'Vakuumiranje sistema klime, punjenje sa tačnom količinom rashladnog gasa (R134a ili R1234yf). Dodavanje UV boje za detekciju curenja. Provjera rada kompresora i kondenzatora. Mjerenje temperature. Trajanje: 60-75 minuta.', 70.00, 75, 'Klima'),
                ('Servis klima uređaja - kompletno', 'Ispuštanje starog gasa, vakuumiranje sistema, zamjena filtera sušača, provjera curenja UV lampom. Punjenje sa novim gasom i UV bojom. Dezinfekcija sistema klime ozonom. Zamjena filtera kabine. Trajanje: 120-140 minuta.', 150.00, 140, 'Klima'),
                ('Zamjena amortizera - komplet', 'Demontaža svih četiri amortizera, montaža novih amortizera sa ležajevima. Geometrija trap traka nakon montaže. Kontrola čvrstoće zavrtnjeva. Provjera na test vožnji. Trajanje: 180-240 minuta.', 400.00, 240, 'Ovjesen'),
                ('Geometrija trap traka - 3D', 'Profesionalno podešavanje geometrije prednjeg i zadnjeg ovjesa na 3D uređaju. Podešavanje ugla otklona (Camber), ugla nagiba (Caster) i konvergencije (Toe). Ispis izvještaja prije/poslije. Trajanje: 60-75 minuta.', 50.00, 75, 'Ovjesen'),
                ('Balansiranje guma - komplet', 'Balansiranje svih 4 točka na profesionalnoj mašini. Uklanjanje starih tegova, montaža novih olovnih ili čeličnih tegova. Provjera centriranja naplatka. Trajanje: 30-45 minuta.', 30.00, 45, 'Gume'),
                ('Sezonska zamjena guma', 'Demontaža ljetnih/zimskih guma, montaža sezonskih guma. Balansiranje svih 4 točka. Provjera pritiska i ventila. Pohrana skinutih guma (opciono). Trajanje: 45-60 minuta.', 40.00, 60, 'Gume'),
                ('Vulkaniziranje - popravka gume', 'Lociranje oštećenja, demontaža gume sa naplatka, unutrašnja popravka sa vulkanizacijskom zakrpom. Balansiranje i montaža. Provjera nepropusnosti. Trajanje: 30-45 minuta po gumi.', 25.00, 45, 'Gume'),
                ('Zamjena autolampi', 'Demontaža farova ili stop svjetla, zamjena pregorjele lampe sa novom (halogena, xenon ili LED). Provjera rada i podešavanje svjetlosnog snopa. Trajanje: 20-40 minuta.', 30.00, 40, 'Električni sistem'),
                ('Punjenje/zamjena akumulatora', 'Testiranje napona i kapaciteta akumulatora. Punjenje slabog akumulatora ili zamjena sa novim. Čišćenje polova i maziva. Provjera alternatora i potrošnje. Trajanje: 30-60 minuta.', 150.00, 60, 'Električni sistem'),
                ('Zamjena zubatog remena', 'Demontaža poklopca motora, zubate remenice i stari zubati remen. Montaža novog kompleta (remen + roler + zatezač). Podešavanje i kontrola. KRITIČNO VAŽNA USLUGA! Trajanje: 240-360 minuta.', 350.00, 360, 'Motor'),
                ('Zamjena svjećica', 'Demontaža zapaljivača i starih svjećica. Montaža novih svjećica sa tačnim momentom zatezanja. Reset adapcije. Testiranje rada motora. Trajanje: 45-75 minuta (zavisi od pristupačnosti).', 80.00, 75, 'Motor'),
                ('Zamjena izduvnog sistema', 'Zamjena korodiranih ili oštećenih dijelova izduvnog sistema (katalizator, srednji lonac, zadnji lonac). Zavarivanje ili montaža sa zaaptivkama. Trajanje: 90-180 minuta.', 200.00, 180, 'Ispuh'),
                ('Auto klima - dezinfekcija ozonom', 'Tretiranje unutrašnjosti vozila i sistema ventilacije generatorom ozona. Uništavanje bakterija, gljivica i neprijatnih mirisa. Trajanje: 45-60 minuta + vrijeme provjetravanja.', 40.00, 60, 'Klima'),
                ('Poliranje farova', 'Mašinsko poliranje zamagljenih plastičnih farova. Brušenje sa 3 stepena finoće, poliranje i zaštita UV lakom. Povećanje vidljivosti do 80%. Trajanje: 60-90 minuta.', 70.00, 90, 'Poliranje'),
                ('Detailing - unutrašnje pranje', 'Dubinsko usisavanje svih površina, pranje i zaštita plastičnih dijelova. Čišćenje tekstilnih površina ekstraktorom. Pranje i impregnacija sjedišta. Poliranje armaturne table. Trajanje: 120-180 minuta.', 100.00, 180, 'Auto detailing'),
                ('Detailing - kompletno', 'Unutrašnje dubinsko čišćenje + vanjsko mašinsko pranje sa pjenom. Poliranje laka u 2 faze. Vosak zaštita. Crnilo guma. Čišćenje motora. Premium usluga! Trajanje: 300-360 minuta.', 250.00, 360, 'Auto detailing'),
                ('Zamjena filtera goriva', 'Demontaža starog dizni ili benzinskog filtera goriva. Montaža novog originalnog filtera. Provjera propusnosti i pritiska. Trajanje: 45-60 minuta.', 60.00, 60, 'Gorivo'),
                ('Čišćenje DPF filtera', 'Demontaža DPF filtera čađi (dizel vozila). Mašinsko ispiranje i regeneracija filtera na specijalnom uređaju. Montaža i reset brojača. Trajanje: 180-240 minuta.', 200.00, 240, 'Gorivo'),
                ('Zamjena letve volana', 'Demontaža volana i stare letve upravljača. Montaža nove hidrauličke ili električne letve. Centriranje, provjera i geometrija. Trajanje: 240-300 minuta.', 450.00, 300, 'Upravljanje'),
                ('Zamjena EGR ventila', 'Demontaža zaprljenog EGR ventila, montaža novog. Čišćenje kanala. Reset adapcije preko dijagnostike. Provjera rada na vožnji. Trajanje: 90-120 minuta.', 180.00, 120, 'Motor'),
                ('Zamjena turbine', 'Demontaža stare turbine, montaža nove ili renovirane. Zamjena ulja i filtera. Provjera cjevovoda. Dijagnostika. Trajanje: 300-420 minuta.', 800.00, 420, 'Motor'),
                ('Zamjena kvačila - komplet', 'Skidanje mjenjača, demontaža starog kompleta kvačila (disk, lamela, ležaj). Montaža novog kompleta, centriranje, provjera. Trajanje: 360-480 minuta.', 500.00, 480, 'Transmisija'),
                ('Servis automatskog mjenjača', 'Ispuštanje starog ATF ulja, demontaža posude i čišćenje filtera. Punjenje sa novim ATF uljem. Reset adaptacije. Trajanje: 120-180 minuta.', 200.00, 180, 'Transmisija')
            ]
            
            for service in services:
                cursor.execute('''
                    INSERT INTO services (name, description, price, duration_minutes, category)
                    VALUES (?, ?, ?, ?, ?)
                ''', service)
            
            conn.commit()
        
        conn.close()

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    # ==================== USER METHODS ====================

    def verify_user(self, username: str, password: str) -> Optional[Dict]:
        """Verify user credentials and return user data if valid."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self._hash_password(password)
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user['id'],))
            conn.commit()
            user_dict = dict(user)
            user_dict.pop('password_hash', None)
            conn.close()
            return user_dict
        
        conn.close()
        return None

    def verify_user_by_email(self, email: str, password: str) -> Optional[Dict]:
        """Verify user credentials by email and return user data if valid."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self._hash_password(password)
        cursor.execute('''
            SELECT * FROM users 
            WHERE email = ? AND password_hash = ? AND is_active = 1
        ''', (email, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user['id'],))
            conn.commit()
            user_dict = dict(user)
            user_dict.pop('password_hash', None)
            conn.close()
            return user_dict
        
        conn.close()
        return None

    def register_user(self, username: str, email: str, password: str, 
                     full_name: str = "", phone: str = "", role: str = "user") -> Tuple[bool, str]:
        """Register a new user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if username or email already exists
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                conn.close()
                return False, "Korisničko ime ili email već postoje"
            
            password_hash = self._hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, phone, role)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, phone, role))
            
            conn.commit()
            conn.close()
            return True, "Korisnik uspešno registrovan"
        except Exception as e:
            conn.close()
            return False, f"Greška pri registraciji: {str(e)}"

    def get_all_users(self) -> List[Dict]:
        """Get all users."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        conn.close()
        
        result = []
        for user in users:
            user_dict = dict(user)
            user_dict.pop('password_hash', None)
            result.append(user_dict)
        return result

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_dict = dict(user)
            user_dict.pop('password_hash', None)
            return user_dict
        return None

    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception:
            conn.close()
            return False

    def change_user_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        old_hash = self._hash_password(old_password)
        cursor.execute("SELECT id FROM users WHERE id = ? AND password_hash = ?", (user_id, old_hash))
        
        if not cursor.fetchone():
            conn.close()
            return False, "Stara lozinka nije tačna"
        
        new_hash = self._hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
        conn.commit()
        conn.close()
        return True, "Lozinka uspešno promenjena"

    def reset_password_request(self, email: str) -> Tuple[bool, str, Optional[str]]:
        """Generate password reset token."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return False, "Email nije pronađen", None
        
        reset_token = secrets.token_urlsafe(32)
        expiry = datetime.now() + timedelta(hours=24)
        
        cursor.execute('''
            UPDATE users 
            SET reset_token = ?, reset_token_expiry = ? 
            WHERE email = ?
        ''', (reset_token, expiry, email))
        
        conn.commit()
        conn.close()
        return True, "Reset token kreiran", reset_token

    def verify_reset_token(self, token: str, new_password: str) -> Tuple[bool, str]:
        """Verify reset token and set new password."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM users 
            WHERE reset_token = ? AND reset_token_expiry > CURRENT_TIMESTAMP
        ''', (token,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return False, "Nevažeći ili istekao token"
        
        new_hash = self._hash_password(new_password)
        cursor.execute('''
            UPDATE users 
            SET password_hash = ?, reset_token = NULL, reset_token_expiry = NULL 
            WHERE id = ?
        ''', (new_hash, user['id']))
        
        conn.commit()
        conn.close()
        return True, "Lozinka uspešno resetovana"

    # ==================== VEHICLE METHODS ====================

    def add_vehicle(self, user_id: int, make: str, model: str, year: int = None,
                   vin: str = None, license_plate: str = None, **kwargs) -> Tuple[bool, str, Optional[int]]:
        """Add a new vehicle."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO vehicles (user_id, make, model, year, vin, license_plate, 
                                     color, engine_type, mileage, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, make, model, year, vin, license_plate,
                  kwargs.get('color'), kwargs.get('engine_type'), 
                  kwargs.get('mileage'), kwargs.get('notes')))
            
            vehicle_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True, "Vozilo uspešno dodato", vehicle_id
        except Exception as e:
            conn.close()
            return False, f"Greška: {str(e)}", None

    def get_user_vehicles(self, user_id: int) -> List[Dict]:
        """Get all vehicles for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        vehicles = cursor.fetchall()
        conn.close()
        return [dict(v) for v in vehicles]

    def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Dict]:
        """Get vehicle by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
        vehicle = cursor.fetchone()
        conn.close()
        return dict(vehicle) if vehicle else None

    def update_vehicle(self, vehicle_id: int, **kwargs) -> bool:
        """Update vehicle information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        allowed_fields = ['make', 'model', 'year', 'vin', 'license_plate', 
                         'color', 'engine_type', 'mileage', 'notes']
        
        updates = []
        values = []
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = ?")
                values.append(value)
        
        if not updates:
            conn.close()
            return False
        
        values.append(vehicle_id)
        query = f"UPDATE vehicles SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def delete_vehicle(self, vehicle_id: int) -> bool:
        """Delete a vehicle."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    # ==================== SERVICE METHODS ====================

    def add_service(self, name: str, price: float, description: str = "", 
                   duration_minutes: int = 60, category: str = "") -> Tuple[bool, str, Optional[int]]:
        """Add a new service."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO services (name, description, price, duration_minutes, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, description, price, duration_minutes, category))
            
            service_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True, "Usluga uspešno dodata", service_id
        except Exception as e:
            conn.close()
            return False, f"Greška: {str(e)}", None

    def get_all_services(self, active_only: bool = True) -> List[Dict]:
        """Get all services."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute("SELECT * FROM services WHERE is_active = 1 ORDER BY name")
        else:
            cursor.execute("SELECT * FROM services ORDER BY name")
        
        services = cursor.fetchall()
        conn.close()
        return [dict(s) for s in services]

    def get_service_by_id(self, service_id: int) -> Optional[Dict]:
        """Get service by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services WHERE id = ?", (service_id,))
        service = cursor.fetchone()
        conn.close()
        return dict(service) if service else None

    def update_service(self, service_id: int, **kwargs) -> bool:
        """Update service information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        allowed_fields = ['name', 'description', 'price', 'duration_minutes', 'category', 'is_active']
        
        updates = []
        values = []
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = ?")
                values.append(value)
        
        if not updates:
            conn.close()
            return False
        
        values.append(service_id)
        query = f"UPDATE services SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def delete_service(self, service_id: int) -> bool:
        """Delete a service."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    # ==================== APPOINTMENT METHODS ====================

    def create_appointment(self, user_id: int, vehicle_id: int, service_id: int,
                          appointment_date: str, notes: str = "") -> Tuple[bool, str, Optional[int]]:
        """Create a new appointment."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get service price
            cursor.execute("SELECT price FROM services WHERE id = ?", (service_id,))
            service = cursor.fetchone()
            total_price = service['price'] if service else 0
            
            cursor.execute('''
                INSERT INTO appointments (user_id, vehicle_id, service_id, appointment_date, 
                                        notes, total_price, status)
                VALUES (?, ?, ?, ?, ?, ?, 'scheduled')
            ''', (user_id, vehicle_id, service_id, appointment_date, notes, total_price))
            
            appointment_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Send notification
            self.send_appointment_notification(user_id, appointment_id, 'created')
            
            return True, "Termin uspešno kreiran", appointment_id
        except Exception as e:
            conn.close()
            return False, f"Greška: {str(e)}", None

    def get_user_appointments(self, user_id: int, status: str = None) -> List[Dict]:
        """Get appointments for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT a.*, s.name as service_name, v.make, v.model, v.license_plate
                FROM appointments a
                JOIN services s ON a.service_id = s.id
                JOIN vehicles v ON a.vehicle_id = v.id
                WHERE a.user_id = ? AND a.status = ?
                ORDER BY a.appointment_date DESC
            ''', (user_id, status))
        else:
            cursor.execute('''
                SELECT a.*, s.name as service_name, v.make, v.model, v.license_plate
                FROM appointments a
                JOIN services s ON a.service_id = s.id
                JOIN vehicles v ON a.vehicle_id = v.id
                WHERE a.user_id = ?
                ORDER BY a.appointment_date DESC
            ''', (user_id,))
        
        appointments = cursor.fetchall()
        conn.close()
        return [dict(a) for a in appointments]

    def get_all_appointments(self, status: str = None) -> List[Dict]:
        """Get all appointments."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT a.*, s.name as service_name, v.make, v.model, v.license_plate,
                       u.full_name as user_name, u.email, u.phone
                FROM appointments a
                JOIN services s ON a.service_id = s.id
                JOIN vehicles v ON a.vehicle_id = v.id
                JOIN users u ON a.user_id = u.id
                WHERE a.status = ?
                ORDER BY a.appointment_date DESC
            ''', (status,))
        else:
            cursor.execute('''
                SELECT a.*, s.name as service_name, v.make, v.model, v.license_plate,
                       u.full_name as user_name, u.email, u.phone
                FROM appointments a
                JOIN services s ON a.service_id = s.id
                JOIN vehicles v ON a.vehicle_id = v.id
                JOIN users u ON a.user_id = u.id
                ORDER BY a.appointment_date DESC
            ''')
        
        appointments = cursor.fetchall()
        conn.close()
        return [dict(a) for a in appointments]

    def update_appointment_status(self, appointment_id: int, status: str, 
                                  technician_notes: str = None) -> bool:
        """Update appointment status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if status == 'completed':
            cursor.execute('''
                UPDATE appointments 
                SET status = ?, technician_notes = ?, completed_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, technician_notes, appointment_id))
        else:
            cursor.execute('''
                UPDATE appointments 
                SET status = ?, technician_notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, technician_notes, appointment_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        
        if success:
            # Get user_id for notification
            cursor.execute("SELECT user_id FROM appointments WHERE id = ?", (appointment_id,))
            result = cursor.fetchone()
            if result:
                self.send_appointment_notification(result['user_id'], appointment_id, status)
        
        conn.close()
        return success

    def delete_appointment(self, appointment_id: int) -> bool:
        """Delete an appointment."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    # ==================== NOTIFICATION METHODS ====================

    def create_notification(self, user_id: Optional[int], title: str, message: str,
                          notification_type: str = 'info', 
                          related_appointment_id: int = None) -> Tuple[bool, Optional[int]]:
        """Create a notification."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO notifications (user_id, title, message, notification_type, related_appointment_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, title, message, notification_type, related_appointment_id))
            
            notification_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True, notification_id
        except Exception:
            conn.close()
            return False, None

    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Dict]:
        """Get notifications for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if unread_only:
            cursor.execute('''
                SELECT * FROM notifications 
                WHERE user_id = ? AND is_read = 0 
                ORDER BY sent_at DESC
            ''', (user_id,))
        else:
            cursor.execute('''
                SELECT * FROM notifications 
                WHERE user_id = ? 
                ORDER BY sent_at DESC
            ''', (user_id,))
        
        notifications = cursor.fetchall()
        conn.close()
        return [dict(n) for n in notifications]

    def mark_notification_read(self, notification_id: int) -> bool:
        """Mark a notification as read."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def mark_all_notifications_read(self, user_id: int) -> bool:
        """Mark all notifications as read for a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True

    def delete_notification(self, notification_id: int) -> bool:
        """Delete a notification."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM notifications WHERE user_id = ? AND is_read = 0", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result['count'] if result else 0

    def send_appointment_notification(self, user_id: int, appointment_id: int, action: str):
        """Send notification about appointment."""
        messages = {
            'created': ('Termin kreiran', 'Vaš termin je uspešno zakazan.'),
            'scheduled': ('Termin zakazan', 'Vaš termin je potvrđen.'),
            'confirmed': ('Termin potvrđen', 'Vaš termin je potvrđen.'),
            'in_progress': ('Servis u toku', 'Servisiranje vašeg vozila je u toku.'),
            'completed': ('Servis završen', 'Servisiranje vašeg vozila je završeno.'),
            'cancelled': ('Termin otkazan', 'Vaš termin je otkazan.')
        }
        
        title, message = messages.get(action, ('Obaveštenje', 'Ažuriranje termina.'))
        self.create_notification(user_id, title, message, 'appointment', appointment_id)

    def broadcast_notification(self, title: str, message: str, 
                              notification_type: str = 'info') -> int:
        """Send notification to all users."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE is_active = 1")
        users = cursor.fetchall()
        
        count = 0
        for user in users:
            success, _ = self.create_notification(user['id'], title, message, notification_type)
            if success:
                count += 1
        
        conn.close()
        return count

    # ==================== SETTINGS METHODS ====================

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            try:
                return json.loads(result['value'])
            except:
                return result['value']
        return default

    def set_setting(self, key: str, value: Any, description: str = None) -> bool:
        """Set a setting value."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        value_str = json.dumps(value) if not isinstance(value, str) else value
        
        cursor.execute("SELECT id FROM settings WHERE key = ?", (key,))
        exists = cursor.fetchone()
        
        if exists:
            cursor.execute('''
                UPDATE settings 
                SET value = ?, description = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE key = ?
            ''', (value_str, description, key))
        else:
            cursor.execute('''
                INSERT INTO settings (key, value, description) 
                VALUES (?, ?, ?)
            ''', (key, value_str, description))
        
        conn.commit()
        conn.close()
        return True

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        settings = cursor.fetchall()
        conn.close()
        
        result = {}
        for setting in settings:
            try:
                result[setting['key']] = json.loads(setting['value'])
            except:
                result[setting['key']] = setting['value']
        
        return result

    # ==================== VEHICLE TYPES METHODS ====================

    def get_all_vehicle_types(self) -> List[Dict]:
        """Vrati sve tipove vozila."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT vt.*, u.username as creator_name 
            FROM vehicle_types vt 
            LEFT JOIN users u ON vt.created_by = u.id
            ORDER BY vt.is_system DESC, vt.name ASC
        """)
        types = cursor.fetchall()
        conn.close()
        return [dict(t) for t in types]

    def create_vehicle_type(self, name: str, description: str = None, icon: str = '🚗', user_id: int = None) -> Tuple[bool, str, Optional[int]]:
        """Kreiraj novi tip vozila."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO vehicle_types (name, description, icon, created_by, is_system)
                VALUES (?, ?, ?, ?, 0)
            """, (name, description, icon, user_id))
            
            type_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True, "Tip vozila kreiran uspješno", type_id
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Tip vozila sa tim nazivom već postoji", None
        except Exception as e:
            conn.close()
            return False, f"Greška: {str(e)}", None

    def delete_vehicle_type(self, type_id: int) -> Tuple[bool, str]:
        """Obriši tip vozila (samo custom, ne sistemske)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Provjeri da li je sistemski
        cursor.execute("SELECT is_system FROM vehicle_types WHERE id = ?", (type_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False, "Tip vozila ne postoji"
        
        if result['is_system'] == 1:
            conn.close()
            return False, "Sistemske tipove vozila nije moguće obrisati"
        
        try:
            cursor.execute("DELETE FROM vehicle_types WHERE id = ?", (type_id,))
            conn.commit()
            conn.close()
            return True, "Tip vozila obrisan"
        except Exception as e:
            conn.close()
            return False, f"Greška: {str(e)}"

    # ==================== SEARCH METHODS ====================

    def search_appointments(self, query: str) -> List[Dict]:
        """Pretraži termine po vozilu, useru ili statusu."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT a.*, u.username, u.full_name, v.make, v.model, v.license_plate, s.name as service_name
            FROM appointments a
            JOIN users u ON a.user_id = u.id
            JOIN vehicles v ON a.vehicle_id = v.id
            JOIN services s ON a.service_id = s.id
            WHERE v.license_plate LIKE ? OR v.make LIKE ? OR v.model LIKE ?
               OR u.username LIKE ? OR u.full_name LIKE ?
               OR a.status LIKE ? OR s.name LIKE ?
            ORDER BY a.appointment_date DESC
            LIMIT 100
        """, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
        
        results = cursor.fetchall()
        conn.close()
        return [dict(r) for r in results]

    def search_users(self, query: str) -> List[Dict]:
        """Pretraži korisnike po imenu, emailu ili usernameu."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT id, username, email, full_name, phone, role, created_at
            FROM users
            WHERE username LIKE ? OR email LIKE ? OR full_name LIKE ? OR phone LIKE ?
            LIMIT 50
        """, (search_pattern, search_pattern, search_pattern, search_pattern))
        
        results = cursor.fetchall()
        conn.close()
        return [dict(r) for r in results]

    def search_services(self, query: str) -> List[Dict]:
        """Pretraži usluge po nazivu ili kategoriji."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM services
            WHERE name LIKE ? OR category LIKE ? OR description LIKE ?
            ORDER BY name
            LIMIT 50
        """, (search_pattern, search_pattern, search_pattern))
        
        results = cursor.fetchall()
        conn.close()
        return [dict(r) for r in results]

    def search_vehicles(self, query: str) -> List[Dict]:
        """Pretraži vozila po registraciji, marki ili modelu."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT v.*, u.username, u.full_name
            FROM vehicles v
            JOIN users u ON v.user_id = u.id
            WHERE v.license_plate LIKE ? OR v.make LIKE ? OR v.model LIKE ? OR v.vin LIKE ?
            ORDER BY v.license_plate
            LIMIT 50
        """, (search_pattern, search_pattern, search_pattern, search_pattern))
        
        results = cursor.fetchall()
        conn.close()
        return [dict(r) for r in results]
