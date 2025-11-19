from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
import database
import random
from datetime import datetime, timedelta

bp = Blueprint('siem', __name__)

@bp.route('/siem')
@login_required
def siem_dashboard():
    logs = database.get_latest_logs(50)
    return render_template('siem_dashboard.html', logs=logs)

@bp.route('/simulate-log', methods=['POST'])
@login_required
def simulate_log():
    severities = ['INFO', 'WARNING', 'ERROR', 'CRITICAL']
    event_types = ['LOGIN', 'LOGOUT', 'FILE_ACCESS', 'PERMISSION_CHANGE', 'SYSTEM_ERROR', 'NETWORK_EVENT']
    messages = [
        'User authentication successful',
        'Failed login attempt detected',
        'File permission modified',
        'Unusual network traffic detected',
        'System resource threshold exceeded',
        'Database connection established',
        'Service restart initiated',
        'Unauthorized access attempt blocked'
    ]
    
    severity = random.choice(severities)
    event_type = random.choice(event_types)
    message = random.choice(messages)
    source_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
    source_host = f"host-{random.randint(1,100)}"
    
    database.insert_log_event(
        severity=severity,
        message=message,
        source_ip=source_ip,
        source_host=source_host,
        event_type=event_type
    )
    
    flash(f'Simulated {severity} log event created', 'success')
    return redirect(url_for('siem.siem_dashboard'))

@bp.route('/generate-sample-logs', methods=['POST'])
@login_required
def generate_sample_logs():
    severities = ['INFO', 'WARNING', 'ERROR', 'CRITICAL']
    event_types = ['LOGIN', 'LOGOUT', 'FILE_ACCESS', 'PERMISSION_CHANGE', 'SYSTEM_ERROR', 'NETWORK_EVENT']
    messages = [
        'User authentication successful',
        'Failed login attempt detected',
        'File permission modified',
        'Unusual network traffic detected',
        'System resource threshold exceeded',
        'Database connection established',
        'Service restart initiated',
        'Unauthorized access attempt blocked',
        'SSL certificate validation failed',
        'Firewall rule updated'
    ]
    
    for _ in range(50):
        severity = random.choice(severities)
        event_type = random.choice(event_types)
        message = random.choice(messages)
        source_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
        source_host = f"host-{random.randint(1,100)}"
        
        database.insert_log_event(
            severity=severity,
            message=message,
            source_ip=source_ip,
            source_host=source_host,
            event_type=event_type
        )
    
    flash('Generated 50 sample log events', 'success')
    return redirect(url_for('siem.siem_dashboard'))
