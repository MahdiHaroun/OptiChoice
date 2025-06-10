# OptiChoice - Movie Recommendation System

## Environment Variables Setup

This project uses environment variables to manage sensitive configuration data like secret keys, passwords, and API credentials. This approach enhances security by keeping secrets out of version control.

### Setup Instructions

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your actual values:**
   - Replace placeholder values with your actual credentials
   - Never commit the `.env` file to version control

### Environment Variables Reference

#### Django Settings
- `SECRET_KEY`: Django secret key for cryptographic signing
- `DEBUG`: Enable/disable debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames

#### Database Settings
- `DB_ENGINE`: Database engine (default: django.db.backends.sqlite3)
- `DB_NAME`: Database name or path for SQLite
- `DB_USER`: Database username (for PostgreSQL/MySQL)
- `DB_PASSWORD`: Database password (for PostgreSQL/MySQL)
- `DB_HOST`: Database host (for PostgreSQL/MySQL)
- `DB_PORT`: Database port (for PostgreSQL/MySQL)

#### Email Configuration
- `EMAIL_BACKEND`: Email backend class
- `EMAIL_HOST`: SMTP server hostname
- `EMAIL_PORT`: SMTP server port
- `EMAIL_USE_TLS`: Enable TLS encryption (True/False)
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password or app password
- `DEFAULT_FROM_EMAIL`: Default sender email address

#### CORS Settings (for React frontend)
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins
- `CORS_ALLOW_CREDENTIALS`: Allow credentials in CORS requests (True/False)

#### JWT Authentication
- `JWT_ACCESS_TOKEN_LIFETIME_MINUTES`: Access token lifetime in minutes
- `JWT_REFRESH_TOKEN_LIFETIME_DAYS`: Refresh token lifetime in days
- `JWT_ALGORITHM`: JWT signing algorithm

#### Security Settings
- `SESSION_COOKIE_AGE`: Session cookie lifetime in seconds

### Security Best Practices

1. **Never commit `.env` files** - They are included in `.gitignore`
2. **Use strong secret keys** - Generate new ones for production
3. **Use app passwords for Gmail** - Don't use your main password
4. **Limit CORS origins** - Only allow necessary domains in production
5. **Use environment-specific settings** - Different values for dev/staging/production

### Gmail SMTP Setup

To use Gmail for sending emails:

1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Use the app password in `EMAIL_HOST_PASSWORD`

### Production Deployment

For production deployment:

1. Set `DEBUG=False`
2. Use a strong, unique `SECRET_KEY`
3. Configure a production database (PostgreSQL recommended)
4. Set appropriate `ALLOWED_HOSTS`
5. Use HTTPS and configure SSL certificates
6. Set restrictive CORS origins

### Environment File Location

The `.env` file should be placed in the same directory as `manage.py`:
```
OPC/
├── .env                 # ← Environment variables file
├── manage.py
├── OPC/
│   └── settings.py
└── ...
```

### Troubleshooting

- **Import errors**: Ensure virtual environment is activated
- **Environment not loading**: Check file path and syntax in `.env`
- **Database errors**: Verify database credentials and permissions
- **Email errors**: Check SMTP settings and app password
