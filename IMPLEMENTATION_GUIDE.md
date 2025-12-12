# 🎯 TeleCareZone - Complete Implementation Guide

## ✅ What Has Been Completed

### 1. XAMPP Compatibility & Restructuring ✅
- **Moved index.php to root directory** (`/app/index.php`)
- **Created comprehensive .htaccess** for Apache URL rewriting
- **Updated all paths** to work from root
- **Created XAMPP_SETUP_GUIDE.md** with step-by-step local setup instructions
- **Enhanced database.php** with detailed comments and auto-detection
- **Maintained backward compatibility** with Emergent platform (Python bridge still works)

### 2. Admin Onboarding API - Backend Complete ✅
- **Created `/app/api/admin_onboarding.php`** with 27-field comprehensive form support
- **All fields implemented:**
  - ✅ Profile Photo (file upload)
  - ✅ First Name, Last Name, Email
  - ✅ Country, State dropdowns
  - ✅ Display Name
  - ✅ Profession + Qualification
  - ✅ Bio (long text)
  - ✅ Display Theme (20 color options)
  - ✅ Social Media URLs (Instagram, YouTube, LinkedIn, Facebook, Twitter)
  - ✅ Bank Details (Account Name, Number, IFSC, Branch)
  - ✅ Appointment Days (Multi-select Monday-Sunday)
  - ✅ Morning Time, Evening Time
  - ✅ Intro Video Link
  - ✅ Testimonial URLs (3 videos)
  - ✅ Consulting Fee

- **API Endpoints Created:**
  ```
  POST   /api/admin/onboarding/create      - Create new professional
  GET    /api/admin/onboarding/list        - List all professionals
  GET    /api/admin/onboarding/:id         - Get single professional
  PUT    /api/admin/onboarding/:id         - Update professional
  DELETE /api/admin/onboarding/:id         - Delete professional
  POST   /api/admin/onboarding/upload      - Handle file uploads
  ```

### 3. Database Schema Enhanced ✅
- **Created `/app/backend/database/mysql_schema_enhanced.sql`**
- **Added all 27 onboarding fields** to professionals table
- **Included 3 sample professionals:**
  - Dr. Rakesh Zha (MBBS MD, 13 years exp, ₹700)
  - Dr. Rubina Shah (BAMS MD, 8 years exp, ₹500)
  - Sania Batra (Wellness Coach, 5 years exp, ₹300)

### 4. Documentation Created ✅
- **XAMPP_SETUP_GUIDE.md** - Complete local setup guide
- **Extensive inline comments** in all PHP files
- **Architecture alignment** with provided diagram

---

## 📋 Next Implementation Steps

### STEP 1: Admin Dashboard Frontend (React)

Create a comprehensive admin dashboard with the following pages:

#### File Structure:
```
/app/frontend/src/pages/admin/
├── AdminOnboarding.jsx          # 27-field onboarding form
├── DoctorsList.jsx              # List all doctors with actions
├── Analytics.jsx                # Platform & doctor analytics
├── NewLeads.jsx                 # Join expert form submissions
└── AccountsReceivable.jsx       # Financial reports
```

#### A. Admin Onboarding Form Component (`AdminOnboarding.jsx`)

