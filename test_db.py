import sys
sys.path.insert(0, 'narudzbe')
try:
    from database import AutoServiceDB
    print("✅ Database module OK")
    db = AutoServiceDB()
    print("✅ Database initialized")
    services = db.get_all_services()
    print(f"✅ {len(services)} services loaded")
    users = db.get_all_users()
    print(f"✅ {len(users)} users loaded")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
