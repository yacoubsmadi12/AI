from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import database

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = database.get_user_by_username(username)
        
        if user and database.verify_password(password, user['password_hash']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['group_id'] = user['group_id']
            
            database.update_last_login(user['id'])
            
            return redirect(url_for('dashboard.show_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    from functools import wraps
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                flash('You do not have permission to access this page', 'error')
                return redirect(url_for('dashboard.show_dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
