# SIEM Dashboard Project

## Overview
A complete, production-ready Security Information & Event Management (SIEM) dashboard application built with Python Flask and PostgreSQL. Features a modern Zain Telecom-themed design with purple gradients, yellow accents, and a comprehensive security event monitoring system.

**Current State**: Fully functional and deployed on Replit with all core features operational.

## Recent Changes (November 19, 2025)

### Log Ingestion System (Latest Update)
- Added comprehensive log ingestion system with three methods:
  - **CSV File Upload**: Upload and import logs from CSV files with log source assignment
  - **Syslog API Endpoint** (`/api/syslog`): Receive raw syslog data from external systems
  - **JSON API Endpoint** (`/api/ingest`): Ingest structured JSON log batches
- Created `log_sources` database table to track log origins
- Added foreign key relationship between `syslog_events` and `log_sources`
- Built UI components for log source management (`upload_logs.html`, `log_sources.html`)
- Implemented robust transaction management with proper error handling and rollback
- Added API key-based authentication for external log ingestion
- Integrated log source statistics tracking (total logs received, last received timestamp)
- Fixed Psycopg2 transaction state issues with separate connections per bulk insert
- Added comprehensive error logging for ingestion failures

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
- **log_sources** - External log sources with API keys and statistics (NEW)
- **syslog_events** - Security event logs with severity tracking and log source linkage
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
   - `/api/ingest` - Ingest JSON log batches (requires API key)
   - `/api/syslog` - Receive raw syslog data (requires API key)

6. **Log Ingestion System**
   - CSV file upload with source assignment
   - Real-time syslog reception from external systems
   - API-based log forwarding with authentication
   - Log source management and statistics tracking
   - Automatic error handling and transaction rollback
   - Support for Arabic and English log formats

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
- Automated email notifications for daily reports
- Advanced anomaly detection algorithms
- WebSocket live updates for real-time log streaming
- PDF/CSV report exports
- Two-factor authentication
- Audit trail enhancements
- Custom parsing rules for different log formats
- Integration with popular SIEM tools (Splunk, ELK)

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
