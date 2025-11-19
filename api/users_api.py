from flask import Blueprint, jsonify, request, session
import database
from routes.auth import login_required, role_required

bp = Blueprint('users_api', __name__, url_prefix='/api')

@bp.route('/users', methods=['GET'])
@login_required
@role_required(['Admin', 'Manager'])
def get_users():
    users = database.get_all_users()
    
    users_list = []
    for user in users:
        users_list.append({
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'group_id': user['group_id'],
            'created_at': user['created_at'].isoformat() if user['created_at'] else None,
            'last_login': user['last_login'].isoformat() if user['last_login'] else None,
            'is_active': user['is_active']
        })
    
    return jsonify(users_list)

@bp.route('/users/add', methods=['POST'])
@login_required
@role_required(['Admin'])
def add_user_api():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    group_id = data.get('group_id')
    
    if not all([username, email, password, role]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        user_id = database.create_user(username, email, password, role, group_id)
        return jsonify({'success': True, 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
