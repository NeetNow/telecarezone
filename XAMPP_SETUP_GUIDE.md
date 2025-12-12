# 🚀 TeleCareZone - XAMPP Local Setup Guide

This guide will help you clone and run TeleCareZone on your local XAMPP server.

---

## 📋 Prerequisites

Before you begin, make sure you have:

1. **XAMPP** installed (Download from [apachefriends.org](https://www.apachefriends.org))
2. **Git** installed (optional, for cloning)
3. **Composer** installed (Download from [getcomposer.org](https://getcomposer.org))
4. **Node.js & Yarn** (for React frontend - Download from [nodejs.org](https://nodejs.org))

---

## 📦 Step 1: Clone the Repository

### Option A: Using Git

```bash
cd C:\xampp\htdocs
git clone <repository-url> telecarezone
cd telecarezone
```

### Option B: Manual Download

1. Download the ZIP file from the repository
2. Extract to `C:\xampp\htdocs\telecarezone`

---

## ⚙️ Step 2: Install PHP Dependencies

Open Command Prompt or PowerShell in the project directory:

```bash
cd C:\xampp\htdocs\telecarezone
composer install
```

This will install the MongoDB PHP library and other dependencies.

---

## 🗄️ Step 3: Setup MySQL Database

### 3.1 Start XAMPP Services

1. Open **XAMPP Control Panel**
2. Start **Apache** and **MySQL** services

### 3.2 Create Database

1. Open your browser and go to: `http://localhost/phpmyadmin`
2. Click on **"New"** in the left sidebar
3. Create a new database named: `telecarezone_db`
4. Set Collation to: `utf8mb4_unicode_ci`

### 3.3 Import Database Schema

#### Method A: Using phpMyAdmin

1. In phpMyAdmin, select `telecarezone_db` database
2. Click on the **"Import"** tab
3. Click **"Choose File"** and select:
   ```
   C:\xampp\htdocs\telecarezone\backend\database\mysql_schema.sql
   ```
4. Click **"Go"** at the bottom

#### Method B: Using Command Line

```bash
cd C:\xampp\htdocs\telecarezone
C:\xampp\mysql\bin\mysql -u root -p telecarezone_db < backend\database\mysql_schema.sql
```

(Press Enter when asked for password if you haven't set one)

---

## 🔧 Step 4: Configure Database Connection

The application is already configured for XAMPP default settings:

- Host: `localhost`
- Username: `root`
- Password: `` (empty)
- Database: `telecarezone_db`

**If you have custom MySQL settings**, edit `/app/config/database.php`:

```php
// Line 13-16
private $mysql_host = 'localhost';
private $mysql_user = 'root';
private $mysql_pass = '';  // Add your password here
private $mysql_db = 'telecarezone_db';
```

---

## ⚛️ Step 5: Setup React Frontend

### 5.1 Install Frontend Dependencies

```bash
cd C:\xampp\htdocs\telecarezone\frontend
yarn install
```

### 5.2 Configure Backend URL

Edit `frontend/.env` file:

```
REACT_APP_BACKEND_URL=http://localhost
```

### 5.3 Build Frontend (Production)

```bash
cd C:\xampp\htdocs\telecarezone\frontend
yarn build
```

This creates a production-ready build in `frontend/build/` directory.

---

## 🌐 Step 6: Configure Apache

### Option A: Using .htaccess (Recommended)

The project already includes a `.htaccess` file. Make sure:

1. Open XAMPP Control Panel
2. Click **Config** button next to Apache
3. Select **httpd.conf**
4. Find the line: `AllowOverride None`
5. Change it to: `AllowOverride All`
6. Save and restart Apache

### Option B: Virtual Host (Advanced)

Edit `C:\xampp\apache\conf\extra\httpd-vhosts.conf`:

```apache
<VirtualHost *:80>
    ServerName telecarezone.local
    DocumentRoot "C:/xampp/htdocs/telecarezone"
    
    <Directory "C:/xampp/htdocs/telecarezone">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

Then edit `C:\Windows\System32\drivers\etc\hosts` (as Administrator):

```
127.0.0.1 telecarezone.local
```

---

## 🎯 Step 7: Access the Application

### Open your browser and navigate to:

**Using localhost:**
```
http://localhost/telecarezone
```

**Using virtual host:**
```
http://telecarezone.local
```

### Admin Dashboard:
```
http://localhost/telecarezone/admin/login
```

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 🧪 Step 8: Test API Endpoints

### Test API Health:
```
http://localhost/telecarezone/api
```

You should see:
```json
{
  "message": "TeleCareZone API - PHP Backend",
  "version": "2.0.0",
  "status": "operational",
  "database": "MySQL"
}
```

### Test Admin Login:

Using Postman or curl:
```bash
curl -X POST http://localhost/telecarezone/api/admin/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

---

## 📁 Project Structure

```
C:\xampp\htdocs\telecarezone\
├── index.php                  # Main entry point
├── .htaccess                  # Apache URL rewriting
├── composer.json              # PHP dependencies
├── config/                    # Configuration files
│   ├── config.php            # App config
│   └── database.php          # Database connection
├── api/                       # API endpoints
│   ├── auth.php              # Authentication
│   ├── professionals.php     # Doctor management
│   ├── appointments.php      # Bookings
│   └── ...
├── services/                  # Business logic
│   ├── JWTService.php
│   ├── RazorpayService.php
│   └── ...
├── models/                    # Data models
├── uploads/                   # User uploads
│   ├── profiles/
│   ├── videos/
│   └── documents/
├── frontend/                  # React application
│   ├── src/
│   ├── public/
│   └── build/                # Production build
└── backend/                   # Old backend (deprecated)
```

---

## 🔍 Troubleshooting

### Issue 1: "Database connection failed"

**Solution:**
- Ensure MySQL service is running in XAMPP Control Panel
- Check database credentials in `/config/database.php`
- Verify `telecarezone_db` database exists

### Issue 2: "404 Not Found" errors

**Solution:**
- Verify `.htaccess` file exists in root directory
- Check `httpd.conf` has `AllowOverride All`
- Restart Apache service

### Issue 3: "Composer not found"

**Solution:**
- Install Composer from [getcomposer.org](https://getcomposer.org)
- Add Composer to your system PATH
- Run: `composer --version` to verify

### Issue 4: Frontend not loading

**Solution:**
- Run `yarn build` in the frontend directory
- Check if `frontend/build/` directory exists
- Verify `.htaccess` routing rules

### Issue 5: File upload errors

**Solution:**
- Check folder permissions for `uploads/` directory
- Verify PHP settings in `php.ini`:
  ```ini
  upload_max_filesize = 50M
  post_max_size = 50M
  ```

---

## 🔒 Security Notes for Production

When deploying to production (Hostinger):

1. **Change Database Password:**
   ```php
   // config/database.php
   private $mysql_pass = 'YOUR_SECURE_PASSWORD';
   ```

2. **Update JWT Secret:**
   ```php
   // config/config.php
   define('JWT_SECRET', 'YOUR_RANDOM_SECRET_KEY_HERE');
   ```

3. **Set Error Display Off:**
   ```php
   // index.php (line 8)
   ini_set('display_errors', 0);
   ```

4. **Enable HTTPS:**
   - Update frontend `.env`:
     ```
     REACT_APP_BACKEND_URL=https://yourdomain.com
     ```

5. **Secure Uploads Directory:**
   - Add `.htaccess` in `uploads/` folder to prevent direct PHP execution

---

## 📚 Additional Resources

- **API Documentation:** `/API_DOCUMENTATION.md`
- **User Guide:** `/USER_GUIDE.md`
- **Features List:** `/FEATURES.md`
- **Migration Guide:** `/MONGODB_TO_MYSQL_MIGRATION.md`

---

## 🆘 Need Help?

1. Check the logs:
   - PHP Errors: `C:\xampp\apache\logs\error.log`
   - API Logs: Browser Developer Console (F12)

2. Common Commands:
   ```bash
   # Reinstall dependencies
   composer install
   
   # Rebuild frontend
   cd frontend && yarn build
   
   # Clear browser cache
   Ctrl + Shift + Delete
   ```

---

## ✅ Verification Checklist

Before starting development, verify:

- [ ] XAMPP Apache and MySQL services are running
- [ ] Database `telecarezone_db` is created with tables
- [ ] PHP dependencies installed (`vendor/` folder exists)
- [ ] Admin login works (`admin` / `admin123`)
- [ ] API responds at `http://localhost/telecarezone/api`
- [ ] Frontend loads at `http://localhost/telecarezone`
- [ ] Can upload files (test with profile photo upload)

---

## 🎉 You're All Set!

Your TeleCareZone platform is now running locally on XAMPP!

Happy Coding! 🚀
