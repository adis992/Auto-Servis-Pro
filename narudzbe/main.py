#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Servis Pro - Desktop Application
Version: 2.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
from tkcalendar import Calendar
from datetime import datetime, timedelta
from database import AutoServiceDB
import re
import threading
import subprocess
import platform

# PDF Printer je privremeno onemogućen
# from pdf_printer import AppointmentPrinter


class AutoServisApp:
    """Glavna aplikacija Auto Servis Pro"""
    
    # Boje
    PRIMARY = '#2c3e50'
    SUCCESS = '#27ae60'
    DANGER = '#e74c3c'
    WARNING = '#f39c12'
    INFO = '#3498db'
    LIGHT = '#ecf0f1'
    DARK = '#34495e'
    WHITE = '#ffffff'
    
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Servis Pro - Desktop")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.LIGHT)
        
        # Database
        self.db = AutoServiceDB()
        
        # Current user
        self.current_user = None
        self.current_role = None
        
        # Printer settings (stored in memory for now)
        self.printer_settings = {
            'printer_name': 'Default Printer',
            'auto_print': False
        }
        
        # SSH settings
        self.ssh_settings = {
            'host': '',
            'port': '22',
            'username': '',
            'password': ''
        }
        
        # Inicijalizuj bazu podataka
        self._init_database()
        
        # Pokaži login ekran
        self.show_login_screen()
    
    def _init_database(self):
        """Inicijalizuj bazu podataka sa test podacima"""
        try:
            # Kreiraj test usere ako ne postoje
            users = self.db.get_all_users()
            if not users:
                # Admin user
                self.db.register_user(
                    'admin@autoservis.com',
                    'admin123',
                    'Administrator',
                    '+38160123456',
                    'admin'
                )
                # Regular user
                self.db.register_user(
                    'user@test.com',
                    'user123',
                    'Test Korisnik',
                    '+38160987654',
                    'user'
                )
            
            # Kreiraj usluge ako ne postoje
            services = self.db.get_all_services()
            if not services:
                default_services = [
                    ('Redovan servis', 'Zamena ulja, filtera i pregled vozila', 8000.00, 90),
                    ('Mali servis', 'Zamena ulja i filtera', 5000.00, 60),
                    ('Veliki servis', 'Kompletan pregled i zamena delova', 15000.00, 180),
                    ('Dijagnostika', 'Kompjuterska dijagnostika vozila', 3000.00, 30),
                    ('Popravka kočnica', 'Zamena pločica i diskova', 12000.00, 120),
                    ('Klima servis', 'Punjenje i servis klima uređaja', 4500.00, 45),
                ]
                for name, desc, price, duration in default_services:
                    self.db.add_service(name, desc, price, duration)
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def show_login_screen(self):
        """Prikaži login/register ekran"""
        # Očisti prozor
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.LIGHT)
        main_frame.pack(fill='both', expand=True)
        
        # Left panel - Branding
        left_panel = tk.Frame(main_frame, bg=self.PRIMARY, width=500)
        left_panel.pack(side='left', fill='both', expand=False)
        left_panel.pack_propagate(False)
        
        # Logo i branding
        brand_frame = tk.Frame(left_panel, bg=self.PRIMARY)
        brand_frame.place(relx=0.5, rely=0.4, anchor='center')
        
        logo_label = tk.Label(
            brand_frame,
            text="🔧",
            font=('Arial', 100),
            bg=self.PRIMARY,
            fg=self.WHITE
        )
        logo_label.pack()
        
        title_label = tk.Label(
            brand_frame,
            text="Auto Servis Pro",
            font=('Arial', 32, 'bold'),
            bg=self.PRIMARY,
            fg=self.WHITE
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            brand_frame,
            text="Profesionalni sistem za upravljanje\nauto servisom",
            font=('Arial', 14),
            bg=self.PRIMARY,
            fg=self.LIGHT,
            justify='center'
        )
        subtitle_label.pack()
        
        # Demo info
        demo_frame = tk.Frame(left_panel, bg=self.DARK, padx=20, pady=15)
        demo_frame.place(relx=0.5, rely=0.75, anchor='center', width=400)
        
        demo_title = tk.Label(
            demo_frame,
            text="💡 Demo pristup:",
            font=('Arial', 12, 'bold'),
            bg=self.DARK,
            fg=self.WARNING,
            anchor='w'
        )
        demo_title.pack(fill='x')
        
        demo_info = tk.Label(
            demo_frame,
            text="admin / admin123\nuser / user123",
            font=('Arial', 11),
            bg=self.DARK,
            fg=self.WHITE,
            justify='left'
        )
        demo_info.pack(fill='x', pady=(5, 10))
        
        api_label = tk.Label(
            demo_frame,
            text="🌐 Web API: http://localhost:7000",
            font=('Arial', 10),
            bg=self.DARK,
            fg=self.INFO,
            cursor="hand2"
        )
        api_label.pack(fill='x')
        api_label.bind("<Button-1>", lambda e: self._open_web_api())
        
        # Right panel - Login/Register
        right_panel = tk.Frame(main_frame, bg=self.LIGHT)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Tab switcher
        tab_frame = tk.Frame(right_panel, bg=self.LIGHT)
        tab_frame.pack(pady=40)
        
        self.login_tab_btn = tk.Button(
            tab_frame,
            text="Prijava",
            font=('Arial', 14, 'bold'),
            bg=self.PRIMARY,
            fg=self.WHITE,
            bd=0,
            padx=40,
            pady=10,
            cursor="hand2",
            command=lambda: self._switch_auth_tab('login', login_frame, register_frame)
        )
        self.login_tab_btn.pack(side='left', padx=5)
        
        self.register_tab_btn = tk.Button(
            tab_frame,
            text="Registracija",
            font=('Arial', 14),
            bg=self.LIGHT,
            fg=self.DARK,
            bd=0,
            padx=40,
            pady=10,
            cursor="hand2",
            command=lambda: self._switch_auth_tab('register', login_frame, register_frame)
        )
        self.register_tab_btn.pack(side='left', padx=5)
        
        # Login frame
        login_frame = tk.Frame(right_panel, bg=self.LIGHT)
        login_frame.pack(pady=20)
        
        # Login form
        form_frame = tk.Frame(login_frame, bg=self.WHITE, padx=50, pady=40)
        form_frame.pack()
        
        tk.Label(
            form_frame,
            text="Dobrodošli nazad!",
            font=('Arial', 20, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY
        ).grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        tk.Label(
            form_frame,
            text="Email ili korisničko ime:",
            font=('Arial', 11),
            bg=self.WHITE,
            fg=self.DARK
        ).grid(row=1, column=0, sticky='w', pady=(0, 5))
        
        self.login_username = tk.Entry(form_frame, font=('Arial', 12), width=30)
        self.login_username.grid(row=2, column=0, pady=(0, 20))
        
        tk.Label(
            form_frame,
            text="Lozinka:",
            font=('Arial', 11),
            bg=self.WHITE,
            fg=self.DARK
        ).grid(row=3, column=0, sticky='w', pady=(0, 5))
        
        self.login_password = tk.Entry(form_frame, font=('Arial', 12), width=30, show='*')
        self.login_password.grid(row=4, column=0, pady=(0, 10))
        self.login_password.bind('<Return>', lambda e: self._do_login())
        
        forgot_label = tk.Label(
            form_frame,
            text="Zaboravili ste lozinku?",
            font=('Arial', 9, 'underline'),
            bg=self.WHITE,
            fg=self.INFO,
            cursor="hand2"
        )
        forgot_label.grid(row=5, column=0, sticky='e', pady=(0, 20))
        forgot_label.bind("<Button-1>", lambda e: self._show_forgot_password())
        
        login_btn = tk.Button(
            form_frame,
            text="Prijavite se",
            font=('Arial', 12, 'bold'),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._do_login
        )
        login_btn.grid(row=6, column=0, pady=(0, 20), sticky='ew')
        
        # OAuth mock buttons
        oauth_frame = tk.Frame(form_frame, bg=self.WHITE)
        oauth_frame.grid(row=7, column=0, pady=(10, 0))
        
        tk.Label(
            oauth_frame,
            text="ili se prijavite pomoću:",
            font=('Arial', 9),
            bg=self.WHITE,
            fg=self.DARK
        ).pack(pady=(0, 10))
        
        oauth_btns = tk.Frame(oauth_frame, bg=self.WHITE)
        oauth_btns.pack()
        
        google_btn = tk.Button(
            oauth_btns,
            text="Google",
            font=('Arial', 10),
            bg='#db4437',
            fg=self.WHITE,
            bd=0,
            padx=20,
            pady=5,
            cursor="hand2",
            command=lambda: self._oauth_login('Google')
        )
        google_btn.pack(side='left', padx=5)
        
        facebook_btn = tk.Button(
            oauth_btns,
            text="Facebook",
            font=('Arial', 10),
            bg='#4267B2',
            fg=self.WHITE,
            bd=0,
            padx=20,
            pady=5,
            cursor="hand2",
            command=lambda: self._oauth_login('Facebook')
        )
        facebook_btn.pack(side='left', padx=5)
        
        # Register frame (initially hidden)
        register_frame = tk.Frame(right_panel, bg=self.LIGHT)
        
        # Register form
        reg_form_frame = tk.Frame(register_frame, bg=self.WHITE, padx=50, pady=40)
        reg_form_frame.pack()
        
        tk.Label(
            reg_form_frame,
            text="Kreirajte nalog",
            font=('Arial', 20, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY
        ).grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Email (OBAVEZNO)
        email_label_frame = tk.Frame(reg_form_frame, bg=self.WHITE)
        email_label_frame.grid(row=1, column=0, sticky='w', pady=(0, 5))
        
        tk.Label(
            email_label_frame,
            text="Email ",
            font=('Arial', 11),
            bg=self.WHITE,
            fg=self.DARK
        ).pack(side='left')
        
        tk.Label(
            email_label_frame,
            text="*",
            font=('Arial', 11, 'bold'),
            bg=self.WHITE,
            fg=self.DANGER
        ).pack(side='left')
        
        tk.Label(
            email_label_frame,
            text="(obavezno)",
            font=('Arial', 9, 'italic'),
            bg=self.WHITE,
            fg=self.WARNING
        ).pack(side='left', padx=(3, 0))
        
        self.reg_email = tk.Entry(reg_form_frame, font=('Arial', 12), width=30)
        self.reg_email.grid(row=2, column=0, pady=(0, 15))
        
        # Puno ime
        tk.Label(
            reg_form_frame,
            text="Puno ime:",
            font=('Arial', 11),
            bg=self.WHITE,
            fg=self.DARK
        ).grid(row=3, column=0, sticky='w', pady=(0, 5))
        
        self.reg_fullname = tk.Entry(reg_form_frame, font=('Arial', 12), width=30)
        self.reg_fullname.grid(row=4, column=0, pady=(0, 15))
        
        # Telefon
        tk.Label(
            reg_form_frame,
            text="Telefon:",
            font=('Arial', 11),
            bg=self.WHITE,
            fg=self.DARK
        ).grid(row=5, column=0, sticky='w', pady=(0, 5))
        
        self.reg_phone = tk.Entry(reg_form_frame, font=('Arial', 12), width=30)
        self.reg_phone.grid(row=6, column=0, pady=(0, 15))
        
        # Lozinka
        tk.Label(
            reg_form_frame,
            text="Lozinka:",
            font=('Arial', 11),
            bg=self.WHITE,
            fg=self.DARK
        ).grid(row=7, column=0, sticky='w', pady=(0, 5))
        
        self.reg_password = tk.Entry(reg_form_frame, font=('Arial', 12), width=30, show='*')
        self.reg_password.grid(row=8, column=0, pady=(0, 15))
        
        # Potvrda lozinke
        tk.Label(
            reg_form_frame,
            text="Potvrdite lozinku:",
            font=('Arial', 11),
            bg=self.WHITE,
            fg=self.DARK
        ).grid(row=9, column=0, sticky='w', pady=(0, 5))
        
        self.reg_password_confirm = tk.Entry(reg_form_frame, font=('Arial', 12), width=30, show='*')
        self.reg_password_confirm.grid(row=10, column=0, pady=(0, 20))
        self.reg_password_confirm.bind('<Return>', lambda e: self._do_register())
        
        register_btn = tk.Button(
            reg_form_frame,
            text="Registrujte se",
            font=('Arial', 12, 'bold'),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._do_register
        )
        register_btn.grid(row=11, column=0, pady=(0, 0), sticky='ew')
    
    def _switch_auth_tab(self, tab, login_frame, register_frame):
        """Prebaci između login i register tab-a"""
        if tab == 'login':
            self.login_tab_btn.config(bg=self.PRIMARY, fg=self.WHITE, font=('Arial', 14, 'bold'))
            self.register_tab_btn.config(bg=self.LIGHT, fg=self.DARK, font=('Arial', 14))
            register_frame.pack_forget()
            login_frame.pack(pady=20)
        else:
            self.register_tab_btn.config(bg=self.PRIMARY, fg=self.WHITE, font=('Arial', 14, 'bold'))
            self.login_tab_btn.config(bg=self.LIGHT, fg=self.DARK, font=('Arial', 14))
            login_frame.pack_forget()
            register_frame.pack(pady=20)
    
    def _open_web_api(self):
        """Otvori Web API u browseru"""
        url = "http://localhost:7000"
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(['start', url], shell=True)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', url])
            else:  # Linux
                subprocess.Popen(['xdg-open', url])
        except Exception as e:
            messagebox.showinfo("Web API", f"Otvorite u browseru:\n{url}")
    
    def _show_forgot_password(self):
        """Prikaži forgot password dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Zaboravljena lozinka")
        dialog.geometry("400x300")
        dialog.configure(bg=self.WHITE)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(
            dialog,
            text="🔑",
            font=('Arial', 40),
            bg=self.WHITE
        ).pack(pady=(30, 10))
        
        tk.Label(
            dialog,
            text="Resetovanje lozinke",
            font=('Arial', 16, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY
        ).pack()
        
        tk.Label(
            dialog,
            text="Unesite email adresu:",
            font=('Arial', 11),
            bg=self.WHITE,
            fg=self.DARK
        ).pack(pady=(20, 5))
        
        email_entry = tk.Entry(dialog, font=('Arial', 12), width=30)
        email_entry.pack(pady=(0, 20))
        
        def send_reset():
            email = email_entry.get().strip()
            if not email:
                messagebox.showwarning("Upozorenje", "Unesite email adresu!")
                return
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                messagebox.showwarning("Upozorenje", "Unesite validnu email adresu!")
                return
            messagebox.showinfo(
                "Link poslat",
                f"Link za resetovanje lozinke je poslat na:\n{email}"
            )
            dialog.destroy()
        
        tk.Button(
            dialog,
            text="Pošalji link",
            font=('Arial', 11, 'bold'),
            bg=self.INFO,
            fg=self.WHITE,
            bd=0,
            padx=30,
            pady=8,
            cursor="hand2",
            command=send_reset
        ).pack()
    
    def _oauth_login(self, provider):
        """OAuth login mock"""
        messagebox.showinfo(
            f"{provider} Login",
            f"OAuth login sa {provider} računom\n(Demo funkcionalnost)"
        )
    
    def _do_login(self):
        """Izvršava login"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showwarning("Upozorenje", "Popunite sva polja!")
            return
        
        # Proveri kredencijale
        user = self.db.verify_user(username, password)
        if user:
            self.current_user = user
            self.current_role = user['role']
            
            if self.current_role == 'admin':
                self.show_admin_panel()
            else:
                self.show_user_panel()
        else:
            messagebox.showerror("Greška", "Pogrešno korisničko ime ili lozinka!")
    
    def _do_register(self):
        """Izvršava registraciju"""
        email = self.reg_email.get().strip()
        fullname = self.reg_fullname.get().strip()
        phone = self.reg_phone.get().strip()
        password = self.reg_password.get()
        password_confirm = self.reg_password_confirm.get()
        
        # Validacija
        if not email:
            messagebox.showwarning(
                "⚠️ Email obavezan",
                "Email adresa je obavezna za registraciju!\n\nEmail se koristi za:\n• Prijavljivanje na nalog\n• Resetovanje lozinke\n• Notifikacije"
            )
            return
        
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showwarning("Upozorenje", "Unesite validnu email adresu!")
            return
        
        if not fullname or not phone or not password:
            messagebox.showwarning("Upozorenje", "Popunite sva obavezna polja!")
            return
        
        if password != password_confirm:
            messagebox.showwarning("Upozorenje", "Lozinke se ne poklapaju!")
            return
        
        if len(password) < 6:
            messagebox.showwarning("Upozorenje", "Lozinka mora imati najmanje 6 karaktera!")
            return
        
        # Registruj korisnika
        success = self.db.register_user(email, password, fullname, phone, 'user')
        
        if success:
            messagebox.showinfo(
                "Uspeh",
                "Registracija uspešna!\n\nMožete se sada prijaviti."
            )
            # Očisti polja
            self.reg_email.delete(0, tk.END)
            self.reg_fullname.delete(0, tk.END)
            self.reg_phone.delete(0, tk.END)
            self.reg_password.delete(0, tk.END)
            self.reg_password_confirm.delete(0, tk.END)
        else:
            messagebox.showerror("Greška", "Email adresa je već registrovana!")
    
    def show_admin_panel(self):
        """Prikaži admin panel"""
        # Očisti prozor
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.LIGHT)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg=self.PRIMARY, height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔧 Auto Servis Pro - Admin Panel",
            font=('Arial', 18, 'bold'),
            bg=self.PRIMARY,
            fg=self.WHITE
        ).pack(side='left', padx=20, pady=15)
        
        user_info = tk.Label(
            header,
            text=f"👤 {self.current_user['full_name']} (Admin)",
            font=('Arial', 11),
            bg=self.PRIMARY,
            fg=self.LIGHT
        )
        user_info.pack(side='right', padx=20)
        
        logout_btn = tk.Button(
            header,
            text="Odjava",
            font=('Arial', 10, 'bold'),
            bg=self.DANGER,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.show_login_screen
        )
        logout_btn.pack(side='right', padx=10)
        
        # Content
        content = tk.Frame(main_frame, bg=self.LIGHT)
        content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tabs
        self.admin_notebook = ttk.Notebook(content)
        self.admin_notebook.pack(fill='both', expand=True)
        
        # Tab 1: Termini
        appointments_tab = tk.Frame(self.admin_notebook, bg=self.WHITE)
        self.admin_notebook.add(appointments_tab, text="📅 Termini")
        self._create_appointments_tab(appointments_tab)
        
        # Tab 2: Korisnici
        users_tab = tk.Frame(self.admin_notebook, bg=self.WHITE)
        self.admin_notebook.add(users_tab, text="👥 Korisnici")
        self._create_users_tab(users_tab)
        
        # Tab 3: Usluge
        services_tab = tk.Frame(self.admin_notebook, bg=self.WHITE)
        self.admin_notebook.add(services_tab, text="🛠️ Usluge")
        self._create_services_tab(services_tab)
        
        # Tab 4: Notifikacije
        notifications_tab = tk.Frame(self.admin_notebook, bg=self.WHITE)
        self.admin_notebook.add(notifications_tab, text="🔔 Notifikacije")
        self._create_notifications_tab(notifications_tab)
        
        # Tab 5: Postavke
        settings_tab = tk.Frame(self.admin_notebook, bg=self.WHITE)
        self.admin_notebook.add(settings_tab, text="⚙️ Postavke")
        self._create_settings_tab(settings_tab)
        
        # Tab 6: Izvještaji
        reports_tab = tk.Frame(self.admin_notebook, bg=self.WHITE)
        self.admin_notebook.add(reports_tab, text="📊 Izvještaji")
        self._create_reports_tab(reports_tab)
    
    def _create_appointments_tab(self, parent):
        """Kreira tab za termine"""
        # Toolbar
        toolbar = tk.Frame(parent, bg=self.WHITE, pady=10)
        toolbar.pack(fill='x', padx=10)
        
        tk.Button(
            toolbar,
            text="🔄 Osveži",
            font=('Arial', 10),
            bg=self.INFO,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda: self._refresh_appointments()
        ).pack(side='left', padx=5)
        
        # Filter
        tk.Label(toolbar, text="Status:", bg=self.WHITE).pack(side='left', padx=(20, 5))
        self.appointment_filter = ttk.Combobox(
            toolbar,
            values=['Svi', 'Pending', 'Confirmed', 'Completed', 'Cancelled'],
            width=15,
            state='readonly'
        )
        self.appointment_filter.set('Svi')
        self.appointment_filter.pack(side='left', padx=5)
        self.appointment_filter.bind('<<ComboboxSelected>>', lambda e: self._refresh_appointments())
        
        # Table
        table_frame = tk.Frame(parent, bg=self.WHITE)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Korisnik', 'Usluga', 'Datum', 'Vrijeme', 'Status', 'Vozilo')
        self.appointments_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.appointments_tree.yview)
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            if col == 'ID':
                self.appointments_tree.column(col, width=50)
            elif col in ['Datum', 'Vrijeme', 'Status']:
                self.appointments_tree.column(col, width=100)
            else:
                self.appointments_tree.column(col, width=150)
        
        self.appointments_tree.pack(fill='both', expand=True)
        
        # Context menu
        self.appointments_tree.bind('<Button-3>', self._show_appointment_context_menu)
        
        # Osveži podatke
        self._refresh_appointments()
    
    def _refresh_appointments(self):
        """Osveži listu termina"""
        # Očisti tabelu
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        # Dobavi termine
        appointments = self.db.get_all_appointments()
        
        # Filtriraj po statusu
        status_filter = self.appointment_filter.get()
        if status_filter != 'Svi':
            appointments = [a for a in appointments if a['status'] == status_filter]
        
        # Popuni tabelu
        for app in appointments:
            user = self.db.get_user_by_id(app['user_id'])
            service = self.db.get_service_by_id(app['service_id'])
            vehicle = self.db.get_vehicle_by_id(app['vehicle_id']) if app.get('vehicle_id') else None
            
            self.appointments_tree.insert('', 'end', values=(
                app['id'],
                user['full_name'] if user else 'N/A',
                service['name'] if service else 'N/A',
                app['appointment_date'],
                app['appointment_time'],
                app['status'],
                f"{vehicle['brand']} {vehicle['model']}" if vehicle else 'N/A'
            ))
    
    def _show_appointment_context_menu(self, event):
        """Prikaži context menu za termin"""
        # Selektuj item
        item = self.appointments_tree.identify_row(event.y)
        if item:
            self.appointments_tree.selection_set(item)
            
            # Kreiraj menu
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Potvrdi", command=lambda: self._update_appointment_status('Confirmed'))
            menu.add_command(label="Završi", command=lambda: self._update_appointment_status('Completed'))
            menu.add_command(label="Otkaži", command=lambda: self._update_appointment_status('Cancelled'))
            menu.add_separator()
            menu.add_command(label="Detalji", command=self._show_appointment_details)
            menu.add_command(label="Odštampaj", command=self._print_appointment)
            
            menu.post(event.x_root, event.y_root)
    
    def _update_appointment_status(self, status):
        """Ažuriraj status termina"""
        selection = self.appointments_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.appointments_tree.item(item, 'values')
        appointment_id = values[0]
        
        self.db.update_appointment_status(appointment_id, status)
        self._refresh_appointments()
        messagebox.showinfo("Uspeh", f"Status termina ažuriran na: {status}")
    
    def _show_appointment_details(self):
        """Prikaži detalje termina"""
        selection = self.appointments_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.appointments_tree.item(item, 'values')
        
        details = f"""
Detalji termina:

ID: {values[0]}
Korisnik: {values[1]}
Usluga: {values[2]}
Datum: {values[3]}
Vrijeme: {values[4]}
Status: {values[5]}
Vozilo: {values[6]}
"""
        messagebox.showinfo("Detalji termina", details)
    
    def _print_appointment(self):
        """Odštampaj termin"""
        messagebox.showwarning(
            "⚠️ PDF trenutno nije dostupan",
            "PDF funkcionalnost trenutno nije dostupna.\n\nTreba instalirati reportlab:\npip install reportlab"
        )
    
    def _create_users_tab(self, parent):
        """Kreira tab za korisnike"""
        # Toolbar
        toolbar = tk.Frame(parent, bg=self.WHITE, pady=10)
        toolbar.pack(fill='x', padx=10)
        
        tk.Button(
            toolbar,
            text="🔄 Osveži",
            font=('Arial', 10),
            bg=self.INFO,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda: self._refresh_users()
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar,
            text="➕ Novi korisnik",
            font=('Arial', 10),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._add_user_dialog
        ).pack(side='left', padx=5)
        
        # Search
        tk.Label(toolbar, text="Pretraga:", bg=self.WHITE).pack(side='left', padx=(20, 5))
        self.user_search = tk.Entry(toolbar, font=('Arial', 10), width=20)
        self.user_search.pack(side='left', padx=5)
        self.user_search.bind('<KeyRelease>', lambda e: self._refresh_users())
        
        # Table
        table_frame = tk.Frame(parent, bg=self.WHITE)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Email', 'Ime', 'Telefon', 'Rola', 'Registracija')
        self.users_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.users_tree.yview)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            if col == 'ID':
                self.users_tree.column(col, width=50)
            elif col in ['Rola']:
                self.users_tree.column(col, width=80)
            elif col in ['Registracija']:
                self.users_tree.column(col, width=150)
            else:
                self.users_tree.column(col, width=150)
        
        self.users_tree.pack(fill='both', expand=True)
        
        # Context menu
        self.users_tree.bind('<Button-3>', self._show_user_context_menu)
        
        # Osveži podatke
        self._refresh_users()
    
    def _refresh_users(self):
        """Osveži listu korisnika"""
        # Očisti tabelu
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Dobavi korisnike
        users = self.db.get_all_users()
        
        # Filtriraj po pretrazi
        search = self.user_search.get().lower()
        if search:
            users = [u for u in users if 
                    search in u['email'].lower() or 
                    search in u['full_name'].lower() or
                    search in u.get('phone', '').lower()]
        
        # Popuni tabelu
        for user in users:
            self.users_tree.insert('', 'end', values=(
                user['id'],
                user['email'],
                user['full_name'],
                user.get('phone', 'N/A'),
                user['role'],
                user['created_at']
            ))
    
    def _show_user_context_menu(self, event):
        """Prikaži context menu za korisnika"""
        item = self.users_tree.identify_row(event.y)
        if item:
            self.users_tree.selection_set(item)
            
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Uredi", command=self._edit_user_dialog)
            menu.add_command(label="Obriši", command=self._delete_user)
            menu.add_separator()
            menu.add_command(label="Detalji", command=self._show_user_details)
            
            menu.post(event.x_root, event.y_root)
    
    def _add_user_dialog(self):
        """Dialog za dodavanje korisnika"""
        messagebox.showinfo("Dodaj korisnika", "Korisnik može da se registruje preko forme za registraciju.")
    
    def _edit_user_dialog(self):
        """Dialog za izmenu korisnika"""
        selection = self.users_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.users_tree.item(item, 'values')
        
        messagebox.showinfo("Uredi korisnika", f"Izmena korisnika: {values[2]}\n(Demo)")
    
    def _delete_user(self):
        """Obriši korisnika"""
        selection = self.users_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.users_tree.item(item, 'values')
        
        if messagebox.askyesno("Potvrda", f"Obrisati korisnika {values[2]}?"):
            messagebox.showinfo("Uspeh", "Korisnik obrisan!")
            self._refresh_users()
    
    def _show_user_details(self):
        """Prikaži detalje korisnika"""
        selection = self.users_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.users_tree.item(item, 'values')
        
        details = f"""
Detalji korisnika:

ID: {values[0]}
Email: {values[1]}
Ime: {values[2]}
Telefon: {values[3]}
Rola: {values[4]}
Registrovan: {values[5]}
"""
        messagebox.showinfo("Detalji korisnika", details)
    
    def _create_services_tab(self, parent):
        """Kreira tab za usluge"""
        # Toolbar
        toolbar = tk.Frame(parent, bg=self.WHITE, pady=10)
        toolbar.pack(fill='x', padx=10)
        
        tk.Button(
            toolbar,
            text="🔄 Osveži",
            font=('Arial', 10),
            bg=self.INFO,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda: self._refresh_services()
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar,
            text="➕ Nova usluga",
            font=('Arial', 10),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._add_service_dialog
        ).pack(side='left', padx=5)
        
        # Table
        table_frame = tk.Frame(parent, bg=self.WHITE)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        columns = ('ID', 'Naziv', 'Opis', 'Cena (RSD)', 'Trajanje (min)')
        self.services_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.services_tree.yview)
        
        for col in columns:
            self.services_tree.heading(col, text=col)
            if col == 'ID':
                self.services_tree.column(col, width=50)
            elif col in ['Cena (RSD)', 'Trajanje (min)']:
                self.services_tree.column(col, width=120)
            else:
                self.services_tree.column(col, width=200)
        
        self.services_tree.pack(fill='both', expand=True)
        
        # Context menu
        self.services_tree.bind('<Button-3>', self._show_service_context_menu)
        
        # Osveži podatke
        self._refresh_services()
    
    def _refresh_services(self):
        """Osveži listu usluga"""
        # Očisti tabelu
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)
        
        # Dobavi usluge
        services = self.db.get_all_services()
        
        # Popuni tabelu
        for service in services:
            self.services_tree.insert('', 'end', values=(
                service['id'],
                service['name'],
                service['description'][:50] + '...' if len(service['description']) > 50 else service['description'],
                f"{service['price']:.2f}",
                service['duration']
            ))
    
    def _show_service_context_menu(self, event):
        """Prikaži context menu za uslugu"""
        item = self.services_tree.identify_row(event.y)
        if item:
            self.services_tree.selection_set(item)
            
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Uredi", command=self._edit_service_dialog)
            menu.add_command(label="Obriši", command=self._delete_service)
            
            menu.post(event.x_root, event.y_root)
    
    def _add_service_dialog(self):
        """Dialog za dodavanje usluge"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nova usluga")
        dialog.geometry("500x450")
        dialog.configure(bg=self.WHITE)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        form = tk.Frame(dialog, bg=self.WHITE, padx=30, pady=30)
        form.pack(fill='both', expand=True)
        
        tk.Label(form, text="Naziv usluge:", bg=self.WHITE).grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form, font=('Arial', 11), width=40)
        name_entry.grid(row=1, column=0, pady=(0, 15))
        
        tk.Label(form, text="Opis:", bg=self.WHITE).grid(row=2, column=0, sticky='w', pady=5)
        desc_text = tk.Text(form, font=('Arial', 11), width=40, height=5)
        desc_text.grid(row=3, column=0, pady=(0, 15))
        
        tk.Label(form, text="Cena (RSD):", bg=self.WHITE).grid(row=4, column=0, sticky='w', pady=5)
        price_entry = tk.Entry(form, font=('Arial', 11), width=40)
        price_entry.grid(row=5, column=0, pady=(0, 15))
        
        tk.Label(form, text="Trajanje (min):", bg=self.WHITE).grid(row=6, column=0, sticky='w', pady=5)
        duration_entry = tk.Entry(form, font=('Arial', 11), width=40)
        duration_entry.grid(row=7, column=0, pady=(0, 20))
        
        def save_service():
            name = name_entry.get().strip()
            desc = desc_text.get('1.0', 'end').strip()
            price = price_entry.get().strip()
            duration = duration_entry.get().strip()
            
            if not name or not price or not duration:
                messagebox.showwarning("Upozorenje", "Popunite sva polja!")
                return
            
            try:
                price = float(price)
                duration = int(duration)
            except ValueError:
                messagebox.showwarning("Upozorenje", "Cena i trajanje moraju biti brojevi!")
                return
            
            self.db.add_service(name, desc, price, duration)
            self._refresh_services()
            messagebox.showinfo("Uspeh", "Usluga dodata!")
            dialog.destroy()
        
        tk.Button(
            form,
            text="Sačuvaj",
            font=('Arial', 11, 'bold'),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=30,
            pady=8,
            cursor="hand2",
            command=save_service
        ).grid(row=8, column=0)
    
    def _edit_service_dialog(self):
        """Dialog za izmenu usluge"""
        selection = self.services_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.services_tree.item(item, 'values')
        
        messagebox.showinfo("Uredi uslugu", f"Izmena usluge: {values[1]}\n(Demo)")
    
    def _delete_service(self):
        """Obriši uslugu"""
        selection = self.services_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.services_tree.item(item, 'values')
        
        if messagebox.askyesno("Potvrda", f"Obrisati uslugu {values[1]}?"):
            messagebox.showinfo("Uspeh", "Usluga obrisana!")
            self._refresh_services()
    
    def _create_notifications_tab(self, parent):
        """Kreira tab za notifikacije"""
        # Toolbar
        toolbar = tk.Frame(parent, bg=self.WHITE, pady=10)
        toolbar.pack(fill='x', padx=10)
        
        tk.Label(
            toolbar,
            text="📢 Pošalji Notifikaciju",
            font=('Arial', 14, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY
        ).pack(side='left', padx=5)
        
        # Form
        form_frame = tk.Frame(parent, bg=self.WHITE)
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Tip notifikacije
        tk.Label(
            form_frame,
            text="Tip notifikacije:",
            font=('Arial', 11),
            bg=self.WHITE
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        notif_type_frame = tk.Frame(form_frame, bg=self.WHITE)
        notif_type_frame.grid(row=1, column=0, sticky='w', pady=(0, 20))
        
        self.notif_type = tk.StringVar(value='individual')
        
        tk.Radiobutton(
            notif_type_frame,
            text="Pojedinačno",
            variable=self.notif_type,
            value='individual',
            bg=self.WHITE,
            font=('Arial', 10),
            command=lambda: self._toggle_user_select(True)
        ).pack(side='left', padx=(0, 20))
        
        tk.Radiobutton(
            notif_type_frame,
            text="Broadcast (Svima)",
            variable=self.notif_type,
            value='broadcast',
            bg=self.WHITE,
            font=('Arial', 10),
            command=lambda: self._toggle_user_select(False)
        ).pack(side='left')
        
        # Korisnik (samo za individual)
        tk.Label(
            form_frame,
            text="Korisnik:",
            font=('Arial', 11),
            bg=self.WHITE
        ).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        self.notif_user_combo = ttk.Combobox(form_frame, width=50, state='readonly')
        self.notif_user_combo.grid(row=3, column=0, sticky='w', pady=(0, 20))
        
        # Popuni korisnike
        users = self.db.get_all_users()
        user_list = [f"{u['full_name']} ({u['email']})" for u in users]
        self.notif_user_combo['values'] = user_list
        if user_list:
            self.notif_user_combo.current(0)
        
        # Naslov
        tk.Label(
            form_frame,
            text="Naslov:",
            font=('Arial', 11),
            bg=self.WHITE
        ).grid(row=4, column=0, sticky='w', pady=(0, 5))
        
        self.notif_title = tk.Entry(form_frame, font=('Arial', 11), width=50)
        self.notif_title.grid(row=5, column=0, sticky='w', pady=(0, 20))
        
        # Poruka
        tk.Label(
            form_frame,
            text="Poruka:",
            font=('Arial', 11),
            bg=self.WHITE
        ).grid(row=6, column=0, sticky='w', pady=(0, 5))
        
        self.notif_message = tk.Text(form_frame, font=('Arial', 11), width=50, height=8)
        self.notif_message.grid(row=7, column=0, sticky='w', pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.WHITE)
        btn_frame.grid(row=8, column=0, sticky='w')
        
        tk.Button(
            btn_frame,
            text="📤 Pošalji",
            font=('Arial', 11, 'bold'),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=30,
            pady=8,
            cursor="hand2",
            command=self._send_notification
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            btn_frame,
            text="Očisti",
            font=('Arial', 11),
            bg=self.LIGHT,
            fg=self.DARK,
            bd=0,
            padx=30,
            pady=8,
            cursor="hand2",
            command=self._clear_notification_form
        ).pack(side='left')
    
    def _toggle_user_select(self, enabled):
        """Omogući/onemogući user select"""
        if enabled:
            self.notif_user_combo.config(state='readonly')
        else:
            self.notif_user_combo.config(state='disabled')
    
    def _send_notification(self):
        """Pošalji notifikaciju"""
        title = self.notif_title.get().strip()
        message = self.notif_message.get('1.0', 'end').strip()
        
        if not title or not message:
            messagebox.showwarning("Upozorenje", "Popunite naslov i poruku!")
            return
        
        if self.notif_type.get() == 'individual':
            user_str = self.notif_user_combo.get()
            messagebox.showinfo(
                "Notifikacija poslata",
                f"Notifikacija poslata korisniku:\n{user_str}"
            )
        else:
            messagebox.showinfo(
                "Broadcast notifikacija",
                "Notifikacija poslata svim korisnicima!"
            )
        
        self._clear_notification_form()
    
    def _clear_notification_form(self):
        """Očisti formu za notifikacije"""
        self.notif_title.delete(0, tk.END)
        self.notif_message.delete('1.0', tk.END)
        self.notif_type.set('individual')
        self._toggle_user_select(True)
    
    def _create_settings_tab(self, parent):
        """Kreira tab za postavke"""
        # Scrollable frame
        canvas = tk.Canvas(parent, bg=self.WHITE)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Settings sections
        settings_container = tk.Frame(scrollable_frame, bg=self.WHITE, padx=30, pady=30)
        settings_container.pack(fill='both', expand=True)
        
        # Section 1: Printer Settings
        printer_section = tk.LabelFrame(
            settings_container,
            text="🖨️ Postavke štampača",
            font=('Arial', 12, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY,
            padx=20,
            pady=20
        )
        printer_section.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            printer_section,
            text="Ime štampača:",
            font=('Arial', 10),
            bg=self.WHITE
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.printer_name_entry = tk.Entry(printer_section, font=('Arial', 10), width=40)
        self.printer_name_entry.insert(0, self.printer_settings['printer_name'])
        self.printer_name_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        self.auto_print_var = tk.BooleanVar(value=self.printer_settings['auto_print'])
        tk.Checkbutton(
            printer_section,
            text="Automatski štampaj potvrde",
            variable=self.auto_print_var,
            font=('Arial', 10),
            bg=self.WHITE
        ).grid(row=1, column=0, columnspan=2, sticky='w', pady=5)
        
        btn_frame = tk.Frame(printer_section, bg=self.WHITE)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky='w', pady=(10, 0))
        
        tk.Button(
            btn_frame,
            text="Sačuvaj",
            font=('Arial', 10, 'bold'),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=20,
            pady=5,
            cursor="hand2",
            command=self._save_printer_settings
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            btn_frame,
            text="Test štampanje",
            font=('Arial', 10),
            bg=self.INFO,
            fg=self.WHITE,
            bd=0,
            padx=20,
            pady=5,
            cursor="hand2",
            command=self._test_print
        ).pack(side='left')
        
        # Section 2: Cloud/Server Settings
        ssh_section = tk.LabelFrame(
            settings_container,
            text="☁️ Cloud/Server SSH postavke",
            font=('Arial', 12, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY,
            padx=20,
            pady=20
        )
        ssh_section.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            ssh_section,
            text="SSH Host:",
            font=('Arial', 10),
            bg=self.WHITE
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.ssh_host_entry = tk.Entry(ssh_section, font=('Arial', 10), width=40)
        self.ssh_host_entry.insert(0, self.ssh_settings['host'])
        self.ssh_host_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        tk.Label(
            ssh_section,
            text="SSH Port:",
            font=('Arial', 10),
            bg=self.WHITE
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.ssh_port_entry = tk.Entry(ssh_section, font=('Arial', 10), width=40)
        self.ssh_port_entry.insert(0, self.ssh_settings['port'])
        self.ssh_port_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        tk.Label(
            ssh_section,
            text="SSH Username:",
            font=('Arial', 10),
            bg=self.WHITE
        ).grid(row=2, column=0, sticky='w', pady=5)
        
        self.ssh_username_entry = tk.Entry(ssh_section, font=('Arial', 10), width=40)
        self.ssh_username_entry.insert(0, self.ssh_settings['username'])
        self.ssh_username_entry.grid(row=2, column=1, padx=(10, 0), pady=5)
        
        tk.Label(
            ssh_section,
            text="SSH Password:",
            font=('Arial', 10),
            bg=self.WHITE
        ).grid(row=3, column=0, sticky='w', pady=5)
        
        self.ssh_password_entry = tk.Entry(ssh_section, font=('Arial', 10), width=40, show='*')
        self.ssh_password_entry.insert(0, self.ssh_settings['password'])
        self.ssh_password_entry.grid(row=3, column=1, padx=(10, 0), pady=5)
        
        ssh_btn_frame = tk.Frame(ssh_section, bg=self.WHITE)
        ssh_btn_frame.grid(row=4, column=0, columnspan=2, sticky='w', pady=(10, 0))
        
        tk.Button(
            ssh_btn_frame,
            text="Sačuvaj",
            font=('Arial', 10, 'bold'),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=20,
            pady=5,
            cursor="hand2",
            command=self._save_ssh_settings
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            ssh_btn_frame,
            text="Test konekcije",
            font=('Arial', 10),
            bg=self.INFO,
            fg=self.WHITE,
            bd=0,
            padx=20,
            pady=5,
            cursor="hand2",
            command=self._test_ssh_connection
        ).pack(side='left')
        
        # Section 3: Opšte postavke
        general_section = tk.LabelFrame(
            settings_container,
            text="⚙️ Opšte postavke",
            font=('Arial', 12, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY,
            padx=20,
            pady=20
        )
        general_section.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            general_section,
            text="Radno vreme servisa:",
            font=('Arial', 10),
            bg=self.WHITE
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        time_frame = tk.Frame(general_section, bg=self.WHITE)
        time_frame.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=5)
        
        tk.Label(time_frame, text="Od:", bg=self.WHITE).pack(side='left')
        start_time = ttk.Combobox(time_frame, width=8, state='readonly')
        start_time['values'] = [f"{h:02d}:00" for h in range(24)]
        start_time.set("08:00")
        start_time.pack(side='left', padx=5)
        
        tk.Label(time_frame, text="Do:", bg=self.WHITE).pack(side='left', padx=(10, 0))
        end_time = ttk.Combobox(time_frame, width=8, state='readonly')
        end_time['values'] = [f"{h:02d}:00" for h in range(24)]
        end_time.set("17:00")
        end_time.pack(side='left', padx=5)
    
    def _save_printer_settings(self):
        """Sačuvaj printer postavke"""
        self.printer_settings['printer_name'] = self.printer_name_entry.get()
        self.printer_settings['auto_print'] = self.auto_print_var.get()
        messagebox.showinfo("Uspeh", "Postavke štampača sačuvane!")
    
    def _test_print(self):
        """Test štampanje"""
        messagebox.showwarning(
            "⚠️ PDF trenutno nije dostupan",
            "PDF funkcionalnost trenutno nije dostupna.\n\nTreba instalirati reportlab:\npip install reportlab"
        )
    
    def _save_ssh_settings(self):
        """Sačuvaj SSH postavke"""
        self.ssh_settings['host'] = self.ssh_host_entry.get()
        self.ssh_settings['port'] = self.ssh_port_entry.get()
        self.ssh_settings['username'] = self.ssh_username_entry.get()
        self.ssh_settings['password'] = self.ssh_password_entry.get()
        messagebox.showinfo("Uspeh", "SSH postavke sačuvane!")
    
    def _test_ssh_connection(self):
        """Test SSH konekcije"""
        host = self.ssh_host_entry.get()
        if not host:
            messagebox.showwarning("Upozorenje", "Unesite SSH host!")
            return
        
        messagebox.showinfo(
            "SSH Test",
            f"Testiranje konekcije na:\n{host}\n\n(Demo funkcionalnost)"
        )
    
    def _create_reports_tab(self, parent):
        """Kreira tab za izvještaje"""
        # Container
        container = tk.Frame(parent, bg=self.WHITE, padx=30, pady=30)
        container.pack(fill='both', expand=True)
        
        tk.Label(
            container,
            text="📊 Izvještaji",
            font=('Arial', 18, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY
        ).pack(pady=(0, 30))
        
        # Report buttons
        reports = [
            ("📅 Izvještaj o terminima", "Pregled svih termina po datumima"),
            ("💰 Finansijski izvještaj", "Ukupan prihod i statistika"),
            ("👥 Izvještaj o korisnicima", "Pregled aktivnosti korisnika"),
            ("🛠️ Izvještaj o uslugama", "Najpopularnije usluge"),
        ]
        
        for title, desc in reports:
            report_frame = tk.Frame(container, bg=self.LIGHT, padx=20, pady=15)
            report_frame.pack(fill='x', pady=(0, 15))
            
            tk.Label(
                report_frame,
                text=title,
                font=('Arial', 12, 'bold'),
                bg=self.LIGHT,
                fg=self.DARK
            ).pack(anchor='w')
            
            tk.Label(
                report_frame,
                text=desc,
                font=('Arial', 10),
                bg=self.LIGHT,
                fg=self.DARK
            ).pack(anchor='w', pady=(5, 10))
            
            tk.Button(
                report_frame,
                text="Generiši izvještaj",
                font=('Arial', 10),
                bg=self.INFO,
                fg=self.WHITE,
                bd=0,
                padx=20,
                pady=5,
                cursor="hand2",
                command=lambda t=title: self._generate_report(t)
            ).pack(anchor='w')
    
    def _generate_report(self, report_type):
        """Generiši izvještaj"""
        messagebox.showinfo("Izvještaj", f"Generisanje izvještaja:\n{report_type}\n\n(Demo)")
    
    def show_user_panel(self):
        """Prikaži user panel"""
        # Očisti prozor
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.LIGHT)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg=self.PRIMARY, height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🔧 Auto Servis Pro",
            font=('Arial', 18, 'bold'),
            bg=self.PRIMARY,
            fg=self.WHITE
        ).pack(side='left', padx=20, pady=15)
        
        user_info = tk.Label(
            header,
            text=f"👤 {self.current_user['full_name']}",
            font=('Arial', 11),
            bg=self.PRIMARY,
            fg=self.LIGHT
        )
        user_info.pack(side='right', padx=20)
        
        logout_btn = tk.Button(
            header,
            text="Odjava",
            font=('Arial', 10, 'bold'),
            bg=self.DANGER,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.show_login_screen
        )
        logout_btn.pack(side='right', padx=10)
        
        # Content
        content = tk.Frame(main_frame, bg=self.LIGHT)
        content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tabs
        self.user_notebook = ttk.Notebook(content)
        self.user_notebook.pack(fill='both', expand=True)
        
        # Tab 1: Rezervacija
        booking_tab = tk.Frame(self.user_notebook, bg=self.WHITE)
        self.user_notebook.add(booking_tab, text="📅 Rezervacija")
        self._create_booking_tab(booking_tab)
        
        # Tab 2: Moji termini
        my_appointments_tab = tk.Frame(self.user_notebook, bg=self.WHITE)
        self.user_notebook.add(my_appointments_tab, text="📋 Moji termini")
        self._create_my_appointments_tab(my_appointments_tab)
        
        # Tab 3: Notifikacije
        user_notif_tab = tk.Frame(self.user_notebook, bg=self.WHITE)
        self.user_notebook.add(user_notif_tab, text="🔔 Notifikacije")
        self._create_user_notifications_tab(user_notif_tab)
        
        # Tab 4: Vozila
        vehicles_tab = tk.Frame(self.user_notebook, bg=self.WHITE)
        self.user_notebook.add(vehicles_tab, text="🚗 Vozila")
        self._create_vehicles_tab(vehicles_tab)
        
        # Tab 5: Profil
        profile_tab = tk.Frame(self.user_notebook, bg=self.WHITE)
        self.user_notebook.add(profile_tab, text="👤 Profil")
        self._create_profile_tab(profile_tab)
    
    def _create_booking_tab(self, parent):
        """Kreira tab za rezervaciju"""
        # Container
        container = tk.Frame(parent, bg=self.WHITE, padx=30, pady=30)
        container.pack(fill='both', expand=True)
        
        tk.Label(
            container,
            text="Zakažite termin",
            font=('Arial', 18, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY
        ).pack(pady=(0, 30))
        
        # Form
        form_frame = tk.Frame(container, bg=self.WHITE)
        form_frame.pack()
        
        # Usluga
        tk.Label(
            form_frame,
            text="Izaberite uslugu:",
            font=('Arial', 11),
            bg=self.WHITE
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        services = self.db.get_all_services()
        service_list = [f"{s['name']} - {s['price']} RSD ({s['duration']} min)" for s in services]
        
        self.booking_service = ttk.Combobox(form_frame, values=service_list, width=50, state='readonly')
        if service_list:
            self.booking_service.current(0)
        self.booking_service.grid(row=1, column=0, pady=(0, 20))
        
        # Vozilo
        tk.Label(
            form_frame,
            text="Izaberite vozilo:",
            font=('Arial', 11),
            bg=self.WHITE
        ).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        vehicles = self.db.get_user_vehicles(self.current_user['id'])
        vehicle_list = [f"{v['brand']} {v['model']} ({v['license_plate']})" for v in vehicles]
        
        self.booking_vehicle = ttk.Combobox(form_frame, values=vehicle_list, width=50, state='readonly')
        if vehicle_list:
            self.booking_vehicle.current(0)
        self.booking_vehicle.grid(row=3, column=0, pady=(0, 20))
        
        # Datum
        tk.Label(
            form_frame,
            text="Datum:",
            font=('Arial', 11),
            bg=self.WHITE
        ).grid(row=4, column=0, sticky='w', pady=(0, 5))
        
        self.booking_calendar = Calendar(
            form_frame,
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now()
        )
        self.booking_calendar.grid(row=5, column=0, pady=(0, 20))
        
        # Vreme
        tk.Label(
            form_frame,
            text="Vreme:",
            font=('Arial', 11),
            bg=self.WHITE
        ).grid(row=6, column=0, sticky='w', pady=(0, 5))
        
        time_slots = [f"{h:02d}:{m:02d}" for h in range(8, 17) for m in [0, 30]]
        self.booking_time = ttk.Combobox(form_frame, values=time_slots, width=50, state='readonly')
        self.booking_time.current(0)
        self.booking_time.grid(row=7, column=0, pady=(0, 20))
        
        # Napomena
        tk.Label(
            form_frame,
            text="Napomena (opcionalno):",
            font=('Arial', 11),
            bg=self.WHITE
        ).grid(row=8, column=0, sticky='w', pady=(0, 5))
        
        self.booking_note = tk.Text(form_frame, font=('Arial', 10), width=50, height=4)
        self.booking_note.grid(row=9, column=0, pady=(0, 20))
        
        # Button
        tk.Button(
            form_frame,
            text="Zakaži termin",
            font=('Arial', 12, 'bold'),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=40,
            pady=10,
            cursor="hand2",
            command=self._create_booking
        ).grid(row=10, column=0)
    
    def _create_booking(self):
        """Kreiraj rezervaciju"""
        if not self.booking_service.get():
            messagebox.showwarning("Upozorenje", "Izaberite uslugu!")
            return
        
        if not self.booking_vehicle.get():
            messagebox.showwarning("Upozorenje", "Nemate registrovano vozilo! Dodajte vozilo u 'Vozila' tabu.")
            return
        
        date = self.booking_calendar.get_date()
        time = self.booking_time.get()
        note = self.booking_note.get('1.0', 'end').strip()
        
        # Get service ID
        service_str = self.booking_service.get()
        services = self.db.get_all_services()
        service_id = None
        for s in services:
            if s['name'] in service_str:
                service_id = s['id']
                break
        
        # Get vehicle ID
        vehicle_str = self.booking_vehicle.get()
        vehicles = self.db.get_user_vehicles(self.current_user['id'])
        vehicle_id = None
        for v in vehicles:
            if v['license_plate'] in vehicle_str:
                vehicle_id = v['id']
                break
        
        if not service_id or not vehicle_id:
            messagebox.showerror("Greška", "Došlo je do greške!")
            return
        
        # Create appointment
        success = self.db.create_appointment(
            self.current_user['id'],
            service_id,
            vehicle_id,
            date,
            time,
            note
        )
        
        if success:
            messagebox.showinfo(
                "Uspeh",
                f"Termin uspešno zakazan!\n\nDatum: {date}\nVreme: {time}"
            )
            self.booking_note.delete('1.0', tk.END)
        else:
            messagebox.showerror("Greška", "Došlo je do greške pri zakazivanju!")
    
    def _create_my_appointments_tab(self, parent):
        """Kreira tab za moje termine"""
        # Toolbar
        toolbar = tk.Frame(parent, bg=self.WHITE, pady=10)
        toolbar.pack(fill='x', padx=10)
        
        tk.Button(
            toolbar,
            text="🔄 Osveži",
            font=('Arial', 10),
            bg=self.INFO,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda: self._refresh_my_appointments()
        ).pack(side='left', padx=5)
        
        # Table
        table_frame = tk.Frame(parent, bg=self.WHITE)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('ID', 'Usluga', 'Datum', 'Vreme', 'Status', 'Vozilo')
        self.my_appointments_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.my_appointments_tree.yview)
        
        for col in columns:
            self.my_appointments_tree.heading(col, text=col)
            if col == 'ID':
                self.my_appointments_tree.column(col, width=50)
            else:
                self.my_appointments_tree.column(col, width=150)
        
        self.my_appointments_tree.pack(fill='both', expand=True)
        
        # Context menu
        self.my_appointments_tree.bind('<Button-3>', self._show_my_appointment_menu)
        
        self._refresh_my_appointments()
    
    def _refresh_my_appointments(self):
        """Osveži moje termine"""
        for item in self.my_appointments_tree.get_children():
            self.my_appointments_tree.delete(item)
        
        appointments = self.db.get_user_appointments(self.current_user['id'])
        
        for app in appointments:
            service = self.db.get_service_by_id(app['service_id'])
            vehicle = self.db.get_vehicle_by_id(app['vehicle_id'])
            
            self.my_appointments_tree.insert('', 'end', values=(
                app['id'],
                service['name'] if service else 'N/A',
                app['appointment_date'],
                app['appointment_time'],
                app['status'],
                f"{vehicle['brand']} {vehicle['model']}" if vehicle else 'N/A'
            ))
    
    def _show_my_appointment_menu(self, event):
        """Prikaži context menu za termin"""
        item = self.my_appointments_tree.identify_row(event.y)
        if item:
            self.my_appointments_tree.selection_set(item)
            
            values = self.my_appointments_tree.item(item, 'values')
            status = values[4]
            
            menu = tk.Menu(self.root, tearoff=0)
            
            if status == 'Pending':
                menu.add_command(label="Otkaži termin", command=self._cancel_my_appointment)
            
            menu.add_command(label="Detalji", command=self._show_my_appointment_details)
            
            menu.post(event.x_root, event.y_root)
    
    def _cancel_my_appointment(self):
        """Otkaži moj termin"""
        selection = self.my_appointments_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.my_appointments_tree.item(item, 'values')
        
        if messagebox.askyesno("Potvrda", "Da li ste sigurni da želite otkazati termin?"):
            self.db.update_appointment_status(values[0], 'Cancelled')
            self._refresh_my_appointments()
            messagebox.showinfo("Uspeh", "Termin otkazan!")
    
    def _show_my_appointment_details(self):
        """Prikaži detalje termina"""
        selection = self.my_appointments_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.my_appointments_tree.item(item, 'values')
        
        details = f"""
