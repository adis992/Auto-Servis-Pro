#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Servis Pro - Network Server
Servira web panel i API na mrezi za pristup sa drugih racunara
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import socket
import sys

# Import API routes from api_server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'narudzbe'))
from api_server import app as api_app

# Create main app that serves both web panel and API
app = Flask(__name__, static_folder='narudzbe/web', static_url_path='')
CORS(app)

# Register API blueprint from api_server
for rule in api_app.url_map.iter_rules():
    if rule.endpoint != 'static':
        app.add_url_rule(
            rule.rule,
            endpoint=rule.endpoint,
            view_func=api_app.view_functions[rule.endpoint],
            methods=rule.methods
        )

@app.route('/')
def serve_panel():
    """Serve main web panel"""
    return send_from_directory('narudzbe/web', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('narudzbe/web', path)

def get_local_ip():
    """Get local network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_local_ip()
    
    print("\n" + "=" * 70)
    print("   🚗 AUTO SERVIS PRO - NETWORK WEB PANEL")
    print("=" * 70)
    print("\n✅ SERVER POKRENUT!\n")
    print("📍 LOKALNI PRISTUP:")
    print(f"   http://localhost:7000")
    print(f"   http://127.0.0.1:7000\n")
    print("🌐 MREZNI PRISTUP (sa drugih PC):")
    print(f"   http://{local_ip}:7000\n")
    print("👤 DEMO NALOZI:")
    print("   Admin: admin / admin123")
    print("   User:  user / user123\n")
    print("💡 SAVJET:")
    print(f"   Daj kolegama IP adresu: {local_ip}:7000")
    print("   Oni mogu pristupiti sa bilo kog PC-a na istoj mrezi!\n")
    print("🛑 Pritisnite Ctrl+C za zaustavljanje servera")
    print("=" * 70 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=False,
        threaded=True
    )
