from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from routes.auth import login_required, role_required
import database

bp = Blueprint('users', __name__)

@bp.route('/users')
@login_required
@role_required(['Admin', 'Manager'])
def list_users():
    users = database.get_all_users()
    groups = database.get_all_groups()
    return render_template('users.html', users=users, groups=groups)

@bp.route('/users/add', methods=['POST'])
@login_required
@role_required(['Admin'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    group_id = request.form.get('group_id')
    
    if group_id == '':
        group_id = None
    
    try:
        database.create_user(username, email, password, role, group_id)
        flash('User created successfully', 'success')
    except Exception as e:
        flash(f'Error creating user: {str(e)}', 'error')
    
    return redirect(url_for('users.list_users'))

@bp.route('/users/edit/<int:user_id>', methods=['POST'])
@login_required
@role_required(['Admin'])
def edit_user(user_id):
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    group_id = request.form.get('group_id')
    is_active = request.form.get('is_active') == 'on'
    
    if group_id == '':
        group_id = None
    
    try:
        database.update_user(user_id, username=username, email=email, role=role, group_id=group_id, is_active=is_active)
        flash('User updated successfully', 'success')
    except Exception as e:
        flash(f'Error updating user: {str(e)}', 'error')
    
    return redirect(url_for('users.list_users'))

@bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@role_required(['Admin'])
def delete_user(user_id):
    try:
        database.delete_user(user_id)
        flash('User deactivated successfully', 'success')
    except Exception as e:
        flash(f'Error deactivating user: {str(e)}', 'error')
    
    return redirect(url_for('users.list_users'))
