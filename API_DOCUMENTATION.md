# TeleCareZone API Documentation

## Base URL
```
Production: https://telecarezone.com/api
Development: http://localhost:8001/api
```

## Authentication

Admin routes require JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### 1. Health Check

#### GET /
Check API status

**Response:**
```json
{
  "message": "TeleHealthZone API",
  "version": "1.0.0"
}
```

---

### 2. Admin Authentication

#### POST /admin/login
Login to admin dashboard

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- `200` - Success
- `401` - Invalid credentials

---

#### POST /admin/create-default
Create default admin user (one-time setup)

**Response:**
```json
{
  "message": "Default admin created",
  "username": "admin",
  "password": "admin123"
}
```

---

### 3. Professional Onboarding

#### POST /onboarding/submit
Submit healthcare professional application

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+919876543210",
  "email": "doctor@example.com",
  "speciality": "Cardiologist",
  "ug_qualification": "MBBS",
  "pg_qualification": "MD",
  "superspeciality": "DM Cardiology",
  "area_of_expertise": "Heart diseases, ECG interpretation",
  "instagram": "@drjohn",
  "youtube": "DrJohnChannel",
  "twitter": "@drjohn",
  "consulting_fees": 500.00
}
```

**Response:**
```json
{
  "id": "prof-uuid-here",
  "first_name": "John",
  "last_name": "Doe",
  "subdomain": "johndoe",
  "status": "pending",
  "created_at": "2025-01-15T10:30:00Z",
  ...
}
```

**Status Codes:**
- `200` - Application submitted successfully
- `400` - Invalid data

---

### 4. Professionals Management (Admin)

#### GET /professionals
Get all professionals (Admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `status` (optional): Filter by status (`pending`, `approved`, `rejected`)

**Response:**
```json
[
  {
    "id": "prof-uuid",
    "first_name": "John",
    "last_name": "Doe",
    "email": "doctor@example.com",
    "phone": "+919876543210",
    "speciality": "Cardiologist",
    "consulting_fees": 500.00,
    "subdomain": "johndoe",
    "status": "pending",
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

---

#### GET /professionals/{professional_id}
Get professional by ID (Admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "prof-uuid",
  "first_name": "John",
  "last_name": "Doe",
  ...
}
```

**Status Codes:**
- `200` - Success
- `404` - Professional not found
- `401` - Unauthorized

---

#### PUT /professionals/{professional_id}
Update professional details (Admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "status": "approved",
  "bio": "Experienced cardiologist with 15 years of practice",
  "experience_years": 15,
  "profile_photo": "https://example.com/photo.jpg"
}
```

**Response:**
```json
{
  "id": "prof-uuid",
  "status": "approved",
  ...
}
```

---

#### POST /professionals
Create new professional (Admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:** Same as onboarding submission

**Response:** Professional object with `status: "approved"`

---

### 5. Public Professional Data

#### GET /professionals/approved
Get all approved professionals (Public)

**Response:**
```json
[
  {
    "id": "prof-uuid",
    "first_name": "John",
    "last_name": "Doe",
    "speciality": "Cardiologist",
    "consulting_fees": 500.00,
    "subdomain": "johndoe",
    "experience_years": 15,
    "profile_photo": "https://...",
    "bio": "...",
    "instagram": "@drjohn",
    "youtube": "DrJohnChannel",
    "twitter": "@drjohn"
  }
]
```

---

#### GET /public/professional/{subdomain}
Get professional by subdomain (Public)

**Example:** `/public/professional/johndoe`

**Response:**
```json
{
  "id": "prof-uuid",
  "first_name": "John",
  "last_name": "Doe",
  "speciality": "Cardiologist",
  "consulting_fees": 500.00,
  ...
}
```

**Status Codes:**
- `200` - Success
- `404` - Professional not found or not approved

---

### 6. Appointments

#### POST /appointments
Create new appointment

**Request Body:**
```json
{
  "professional_id": "prof-uuid",
  "appointment_datetime": "2025-01-20T14:00:00Z",
  "patient_first_name": "Jane",
  "patient_last_name": "Smith",
  "patient_phone": "+919876543210",
  "patient_email": "patient@example.com",
  "patient_gender": "female",
  "patient_age": 35,
  "referral_source": "search",
  "issue_detail": "Chest pain for 2 days"
}
```

**Response:**
```json
{
  "id": "appt-uuid",
  "professional_id": "prof-uuid",
  "patient_id": "patient-uuid",
  "appointment_datetime": "2025-01-20T14:00:00Z",
  "patient_first_name": "Jane",
  "patient_last_name": "Smith",
  "payment_status": "pending",
  "status": "scheduled",
  "created_at": "2025-01-15T10:45:00Z"
}
```

**Status Codes:**
- `200` - Appointment created
- `404` - Professional not found
- `400` - Invalid data

---

#### GET /appointments/{appointment_id}
Get appointment details

**Response:**
```json
{
  "id": "appt-uuid",
  "professional_id": "prof-uuid",
  "appointment_datetime": "2025-01-20T14:00:00Z",
  "patient_first_name": "Jane",
  "patient_last_name": "Smith",
  "patient_phone": "+919876543210",
  "patient_email": "patient@example.com",
  "meeting_link": "https://meet.google.com/abc-defg-hij",
  "payment_status": "completed",
  "status": "scheduled",
  "whatsapp_sent": true,
  "reminder_sent": false
}
```

**Status Codes:**
- `200` - Success
- `404` - Appointment not found

---

#### GET /appointments/professional/{professional_id}
Get all appointments for a professional (Admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": "appt-uuid",
    "appointment_datetime": "2025-01-20T14:00:00Z",
    "patient_first_name": "Jane",
    "patient_last_name": "Smith",
    "payment_status": "completed",
    "status": "scheduled"
  }
]
```

---

#### PUT /appointments/{appointment_id}/complete-payment
Complete payment and send notifications

**Query Parameters:**
- `payment_id` (required): Razorpay payment ID
- `razorpay_order_id` (required): Razorpay order ID

**Response:**
```json
{
  "success": true,
  "meeting_link": "https://meet.google.com/abc-defg-hij"
}
```

**Actions Performed:**
1. Updates appointment with payment details
2. Creates payment record
3. Generates Google Meet link
4. Sends WhatsApp notification to patient
5. Sends WhatsApp notification to doctor

---

### 7. Payments

#### POST /payments/create-order
Create Razorpay order for appointment

**Query Parameters:**
- `appointment_id` (required)

**Response:**
```json
{
  "order_id": "order_abc123",
  "amount": 50000,
  "currency": "INR",
  "key_id": "rzp_test_xxxxx"
}
```

**Note:** Amount is in paise (50000 = ₹500)

---

### 8. Testimonials

#### POST /testimonials
Create testimonial (Admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "professional_id": "prof-uuid",
  "patient_name": "John Smith",
  "content": "Excellent consultation. Very professional and caring.",
  "rating": 5
}
```

**Response:**
```json
{
  "id": "test-uuid",
  "professional_id": "prof-uuid",
  "patient_name": "John Smith",
  "content": "Excellent consultation...",
  "rating": 5,
  "created_at": "2025-01-15T11:00:00Z"
}
```

---

#### GET /testimonials/{professional_id}
Get testimonials for a professional

**Response:**
```json
[
  {
    "id": "test-uuid",
    "professional_id": "prof-uuid",
    "patient_name": "John Smith",
    "content": "Excellent consultation...",
    "rating": 5,
    "created_at": "2025-01-15T11:00:00Z"
  }
]
```

---

### 9. Analytics (Admin)

#### GET /admin/analytics/{professional_id}
Get analytics for specific professional

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "professional_id": "prof-uuid",
  "total_appointments": 25,
  "completed_appointments": 20,
  "total_revenue": 12500.00,
  "platform_revenue": 1250.00,
  "doctor_revenue": 11250.00
}
```

---

#### GET /admin/analytics/overview
Get platform-wide analytics

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_professionals": 15,
  "approved_professionals": 12,
  "pending_professionals": 3,
  "total_appointments": 150,
  "completed_appointments": 120,
  "total_revenue": 75000.00,
  "platform_revenue": 7500.00
}
```

---

## Error Responses

All endpoints return errors in the following format:

```json
{
  "detail": "Error message here"
}
```

### Common Status Codes:
- `200` - Success
- `400` - Bad Request (invalid data)
- `401` - Unauthorized (missing or invalid token)
- `404` - Not Found
- `500` - Internal Server Error

---

## Data Models

### Professional
```typescript
{
  id: string
  first_name: string
  last_name: string
  phone: string
  email: string
  speciality: string | null
  ug_qualification: string | null
  pg_qualification: string | null
  superspeciality: string | null
  area_of_expertise: string | null
  instagram: string | null
  youtube: string | null
  twitter: string | null
  consulting_fees: number
  subdomain: string
  profile_photo: string | null
  bio: string | null
  experience_years: number | null
  status: "pending" | "approved" | "rejected"
  created_at: string (ISO 8601)
  razorpay_account_id: string | null
}
```

### Appointment
```typescript
{
  id: string
  professional_id: string
  patient_id: string
  appointment_datetime: string (ISO 8601)
  patient_first_name: string
  patient_last_name: string
  patient_phone: string
  patient_email: string
  patient_gender: "male" | "female" | "other"
  patient_age: number
  referral_source: string
  issue_detail: string
  payment_id: string | null
  payment_status: "pending" | "completed" | "failed"
  meeting_link: string | null
  status: "scheduled" | "completed" | "cancelled"
  whatsapp_sent: boolean
  reminder_sent: boolean
  created_at: string (ISO 8601)
}
```

### Payment
```typescript
{
  id: string
  appointment_id: string
  professional_id: string
  razorpay_payment_id: string | null
  razorpay_order_id: string | null
  amount: number
  platform_fee: number (10% of amount)
  doctor_amount: number (90% of amount)
  status: string
  created_at: string (ISO 8601)
}
```

---

## Rate Limiting

Current implementation: No rate limiting (add in production)

Recommended limits:
- Public endpoints: 100 requests/minute
- Authenticated endpoints: 500 requests/minute
- Payment endpoints: 10 requests/minute

---

## Webhooks

### Razorpay Webhook (To be implemented)

**Endpoint:** `POST /webhooks/razorpay`

**Events:**
- `payment.captured` - Payment successful
- `payment.failed` - Payment failed

---

## Testing

### cURL Examples

#### Admin Login
```bash
curl -X POST "https://telecarezone.com/api/admin/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

#### Create Appointment
```bash
curl -X POST "https://telecarezone.com/api/appointments" \
  -H "Content-Type: application/json" \
  -d '{
    "professional_id": "prof-123",
    "appointment_datetime": "2025-01-20T14:00:00Z",
    "patient_first_name": "Jane",
    "patient_last_name": "Smith",
    "patient_phone": "+919876543210",
    "patient_email": "jane@example.com",
    "patient_gender": "female",
    "patient_age": 35,
    "referral_source": "search",
    "issue_detail": "Consultation needed"
  }'
