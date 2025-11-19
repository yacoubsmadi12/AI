from flask import Blueprint, jsonify, request, session
from datetime import datetime
import database
from routes.auth import login_required, role_required

bp = Blueprint('reports_api', __name__, url_prefix='/api')

@bp.route('/daily-report', methods=['GET'])
@login_required
@role_required(['Admin', 'Manager'])
def get_daily_report_api():
    group_id = request.args.get('group')
    date_str = request.args.get('date')
    
    if not group_id:
        return jsonify({'error': 'Group ID is required'}), 400
    
    try:
        group_id = int(group_id)
    except ValueError:
        return jsonify({'error': 'Invalid group ID'}), 400
    
    if date_str:
        try:
            report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    else:
        report_date = None
    
    report = database.get_daily_report(group_id, report_date)
    
    if not report:
        database.generate_daily_report(group_id)
        report = database.get_daily_report(group_id, report_date)
    
    if report:
        return jsonify({
            'id': report['id'],
            'group_id': report['group_id'],
            'report_date': report['report_date'].isoformat() if report['report_date'] else None,
            'total_users': report['total_users'],
            'active_users': report['active_users'],
            'total_events': report['total_events'],
            'critical_events': report['critical_events'],
            'unusual_behavior_count': report['unusual_behavior_count'],
            'missing_work_count': report['missing_work_count'],
            'rule_violations': report['rule_violations'],
            'summary': report['summary'],
            'created_at': report['created_at'].isoformat() if report['created_at'] else None
        })
    else:
        return jsonify({'error': 'Unable to generate report'}), 500
