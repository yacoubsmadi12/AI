from flask import Blueprint, jsonify, request
import database

bp = Blueprint('logs_api', __name__, url_prefix='/api')

@bp.route('/logs', methods=['GET'])
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