```jsx
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import axios from 'axios';
import { toast } from 'sonner';

const THEME_COLORS = [
  '#667eea', '#3B82F6', '#10B981', '#F59E0B', '#EF4444',
  '#8B5CF6', '#EC4899', '#14B8A6', '#F97316', '#06B6D4',
  '#84CC16', '#A855F7', '#F43F5E', '#22C55E', '#FACC15',
  '#6366F1', '#EAB308', '#10B981', '#8B5CF6', '#F59E0B'
];

const COUNTRIES = ['India', 'USA', 'UK', 'Canada', 'Australia'];
const INDIAN_STATES = [
  'Maharashtra', 'Gujarat', 'Karnataka', 'Tamil Nadu', 'Delhi',
  'Uttar Pradesh', 'West Bengal', 'Rajasthan', 'Punjab', 'Haryana'
];

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

export default function AdminOnboarding() {
  const [formData, setFormData] = useState({
    // Basic Info
    first_name: '',
    last_name: '',
    email: '',
    country: 'India',
    state: '',
    display_name: '',
    
    // Professional Info
    profession_qualification: '',
    bio: '',
    theme_color: '#667eea',
    
    // Social Media
    instagram: '',
    youtube: '',
    linkedin: '',
    facebook: '',
    twitter: '',
    
    // Bank Details
    bank_account_name: '',
    bank_account_number: '',
    bank_ifsc_code: '',
    bank_branch: '',
    
    // Appointment Settings
    appointment_days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    morning_time: '9:00 AM - 1:00 PM',
    evening_time: '5:00 PM - 9:00 PM',
    
    // Media Links
    intro_video: '',
    testimonial_1: '',
    testimonial_2: '',
    testimonial_3: '',
    
    // Fee
    consulting_fees: 500,
    
    // File Upload
    profile_photo: ''
  });

  const [uploading, setUploading] = useState(false);

  // Handle file upload
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('profile_photo', file);

    setUploading(true);
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/api/admin/onboarding/upload`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('admin_token')}`
          }
        }
      );
      
      setFormData(prev => ({
        ...prev,
        profile_photo: response.data.files.profile_photo
      }));
      
      toast.success('Profile photo uploaded successfully');
    } catch (error) {
      toast.error('File upload failed');
    } finally {
      setUploading(false);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/api/admin/onboarding/create`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('admin_token')}`,
            'Content-Type': 'application/json'
          }
        }
      );

      toast.success(`Professional created! Landing page: ${response.data.landing_page_url}`);
      
      // Reset form
      setFormData({...initialState});
      
    } catch (error) {
      toast.error(error.response?.data?.error || 'Failed to create professional');
    }
  };

  // Handle day selection
  const toggleDay = (day) => {
    setFormData(prev => ({
      ...prev,
      appointment_days: prev.appointment_days.includes(day)
        ? prev.appointment_days.filter(d => d !== day)
        : [...prev.appointment_days, day]
    }));
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Doctor Onboarding</h1>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Profile Photo Upload */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Profile Photo</h2>
          <Input 
            type="file" 
            accept="image/*"
            onChange={handleFileUpload}
            disabled={uploading}
          />
          {formData.profile_photo && (
            <img 
              src={formData.profile_photo} 
              alt="Profile" 
              className="mt-4 w-32 h-32 rounded-full object-cover"
            />
          )}
        </Card>

        {/* Basic Information */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Basic Information</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>First Name *</Label>
              <Input
                value={formData.first_name}
                onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                required
              />
            </div>
            <div>
              <Label>Last Name *</Label>
              <Input
                value={formData.last_name}
                onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                required
              />
            </div>
            <div>
              <Label>Email *</Label>
              <Input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
            </div>
            <div>
              <Label>Country *</Label>
              <Select 
                value={formData.country}
                onValueChange={(value) => setFormData({...formData, country: value})}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {COUNTRIES.map(country => (
                    <SelectItem key={country} value={country}>{country}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>State *</Label>
              <Select 
                value={formData.state}
                onValueChange={(value) => setFormData({...formData, state: value})}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {INDIAN_STATES.map(state => (
                    <SelectItem key={state} value={state}>{state}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Display Name *</Label>
              <Input
                value={formData.display_name}
                onChange={(e) => setFormData({...formData, display_name: e.target.value})}
                placeholder="Dr. John Doe"
                required
              />
            </div>
          </div>
        </Card>

        {/* Professional Information */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Professional Information</h2>
          <div className="space-y-4">
            <div>
              <Label>Profession + Qualification</Label>
              <Input
                value={formData.profession_qualification}
                onChange={(e) => setFormData({...formData, profession_qualification: e.target.value})}
                placeholder="MBBS, MD (General Medicine)"
              />
            </div>
            <div>
              <Label>Bio</Label>
              <Textarea
                value={formData.bio}
                onChange={(e) => setFormData({...formData, bio: e.target.value})}
                rows={5}
                placeholder="Write a professional bio..."
              />
            </div>
          </div>
        </Card>

        {/* Theme Color Selection */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Landing Page Theme</h2>
          <Label>Choose Theme Color</Label>
          <div className="grid grid-cols-10 gap-2 mt-2">
            {THEME_COLORS.map(color => (
              <button
                key={color}
                type="button"
                className={`w-10 h-10 rounded-full border-2 ${
                  formData.theme_color === color ? 'border-black' : 'border-gray-300'
                }`}
                style={{ backgroundColor: color }}
                onClick={() => setFormData({...formData, theme_color: color})}
              />
            ))}
          </div>
        </Card>

        {/* Social Media Links */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Social Media URLs</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Instagram</Label>
              <Input
                type="url"
                value={formData.instagram}
                onChange={(e) => setFormData({...formData, instagram: e.target.value})}
                placeholder="https://instagram.com/..."
              />
            </div>
            <div>
              <Label>YouTube</Label>
              <Input
                type="url"
                value={formData.youtube}
                onChange={(e) => setFormData({...formData, youtube: e.target.value})}
                placeholder="https://youtube.com/..."
              />
            </div>
            <div>
              <Label>LinkedIn</Label>
              <Input
                type="url"
                value={formData.linkedin}
                onChange={(e) => setFormData({...formData, linkedin: e.target.value})}
                placeholder="https://linkedin.com/..."
              />
            </div>
            <div>
              <Label>Facebook</Label>
              <Input
                type="url"
                value={formData.facebook}
                onChange={(e) => setFormData({...formData, facebook: e.target.value})}
                placeholder="https://facebook.com/..."
              />
            </div>
            <div>
              <Label>Twitter</Label>
              <Input
                type="url"
                value={formData.twitter}
                onChange={(e) => setFormData({...formData, twitter: e.target.value})}
                placeholder="https://twitter.com/..."
              />
            </div>
          </div>
        </Card>

        {/* Bank Details */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Bank Account Details</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Account Holder Name</Label>
              <Input
                value={formData.bank_account_name}
                onChange={(e) => setFormData({...formData, bank_account_name: e.target.value})}
              />
            </div>
            <div>
              <Label>Account Number</Label>
              <Input
                type="number"
                value={formData.bank_account_number}
                onChange={(e) => setFormData({...formData, bank_account_number: e.target.value})}
              />
            </div>
            <div>
              <Label>IFSC Code</Label>
              <Input
                value={formData.bank_ifsc_code}
                onChange={(e) => setFormData({...formData, bank_ifsc_code: e.target.value})}
              />
            </div>
            <div>
              <Label>Home Branch</Label>
              <Input
                value={formData.bank_branch}
                onChange={(e) => setFormData({...formData, bank_branch: e.target.value})}
              />
            </div>
          </div>
        </Card>

        {/* Appointment Schedule */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Appointment Schedule</h2>
          <div className="space-y-4">
            <div>
              <Label>Available Days</Label>
              <div className="flex flex-wrap gap-2 mt-2">
                {DAYS.map(day => (
                  <button
                    key={day}
                    type="button"
                    className={`px-4 py-2 rounded-lg border ${
                      formData.appointment_days.includes(day)
                        ? 'bg-purple-600 text-white border-purple-600'
                        : 'bg-white text-gray-700 border-gray-300'
                    }`}
                    onClick={() => toggleDay(day)}
                  >
                    {day}
                  </button>
                ))}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Morning Time</Label>
                <Input
                  value={formData.morning_time}
                  onChange={(e) => setFormData({...formData, morning_time: e.target.value})}
                  placeholder="9:00 AM - 1:00 PM"
                />
              </div>
              <div>
                <Label>Evening Time</Label>
                <Input
                  value={formData.evening_time}
                  onChange={(e) => setFormData({...formData, evening_time: e.target.value})}
                  placeholder="5:00 PM - 9:00 PM"
                />
              </div>
            </div>
          </div>
        </Card>

        {/* Media Links */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Video Links</h2>
          <div className="space-y-4">
            <div>
              <Label>Intro Video URL</Label>
              <Input
                type="url"
                value={formData.intro_video}
                onChange={(e) => setFormData({...formData, intro_video: e.target.value})}
                placeholder="YouTube or Vimeo link"
              />
            </div>
            <div>
              <Label>Testimonial Video 1</Label>
              <Input
                type="url"
                value={formData.testimonial_1}
                onChange={(e) => setFormData({...formData, testimonial_1: e.target.value})}
              />
            </div>
            <div>
              <Label>Testimonial Video 2</Label>
              <Input
                type="url"
                value={formData.testimonial_2}
                onChange={(e) => setFormData({...formData, testimonial_2: e.target.value})}
              />
            </div>
            <div>
              <Label>Testimonial Video 3</Label>
              <Input
                type="url"
                value={formData.testimonial_3}
                onChange={(e) => setFormData({...formData, testimonial_3: e.target.value})}
              />
            </div>
          </div>
        </Card>

        {/* Consulting Fee */}
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Consulting Fee</h2>
          <div>
            <Label>Consultation Fee (₹)</Label>
            <Input
              type="number"
              value={formData.consulting_fees}
              onChange={(e) => setFormData({...formData, consulting_fees: parseFloat(e.target.value)})}
              min="0"
              step="50"
            />
          </div>
        </Card>

        {/* Submit Button */}
        <Button 
          type="submit" 
          className="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 text-lg"
        >
          Create Professional Profile
        </Button>
      </form>
    </div>
  );
}
```

