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

## 🚀 Deployment

### Prerequisites
- Hostinger shared hosting account
- Domain name (telecarezone.com)
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
   - Visit: https://telecarezone.com
   - Login: teleadmin / teleadm@2026

### Detailed Instructions

📖 **See:** [HOSTINGER_DEPLOYMENT_GUIDE.md](HOSTINGER_DEPLOYMENT_GUIDE.md)

📋 **Quick Reference:** [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## 🔑 Default Credentials

**Admin Dashboard:**
- URL: https://telecarezone.com/admin/login
- Username: `teleadmin`
- Password: `teleadm@2026`

⚠️ **Important:** Change the admin password after first login!

---

## 📚 Documentation

- **[Hostinger Deployment Guide](HOSTINGER_DEPLOYMENT_GUIDE.md)** - Complete deployment instructions
- **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Quick reference checklist
- **[XAMPP Setup Guide](XAMPP_SETUP_GUIDE.md)** - Local development setup

---

## 🧪 Testing

### Test URLs

**Homepage:**
```
https://telecarezone.com
```

**API Health Check:**
```
https://telecarezone.com/api
```

**Admin Dashboard:**
```
https://telecarezone.com/admin/dashboard
```

**Doctor Landing Pages:**
```
https://telecarezone.com/doctor/priya-sharma
https://telecarezone.com/doctor/rajesh-kumar
https://telecarezone.com/doctor/ananya-desai
```

---

## 📝 License

This project is proprietary software. All rights reserved.

---

## 🎉 Credits

**Developed by:** TeleCareZone Development Team  
**Platform:** Built on Hostinger  
**Domain:** telecarezone.com

---

**Need help?** See the deployment guide or contact Hostinger support! 🚀