# SIEM Dashboard Project

## Overview
A complete, production-ready Security Information & Event Management (SIEM) dashboard application built with Python Flask and PostgreSQL. Features a modern Zain Telecom-themed design with purple gradients, yellow accents, and a comprehensive security event monitoring system.

**Current State**: Fully functional and deployed on Replit with all core features operational.

## Recent Changes (November 19, 2025)

### Initial Project Build
- Created complete SIEM dashboard application from scratch
- Implemented user authentication and role-based access control (Admin, Manager, Analyst, User)
- Built comprehensive database schema with PostgreSQL
- Created beautiful Zain Telecom-themed UI with purple/yellow/black/white color scheme
- Implemented all CRUD operations for users and groups
- Built SIEM event monitoring with real-time visualization using Chart.js
- Created RESTful API endpoints for all major functions
- Generated custom Zain-themed logo with AI
- Added complete deployment documentation for Linux servers

## Project Architecture

### Backend (Python Flask)
- **app.py** - Main application entry point with route registration
- **config.py** - Configuration management with environment variables
- **database.py** - PostgreSQL connection pool and all database helper functions
- **routes/** - Modular route handlers (auth, dashboard, users, groups, siem)
- **api/** - RESTful API endpoints (logs, users, groups, reports)

### Frontend
- **templates/** - Jinja2 HTML templates with role-specific dashboards
- **static/css/** - Zain Telecom themed CSS with purple gradients
- **static/js/** - Chart.js integration and interactive JavaScript
- **static/img/** - Generated logo and assets

### Database Schema
- **users** - User accounts with bcrypt password hashing
- **groups** - User group organization
- **permissions** - Granular group-based permissions (CRUD)
- **syslog_events** - Security event logs with severity tracking
- **activity_reports** - Automated daily activity summaries

## User Preferences

### Design Requirements
- Zain Telecom visual identity must be maintained
- Purple gradients (#4a148c to #8e24aa)
- Yellow accent color (#ffd700)
- Black (#1a1a1a) and white (#ffffff) contrast
- Modern, rounded UI components
- Mobile-responsive layout
- Professional, clean aesthetic

### Functional Requirements
- Four distinct user roles with different access levels
- Real-time event monitoring and alerting
- Complete user and group management
- RESTful API for integration
- Production-ready code quality
- Exportable to Linux servers

## Default Credentials
- Username: `admin`
- Password: `admin123`
- **Action Required**: Change these credentials in production!

## Key Features

1. **Role-Based Dashboards**
   - Admin: Full system control with user/group management
   - Manager: Team oversight and monitoring
   - Analyst: Security event analysis and monitoring
   - User: Basic read-only access

2. **SIEM Capabilities**
   - Real-time event logging and display
   - Severity-based categorization (INFO, WARNING, ERROR, CRITICAL)
   - Interactive Chart.js visualizations
   - Log simulation for testing
   - Event timeline and type distribution charts

3. **User Management**
   - CRUD operations for user accounts
   - Role assignment
   - Group membership
   - Active/inactive status tracking

4. **Group & Permissions**
   - Flexible group creation
   - Granular CRUD permissions per group
   - Permission inheritance system

5. **API Endpoints**
   - `/api/logs` - Retrieve logs with filtering
   - `/api/users` - User management
   - `/api/groups` - Group operations
   - `/api/daily-report` - Automated activity reports

## Running on Replit
- Click "Run" button to start Flask server
- Application runs on port 5000
- Access via webview (automatically configured)
- Database initializes automatically on first run
- Default admin user created on initialization

## Exporting to Production
See README.md for detailed Linux server deployment instructions including:
- Nginx configuration
- Gunicorn setup
- Systemd service configuration
- Real syslog integration options
- Security hardening recommendations

## Future Enhancements
- Real syslog protocol integration (prepared function exists)
- Automated email notifications for daily reports
- Advanced anomaly detection algorithms
- WebSocket live updates
- PDF/CSV report exports
- Two-factor authentication
- Audit trail enhancements

## Technical Notes

### Database Connection
- Uses PostgreSQL via Replit integration
- Connection pooling implemented
- All queries use parameterized statements (SQL injection protection)
- Automatic schema initialization

### Security Features
- bcrypt password hashing (cost factor 12)
- Session-based authentication
- CSRF protection ready (Flask-WTF can be added)
- Role-based access decorators
- SQL injection prevention via parameterized queries

### Performance
- Optimized database queries with indexes ready
- Static asset caching configured
- Minimal JavaScript bundle size
- Responsive design for mobile performance

## Troubleshooting

### Database Issues
- Database auto-initializes on startup
- Check DATABASE_URL environment variable
- Verify PostgreSQL service is running

### Login Issues
- Ensure default admin user exists (auto-created)
- Check session configuration
- Verify SESSION_SECRET is set

### UI/Display Issues
- Clear browser cache
- Check static files are loading (browser console)
- Verify CSS path in templates

## Dependencies
- flask - Web framework
- flask-session - Session management
- psycopg2-binary - PostgreSQL adapter
- bcrypt - Password hashing
- python-dotenv - Environment configuration
- bootstrap 5 - Frontend framework (CDN)
- chart.js - Data visualization (CDN)
- font-awesome - Icons (CDN)

## Project Structure Rationale
- Modular design for maintainability
- Separation of concerns (routes, API, database)
- Template inheritance for DRY principle
- RESTful API design patterns
- Production-ready code organization
