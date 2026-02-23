import sys
sys.path.insert(0, 'narudzbe')
from api_server import app, db

print("=" * 60)
print("Auto Servis Pro API Server")
print("=" * 60)
print("Server starting on http://localhost:7000")
print("API Documentation: http://localhost:7000/")
print("Health Check: http://localhost:7000/api/health")
print("=" * 60)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=False,
        use_reloader=False
    )
