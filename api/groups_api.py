from flask import Blueprint, jsonify, request
import database

bp = Blueprint('groups_api', __name__, url_prefix='/api')

@bp.route('/groups', methods=['GET'])
def get_groups():
    groups = database.get_all_groups()
    
    groups_list = []
    for group in groups:
        groups_list.append({
            'id': group['id'],
            'name': group['name'],
            'description': group['description'],
            'created_at': group['created_at'].isoformat() if group['created_at'] else None
        })
    
    return jsonify(groups_list)

@bp.route('/groups/add', methods=['POST'])
def add_group_api():
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description', '')
    
    if not name:
        return jsonify({'error': 'Group name is required'}), 400
    
    try:
        group_id = database.create_group(name, description)
        return jsonify({'success': True, 'group_id': group_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
