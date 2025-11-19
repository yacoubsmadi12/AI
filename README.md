# SIEM Dashboard - Security Information & Event Management

A complete, production-ready SIEM dashboard application with user management, role-based access control, and real-time security event monitoring. Built with Flask, PostgreSQL, and featuring the Zain Telecom visual design theme.

## Features

### Core Functionality
- **User Authentication** - Secure login system with session management
- **Role-Based Access Control** - Four distinct user roles (Admin, Manager, Analyst, User)
- **SIEM Dashboard** - Real-time security event monitoring with visualizations
- **User Management** - Complete CRUD operations for user accounts
- **Group & Permissions** - Flexible group management with granular permissions
- **Event Logging** - Comprehensive system event tracking and analysis
- **Daily Reports** - Automated activity reports for team monitoring
- **RESTful API** - Full API access for all major functions

### Design
- **Zain Telecom Theme** - Purple gradients, yellow accents, black/white contrast
- **Responsive Layout** - Mobile-friendly design using Bootstrap 5
- **Interactive Charts** - Data visualization with Chart.js
- **Modern UI** - Clean, rounded components with smooth animations

## Technology Stack

### Backend
- **Python Flask** - Web framework
- **PostgreSQL** - Database (via Replit integration)
- **bcrypt** - Password hashing
- **psycopg2** - PostgreSQL adapter

### Frontend
- **HTML5/CSS3/JavaScript**
- **Bootstrap 5** - UI framework
- **Chart.js** - Data visualization
- **Font Awesome** - Icons

## Project Structure

```
/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── database.py             # Database connection and helpers
├── routes/                 # Route modules
│   ├── auth.py            # Authentication routes
│   ├── dashboard.py       # Dashboard routes
│   ├── users.py           # User management routes
│   ├── groups.py          # Group management routes
│   └── siem.py            # SIEM dashboard routes
├── api/                    # API endpoints
│   ├── logs_api.py        # Log APIs
│   ├── users_api.py       # User APIs
│   ├── groups_api.py      # Group APIs
│   └── reports_api.py     # Report APIs
├── templates/              # Jinja2 HTML templates
├── static/                 # Static assets
│   ├── css/style.css      # Zain-themed styles
│   ├── js/main.js         # Frontend JavaScript
│   └── img/logo.png       # Application logo
└── models/                 # Data models (future use)
```

## Database Schema

### Tables
- **users** - User accounts with roles and group assignments
- **groups** - User groups for organization
- **permissions** - Group-based permission system
- **syslog_events** - Security event logs
- **activity_reports** - Daily activity summaries

## Getting Started on Replit

1. The application is pre-configured and ready to run
2. Click the "Run" button to start the Flask server
3. Access the application through the webview
4. Default login credentials:
   - Username: `admin`
   - Password: `admin123`

## API Endpoints

### Logs
- `GET /api/logs` - Retrieve logs (with optional severity filter)
- `GET /api/logs/latest` - Get latest logs

### Users
- `GET /api/users` - List all users
- `POST /api/users/add` - Create new user (JSON)

### Groups
- `GET /api/groups` - List all groups
- `POST /api/groups/add` - Create new group (JSON)

### Reports
- `GET /api/daily-report?group=<id>` - Get daily report for a group

## Deploying to Production Linux Server

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Nginx (recommended)
- Gunicorn or uWSGI

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd siem-dashboard
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install flask flask-session psycopg2-binary bcrypt python-dotenv gunicorn
   ```

3. **Configure PostgreSQL**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE siem_db;
   CREATE USER siem_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE siem_db TO siem_user;
   \q
   ```

4. **Set environment variables**
   Create a `.env` file:
   ```env
   DATABASE_URL=postgresql://siem_user:your_secure_password@localhost/siem_db
   PGHOST=localhost
   PGPORT=5432
   PGDATABASE=siem_db
   PGUSER=siem_user
   PGPASSWORD=your_secure_password
   SESSION_SECRET=your-random-secret-key-here
   ```

5. **Initialize the database**
   ```bash
   python3 -c "from database import init_database; init_database()"
   ```

6. **Run with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
   ```

### Production Configuration with Nginx

Create `/etc/nginx/sites-available/siem-dashboard`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/siem-dashboard/static;
        expires 30d;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/siem-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Systemd Service

Create `/etc/systemd/system/siem-dashboard.service`:

```ini
[Unit]
Description=SIEM Dashboard Application
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/siem-dashboard
Environment="PATH=/path/to/siem-dashboard/venv/bin"
EnvironmentFile=/path/to/siem-dashboard/.env
ExecStart=/path/to/siem-dashboard/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable siem-dashboard
sudo systemctl start siem-dashboard
```

## Real Syslog Integration

The application includes a placeholder function `receive_syslog_event()` in `database.py` for production syslog integration.

### Option 1: Syslog-ng Forwarding

Configure syslog-ng to forward to your application:

```
destination d_siem {
    program("/path/to/siem-dashboard/venv/bin/python3 /path/to/siem-dashboard/syslog_receiver.py");
};

log {
    source(s_src);
    destination(d_siem);
};
```

### Option 2: UDP/TCP Listener

Add a syslog listener to your Flask app or create a separate daemon to receive syslog messages and insert them via `receive_syslog_event()`.

## Security Recommendations

1. **Change Default Credentials** - Immediately change the admin password
2. **Use HTTPS** - Configure SSL/TLS with Let's Encrypt
3. **Firewall Rules** - Restrict database and application access
4. **Regular Updates** - Keep all dependencies updated
5. **Strong Passwords** - Enforce strong password policies
6. **Backup Database** - Regular automated backups
7. **Monitor Logs** - Set up alerts for critical events

## Daily Report Generation

To schedule automatic daily reports, add a cron job:

```bash
0 0 * * * cd /path/to/siem-dashboard && /path/to/venv/bin/python3 -c "from database import generate_daily_report, get_all_groups; groups = get_all_groups(); [generate_daily_report(g['id']) for g in groups]"
```

## Customization

### Changing the Theme Colors

Edit `static/css/style.css` and modify the CSS variables:

```css
:root {
    --zain-purple-dark: #4a148c;
    --zain-purple: #6a1b9a;
    --zain-purple-light: #8e24aa;
    --zain-yellow: #ffd700;
    --zain-black: #1a1a1a;
    --zain-white: #ffffff;
}
```

### Adding Custom Event Types

Modify the `event_types` list in `routes/siem.py` to include your specific event categories.

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check credentials in `.env` file
- Ensure database exists: `psql -U siem_user -d siem_db`

### Permission Errors
- Check file permissions: `chmod -R 755 /path/to/siem-dashboard`
- Verify user running the service has access

### Port Already in Use
- Change port in app.py or gunicorn command
- Check for conflicting services: `sudo lsof -i :5000`

## Support & Documentation

For issues or questions:
1. Check application logs
2. Review database logs
3. Verify environment variables
4. Ensure all dependencies are installed

## License

This project is provided as-is for educational and production use.

## Credits

Designed with the Zain Telecom visual identity:
- Purple gradient theme
- Yellow accent colors
- Modern, professional UI/UX
