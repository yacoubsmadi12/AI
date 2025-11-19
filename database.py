import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
import bcrypt
from datetime import datetime

def get_db_connection():
    conn = psycopg2.connect(Config.DATABASE_URL)
    return conn

def init_database():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL,
            group_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id SERIAL PRIMARY KEY,
            group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
            permission_name VARCHAR(100) NOT NULL,
            can_create BOOLEAN DEFAULT FALSE,
            can_read BOOLEAN DEFAULT TRUE,
            can_update BOOLEAN DEFAULT FALSE,
            can_delete BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS syslog_events (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            severity VARCHAR(50) NOT NULL,
            source_ip VARCHAR(50),
            source_host VARCHAR(255),
            event_type VARCHAR(100),
            message TEXT NOT NULL,
            user_id INTEGER REFERENCES users(id),
            raw_log TEXT,
            processed BOOLEAN DEFAULT FALSE
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS activity_reports (
            id SERIAL PRIMARY KEY,
            group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
            report_date DATE NOT NULL,
            total_users INTEGER DEFAULT 0,
            active_users INTEGER DEFAULT 0,
            total_events INTEGER DEFAULT 0,
            critical_events INTEGER DEFAULT 0,
            unusual_behavior_count INTEGER DEFAULT 0,
            missing_work_count INTEGER DEFAULT 0,
            rule_violations INTEGER DEFAULT 0,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]
    
    if user_count == 0:
        password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cur.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            ('admin', 'admin@siem.local', password, 'Admin')
        )
        conn.commit()
    
    cur.close()
    conn.close()

def get_user_by_username(username):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE username = %s AND is_active = TRUE", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_user(username, email, password, role, group_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash, role, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (username, email, password_hash, role, group_id)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return user_id
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise e

def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, username, email, role, group_id, created_at, last_login, is_active FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def update_user(user_id, **kwargs):
    conn = get_db_connection()
    cur = conn.cursor()
    
    allowed_fields = ['username', 'email', 'role', 'group_id', 'is_active']
    updates = []
    values = []
    
    for key, value in kwargs.items():
        if key in allowed_fields:
            updates.append(f"{key} = %s")
            values.append(value)
    
    if updates:
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        cur.execute(query, values)
        conn.commit()
    
    cur.close()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_active = FALSE WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def get_all_groups():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM groups ORDER BY name")
    groups = cur.fetchall()
    cur.close()
    conn.close()
    return groups

def create_group(name, description=''):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "INSERT INTO groups (name, description) VALUES (%s, %s) RETURNING id",
            (name, description)
        )
        group_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return group_id
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise e

def get_permissions_by_group(group_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM permissions WHERE group_id = %s", (group_id,))
    permissions = cur.fetchall()
    cur.close()
    conn.close()
    return permissions

def create_permission(group_id, permission_name, can_create=False, can_read=True, can_update=False, can_delete=False):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO permissions (group_id, permission_name, can_create, can_read, can_update, can_delete) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
        (group_id, permission_name, can_create, can_read, can_update, can_delete)
    )
    perm_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return perm_id

def get_latest_logs(limit=100):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM syslog_events ORDER BY timestamp DESC LIMIT %s", (limit,))
    logs = cur.fetchall()
    cur.close()
    conn.close()
    return logs

def get_logs_by_severity(severity, limit=100):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM syslog_events WHERE severity = %s ORDER BY timestamp DESC LIMIT %s", (severity, limit))
    logs = cur.fetchall()
    cur.close()
    conn.close()
    return logs

def insert_log_event(severity, message, source_ip=None, source_host=None, event_type=None, user_id=None, raw_log=None):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO syslog_events (severity, message, source_ip, source_host, event_type, user_id, raw_log) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (severity, message, source_ip, source_host, event_type, user_id, raw_log)
    )
    log_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return log_id

def receive_syslog_event(raw_data):
    insert_log_event(
        severity='INFO',
        message=raw_data,
        event_type='SYSLOG',
        raw_log=raw_data
    )

def generate_daily_report(group_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    today = datetime.now().date()
    
    cur.execute("SELECT COUNT(*) as total FROM users WHERE group_id = %s", (group_id,))
    total_users = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as active FROM users WHERE group_id = %s AND last_login::date = %s", (group_id, today))
    active_users = cur.fetchone()['active']
    
    cur.execute("SELECT COUNT(*) as total FROM syslog_events WHERE timestamp::date = %s", (today,))
    total_events = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as critical FROM syslog_events WHERE severity = 'CRITICAL' AND timestamp::date = %s", (today,))
    critical_events = cur.fetchone()['critical']
    
    unusual_behavior = 0
    missing_work = total_users - active_users
    rule_violations = critical_events
    
    summary = f"Daily report for group {group_id}: {active_users}/{total_users} users active, {total_events} events, {critical_events} critical alerts"
    
    cur.execute(
        """INSERT INTO activity_reports 
           (group_id, report_date, total_users, active_users, total_events, critical_events, 
            unusual_behavior_count, missing_work_count, rule_violations, summary) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
        (group_id, today, total_users, active_users, total_events, critical_events, 
         unusual_behavior, missing_work, rule_violations, summary)
    )
    
    report_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return report_id

def get_daily_report(group_id, date=None):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if date is None:
        date = datetime.now().date()
    
    cur.execute("SELECT * FROM activity_reports WHERE group_id = %s AND report_date = %s", (group_id, date))
    report = cur.fetchone()
    cur.close()
    conn.close()
    return report

def update_last_login(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
