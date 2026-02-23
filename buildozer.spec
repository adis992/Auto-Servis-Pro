[app]

# (str) Title aplikacije
title = Auto Servis Pro

# (str) Ime paketa
package.name = autoservispro

# (str) Domen paketa (jedinstveni identifikator)
package.domain = com.autoservis

# (str) Izvorni kod koji se uključuje
source.dir = .

# (list) Lista fajl ekstenzija koje se uključuju
source.include_exts = py,png,jpg,kv,atlas,db,ttf,txt

# (list) Lista direktorijuma koje se uključuju
source.include_patterns = narudzbe/*,narudzbe/web/*

# (str) Verzija aplikacije
version = 2.0

# (list) Python dependencies
requirements = python3,kivy,sqlite3,pillow

# (str) Custom source folders za requirements
# requirements.source.kivy = ../../kivy

# (list) Dozvoljene orijentacije
# (landscape, sensorLandscape, portrait, sensorPortrait)
orientation = portrait

# (bool) Indikuj da li app treba full screen
fullscreen = 0

# (list) Dozvole koje app zahtijeva
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API verzija
android.api = 33

# (int) Minimalna Android API verzija
android.minapi = 21

# (str) Android NDK verzija
android.ndk = 25b

# (bool) Ako True, pravi AAB umjesto APK
# android.release_artifact = aab

# (str) Android logcat filter tokom debuga
android.logcat_filters = *:S python:D

# (str) Android app tema
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Dodate Java klase
# android.add_src = 

# (list) Dodate Gradle dependencies
# android.gradle_dependencies = 

# (str) Ikona aplikacije
# icon.filename = %(source.dir)s/data/icon.png

# (str) Presplash pozadina (opciono)
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Bootstrap Python verzija
# android.bootstrap = sdl2

# (str) Python build verzija (Python 3.x)
android.python_version = 3

# (bool) Kopiraj library umjesto symlinkovanja
android.copy_libs = 1

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) Dodatne Java opcije
# android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) Dodatne compile opcije
# android.add_compile_options = 

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (sa svim command outputima))
log_level = 2

# (int) Prikaz upozorenja ako buildozer verzija nije najnovija
warn_on_root = 1

# (str) Put do Android SDK-a
# android.sdk_path = 

# (str) Put do Android NDK-a
# android.ndk_path = 

# (bool) Ako je True, pravi debug verziju aplikacije
# buildozer.debug = 1
