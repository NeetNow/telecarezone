# TeleCareZone - Deployment Guide

## Production Deployment Checklist

### 1. Environment Configuration

#### Backend Environment Variables
Update `/app/backend/.env` with production values:

```env
# Database
MONGO_URL="mongodb://your-production-mongodb:27017"
DB_NAME="telecarezone_production"
CORS_ORIGINS="https://telecarezone.com,https://*.telecarezone.com"

# Security
JWT_SECRET="CHANGE-THIS-TO-STRONG-RANDOM-STRING-IN-PRODUCTION"

# Razorpay (Production Keys)
RAZORPAY_KEY_ID="rzp_live_xxxxxxxxxxxxx"
RAZORPAY_KEY_SECRET="your_production_secret"

# Twilio WhatsApp
TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN="your_auth_token"
TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"

# Google Calendar
GOOGLE_CLIENT_ID="your_client_id"
GOOGLE_CLIENT_SECRET="your_client_secret"
```

#### Frontend Environment Variables
Update `/app/frontend/.env`:

```env
REACT_APP_BACKEND_URL=https://telecarezone.com
```

### 2. Database Setup

#### MongoDB Production Setup

1. **Create MongoDB Atlas Cluster** (or your preferred hosting):
   - Go to https://www.mongodb.com/cloud/atlas
   - Create new cluster
   - Configure network access (whitelist your server IP)
   - Create database user with read/write permissions

2. **Get Connection String**:
   ```
   mongodb+srv://<username>:<password>@cluster.mongodb.net/telecarezone_production
   ```

3. **Create Indexes** for performance:
   ```javascript
   // Connect to MongoDB
   db.professionals.createIndex({ "subdomain": 1 }, { unique: true })
   db.professionals.createIndex({ "email": 1 }, { unique: true })
   db.professionals.createIndex({ "status": 1 })
   db.appointments.createIndex({ "professional_id": 1 })
   db.appointments.createIndex({ "appointment_datetime": 1 })
   db.payments.createIndex({ "professional_id": 1 })
   db.payments.createIndex({ "appointment_id": 1 })
   ```

### 3. Razorpay Setup

1. **Create Razorpay Account**:
   - Sign up at https://razorpay.com
   - Complete KYC verification
   - Get Live API Keys

2. **Enable Razorpay Route**:
   - Navigate to Dashboard → Route
   - Enable Route feature
   - Set up linked accounts for each doctor
   - Configure automatic settlement (90% to doctor, 10% platform)

3. **Webhook Configuration**:
   - Add webhook URL: `https://telecarezone.com/api/webhooks/razorpay`
   - Subscribe to: `payment.captured`, `payment.failed`

### 4. Twilio WhatsApp Setup

1. **Create Twilio Account**:
   - Sign up at https://www.twilio.com
   - Verify phone number
   - Purchase WhatsApp-enabled number

2. **WhatsApp Business API**:
   - Apply for WhatsApp Business API access
   - Complete business verification
   - Get approved WhatsApp sender number
   - Configure message templates

3. **Message Templates** (required for WhatsApp Business):
   ```
   Template 1: appointment_confirmation
   Hello {{1}}, your appointment with Dr. {{2}} is confirmed for {{3}}. 
   Meeting Link: {{4}}
   
   Template 2: appointment_reminder
   Reminder: Your appointment with Dr. {{1}} starts in 15 minutes. 
   Join here: {{2}}
   ```

### 5. Google Meet Integration

1. **Create Google Cloud Project**:
   - Go to https://console.cloud.google.com
   - Create new project
   - Enable Google Calendar API

2. **OAuth Credentials**:
   - Create OAuth 2.0 Client ID
   - Add authorized redirect URIs
   - Download credentials JSON

3. **Service Account** (for backend):
   - Create service account
   - Grant Calendar API permissions
   - Download service account key

### 6. DNS Configuration

#### Wildcard Subdomain Setup

**For Cloudflare**:
1. Add A record: `@` → `Your Server IP`
2. Add CNAME record: `*` → `telecarezone.com`
3. Enable SSL/TLS (Full mode)

**For AWS Route53**:
```
Type: A
Name: telecarezone.com
Value: Your Server IP

Type: A
Name: *.telecarezone.com
Value: Your Server IP
```

**For Other DNS Providers**:
- Add A record for main domain
- Add wildcard A record (*.telecarezone.com)

### 7. SSL Certificate

#### Using Let's Encrypt (Certbot)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get wildcard certificate
sudo certbot certonly --manual \
  -d telecarezone.com \
  -d *.telecarezone.com \
  --preferred-challenges dns

# Add DNS TXT record as instructed
# Verify and complete

# Auto-renewal
sudo certbot renew --dry-run
```

### 8. Nginx Configuration

Create `/etc/nginx/sites-available/telecarezone`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name telecarezone.com *.telecarezone.com;
    return 301 https://$host$request_uri;
}

# Main domain + subdomains
server {
    listen 443 ssl http2;
    server_name telecarezone.com *.telecarezone.com;

    ssl_certificate /etc/letsencrypt/live/telecarezone.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/telecarezone.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # Frontend (React)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (production build)
    location /static {
        alias /app/frontend/build/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/telecarezone /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Production Build

#### Backend
```bash
cd /app/backend
pip install -r requirements.txt
```

#### Frontend
```bash
cd /app/frontend
yarn install
yarn build
```

### 10. Process Management

#### Using Supervisor

Update `/etc/supervisor/conf.d/telecarezone.conf`:

```ini
[program:telecarezone-backend]
command=/root/.venv/bin/uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4
directory=/app/backend
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/telecarezone/backend.err.log
stdout_logfile=/var/log/telecarezone/backend.out.log