---

### STEP 2: Expert Landing Pages (3 Fully Functional Pages)

#### Implementation Plan:

1. **Update React Router** in `/app/frontend/src/App.js`:

```jsx
// Add these routes
<Route path="/doctor/:subdomain" element={<ExpertLanding />} />
<Route path="/doctor/:subdomain/book" element={<BookingFlow />} />
```

2. **Create Expert Landing Page Component** (`ExpertLanding.jsx`):

```jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function ExpertLanding() {
  const { subdomain } = useParams();
  const navigate = useNavigate();
  const [expert, setExpert] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch expert data by subdomain
    const fetchExpert = async () => {
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_BACKEND_URL}/api/public/professional/${subdomain}`
        );
        setExpert(response.data);
      } catch (error) {
        console.error('Expert not found');
      } finally {
        setLoading(false);
      }
    };

    fetchExpert();
  }, [subdomain]);

  if (loading) return <div>Loading...</div>;
  if (!expert) return <div>Expert not found</div>;

  return (
    <div className="min-h-screen" style={{ backgroundColor: expert.theme_color + '10' }}>
      {/* Header */}
      <header className="bg-white shadow-sm p-6">
        <div className="container mx-auto flex items-center justify-between">
          <h1 className="text-2xl font-bold">{expert.display_name}</h1>
          <button 
            onClick={() => navigate(`/doctor/${subdomain}/book`)}
            className="px-6 py-3 rounded-lg text-white"
            style={{ backgroundColor: expert.theme_color }}
          >
            Book Appointment
          </button>
        </div>
      </header>

      {/* Profile Section */}
      <section className="container mx-auto py-12">
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <img 
              src={expert.profile_photo || '/default-profile.png'} 
              alt={expert.display_name}
              className="w-64 h-64 rounded-full object-cover mx-auto"
            />
          </div>
          <div>
            <h2 className="text-4xl font-bold mb-2">{expert.display_name}</h2>
            <p className="text-xl text-gray-600 mb-4">{expert.profession_qualification}</p>
            <p className="text-lg mb-4">{expert.bio}</p>
            <p className="text-2xl font-bold" style={{ color: expert.theme_color }}>
              ₹{expert.consulting_fees} per consultation
            </p>
          </div>
        </div>
      </section>

      {/* Social Media Links */}
      {(expert.instagram || expert.youtube || expert.linkedin) && (
        <section className="container mx-auto py-8">
          <h3 className="text-2xl font-bold mb-4">Connect with me</h3>
          <div className="flex gap-4">
            {expert.instagram && (
              <a href={expert.instagram} target="_blank" className="text-purple-600">Instagram</a>
            )}
            {expert.youtube && (
              <a href={expert.youtube} target="_blank" className="text-red-600">YouTube</a>
            )}
            {expert.linkedin && (
              <a href={expert.linkedin} target="_blank" className="text-blue-600">LinkedIn</a>
            )}
          </div>
        </section>
      )}

      {/* Intro Video */}
      {expert.intro_video && (
        <section className="container mx-auto py-8">
          <h3 className="text-2xl font-bold mb-4">Introduction</h3>
          <iframe 
            src={expert.intro_video} 
            className="w-full h-96 rounded-lg"
            allowFullScreen
          />
        </section>
      )}

      {/* Book Now CTA */}
      <section className="text-center py-12">
        <button 
          onClick={() => navigate(`/doctor/${subdomain}/book`)}
          className="px-12 py-4 rounded-lg text-white text-xl font-bold"
          style={{ backgroundColor: expert.theme_color }}
        >
          Book Your Consultation Now
        </button>
      </section>
    </div>
  );
}
```

3. **Create Booking Flow** (`BookingFlow.jsx`) - Multi-step:
   - Step 1: Select Date & Time
   - Step 2: Patient Information
   - Step 3: Payment (Mock UI)
   - Step 4: Confirmation

---

### STEP 3: Enhanced Main Landing Page

Add to `/app/frontend/src/pages/MainLanding.jsx`:

1. **Testimonials Section**:
```jsx
<section className="py-16 bg-gray-50">
  <div className="container mx-auto">
    <h2 className="text-4xl font-bold text-center mb-12">What Our Patients Say</h2>
    <div className="grid md:grid-cols-3 gap-8">
      {testimonials.map(testimonial => (
        <Card key={testimonial.id}>
          <p className="italic">"{testimonial.content}"</p>
          <p className="font-bold mt-4">- {testimonial.patient_name}</p>
        </Card>
      ))}
    </div>
  </div>
</section>
```

2. **Blog Section**
3. **Company Mission**
4. **Government Guidelines Section**

---

## 📄 Testing Checklist

- [ ] XAMPP setup works locally (follow XAMPP_SETUP_GUIDE.md)
- [ ] Admin onboarding form creates professionals
- [ ] File upload works for profile photos
- [ ] 3 expert landing pages are accessible
- [ ] Booking flow works end-to-end
- [ ] Payment UI is complete (mock)
- [ ] Email/WhatsApp notifications configured

---

## 🚀 Deployment to Hostinger

1. Upload files via FTP to public_html
2. Import MySQL schema
3. Update config/database.php with production credentials
4. Build React frontend: `yarn build`
5. Configure .htaccess for production domain

---

**All backend APIs are complete and ready. Frontend components need to be built following the code samples above.**
