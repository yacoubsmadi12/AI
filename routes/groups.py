from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required, role_required
import database

bp = Blueprint('groups', __name__)

@bp.route('/groups')
@login_required
@role_required(['Admin', 'Manager'])
def list_groups():
    groups = database.get_all_groups()
    groups_with_perms = []
    
    for group in groups:
        perms = database.get_permissions_by_group(group['id'])
        groups_with_perms.append({
            'group': group,
            'permissions': perms
        })
    
    return render_template('groups.html', groups=groups_with_perms)

@bp.route('/groups/add', methods=['POST'])
@login_required
@role_required(['Admin'])
def add_group():
    name = request.form.get('name')
    description = request.form.get('description')
    
    try:
        database.create_group(name, description)
        flash('Group created successfully', 'success')
    except Exception as e:
        flash(f'Error creating group: {str(e)}', 'error')
    
    return redirect(url_for('groups.list_groups'))

@bp.route('/groups/<int:group_id>/permissions/add', methods=['POST'])
@login_required
@role_required(['Admin'])
def add_permission(group_id):
    permission_name = request.form.get('permission_name')
    can_create = request.form.get('can_create') == 'on'
    can_read = request.form.get('can_read') == 'on'
    can_update = request.form.get('can_update') == 'on'
    can_delete = request.form.get('can_delete') == 'on'
    
    try:
        database.create_permission(group_id, permission_name, can_create, can_read, can_update, can_delete)
        flash('Permission created successfully', 'success')
    except Exception as e:
        flash(f'Error creating permission: {str(e)}', 'error')
    
    return redirect(url_for('groups.list_groups'))
