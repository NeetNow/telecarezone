# MongoDB to MySQL Migration Guide
## For Hostinger Hosting Deployment

---

## Overview

TeleCareZone backend is built with **dual database support**:
- **MongoDB** - Currently running on Emergent
- **MySQL** - Ready for Hostinger deployment

The backend **automatically detects** which database to use based on the environment. No code changes needed!

---

## How Auto-Detection Works

The backend checks the environment and automatically switches:

```php
// In /app/backend/config/database.php

if (getenv('DB_TYPE') === 'mysql' || file_exists('/var/www/html/.htaccess')) {
    // Use MySQL (Hostinger detected)
    $this->connectMySQL();
} else {
    // Use MongoDB (Emergent)
    $this->connectMongoDB();
}
```

**When you upload to Hostinger**, it detects the `.htaccess` file and automatically uses MySQL!

---

## Step-by-Step Migration to Hostinger

### Step 1: Backup MongoDB Data

On Emergent, export your current data:

```bash
# Export professionals
mongoexport --uri="mongodb://localhost:27017/telecarezone_db" \
  --collection=professionals \
  --out=/tmp/professionals.json

# Export testimonials
mongoexport --uri="mongodb://localhost:27017/telecarezone_db" \
  --collection=testimonials \
  --out=/tmp/testimonials.json

# Export admin users
mongoexport --uri="mongodb://localhost:27017/telecarezone_db" \
  --collection=admin_users \
  --out=/tmp/admin_users.json

# Export appointments (if any)
mongoexport --uri="mongodb://localhost:27017/telecarezone_db" \
  --collection=appointments \
  --out=/tmp/appointments.json
```

---

### Step 2: Hostinger Setup

#### A. Login to Hostinger cPanel

1. Go to your Hostinger dashboard
2. Click on **cPanel** or **hPanel**
3. Navigate to **Databases** section

#### B. Create MySQL Database

1. Click **MySQL Databases**
2. Create new database:
   - Database name: `telecarezone_db`
3. Create database user:
   - Username: `telecarezone_user`
   - Password: `[generate strong password]`
4. Add user to database with **ALL PRIVILEGES**
5. Note down:
   - Database name
   - Username
   - Password
   - Host (usually `localhost`)

#### C. Import Database Schema

1. Go to **phpMyAdmin** in cPanel
2. Select your database: `telecarezone_db`
3. Click **Import** tab
4. Choose file: `/app/backend/database/mysql_schema.sql`
5. Click **Go**

✅ Your database structure is now created!

---

### Step 3: Upload Backend Files to Hostinger

#### A. Using File Manager (cPanel)

1. Go to **File Manager** in cPanel
2. Navigate to `public_html/`
3. Create folder structure:
   ```
   public_html/
   ├── api/
   ├── config/
   ├── services/
   └── .htaccess
   ```

4. Upload all files from `/app/backend/`:
   - Upload `api/` folder → to `public_html/api/`
   - Upload `config/` folder → to `public_html/config/`
   - Upload `services/` folder → to `public_html/services/`
   - Upload `public/index.php` → to `public_html/index.php`
   - Upload `config/.htaccess` → to `public_html/.htaccess`

#### B. Using FTP (FileZilla)

1. Open FileZilla
2. Connect to Hostinger FTP:
   - Host: Your Hostinger domain
   - Username: Your FTP username
   - Password: Your FTP password
   - Port: 21

3. Upload `/app/backend/` contents to `public_html/`

---

### Step 4: Configure Database Connection

#### Option A: Edit config file directly

1. In File Manager, navigate to `public_html/config/database.php`
2. Click **Edit**
3. Update MySQL credentials:

```php
// Around line 13-16
private $mysql_host = 'localhost';  // Usually localhost on Hostinger
private $mysql_user = 'telecarezone_user';  // Your database user
private $mysql_pass = 'your_strong_password';  // Your database password
private $mysql_db = 'telecarezone_db';  // Your database name
```

4. Save file

#### Option B: Use environment variables (Recommended)

Create `.env` file in `public_html/`:

```env
DB_TYPE=mysql
DB_HOST=localhost
DB_USER=telecarezone_user
DB_PASSWORD=your_strong_password
DB_NAME=telecarezone_db

RAZORPAY_KEY_ID=rzp_live_xxxxx
RAZORPAY_KEY_SECRET=your_secret
FAST2SMS_API_KEY=your_api_key
```

Then update `database.php` to read from .env

---

### Step 5: Migrate Data from MongoDB to MySQL

You have two options:

#### Option A: Manual Data Entry via Admin Panel

1. Login to admin: `https://yourdomain.com/admin/login`
2. Manually create professionals through admin interface
3. Add testimonials for each professional

#### Option B: Automated Migration Script

Create `migrate.php` in `public_html/`:

```php
<?php
require_once 'config/config.php';

// Read MongoDB exports
$professionals = json_decode(file_get_contents('/path/to/professionals.json'), true);
$testimonials = json_decode(file_get_contents('/path/to/testimonials.json'), true);

$db = Database::getInstance();
$conn = $db->getConnection();

// Migrate professionals
foreach ($professionals as $prof) {
    $stmt = $conn->prepare("INSERT INTO professionals 
        (id, first_name, last_name, phone, email, speciality, consulting_fees, subdomain, status, created_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
    
    $stmt->execute([
        $prof['id'],
        $prof['first_name'],
        $prof['last_name'],
        $prof['phone'],
        $prof['email'],
        $prof['speciality'] ?? null,
        $prof['consulting_fees'],
        $prof['subdomain'],
        $prof['status'],
        date('Y-m-d H:i:s')
    ]);
}

echo "Migration completed!";
?>
```

Run once: `https://yourdomain.com/migrate.php`

Then **DELETE** the migrate.php file for security!

