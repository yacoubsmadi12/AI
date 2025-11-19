import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'dev-secret-key-change-in-production'
    
    DATABASE_URL = os.environ.get('DATABASE_URL')
    PGHOST = os.environ.get('PGHOST')
    PGPORT = os.environ.get('PGPORT')
    PGDATABASE = os.environ.get('PGDATABASE')
    PGUSER = os.environ.get('PGUSER')
    PGPASSWORD = os.environ.get('PGPASSWORD')
    
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    ROLES = ['Admin', 'Manager', 'Analyst', 'User']
    
    LOG_SEVERITIES = ['INFO', 'WARNING', 'ERROR', 'CRITICAL']
