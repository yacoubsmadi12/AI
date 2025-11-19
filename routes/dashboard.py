from flask import Blueprint, render_template, session
from routes.auth import login_required

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
@login_required
def show_dashboard():
    role = session.get('role', 'User')
    
    if role == 'Admin':
        return render_template('dashboard_admin.html', role=role, username=session.get('username'))
    elif role == 'Manager':
        return render_template('dashboard_manager.html', role=role, username=session.get('username'))
    elif role == 'Analyst':
        return render_template('dashboard_analyst.html', role=role, username=session.get('username'))
    else:
        return render_template('dashboard_user.html', role=role, username=session.get('username'))
