import sqlite3

conn = sqlite3.connect('narudzbe/autoservice.db')
c = conn.cursor()

print("\n" + "="*50)
print("  AUTO SERVIS PRO - PROVJERA BAZE")
print("="*50 + "\n")

# Servisi
c.execute('SELECT COUNT(*) FROM services')
print(f"✅ Servisi: {c.fetchone()[0]}")

# Tipovi vozila
c.execute('SELECT COUNT(*) FROM vehicle_types')
print(f"✅ Tipovi vozila: {c.fetchone()[0]}")

# Korisnici
c.execute('SELECT COUNT(*) FROM users')
print(f"✅ Korisnici: {c.fetchone()[0]}")

print("\n" + "-"*50)
print("  KORISNICI:")
print("-"*50)
c.execute('SELECT username, email, role FROM users')
for u in c.fetchall():
    print(f"  👤 {u[0]} ({u[1]}) - {u[2]}")

print("\n" + "-"*50)
print("  TIPOVI VOZILA (prvih 6):")
print("-"*50)
c.execute('SELECT name, icon FROM vehicle_types LIMIT 6')
for v in c.fetchall():
    print(f"  {v[1]} {v[0]}")

print("\n" + "-"*50)
print("  SERVISI (prvih 10):")
print("-"*50)
c.execute('SELECT name, price, category FROM services LIMIT 10')
for s in c.fetchall():
    print(f"  🔧 {s[0]} - {s[1]} KM ({s[2]})")

conn.close()

print("\n" + "="*50)
print("  PROVJERA ZAVRŠENA ✅")
print("="*50 + "\n")
