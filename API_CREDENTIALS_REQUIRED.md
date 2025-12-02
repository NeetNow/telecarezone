# TeleCareZone - Required API Credentials & Configuration

## Overview
This document lists all external API credentials and configuration details required for the platform to function in production. Currently, the platform uses mock/placeholder implementations for testing.

---

## 1. Payment Gateway - Razorpay

### Purpose
- Process consultation payments
- Split payments (10% platform, 90% doctor)
- Automatic settlement to doctor accounts

### Required Credentials

```env
# Add to /app/backend/.env
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_razorpay_secret_key
```

### Setup Steps
1. Create Razorpay account: https://razorpay.com
2. Complete KYC verification
3. Enable Razorpay Route for split payments
4. Get Live API keys from Dashboard
5. Configure webhooks for payment confirmation

### Integration Points in Code
- **File**: `/app/backend/server.py`
- **Line**: ~18 (RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
- **Function**: `create_razorpay_order()` - Line ~430
- **Comment**: `# TODO: Replace with actual Razorpay client initialization`

### Doctor Bank Account Linking
Each doctor needs to link their bank account via Razorpay Route:
- Bank Name
- Account Number
- IFSC Code
- Account Holder Name

---

## 2. WhatsApp Notifications - Twilio

### Purpose
- Send appointment confirmations
- Send 15-minute reminders
- Doctor notifications

### Required Credentials

```env
# Add to /app/backend/.env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### Setup Steps
1. Create Twilio account: https://www.twilio.com
2. Apply for WhatsApp Business API
3. Get approved WhatsApp sender number
4. Configure message templates
5. Get Account SID and Auth Token

### Integration Points in Code
- **File**: `/app/backend/server.py`
- **Line**: ~21-23 (Twilio credentials)
- **Function**: `send_whatsapp_notification()` - Line ~155
- **Comment**: `# TODO: Configure Twilio credentials for production`

### Required Message Templates
```
Template 1: appointment_confirmation
Hello {{patient_name}}, your appointment with Dr. {{doctor_name}} is confirmed for {{date_time}}. 
Meeting Link: {{meeting_link}}

Template 2: appointment_reminder  
Reminder: Your appointment with Dr. {{doctor_name}} starts in 15 minutes.
Join here: {{meeting_link}}
```

---

## 3. Google Meet/Calendar Integration

### Purpose
- Generate meeting links for consultations
- Schedule appointments in calendar
- Send calendar invites

### Required Credentials

```env
# Add to /app/backend/.env
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=https://telecarezone.com/auth/google/callback
```

### Setup Steps
1. Create Google Cloud Project: https://console.cloud.google.com
2. Enable Google Calendar API
3. Create OAuth 2.0 credentials
4. Add authorized redirect URIs
5. Download credentials

### Integration Points in Code
- **File**: `/app/backend/server.py`
- **Function**: `generate_google_meet_link()` - Line ~180
- **Comment**: `# TODO: Integrate with Google Calendar API for real meeting links`

### Current Implementation
- Mock meeting link generation: `https://meet.google.com/mock-{appointment_id}`
- Replace with actual Google Calendar API call

---

## 4. Email Service (Optional but Recommended)

### Purpose
- Send appointment confirmations via email
- Password reset emails
- Weekly reports to doctors

### Recommended Service: SendGrid

```env
# Add to /app/backend/.env
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@telecarezone.com
```

### Setup Steps
1. Create SendGrid account: https://sendgrid.com
2. Verify sender email
3. Get API key
4. Configure email templates

### Integration Points
- **New File**: Create `/app/backend/email_service.py`
- **Function**: Add `send_appointment_confirmation_email()`
- **Comment**: `# TODO: Implement SendGrid email service`

---

## 5. File Storage - AWS S3 (for profile photos, videos)

### Purpose
- Store doctor profile photos
- Store intro videos
- Store testimonial videos
- Store template images

### Required Credentials

```env
# Add to /app/backend/.env
AWS_ACCESS_KEY_ID=AKIAxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET_NAME=telecarezone-media
AWS_REGION=ap-south-1
```

### Setup Steps
1. Create AWS account: https://aws.amazon.com
2. Create S3 bucket
3. Configure CORS policy
4. Create IAM user with S3 access
5. Get access keys

### Integration Points
- **New File**: Create `/app/backend/file_upload.py`
- **Function**: `upload_to_s3(file, folder)`
- **Comment**: `# TODO: Implement S3 file upload for media storage`

### Current Implementation
- Using placeholder URLs
- Profile photos: UI Avatars API
- Videos/Images: Need S3 integration

---

## 6. Database - MongoDB

### Production Setup

```env
# Add to /app/backend/.env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=telecarezone_production
```

### Setup Steps
1. Create MongoDB Atlas cluster: https://www.mongodb.com/cloud/atlas
2. Configure network access (whitelist IPs)
3. Create database user
4. Get connection string
5. Create indexes for performance

### Required Indexes
```javascript
db.professionals.createIndex({ "subdomain": 1 }, { unique: true })
db.professionals.createIndex({ "email": 1 }, { unique: true })
db.professionals.createIndex({ "status": 1 })
db.appointments.createIndex({ "professional_id": 1 })
db.appointments.createIndex({ "appointment_datetime": 1 })
db.appointments.createIndex({ "patient_phone": 1 })
```

---

## 7. SMS Service (Alternative to WhatsApp)

### Purpose
- Backup notification channel
- OTP verification
- Appointment reminders

### Recommended Service: Twilio SMS

```env
# Add to /app/backend/.env
TWILIO_SMS_FROM=+1234567890
```

### Integration Points
- **File**: `/app/backend/server.py`
- **Function**: Add `send_sms_notification()`

---

## 8. Video Conferencing (Alternative to Google Meet)

### Recommended: Zoom API

```env
# Add to /app/backend/.env
ZOOM_API_KEY=your_api_key
ZOOM_API_SECRET=your_api_secret
```

### Setup Steps
1. Create Zoom account
2. Create Zoom App
3. Get API credentials
4. Configure meeting settings

---

## 9. Analytics & Monitoring

### Recommended: Sentry (Error Tracking)

```env
# Add to /app/backend/.env
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx
```

### Setup Steps
1. Create Sentry account: https://sentry.io
2. Create new project
3. Get DSN
4. Install SDK: `pip install sentry-sdk`

### Integration
```python
import sentry_sdk
sentry_sdk.init(dsn=os.environ.get('SENTRY_DSN'))
```

---

## 10. Doctor Bank Details (Per Doctor)

### Required Information
Each doctor must provide:

```json
{
  "bank_name": "HDFC Bank",
  "account_number": "123456789012",
  "ifsc_code": "HDFC0001234",
  "branch_name": "Mumbai Main Branch",
  "account_holder_name": "Dr. John Doe",
  "upi_phone": "+919876543210",
  "pan_number": "ABCDE1234F"
}
```

### Storage Location
- **Collection**: `professionals` in MongoDB
- **Fields**: Added to professional document
- **Security**: Encrypted at rest

### Razorpay Route Setup
- Link bank account via Razorpay Dashboard
- Verify bank details
- Enable automatic settlements

---

## 11. Domain & DNS Configuration

### Wildcard Subdomain Setup

**For Cloudflare:**
```
Type: A
Name: @
Value: Your_Server_IP

Type: CNAME
Name: *
Value: telecarezone.com
```

**For Route53:**
```
Type: A
Name: telecarezone.com
Value: Your_Server_IP

Type: A
Name: *.telecarezone.com
Value: Your_Server_IP
```

---

## 12. SSL Certificate

### Let's Encrypt Setup

```bash
sudo certbot certonly --manual \
  -d telecarezone.com \
  -d *.telecarezone.com \
  --preferred-challenges dns
```

---

## Configuration Checklist

Before going to production:

- [ ] Razorpay Live keys configured
- [ ] Twilio WhatsApp Business approved
- [ ] Google Calendar API enabled
- [ ] SendGrid sender verified
- [ ] AWS S3 bucket created
- [ ] MongoDB production cluster ready
- [ ] Wildcard DNS configured
- [ ] SSL certificate installed
- [ ] Sentry error tracking setup
- [ ] All environment variables set
- [ ] Backup system configured
- [ ] Monitoring alerts configured

---

## Testing Credentials (Development)

### Admin Login
- URL: `/admin/login`
- Username: `admin`
- Password: `admin123`

### Test Payment (Razorpay Test Mode)
- Card: 4111 1111 1111 1111
- CVV: Any 3 digits
- Expiry: Any future date

---

## Security Notes

⚠️ **Important Security Practices:**

1. Never commit `.env` files to git
2. Use environment variables for all secrets
3. Rotate credentials regularly
4. Use different credentials for dev/staging/production
5. Enable 2FA on all service accounts
6. Audit access logs monthly
7. Encrypt sensitive data at rest
8. Use HTTPS for all communications

---

## Support Contacts

### Payment Issues
- Razorpay Support: support@razorpay.com
- Phone: 1800-123-RAZORPAY

### WhatsApp Issues
- Twilio Support: help@twilio.com
- Console: https://console.twilio.com

### Google API Issues
- Support: https://support.google.com/cloud

### AWS Issues
- Support: https://console.aws.amazon.com/support

---

## Update Log

| Date | Updated By | Changes |
|------|------------|---------|
| Dec 2025 | Dev Team | Initial documentation |

---

**For immediate deployment support, contact: tech@telecarezone.com**
