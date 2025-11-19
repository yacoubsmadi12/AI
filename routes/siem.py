from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required, role_required
import database
import random
from datetime import datetime, timedelta
import csv
import io
from werkzeug.utils import secure_filename

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

@bp.route('/upload-logs', methods=['GET', 'POST'])
@login_required
@role_required(['Admin', 'Manager'])
def upload_logs():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(request.url)
        
        file = request.files['csv_file']
        log_source_id = request.form.get('log_source_id')
        log_source_id = int(log_source_id) if log_source_id and log_source_id.isdigit() else None
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            try:
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_reader = csv.DictReader(stream)
                
                logs_data = []
                for row in csv_reader:
                    severity_map = {
                        'Minor': 'INFO',
                        'Warning': 'WARNING',
                        'Major': 'ERROR',
                        'Critical': 'CRITICAL'
                    }
                    
                    severity = severity_map.get(row.get('Level', 'Minor'), 'INFO')
                    
                    log_entry = {
                        'severity': severity,
                        'message': row.get('Operation', '') + ' - ' + row.get('Details', ''),
                        'source_ip': row.get('Terminal IP Address', ''),
                        'source_host': row.get('Source', ''),
                        'event_type': row.get('Operation', ''),
                        'raw_log': str(row),
                        'timestamp': row.get('Time') if row.get('Time') else None
                    }
                    logs_data.append(log_entry)
                
                inserted_count, errors = database.insert_bulk_logs(logs_data, log_source_id)
                
                if errors:
                    flash(f'Imported {inserted_count} log entries with {len(errors)} errors. First error: {errors[0] if errors else ""}', 'warning')
                else:
                    flash(f'Successfully imported {inserted_count} log entries from CSV', 'success')
                    
                return redirect(url_for('siem.siem_dashboard'))
                
            except Exception as e:
                flash(f'Error processing CSV file: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Please upload a CSV file', 'error')
            return redirect(request.url)
    
    log_sources = database.get_all_log_sources()
    return render_template('upload_logs.html', log_sources=log_sources)

@bp.route('/log-sources')
@login_required
@role_required(['Admin', 'Manager'])
def manage_log_sources():
    sources = database.get_all_log_sources()
    return render_template('log_sources.html', sources=sources)

@bp.route('/log-sources/create', methods=['POST'])
@login_required
@role_required(['Admin'])
def create_log_source():
    name = request.form.get('name')
    source_type = request.form.get('source_type')
    source_ip = request.form.get('source_ip')
    
    import secrets
    api_key = secrets.token_urlsafe(32)
    
    database.create_log_source(name, source_type, source_ip, api_key)
    flash(f'Log source created successfully. API Key: {api_key}', 'success')
    return redirect(url_for('siem.manage_log_sources'))
