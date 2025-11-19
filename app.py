from flask import Flask, session, redirect, url_for
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import Config
import database
import os

app = Flask(__name__)
app.config.from_object(Config)

Session(app)
csrf = CSRFProtect(app)

database.init_database()

from routes import auth, dashboard, users, groups, siem
from api import logs_api, users_api, groups_api, reports_api

app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(users.bp)
app.register_blueprint(groups.bp)
app.register_blueprint(siem.bp)
app.register_blueprint(logs_api.bp)
app.register_blueprint(users_api.bp)
app.register_blueprint(groups_api.bp)
app.register_blueprint(reports_api.bp)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard.show_dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
