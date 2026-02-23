#!/usr/bin/env python3
"""
Auto Servis Pro - Simple Web Server
Sluzi web interfejs na port 8000 bez potrebe za Flask
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Port za web interfejs
PORT = 8000

# Odredji web direktorijum
WEB_DIR = Path(__file__).parent / "web"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)
    
    def end_headers(self):
        # Dodaj CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    # Proveri da li web folder postoji
    if not WEB_DIR.exists():
        print(f"❌ ERROR: Web folder ne postoji: {WEB_DIR}")
        print(f"   Kreiraj folder 'web' sa index.html fajlom")
        sys.exit(1)

    # Proveri da li index.html postoji
    index_file = WEB_DIR / "index.html"
    if not index_file.exists():
        print(f"❌ ERROR: index.html ne postoji u: {WEB_DIR}")
        sys.exit(1)

    # Pokreni server
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print("\n" + "="*50)
            print("   AUTO SERVIS PRO - WEB INTERFACE")
            print("="*50)
            print(f"\n🌐 Web interfejs dostupan na:")
            print(f"   http://localhost:{PORT}")
            print(f"   http://127.0.0.1:{PORT}")
            print(f"\n📁 Servira fajlove iz: {WEB_DIR}")
            print(f"\n💡 Za API funkcionalnost pokreni api_server.py na port 7000")
            print(f"\n⚠️  Za zatvaranje pritisni CTRL+C\n")
            print("="*50 + "\n")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Web server zaustavljen")
        sys.exit(0)
    except OSError as e:
        if e.errno == 10048 or e.errno == 98:
            print(f"\n❌ ERROR: Port {PORT} je već u upotrebi!")
            print(f"   Zatvori drugi program ili promeni port")
        else:
            print(f"\n❌ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