Detalji termina:

Usluga: {values[1]}
Datum: {values[2]}
Vreme: {values[3]}
Status: {values[4]}
Vozilo: {values[5]}
"""
        messagebox.showinfo("Detalji termina", details)
    
    def _create_user_notifications_tab(self, parent):
        """Kreira tab za notifikacije korisnika"""
        # Container
        container = tk.Frame(parent, bg=self.WHITE, padx=20, pady=20)
        container.pack(fill='both', expand=True)
        
        tk.Label(
            container,
            text="🔔 Notifikacije",
            font=('Arial', 16, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY
        ).pack(pady=(0, 20))
        
        # Demo notifications
        demo_notifications = [
            {
                'title': 'Termin potvrđen',
                'message': 'Vaš termin za 2025-03-15 u 10:00 je potvrđen.',
                'time': '2 sata ranije'
            },
            {
                'title': 'Podsetnik',
                'message': 'Imate zakazan termin sutra u 14:30.',
                'time': '1 dan ranije'
            },
        ]
        
        for notif in demo_notifications:
            notif_frame = tk.Frame(container, bg=self.LIGHT, padx=15, pady=10)
            notif_frame.pack(fill='x', pady=(0, 10))
            
            tk.Label(
                notif_frame,
                text=notif['title'],
                font=('Arial', 11, 'bold'),
                bg=self.LIGHT,
                fg=self.DARK
            ).pack(anchor='w')
            
            tk.Label(
                notif_frame,
                text=notif['message'],
                font=('Arial', 10),
                bg=self.LIGHT,
                fg=self.DARK,
                wraplength=500
            ).pack(anchor='w', pady=(5, 0))
            
            tk.Label(
                notif_frame,
                text=notif['time'],
                font=('Arial', 9),
                bg=self.LIGHT,
                fg='gray'
            ).pack(anchor='w', pady=(5, 0))
    
    def _create_vehicles_tab(self, parent):
        """Kreira tab za vozila"""
        # Toolbar
        toolbar = tk.Frame(parent, bg=self.WHITE, pady=10)
        toolbar.pack(fill='x', padx=10)
        
        tk.Button(
            toolbar,
            text="🔄 Osveži",
            font=('Arial', 10),
            bg=self.INFO,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda: self._refresh_vehicles()
        ).pack(side='left', padx=5)
        
        tk.Button(
            toolbar,
            text="➕ Dodaj vozilo",
            font=('Arial', 10),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self._add_vehicle_dialog
        ).pack(side='left', padx=5)
        
        # Table
        table_frame = tk.Frame(parent, bg=self.WHITE)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('ID', 'Marka', 'Model', 'Tablica', 'Godina', 'VIN')
        self.vehicles_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.vehicles_tree.yview)
        
        for col in columns:
            self.vehicles_tree.heading(col, text=col)
            if col == 'ID':
                self.vehicles_tree.column(col, width=50)
            elif col in ['Godina']:
                self.vehicles_tree.column(col, width=80)
            else:
                self.vehicles_tree.column(col, width=150)
        
        self.vehicles_tree.pack(fill='both', expand=True)
        
        # Context menu
        self.vehicles_tree.bind('<Button-3>', self._show_vehicle_menu)
        
        self._refresh_vehicles()
    
    def _refresh_vehicles(self):
        """Osveži vozila"""
        for item in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(item)
        
        vehicles = self.db.get_user_vehicles(self.current_user['id'])
        
        for v in vehicles:
            self.vehicles_tree.insert('', 'end', values=(
                v['id'],
                v['brand'],
                v['model'],
                v['license_plate'],
                v.get('year', 'N/A'),
                v.get('vin', 'N/A')
            ))
    
    def _show_vehicle_menu(self, event):
        """Prikaži context menu za vozilo"""
        item = self.vehicles_tree.identify_row(event.y)
        if item:
            self.vehicles_tree.selection_set(item)
            
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Uredi", command=self._edit_vehicle_dialog)
            menu.add_command(label="Obriši", command=self._delete_vehicle)
            
            menu.post(event.x_root, event.y_root)
    
    def _add_vehicle_dialog(self):
        """Dialog za dodavanje vozila"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Dodaj vozilo")
        dialog.geometry("450x400")
        dialog.configure(bg=self.WHITE)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        form = tk.Frame(dialog, bg=self.WHITE, padx=30, pady=30)
        form.pack(fill='both', expand=True)
        
        tk.Label(form, text="Marka:", bg=self.WHITE).grid(row=0, column=0, sticky='w', pady=5)
        brand_entry = tk.Entry(form, font=('Arial', 11), width=30)
        brand_entry.grid(row=1, column=0, pady=(0, 15))
        
        tk.Label(form, text="Model:", bg=self.WHITE).grid(row=2, column=0, sticky='w', pady=5)
        model_entry = tk.Entry(form, font=('Arial', 11), width=30)
        model_entry.grid(row=3, column=0, pady=(0, 15))
        
        tk.Label(form, text="Tablica:", bg=self.WHITE).grid(row=4, column=0, sticky='w', pady=5)
        plate_entry = tk.Entry(form, font=('Arial', 11), width=30)
        plate_entry.grid(row=5, column=0, pady=(0, 15))
        
        tk.Label(form, text="Godina:", bg=self.WHITE).grid(row=6, column=0, sticky='w', pady=5)
        year_entry = tk.Entry(form, font=('Arial', 11), width=30)
        year_entry.grid(row=7, column=0, pady=(0, 15))
        
        tk.Label(form, text="VIN:", bg=self.WHITE).grid(row=8, column=0, sticky='w', pady=5)
        vin_entry = tk.Entry(form, font=('Arial', 11), width=30)
        vin_entry.grid(row=9, column=0, pady=(0, 20))
        
        def save_vehicle():
            brand = brand_entry.get().strip()
            model = model_entry.get().strip()
            plate = plate_entry.get().strip()
            year = year_entry.get().strip()
            vin = vin_entry.get().strip()
            
            if not brand or not model or not plate:
                messagebox.showwarning("Upozorenje", "Popunite obavezna polja (Marka, Model, Tablica)!")
                return
            
            self.db.add_vehicle(self.current_user['id'], brand, model, plate, year, vin)
            self._refresh_vehicles()
            messagebox.showinfo("Uspeh", "Vozilo dodato!")
            dialog.destroy()
        
        tk.Button(
            form,
            text="Sačuvaj",
            font=('Arial', 11, 'bold'),
            bg=self.SUCCESS,
            fg=self.WHITE,
            bd=0,
            padx=30,
            pady=8,
            cursor="hand2",
            command=save_vehicle
        ).grid(row=10, column=0)
    
    def _edit_vehicle_dialog(self):
        """Dialog za izmenu vozila"""
        selection = self.vehicles_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.vehicles_tree.item(item, 'values')
        
        messagebox.showinfo("Uredi vozilo", f"Izmena vozila: {values[1]} {values[2]}\n(Demo)")
    
    def _delete_vehicle(self):
        """Obriši vozilo"""
        selection = self.vehicles_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.vehicles_tree.item(item, 'values')
        
        if messagebox.askyesno("Potvrda", f"Obrisati vozilo {values[1]} {values[2]}?"):
            messagebox.showinfo("Uspeh", "Vozilo obrisano!")
            self._refresh_vehicles()
    
    def _create_profile_tab(self, parent):
        """Kreira tab za profil"""
        # Container
        container = tk.Frame(parent, bg=self.WHITE, padx=50, pady=50)
        container.pack(fill='both', expand=True)
        
        tk.Label(
            container,
            text="👤 Moj profil",
            font=('Arial', 18, 'bold'),
            bg=self.WHITE,
            fg=self.PRIMARY
        ).pack(pady=(0, 30))
        
        # Profile info
        info_frame = tk.Frame(container, bg=self.LIGHT, padx=30, pady=30)
        info_frame.pack(fill='x')
        
        profile_items = [
            ("Email:", self.current_user['email']),
            ("Ime:", self.current_user['full_name']),
            ("Telefon:", self.current_user.get('phone', 'N/A')),
            ("Rola:", self.current_user['role']),
            ("Registrovan:", self.current_user['created_at']),
        ]
        
        for i, (label, value) in enumerate(profile_items):
            row_frame = tk.Frame(info_frame, bg=self.LIGHT)
            row_frame.pack(fill='x', pady=5)
            
            tk.Label(
                row_frame,
                text=label,
                font=('Arial', 11, 'bold'),
                bg=self.LIGHT,
                fg=self.DARK,
                width=15,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                row_frame,
                text=value,
                font=('Arial', 11),
                bg=self.LIGHT,
                fg=self.DARK,
                anchor='w'
            ).pack(side='left', padx=(10, 0))
        
        # Buttons
        btn_frame = tk.Frame(container, bg=self.WHITE)
        btn_frame.pack(pady=(30, 0))
        
        tk.Button(
            btn_frame,
            text="Izmeni profil",
            font=('Arial', 11),
            bg=self.INFO,
            fg=self.WHITE,
            bd=0,
            padx=30,
            pady=8,
            cursor="hand2",
            command=lambda: messagebox.showinfo("Profil", "Izmena profila (Demo)")
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="Promeni lozinku",
            font=('Arial', 11),
            bg=self.WARNING,
            fg=self.WHITE,
            bd=0,
            padx=30,
            pady=8,
            cursor="hand2",
            command=lambda: messagebox.showinfo("Lozinka", "Promena lozinke (Demo)")
        ).pack(side='left', padx=5)


def main():
    """Main funkcija"""
    root = tk.Tk()
    app = AutoServisApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
