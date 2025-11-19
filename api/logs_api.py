from flask import Blueprint, jsonify, request, session
import database
from routes.auth import login_required, role_required

bp = Blueprint('logs_api', __name__, url_prefix='/api')

@bp.route('/logs', methods=['GET'])
@login_required
@role_required(['Admin', 'Manager', 'Analyst'])
def get_logs():
    limit = request.args.get('limit', 100, type=int)
    severity = request.args.get('severity')
    
    if severity:
        logs = database.get_logs_by_severity(severity, limit)
    else:
        logs = database.get_latest_logs(limit)
    
    logs_list = []
    for log in logs:
        logs_list.append({
            'id': log['id'],
            'timestamp': log['timestamp'].isoformat() if log['timestamp'] else None,
            'severity': log['severity'],
            'source_ip': log['source_ip'],
            'source_host': log['source_host'],
            'event_type': log['event_type'],
            'message': log['message']
        })
    
    return jsonify(logs_list)

@bp.route('/logs/latest', methods=['GET'])
@login_required
@role_required(['Admin', 'Manager', 'Analyst'])
def get_latest_logs():
    limit = request.args.get('limit', 20, type=int)
    logs = database.get_latest_logs(limit)
    
    logs_list = []
    for log in logs:
        logs_list.append({
            'id': log['id'],
            'timestamp': log['timestamp'].isoformat() if log['timestamp'] else None,
            'severity': log['severity'],
            'source_ip': log['source_ip'],
            'source_host': log['source_host'],
            'event_type': log['event_type'],
            'message': log['message']
        })
    
    return jsonify(logs_list)

@bp.route('/ingest', methods=['POST'])
def ingest_logs():
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'API key required'}), 401
    
    source = database.verify_api_key(api_key)
    if not source:
        return jsonify({'error': 'Invalid API key'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    logs = data if isinstance(data, list) else [data]
    
    inserted_count = 0
    errors = []
    
    for idx, log in enumerate(logs):
        try:
            severity = log.get('severity', 'INFO').upper()
            message = log.get('message', '')
            
            if not message:
                errors.append(f"Log {idx}: message is required")
                continue
            
            source_ip = log.get('source_ip') or log.get('host')
            source_host = log.get('source_host') or log.get('hostname')
            event_type = log.get('event_type') or log.get('type')
            raw_log = log.get('raw_log') or str(log)
            
            database.insert_log_event_with_source(
                severity=severity,
                message=message,
                source_id=source['id'],
                source_ip=source_ip,
                source_host=source_host,
                event_type=event_type,
                raw_log=raw_log
            )
            inserted_count += 1
        except Exception as e:
            import logging
            logging.error(f"Failed to ingest log {idx}: {str(e)}")
            errors.append(f"Log {idx}: {str(e)}")
            continue
    
    response = {
        'status': 'success' if inserted_count > 0 else 'error',
        'inserted': inserted_count,
        'total': len(logs)
    }
    
    if errors:
        response['errors'] = errors[:10]
        response['error_count'] = len(errors)
    
    return jsonify(response), 201 if inserted_count > 0 else 400

@bp.route('/syslog', methods=['POST'])
def receive_syslog():
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'API key required'}), 401
    
    source = database.verify_api_key(api_key)
    if not source:
        return jsonify({'error': 'Invalid API key'}), 403
    
    raw_data = request.data.decode('utf-8')
    
    if not raw_data:
        return jsonify({'error': 'No data provided'}), 400
    
    if not raw_data.strip():
        return jsonify({'error': 'Empty syslog data'}), 400
    
    try:
        database.insert_log_event_with_source(
            severity='INFO',
            message=raw_data[:500],
            source_id=source['id'],
            source_ip=source.get('source_ip'),
            source_host=source.get('name'),
            event_type='SYSLOG',
            raw_log=raw_data
        )
        
        return jsonify({'status': 'success', 'message': 'Syslog event received'}), 201
    except Exception as e:
        import logging
        logging.error(f"Syslog ingestion failed: {str(e)}")
        return jsonify({'error': f'Failed to process syslog: {str(e)}'}), 500
