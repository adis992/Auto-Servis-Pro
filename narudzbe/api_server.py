"""
Auto Servis Pro - REST API Server
Kompletan Flask API server sa svim endpointima za Auto Servis Pro aplikaciju
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from datetime import datetime
import secrets
import os
from database import AutoServiceDB

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
CORS(app)

# Initialize database
db = AutoServiceDB()

# Active sessions storage (in production use Redis or similar)
active_sessions = {}


# ==================== DECORATORS ====================

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token required'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        if token not in active_sessions:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        request.current_user = active_sessions[token]
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token required'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        if token not in active_sessions:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = active_sessions[token]
        if user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROOT & HEALTH ====================

@app.route('/', methods=['GET'])
def index():
    """API documentation."""
    return jsonify({
        'name': 'Auto Servis Pro API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'POST /api/auth/login': 'Login user',
                'POST /api/auth/register': 'Register new user'
            },
            'services': {
                'GET /api/services': 'Get all services',
                'POST /api/services': 'Create new service (admin)',
                'PUT /api/services/<id>': 'Update service (admin)',
                'DELETE /api/services/<id>': 'Delete service (admin)'
            },
            'appointments': {
                'GET /api/appointments': 'Get appointments',
                'POST /api/appointments': 'Create new appointment',
                'PUT /api/appointments/<id>': 'Update appointment',
                'DELETE /api/appointments/<id>': 'Cancel appointment'
            },
            'vehicles': {
                'GET /api/vehicles': 'Get user vehicles',
                'POST /api/vehicles': 'Add new vehicle'
            },
            'notifications': {
                'GET /api/notifications': 'Get user notifications',
                'PUT /api/notifications/<id>/read': 'Mark notification as read',
                'POST /api/notifications/broadcast': 'Broadcast notification (admin)'
            },
            'settings': {
                'GET /api/settings': 'Get settings',
                'POST /api/settings': 'Update settings (admin)'
            },
            'health': {
                'GET /api/health': 'Health check'
            }
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        conn = db.get_connection()
        conn.close()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500


# ==================== AUTH ENDPOINTS ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login endpoint."""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Verify user
        user = db.verify_user(username, password)
        
        if not user:
            # Try login with email
            user = db.verify_user_by_email(username, password)
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token
        token = secrets.token_urlsafe(32)
        active_sessions[token] = user
        
        return jsonify({
            'success': True,
            'token': token,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user endpoint."""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        phone = data.get('phone')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email and password required'}), 400
        
        # Create user
        user_id = db.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            phone=phone
        )
        
        if user_id:
            # Get created user
            user = db.get_user_by_id(user_id)
            
            # Generate token
            token = secrets.token_urlsafe(32)
            active_sessions[token] = user
            
            return jsonify({
                'success': True,
                'token': token,
                'user': user
            }), 201
        else:
            return jsonify({'error': 'User already exists'}), 409
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== SERVICES ENDPOINTS ====================

@app.route('/api/services', methods=['GET'])
def get_services():
    """Get all services."""
    try:
        services = db.get_all_services()
        return jsonify({
            'success': True,
            'services': services
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/services', methods=['POST'])
@require_admin
def create_service():
    """Create new service (admin only)."""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        duration_minutes = data.get('duration_minutes', 60)
        category = data.get('category')
        
        if not name or price is None:
            return jsonify({'error': 'Name and price required'}), 400
        
        service_id = db.create_service(
            name=name,
            description=description,
            price=float(price),
            duration_minutes=int(duration_minutes),
            category=category
        )
        
        if service_id:
            service = db.get_service_by_id(service_id)
            return jsonify({
                'success': True,
                'service': service
            }), 201
        else:
            return jsonify({'error': 'Failed to create service'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/services/<int:service_id>', methods=['PUT'])
@require_admin
def update_service(service_id):
    """Update service (admin only)."""
    try:
        data = request.get_json()
        
        success = db.update_service(
            service_id=service_id,
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            duration_minutes=data.get('duration_minutes'),
            category=data.get('category'),
            is_active=data.get('is_active')
        )
        
        if success:
            service = db.get_service_by_id(service_id)
            return jsonify({
                'success': True,
                'service': service
            }), 200
        else:
            return jsonify({'error': 'Service not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/services/<int:service_id>', methods=['DELETE'])
@require_admin
def delete_service(service_id):
    """Delete service (admin only)."""
    try:
        success = db.delete_service(service_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Service deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Service not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== APPOINTMENTS ENDPOINTS ====================

@app.route('/api/appointments', methods=['GET'])
@require_auth
def get_appointments():
    """Get appointments."""
    try:
        user = request.current_user
        
        # Admin can see all appointments
        if user.get('role') == 'admin':
            appointments = db.get_all_appointments()
        else:
            appointments = db.get_user_appointments(user['id'])
        
        return jsonify({
            'success': True,
            'appointments': appointments
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/appointments', methods=['POST'])
@require_auth
def create_appointment():
    """Create new appointment."""
    try:
        data = request.get_json()
        user = request.current_user
        
        vehicle_id = data.get('vehicle_id')
        service_id = data.get('service_id')
        appointment_date = data.get('appointment_date')
        notes = data.get('notes')
        
        if not vehicle_id or not service_id or not appointment_date:
            return jsonify({'error': 'Vehicle, service and date required'}), 400
        
        appointment_id = db.create_appointment(
            user_id=user['id'],
            vehicle_id=int(vehicle_id),
            service_id=int(service_id),
            appointment_date=appointment_date,
            notes=notes
        )
        
        if appointment_id:
            appointment = db.get_appointment_by_id(appointment_id)
            
            # Create notification
            db.create_notification(
                user_id=user['id'],
                title='Appointment Confirmed',
                message=f'Your appointment has been scheduled for {appointment_date}',
                notification_type='appointment',
                related_appointment_id=appointment_id
            )
            
            return jsonify({
                'success': True,
                'appointment': appointment
            }), 201
        else:
            return jsonify({'error': 'Failed to create appointment'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
@require_auth
def update_appointment(appointment_id):
    """Update appointment."""
    try:
        data = request.get_json()
        user = request.current_user
        
        # Get appointment to verify ownership
        appointment = db.get_appointment_by_id(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Only owner or admin can update
        if user['role'] != 'admin' and appointment['user_id'] != user['id']:
            return jsonify({'error': 'Not authorized'}), 403
        
        success = db.update_appointment(
            appointment_id=appointment_id,
            appointment_date=data.get('appointment_date'),
            status=data.get('status'),
            notes=data.get('notes'),
            technician_notes=data.get('technician_notes'),
            total_price=data.get('total_price')
        )
        
        if success:
            appointment = db.get_appointment_by_id(appointment_id)
            return jsonify({
                'success': True,
                'appointment': appointment
            }), 200
        else:
            return jsonify({'error': 'Failed to update appointment'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
@require_auth
def cancel_appointment(appointment_id):
    """Cancel appointment."""
    try:
        user = request.current_user
        
        # Get appointment to verify ownership
        appointment = db.get_appointment_by_id(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Only owner or admin can cancel
        if user['role'] != 'admin' and appointment['user_id'] != user['id']:
            return jsonify({'error': 'Not authorized'}), 403
        
        success = db.update_appointment(
            appointment_id=appointment_id,
            status='cancelled'
        )
        
        if success:
            # Create notification
            db.create_notification(
                user_id=appointment['user_id'],
                title='Appointment Cancelled',
                message=f'Your appointment has been cancelled',
                notification_type='appointment',
                related_appointment_id=appointment_id
            )
            
            return jsonify({
                'success': True,
                'message': 'Appointment cancelled successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to cancel appointment'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== VEHICLES ENDPOINTS ====================

@app.route('/api/vehicles', methods=['GET'])
@require_auth
def get_vehicles():
    """Get user vehicles."""
    try:
        user = request.current_user
        vehicles = db.get_user_vehicles(user['id'])
        
        return jsonify({
            'success': True,
            'vehicles': vehicles
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/vehicles', methods=['POST'])
@require_auth
def create_vehicle():
    """Add new vehicle."""
    try:
        data = request.get_json()
        user = request.current_user
        
        make = data.get('make')
        model = data.get('model')
        year = data.get('year')
        vin = data.get('vin')
        license_plate = data.get('license_plate')
        color = data.get('color')
        engine_type = data.get('engine_type')
        mileage = data.get('mileage')
        notes = data.get('notes')
        
        if not make or not model:
            return jsonify({'error': 'Make and model required'}), 400
        
        vehicle_id = db.create_vehicle(
            user_id=user['id'],
            make=make,
            model=model,
            year=year,
            vin=vin,
            license_plate=license_plate,
            color=color,
            engine_type=engine_type,
            mileage=mileage,
            notes=notes
        )
        
        if vehicle_id:
            vehicle = db.get_vehicle_by_id(vehicle_id)
            return jsonify({
                'success': True,
                'vehicle': vehicle
            }), 201
        else:
            return jsonify({'error': 'Failed to create vehicle'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== NOTIFICATIONS ENDPOINTS ====================

@app.route('/api/notifications', methods=['GET'])
@require_auth
def get_notifications():
    """Get user notifications."""
    try:
        user = request.current_user
        notifications = db.get_user_notifications(user['id'])
        
        return jsonify({
            'success': True,
            'notifications': notifications
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications/<int:notification_id>/read', methods=['PUT'])
@require_auth
def mark_notification_read(notification_id):
    """Mark notification as read."""
    try:
        user = request.current_user
        
        # Get notification to verify ownership
        notification = db.get_notification_by_id(notification_id)
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        if notification['user_id'] != user['id']:
            return jsonify({'error': 'Not authorized'}), 403
        
        success = db.mark_notification_read(notification_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Notification marked as read'
            }), 200
        else:
            return jsonify({'error': 'Failed to update notification'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications/broadcast', methods=['POST'])
@require_admin
def broadcast_notification():
    """Broadcast notification to all users (admin only)."""
    try:
        data = request.get_json()
        title = data.get('title')
        message = data.get('message')
        notification_type = data.get('notification_type', 'info')
        
        if not title or not message:
            return jsonify({'error': 'Title and message required'}), 400
        
        # Get all active users
        users = db.get_all_users()
        count = 0
        
        for user in users:
            if user.get('is_active'):
                db.create_notification(
                    user_id=user['id'],
                    title=title,
                    message=message,
                    notification_type=notification_type
                )
                count += 1
        
        return jsonify({
            'success': True,
            'message': f'Notification sent to {count} users'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== SETTINGS ENDPOINTS ====================

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get settings."""
    try:
        settings = db.get_all_settings()
        
        # Convert to dict for easier access
        settings_dict = {s['key']: s['value'] for s in settings}
        
        return jsonify({
            'success': True,
            'settings': settings_dict
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/settings', methods=['POST'])
@require_admin
def update_settings():
    """Update settings (admin only)."""
    try:
        data = request.get_json()
        
        if not isinstance(data, dict):
            return jsonify({'error': 'Settings must be a dictionary'}), 400
        
        for key, value in data.items():
            db.set_setting(key, value)
        
        return jsonify({
            'success': True,
            'message': 'Settings updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'path': request.path
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 60)
    print("Auto Servis Pro API Server")
    print("=" * 60)
    print("Server starting on http://localhost:7000")
    print("API Documentation: http://localhost:7000/")
    print("Health Check: http://localhost:7000/api/health")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=7000,
        debug=False
    )
