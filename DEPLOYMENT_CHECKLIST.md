# ✅ Hostinger Deployment - Quick Checklist

**Domain:** mykitchenfarm.com  
**Database:** u913267094_telecaredev

---

## 🚀 Pre-Deployment (Do on Local Machine)

- [ ] Download all files from GitHub
- [ ] Verify all files are present
- [ ] No code changes needed (already configured)

---

## 📤 Upload to Hostinger

### Files to Upload to public_html/:
- [ ] `index.html` (React frontend)
- [ ] `api_index.php` (Backend API)
- [ ] `.htaccess` (URL rewriting rules)
- [ ] `api/` folder (API endpoints)
- [ ] `config/` folder (with .env file)
- [ ] `services/` folder (business logic)
- [ ] `models/` folder (data models)
- [ ] `uploads/` folder (file storage)
- [ ] `static/` folder (React assets)
- [ ] `vendor/` folder (PHP dependencies)
- [ ] `database_import.sql` (database schema)

---

## 🗄️ Database Setup

- [ ] Open phpMyAdmin in cPanel
- [ ] Select database: `u913267094_telecaredev`
- [ ] Import `database_import.sql`
- [ ] Run admin password update query:
```sql
UPDATE admin_users 
SET password = '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi' 
WHERE username = 'admin';
```
- [ ] Verify 3 doctors imported (professionals table)

---

## ⚙️ Configuration (Must Do!)

### Edit config/.env file:

```env
DB_PASS=YOUR_ACTUAL_PASSWORD    ← Update this!
JWT_SECRET=random_32_chars      ← Generate new!
```

**Get Your Database Password:**
1. Hostinger cPanel → MySQL Databases
2. Find database user password
3. Paste in .env file

**Generate JWT Secret:**
- Visit: https://www.random.org/strings/
- Generate 32-character string
- Paste in .env file

---

## 🔒 SSL Setup

- [ ] cPanel → SSL → Install Free SSL
- [ ] Wait 10 minutes for activation
- [ ] Add HTTPS redirect to .htaccess (already included)

---

## 🧪 Testing (Must Test All!)

### Test 1: Homepage
- [ ] Visit: https://mykitchenfarm.com
- [ ] Should show 3 doctor cards

### Test 2: API
- [ ] Visit: https://mykitchenfarm.com/api
- [ ] Should return JSON with version info

### Test 3: Admin Login
- [ ] Visit: https://mykitchenfarm.com/admin/login
- [ ] Login: admin / admin123
- [ ] Should redirect to dashboard

### Test 4: Doctor Pages
- [ ] https://mykitchenfarm.com/doctor/rakeshzha
- [ ] https://mykitchenfarm.com/doctor/rubinashah
- [ ] https://mykitchenfarm.com/doctor/saniabatra

### Test 5: Admin Features
- [ ] Onboarding form: /admin/onboarding
- [ ] Doctor management: /admin/doctors
- [ ] Analytics: /admin/analytics
- [ ] Leads: /admin/leads

---

## 🐛 If Something Goes Wrong

### Problem: 500 Error
**Fix:** Check PHP version (must be 8.0+)
- cPanel → PHP Configuration → Select PHP 8.0+

### Problem: Database Error
**Fix:** Verify .env password is correct
- Double-check DB_PASS in config/.env

### Problem: Can't Login
**Fix:** Re-run password update SQL
- Use query from Database Setup section

### Problem: Page Not Found
**Fix:** Check .htaccess exists in root
- Should be in public_html/ directory

---

## 📁 File Permissions

Set these in cPanel File Manager:

- `uploads/` → 755
- `config/` → 755
- All folders → 755
- All files → 644

---

## 🎯 Success Criteria

✅ Homepage loads with doctors  
✅ API responds with JSON  
✅ Admin login works  
✅ All admin features accessible  
✅ No errors in browser console  
✅ SSL padlock shows in browser  

---

## ⏳ Configure Later (Optional)

These require external API keys (not needed for basic functionality):

- Email notifications (SMTP setup)
- WhatsApp/SMS (Fast2SMS API)
- Google Meet (OAuth setup)
- Razorpay payments (API keys)

**Instructions:** See HOSTINGER_DEPLOYMENT_GUIDE.md

---

## 🆘 Need Help?

1. **Check Error Log**: cPanel → Error Log
2. **Hostinger Support**: 24/7 live chat in cPanel
3. **Review Full Guide**: HOSTINGER_DEPLOYMENT_GUIDE.md

---

**Estimated Deployment Time:** 15-30 minutes  
**Difficulty:** Easy (Just follow checklist!)

🎉 **Good luck with your deployment!**
