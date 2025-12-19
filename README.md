# 🏥 TeleCareZone - Healthcare Professional Platform

A complete SAAS platform for healthcare professionals to manage their online presence, appointments, and patient consultations.

---

## 🌟 Features

### For Healthcare Professionals
- **Personalized Landing Pages** - Each professional gets their own profile page
- **Appointment Management** - Schedule and manage patient consultations
- **Payment Processing** - Integrated Razorpay with automatic fee splitting
- **Video Consultations** - Google Meet integration
- **Profile Customization** - Custom themes, bio, qualifications, social media

### For Administrators
- **27-Field Onboarding System** - Comprehensive professional registration
- **Doctor Management** - Full CRUD operations for professionals
- **Analytics Dashboard** - Revenue tracking, appointment metrics, performance insights
- **Leads Management** - Review and approve new professional applications
- **Multi-level Access Control** - Secure admin authentication

### For Patients
- **Easy Booking** - Simple appointment scheduling
- **Multiple Payment Options** - Razorpay integration
- **WhatsApp Notifications** - Automated booking confirmations
- **Email Reminders** - Appointment notifications
- **Professional Profiles** - View qualifications, experience, fees

---

## 🛠️ Technology Stack

**Frontend:**
- React 18
- TailwindCSS
- Shadcn UI Components
- React Router
- Axios

**Backend:**
- PHP 8.0+ (Core PHP)
- MySQL/MariaDB
- JWT Authentication
- RESTful API

**Integrations:**
- Razorpay (Payment Gateway)
- Google Meet (Video Consultations)
- Fast2SMS (WhatsApp/SMS Notifications)
- Email (SMTP)

---

## 📦 Project Structure

```
telecarezone/
├── index.html              # React frontend (production build)
├── api_index.php           # Backend API entry point
├── .htaccess              # Apache URL rewriting
├── api/                   # API endpoint handlers
│   ├── admin_onboarding.php
│   ├── auth.php
│   ├── professionals.php
│   ├── appointments.php
│   └── ...
├── config/                # Configuration files
│   ├── config.php
│   ├── database.php
│   └── .env              # Environment variables
├── services/              # Business logic
│   ├── JWTService.php
│   ├── RazorpayService.php
│   └── ...
├── models/               # Data models
├── uploads/              # User uploaded files
│   ├── profiles/
│   ├── videos/
│   └── documents/
├── static/               # React static assets
├── vendor/               # Composer dependencies
└── database_import.sql   # Database schema
```

---

## 🚀 Deployment

### Prerequisites
- Hostinger shared hosting account
- Domain name (mykitchenfarm.com)
- MySQL database
- PHP 8.0 or higher
- cPanel access

### Quick Start

1. **Download Project Files**
   ```bash
   git clone <repository-url>
   ```

2. **Upload to Hostinger**
   - Use cPanel File Manager
   - Upload all files to `public_html/`

3. **Import Database**
   - Open phpMyAdmin
   - Import `database_import.sql`

4. **Configure Environment**
   - Edit `config/.env`
   - Update database credentials
   - Generate JWT secret

5. **Test Deployment**
   - Visit: https://mykitchenfarm.com
   - Login: admin / admin123

### Detailed Instructions

📖 **See:** [HOSTINGER_DEPLOYMENT_GUIDE.md](HOSTINGER_DEPLOYMENT_GUIDE.md)

📋 **Quick Reference:** [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## 🔑 Default Credentials

**Admin Dashboard:**
- URL: https://mykitchenfarm.com/admin/login
- Username: `admin`
- Password: `admin123`

⚠️ **Important:** Change the admin password after first login!

---

## 📚 Documentation

- **[Hostinger Deployment Guide](HOSTINGER_DEPLOYMENT_GUIDE.md)** - Complete deployment instructions
- **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Quick reference checklist
- **[XAMPP Setup Guide](XAMPP_SETUP_GUIDE.md)** - Local development setup
- **[Implementation Guide](IMPLEMENTATION_GUIDE.md)** - Code structure and architecture
- **[API Documentation](API_DOCUMENTATION.md)** - API endpoints reference

---

## 🧪 Testing

### Test URLs

**Homepage:**
```
https://mykitchenfarm.com
```

**API Health Check:**
```
https://mykitchenfarm.com/api
```

**Admin Dashboard:**
```
https://mykitchenfarm.com/admin/dashboard
```

**Doctor Landing Pages:**
```
https://mykitchenfarm.com/doctor/rakeshzha
https://mykitchenfarm.com/doctor/rubinashah
https://mykitchenfarm.com/doctor/saniabatra
```

---

## ⚙️ Configuration

### Environment Variables

Edit `config/.env` file:

```env
# Database
DB_HOST=localhost
DB_USER=u913267094_telecaredev
DB_PASS=your_password_here
DB_NAME=u913267094_telecaredev

# Application
APP_URL=https://mykitchenfarm.com
APP_ENV=production
APP_DEBUG=false

# Security
JWT_SECRET=your_random_secret_32_chars_minimum
```

### Optional Integrations

**Email (Hostinger SMTP):**
```env
SMTP_HOST=smtp.hostinger.com
SMTP_PORT=587
SMTP_USER=noreply@mykitchenfarm.com
SMTP_PASS=your_email_password
```

**Fast2SMS:**
```env
FAST2SMS_API_KEY=your_api_key
```

**Google Meet:**
```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_secret
```

**Razorpay:**
```env
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_secret
```

---

## 🐛 Troubleshooting

### Common Issues

**500 Internal Server Error**
- Check PHP version (must be 8.0+)
- Verify `.htaccess` exists
- Check error logs in cPanel

**Database Connection Failed**
- Verify credentials in `.env`
- Check database user permissions
- Ensure database exists

**Admin Login Not Working**
- Run password update SQL query
- Clear browser cache
- Check JWT_SECRET is set

**Page Not Found (404)**
- Verify `.htaccess` is in root
- Check mod_rewrite is enabled
- Ensure index.html exists

---

## 📊 Sample Data

The database comes with 3 sample healthcare professionals:

1. **Dr. Rakesh Zha**
   - MBBS, MD (General Medicine)
   - 13 years experience
   - Fee: ₹700

2. **Dr. Rubina Shah**
   - BAMS, MD (Rasashastra)
   - 8 years experience
   - Fee: ₹500

3. **Sania Batra**
   - Wellness Coach
   - 5 years experience
   - Fee: ₹300

---

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- SQL injection protection (PDO prepared statements)
- XSS protection headers
- CSRF token validation
- Secure file upload validation
- HTTPS enforcement

---

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

---

## 🤝 Support

### Hostinger Support
- **Live Chat:** 24/7 in cPanel
- **Email:** support@hostinger.com
- **Knowledge Base:** https://support.hostinger.com/

### Project Issues
- Check documentation first
- Review error logs
- Contact Hostinger support for hosting issues

---

## 📝 License

This project is proprietary software. All rights reserved.

---

## 🎉 Credits

**Developed by:** TeleCareZone Development Team  
**Platform:** Built on Hostinger  
**Domain:** mykitchenfarm.com

---

## 🚀 Getting Started

1. Read: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
2. Follow: [HOSTINGER_DEPLOYMENT_GUIDE.md](HOSTINGER_DEPLOYMENT_GUIDE.md)
3. Deploy: Upload files to Hostinger
4. Test: Visit your domain
5. Customize: Add your healthcare professionals

**Deployment Time:** 15-30 minutes  
**Difficulty:** Easy

---

**Need help?** See the deployment guide or contact Hostinger support! 🚀
