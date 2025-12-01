# TeleCareZone - Healthcare Experts SAAS Platform

## Overview

TeleCareZone is a complete production-grade SAAS platform designed exclusively for healthcare professionals who conduct teleconsultations. The platform enables doctors to have their personalized landing pages with automated appointment scheduling, payment processing, and notification systems.

## Features

### Main Domain Features
- **Landing Page** with healthcare expert listings
- **Expert Onboarding** form with comprehensive professional details
- **Admin Dashboard** for managing professionals and analytics
- **Secure Authentication** for admin access

### Subdomain Features (Doctor Landing Pages)
- **Personalized Landing Pages** for each approved healthcare professional
- **Professional Profile** with credentials, social media links, and testimonials
- **Appointment Booking System** with real-time slot selection
- **Secure Payment Gateway** via Razorpay with 10/90 split
- **Automated Notifications** via WhatsApp (confirmation + 15min reminder)
- **Google Meet Integration** for video consultations

### Admin Dashboard Features
- Platform-wide analytics and metrics
- Professional application management (approve/reject)
- Individual doctor analytics (appointments, revenue)
- Business reports per healthcare professional

## Technology Stack

- **Frontend**: React 19, Tailwind CSS, Shadcn UI
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Payment**: Razorpay Route (split payments)
- **Notifications**: Twilio WhatsApp Business API
- **Video**: Google Meet (Calendar API integration)
- **Authentication**: JWT-based admin authentication

## Quick Start

### Default Admin Credentials
- Username: `admin`
- Password: `admin123`

### Access URLs
- Main Site: https://your-domain.com
- Admin Login: https://your-domain.com/admin/login
- API Docs: https://your-domain.com/api/

## Configuration

### Environment Variables

**Backend** (`/app/backend/.env`):
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="telecarezone_db"
JWT_SECRET="your-secret-key-change-in-production"

# Razorpay
RAZORPAY_KEY_ID="your_key_id"
RAZORPAY_KEY_SECRET="your_key_secret"

# Twilio WhatsApp
TWILIO_ACCOUNT_SID="your_account_sid"
TWILIO_AUTH_TOKEN="your_auth_token"
TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"
```

**Frontend** (`/app/frontend/.env`):
```env
REACT_APP_BACKEND_URL=https://your-domain.com
```

## Subdomain Setup

Configure wildcard DNS for subdomain routing:
```
*.telecarezone.com -> Your Server IP
```

## Payment Integration

1. Sign up at https://razorpay.com
2. Enable Razorpay Route for split payments
3. Update credentials in backend `.env`

## WhatsApp Integration

1. Sign up at https://www.twilio.com
2. Enable WhatsApp Business API
3. Update credentials in backend `.env`

## User Workflows

### Admin Workflow
1. Login at `/admin/login`
2. Review pending applications
3. Approve/reject professionals
4. View analytics

### Doctor Onboarding
1. Fill form at `/join-expert`
2. Wait for admin approval
3. Receive subdomain (e.g., `drjohn.telecarezone.com`)
4. Share link with patients

### Patient Booking
1. Visit doctor subdomain
2. Select time slot
3. Enter personal details
4. Complete payment
5. Receive meeting link via WhatsApp

## API Endpoints

### Public
- `POST /api/onboarding/submit` - Submit expert application
- `GET /api/professionals/approved` - List approved experts
- `POST /api/appointments` - Create appointment
- `POST /api/payments/create-order` - Create payment order

### Admin (Protected)
- `POST /api/admin/login` - Admin login
- `GET /api/professionals` - List all professionals
- `PUT /api/professionals/{id}` - Update professional
- `GET /api/admin/analytics/overview` - Platform analytics

## Database Collections

- **professionals** - Healthcare expert profiles
- **appointments** - Booking records
- **patients** - Patient information
- **payments** - Transaction records
- **admin_users** - Admin accounts
- **testimonials** - Doctor reviews

## Development

### Restart Services
```bash
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
```

### View Logs
```bash
tail -f /var/log/supervisor/backend.*.log
```

## Security Notes

⚠️ **Production Checklist:**
- Change JWT_SECRET
- Use real API keys (not test keys)
- Enable HTTPS
- Configure proper CORS origins
- Set up firewall rules
- Regular security audits

## Support

For issues or questions:
- Check logs: `/var/log/supervisor/`
- Verify environment variables
- Ensure MongoDB is running
- Test API endpoints with curl

---

Built with React + FastAPI + MongoDB