```

#### Get Approved Professionals
```bash
curl "https://telecarezone.com/api/professionals/approved"
```

---

## SDK Examples

### JavaScript/TypeScript

```javascript
const API_BASE = 'https://telecarezone.com/api';

// Admin Login
async function adminLogin(username, password) {
  const response = await fetch(`${API_BASE}/admin/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  return data.access_token;
}

// Get Professionals
async function getProfessionals(token, status = null) {
  const url = status 
    ? `${API_BASE}/professionals?status=${status}`
    : `${API_BASE}/professionals`;
  
  const response = await fetch(url, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
}

// Create Appointment
async function createAppointment(appointmentData) {
  const response = await fetch(`${API_BASE}/appointments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(appointmentData)
  });
  return await response.json();
}
```

### Python

```python
import requests

API_BASE = 'https://telecarezone.com/api'

# Admin Login
def admin_login(username, password):
    response = requests.post(
        f'{API_BASE}/admin/login',
        json={'username': username, 'password': password}
    )
    return response.json()['access_token']

# Get Professionals
def get_professionals(token, status=None):
    headers = {'Authorization': f'Bearer {token}'}
    params = {'status': status} if status else {}
    response = requests.get(
        f'{API_BASE}/professionals',
        headers=headers,
        params=params
    )
    return response.json()

# Create Appointment
def create_appointment(data):
    response = requests.post(
        f'{API_BASE}/appointments',
        json=data
    )
    return response.json()
```

---

## Support

For API support:
- Email: api-support@telecarezone.com
- Documentation: https://docs.telecarezone.com
- Status Page: https://status.telecarezone.com

---

**Version:** 1.0.0  
**Last Updated:** December 2025