---

### Step 6: Test the Setup

#### A. Test API Root

Visit: `https://yourdomain.com/api/`

Should return:
```json
{
  "message": "TeleCareZone API - PHP Backend",
  "version": "1.0.0"
}
```

#### B. Create Default Admin

Visit: `https://yourdomain.com/api/admin/create-default`

Should return:
```json
{
  "message": "Default admin created",
  "username": "admin",
  "password": "admin123"
}
```

#### C. Test Admin Login

```bash
curl -X POST https://yourdomain.com/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Should return JWT token.

#### D. Test Professional List

Visit: `https://yourdomain.com/api/professionals/approved`

Should return array of professionals (empty if no data migrated yet).

---

### Step 7: Update Frontend

Update React app to use new backend URL:

1. Edit `/app/frontend/.env`:
```env
REACT_APP_BACKEND_URL=https://yourdomain.com
```

2. Rebuild frontend:
```bash
cd /app/frontend
yarn build
```

3. Upload `build/` folder contents to Hostinger:
   - Upload to `public_html/` or subdomain folder

---

## Verification Checklist

After migration, verify:

- [ ] API root endpoint works
- [ ] Admin login works
- [ ] Professionals list displays
- [ ] Can create new professional via admin
- [ ] Frontend connects to PHP backend
- [ ] Appointment booking works
- [ ] Payment flow functional (with Razorpay keys)
- [ ] WhatsApp notifications work (with Fast2SMS key)

---

## Database Comparison

### MongoDB (Emergent)
```javascript
// Data structure
{
  "_id": ObjectId("..."),
  "id": "prof_abc123",
  "first_name": "John",
  "last_name": "Doe",
  ...
}
```

### MySQL (Hostinger)
```sql
-- Table structure
CREATE TABLE professionals (
  id VARCHAR(50) PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  ...
)
```

**Key Differences:**
- MongoDB uses `_id` (ObjectId) - ignored in our code
- MySQL uses `id` (VARCHAR) - our primary identifier
- Both use the same `id` field for queries
- No code changes needed!

---

## Troubleshooting

### Issue: "Database connection failed"

**Solution:**
1. Check MySQL credentials in `config/database.php`
2. Verify database exists in phpMyAdmin
3. Ensure user has privileges
4. Check Hostinger firewall settings

### Issue: "Table doesn't exist"

**Solution:**
1. Re-import `mysql_schema.sql` in phpMyAdmin
2. Verify all 6 tables created:
   - professionals
   - appointments
   - patients
   - payments
   - testimonials
   - admin_users

### Issue: "500 Internal Server Error"

**Solution:**
1. Check PHP error logs in cPanel
2. Verify PHP version is 8.0+
3. Ensure all files uploaded correctly
4. Check file permissions (755 for folders, 644 for files)

### Issue: "CORS error in frontend"

**Solution:**
1. Check `config/config.php` - ensure CORS headers present
2. Update `.htaccess` with CORS headers:
```apache
Header set Access-Control-Allow-Origin "*"
Header set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
Header set Access-Control-Allow-Headers "Content-Type, Authorization"
```

---

## Rollback Plan

If migration fails, you can rollback:

1. **Keep Emergent backend running** (don't delete `/app/backend-python-old/`)
2. Frontend can switch back: `REACT_APP_BACKEND_URL=https://emergent-url.com/api`
3. Debug Hostinger setup
4. Try migration again

---

## Performance Notes

### MongoDB vs MySQL Performance

**MongoDB (Emergent):**
- Good for rapid development
- Flexible schema
- No joins needed

**MySQL (Hostinger):**
- Better for production
- ACID compliance
- Better indexing
- Industry standard
- cPanel integration

**Both perform well for TeleCareZone scale (<10K records)**

---

## Security Best Practices

After migration to Hostinger:

1. **Change default admin password**
   ```sql
   UPDATE admin_users 
   SET password = '$2y$10$NEW_HASH_HERE' 
   WHERE username = 'admin';
   ```

2. **Remove migrate.php** after data migration

3. **Set proper file permissions**
   ```bash
   chmod 755 public_html
   chmod 644 public_html/*.php
   ```

4. **Enable HTTPS** (Let's Encrypt via cPanel)

5. **Regular backups** (Hostinger Auto Backup recommended)

---

## Cost Comparison

### Emergent (MongoDB)
- Development environment
- Free tier available
- MongoDB hosting

### Hostinger (MySQL)
- Production hosting
- Starting ₹79/month
- MySQL included
- cPanel included
- 24/7 support
- 99.9% uptime

---

## Support

### Hostinger Support
- Live Chat: 24/7
- Email: support@hostinger.com
- Knowledge Base: https://support.hostinger.com

### TeleCareZone Issues
- Check documentation in `/app/`
- Review error logs
- Test API endpoints individually

---

## Quick Reference Commands

### Export from MongoDB
```bash
mongoexport --uri="mongodb://localhost:27017/telecarezone_db" \
  --collection=professionals --out=professionals.json
```

### Import to MySQL
```bash
mysql -u username -p database_name < mysql_schema.sql
```

### Check MySQL Connection
```bash
mysql -u telecarezone_user -p -e "SHOW DATABASES;"
```

### Test PHP Backend
```bash
curl https://yourdomain.com/api/
```

---

## Summary

**Migration is Simple:**
1. ✅ Create MySQL database on Hostinger
2. ✅ Import schema (mysql_schema.sql)
3. ✅ Upload backend files
4. ✅ Update database credentials
5. ✅ Migrate data (optional - can start fresh)
6. ✅ Test API endpoints
7. ✅ Update frontend URL
8. ✅ Go live!

**No code changes needed - backend auto-detects database type!**

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Platform:** TeleCareZone Healthcare SAAS
