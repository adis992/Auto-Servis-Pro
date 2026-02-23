"""
Auto Servis Pro - Mobilna Aplikacija (Kivy)
Jednostavna verzija za Android/iOS
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import sys
import os

# Dodaj narudzbe u path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'narudzbe'))

from narudzbe.database import AutoServiceDB

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Logo
        layout.add_widget(Label(text='🚗 Auto Servis Pro', font_size='32sp', size_hint_y=0.2))
        
        # Username input
        self.username_input = TextInput(hint_text='Username ili Email', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.username_input)
        
        # Password input
        self.password_input = TextInput(hint_text='Lozinka', password=True, multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.password_input)
        
        # Login button
        login_btn = Button(text='Prijavi se', size_hint_y=None, height=50, background_color=(0.4, 0.5, 0.9, 1))
        login_btn.bind(on_press=self.do_login)
        layout.add_widget(login_btn)
        
        # Register button
        register_btn = Button(text='Registruj se', size_hint_y=None, height=50, background_color=(0.5, 0.7, 0.5, 1))
        register_btn.bind(on_press=self.go_register)
        layout.add_widget(register_btn)
        
        # Error label
        self.error_label = Label(text='', color=(1, 0, 0, 1), size_hint_y=0.2)
        layout.add_widget(self.error_label)
        
        # Demo info
        layout.add_widget(Label(text='💡 Demo: admin/admin123 ili user/user123', font_size='12sp', size_hint_y=0.2))
        
        self.add_widget(layout)
    
    def do_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        
        if not username or not password:
            self.error_label.text = 'Unesi username i lozinku!'
            return
        
        db = AutoServiceDB()
        user = db.verify_user(username, password)
        
        if user:
            app = App.get_running_app()
            app.current_user = user
            self.manager.current = 'dashboard'
        else:
            self.error_label.text = 'Pogrešno korisničko ime ili lozinka!'
    
    def go_register(self, instance):
        self.manager.current = 'register'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text='Registracija', font_size='28sp', size_hint_y=0.15))
        
        self.email_input = TextInput(hint_text='Email (obavezno)', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.email_input)
        
        self.username_input = TextInput(hint_text='Username', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.username_input)
        
        self.password_input = TextInput(hint_text='Lozinka', password=True, multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.password_input)
        
        self.fullname_input = TextInput(hint_text='Puno ime', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.fullname_input)
        
        register_btn = Button(text='Registruj se', size_hint_y=None, height=50, background_color=(0.5, 0.7, 0.5, 1))
        register_btn.bind(on_press=self.do_register)
        layout.add_widget(register_btn)
        
        back_btn = Button(text='Nazad', size_hint_y=None, height=50, background_color=(0.7, 0.7, 0.7, 1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.error_label = Label(text='', color=(1, 0, 0, 1), size_hint_y=0.2)
        layout.add_widget(self.error_label)
        
        self.add_widget(layout)
    
    def do_register(self, instance):
        email = self.email_input.text
        username = self.username_input.text
        password = self.password_input.text
        fullname = self.fullname_input.text
        
        if not email or not username or not password:
            self.error_label.text = 'Email, username i lozinka su obavezni!'
            return
        
        db = AutoServiceDB()
        success, message, user_id = db.register_user(
            username=username,
            email=email,
            password=password,
            full_name=fullname
        )
        
        if success:
            self.error_label.text = ''
            self.error_label.color = (0, 1, 0, 1)
            self.error_label.text = '✅ Registracija uspješna!'
            self.manager.current = 'login'
        else:
            self.error_label.color = (1, 0, 0, 1)
            self.error_label.text = message
    
    def go_back(self, instance):
        self.manager.current = 'login'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)
    
    def on_enter(self):
        self.layout.clear_widgets()
        
        app = App.get_running_app()
        user = app.current_user
        
        # Header
        header = Label(text=f"Dobrodošao, {user.get('full_name', user['username'])}!", font_size='24sp', size_hint_y=0.1)
        self.layout.add_widget(header)
        
        # Menu buttons
        menu = GridLayout(cols=2, spacing=10, size_hint_y=0.7)
        
        buttons = [
            ('📅 Termini', self.show_appointments),
            ('🚗 Vozila', self.show_vehicles),
            ('🔔 Notifikacije', self.show_notifications),
            ('👤 Profil', self.show_profile),
        ]
        
        for text, callback in buttons:
            btn = Button(text=text, font_size='18sp')
            btn.bind(on_press=callback)
            menu.add_widget(btn)
        
        self.layout.add_widget(menu)
        
        # Logout button
        logout_btn = Button(text='Odjavi se', size_hint_y=0.1, background_color=(0.8, 0.3, 0.3, 1))
        logout_btn.bind(on_press=self.logout)
        self.layout.add_widget(logout_btn)
    
    def show_appointments(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='📅 Termini', font_size='24sp', size_hint_y=0.1))
        
        db = AutoServiceDB()
        app = App.get_running_app()
        appointments = db.get_user_appointments(app.current_user['id'])
        
        scroll = ScrollView(size_hint_y=0.8)
        grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        if appointments:
            for apt in appointments:
                btn = Button(
                    text=f"{apt['appointment_date']}\n{apt.get('service_name', 'N/A')} - {apt['status']}",
                    size_hint_y=None,
                    height=80
                )
                grid.add_widget(btn)
        else:
            grid.add_widget(Label(text='Nema termina', size_hint_y=None, height=50))
        
        scroll.add_widget(grid)
        self.layout.add_widget(scroll)
        
        back_btn = Button(text='Nazad', size_hint_y=0.1)
        back_btn.bind(on_press=lambda x: self.on_enter())
        self.layout.add_widget(back_btn)
    
    def show_vehicles(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='🚗 Vozila', font_size='24sp', size_hint_y=0.1))
        self.layout.add_widget(Label(text='Funkcija u razvoju...', size_hint_y=0.8))
        
        back_btn = Button(text='Nazad', size_hint_y=0.1)
        back_btn.bind(on_press=lambda x: self.on_enter())
        self.layout.add_widget(back_btn)
    
    def show_notifications(self, instance):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='🔔 Notifikacije', font_size='24sp', size_hint_y=0.1))
        
        db = AutoServiceDB()
        app = App.get_running_app()
        notifications = db.get_user_notifications(app.current_user['id'])
        
        scroll = ScrollView(size_hint_y=0.8)
        grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        if notifications:
            for notif in notifications:
                is_read = '✓' if notif['is_read'] else '●'
                btn = Button(
                    text=f"{is_read} {notif['title']}\n{notif['message'][:50]}...",
                    size_hint_y=None,
                    height=80
                )
                grid.add_widget(btn)
        else:
            grid.add_widget(Label(text='Nema notifikacija', size_hint_y=None, height=50))
        
        scroll.add_widget(grid)
        self.layout.add_widget(scroll)
        
        back_btn = Button(text='Nazad', size_hint_y=0.1)
        back_btn.bind(on_press=lambda x: self.on_enter())
        self.layout.add_widget(back_btn)
    
    def show_profile(self, instance):
        self.layout.clear_widgets()
        app = App.get_running_app()
        user = app.current_user
        
        self.layout.add_widget(Label(text='👤 Profil', font_size='24sp', size_hint_y=0.1))
        
        info = BoxLayout(orientation='vertical', size_hint_y=0.8, padding=20, spacing=10)
        info.add_widget(Label(text=f"Username: {user['username']}", font_size='16sp'))
        info.add_widget(Label(text=f"Email: {user['email']}", font_size='16sp'))
        info.add_widget(Label(text=f"Ime: {user.get('full_name', 'N/A')}", font_size='16sp'))
        info.add_widget(Label(text=f"Telefon: {user.get('phone', 'N/A')}", font_size='16sp'))
        info.add_widget(Label(text=f"Role: {user['role']}", font_size='16sp'))
        
        self.layout.add_widget(info)
        
        back_btn = Button(text='Nazad', size_hint_y=0.1)
        back_btn.bind(on_press=lambda x: self.on_enter())
        self.layout.add_widget(back_btn)
    
    def logout(self, instance):
        app = App.get_running_app()
        app.current_user = None
        self.manager.current = 'login'

class AutoServisApp(App):
    current_user = None
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    AutoServisApp().run()