[program:telecarezone-frontend]
command=yarn start
directory=/app/frontend
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/telecarezone/frontend.err.log
stdout_logfile=/var/log/telecarezone/frontend.out.log
```

For production, use `serve` instead of dev server:
```bash
yarn global add serve
# Update supervisor command to: serve -s build -l 3000
```

Reload supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
```

#### Using PM2 (Alternative)

```bash
npm install -g pm2

# Backend
pm2 start "uvicorn server:app --host 0.0.0.0 --port 8001 --workers 4" --name telecarezone-backend

# Frontend (production)
pm2 serve /app/frontend/build 3000 --name telecarezone-frontend --spa

# Save and auto-start
pm2 save
pm2 startup
```

### 11. Security Hardening

1. **Firewall Rules**:
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. **MongoDB Security**:
   - Enable authentication
   - Use strong passwords
   - Restrict network access
   - Enable encryption at rest

3. **API Rate Limiting**:
   Add to FastAPI:
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   ```

4. **Environment Variables**:
   - Never commit `.env` files
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault)
   - Rotate keys regularly

### 12. Monitoring & Logging

#### Setup Monitoring

1. **Application Monitoring**:
   - Install Sentry: https://sentry.io
   - Add DSN to environment variables
   - Track errors and performance

2. **Server Monitoring**:
   - Use tools like Datadog, New Relic, or Prometheus
   - Monitor CPU, memory, disk usage
   - Set up alerts

3. **Log Management**:
```bash
# Centralized logging
sudo apt install rsyslog
# Configure log rotation
sudo nano /etc/logrotate.d/telecarezone
```

#### Health Checks

Add health check endpoint:
```python
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}
```

### 13. Backup Strategy

#### Database Backups

```bash
# MongoDB backup script
#!/bin/bash
BACKUP_DIR="/backups/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)
mongodump --uri="$MONGO_URL" --out="$BACKUP_DIR/$DATE"

# Compress
tar -czf "$BACKUP_DIR/$DATE.tar.gz" "$BACKUP_DIR/$DATE"
rm -rf "$BACKUP_DIR/$DATE"

# Upload to S3 (optional)
aws s3 cp "$BACKUP_DIR/$DATE.tar.gz" s3://your-bucket/backups/
```

Schedule with cron:
```bash
0 2 * * * /scripts/backup-mongodb.sh
```

### 14. Performance Optimization

1. **Enable Gzip Compression** (Nginx):
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

2. **Redis Caching**:
```bash
sudo apt install redis-server
# Configure Redis for session storage
```

3. **CDN Setup**:
   - Use Cloudflare or AWS CloudFront
   - Cache static assets
   - Enable image optimization

### 15. Testing Production

1. **Pre-deployment Checklist**:
   - [ ] All environment variables configured
   - [ ] Database backed up
   - [ ] SSL certificate valid
   - [ ] DNS records propagated
   - [ ] Payment gateway in live mode
   - [ ] WhatsApp templates approved
   - [ ] Monitoring configured
   - [ ] Backup system working

2. **Smoke Tests**:
```bash
# API health
curl https://telecarezone.com/api/health

# Admin login
curl -X POST https://telecarezone.com/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"production_password"}'

# Create test appointment
curl -X POST https://telecarezone.com/api/appointments \
  -H "Content-Type: application/json" \
  -d '{...test data...}'
```

### 16. Rollback Plan

Keep previous version ready:
```bash
# Tag current version
git tag -a v1.0.0 -m "Production release"

# If rollback needed
git checkout v1.0.0
sudo supervisorctl restart all
```

### 17. Post-Deployment

1. **Monitor logs** for 24-48 hours
2. **Test all critical flows**:
   - Expert onboarding
   - Admin approval
   - Appointment booking
   - Payment processing
3. **Check analytics** dashboard
4. **Verify notifications** working
5. **Test subdomain** routing

### 18. Maintenance

#### Regular Tasks:
- Weekly: Review error logs
- Monthly: Database cleanup, update dependencies
- Quarterly: Security audit, certificate renewal check
- Yearly: Infrastructure review, cost optimization

### Support Contacts

- **Hosting Issues**: Contact your cloud provider
- **Payment Issues**: Razorpay support
- **WhatsApp Issues**: Twilio support
- **SSL Issues**: Let's Encrypt community

---

## Quick Deploy Commands

```bash
# Pull latest code
cd /app && git pull

# Backend
cd /app/backend
pip install -r requirements.txt
sudo supervisorctl restart backend

# Frontend
cd /app/frontend
yarn install
yarn build
sudo supervisorctl restart frontend

# Verify
curl https://telecarezone.com/api/health
```

---

**For emergency rollback, always keep the previous working version tagged and ready to deploy within minutes.**
