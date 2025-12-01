from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext
import razorpay
import requests
from urllib.parse import urlparse

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = "HS256"

# Razorpay (Test Mode)
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'test_key')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'test_secret')

# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')

# Create the main app
app = FastAPI(title="TeleHealthZone API")
api_router = APIRouter(prefix="/api")

# =========================
# MODELS
# =========================

class Professional(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    speciality: Optional[str] = None
    ug_qualification: Optional[str] = None
    pg_qualification: Optional[str] = None
    superspeciality: Optional[str] = None
    area_of_expertise: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    twitter: Optional[str] = None
    consulting_fees: float = 0.0
    subdomain: str  # doctorname
    profile_photo: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    status: str = "pending"  # pending, approved, rejected
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    razorpay_account_id: Optional[str] = None

class ProfessionalCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    speciality: Optional[str] = None
    ug_qualification: Optional[str] = None
    pg_qualification: Optional[str] = None
    superspeciality: Optional[str] = None
    area_of_expertise: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    twitter: Optional[str] = None
    consulting_fees: float = 0.0

class ProfessionalUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    speciality: Optional[str] = None
    ug_qualification: Optional[str] = None
    pg_qualification: Optional[str] = None
    superspeciality: Optional[str] = None
    area_of_expertise: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    twitter: Optional[str] = None
    consulting_fees: Optional[float] = None
    profile_photo: Optional[str] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    status: Optional[str] = None

class Appointment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    professional_id: str
    patient_id: str
    appointment_datetime: str
    patient_first_name: str
    patient_last_name: str
    patient_phone: str
    patient_email: EmailStr
    patient_gender: str
    patient_age: int
    referral_source: str
    issue_detail: str
    payment_id: Optional[str] = None
    payment_status: str = "pending"  # pending, completed, failed
    meeting_link: Optional[str] = None
    status: str = "scheduled"  # scheduled, completed, cancelled
    whatsapp_sent: bool = False
    reminder_sent: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AppointmentCreate(BaseModel):
    professional_id: str
    appointment_datetime: str
    patient_first_name: str
    patient_last_name: str
    patient_phone: str
    patient_email: EmailStr
    patient_gender: str
    patient_age: int
    referral_source: str
    issue_detail: str

class Payment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    appointment_id: str
    professional_id: str
    razorpay_payment_id: Optional[str] = None
    razorpay_order_id: Optional[str] = None
    amount: float
    platform_fee: float
    doctor_amount: float
    status: str = "pending"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class Testimonial(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    professional_id: str
    patient_name: str
    content: str
    rating: int = 5
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class TestimonialCreate(BaseModel):
    professional_id: str
    patient_name: str
    content: str
    rating: int = 5

class AdminUser(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    password_hash: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# =========================
# AUTHENTICATION
# =========================

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# =========================
# HELPER FUNCTIONS
# =========================

def generate_subdomain(first_name: str, last_name: str) -> str:
    """Generate subdomain from name"""
    subdomain = f"{first_name.lower()}{last_name.lower()}"
    subdomain = ''.join(e for e in subdomain if e.isalnum())
    return subdomain

async def send_whatsapp_notification(to_phone: str, message: str):
    """Send WhatsApp notification via Twilio"""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logging.warning("Twilio credentials not configured. WhatsApp notification skipped.")
        return {"status": "skipped", "message": "Twilio not configured"}
    
    try:
        # Twilio WhatsApp API structure
        url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
        data = {
            "From": TWILIO_WHATSAPP_FROM,
            "To": f"whatsapp:{to_phone}",
            "Body": message
        }
        response = requests.post(url, data=data, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        return {"status": "sent", "response": response.json()}
    except Exception as e:
        logging.error(f"WhatsApp notification failed: {str(e)}")
        return {"status": "failed", "error": str(e)}

def generate_google_meet_link(appointment_id: str) -> str:
    """Generate Google Meet link (mocked for now)"""
    # TODO: Integrate with Google Calendar API
    return f"https://meet.google.com/mock-{appointment_id[:8]}"

def extract_subdomain(host: str) -> Optional[str]:
    """Extract subdomain from host header"""
    try:
        parts = host.split('.')
        if len(parts) > 2:  # subdomain.telecarezone.com
            return parts[0]
        return None
    except:
        return None

# =========================
# ADMIN ROUTES
# =========================

@api_router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(credentials: AdminLogin):
    admin = await db.admin_users.find_one({"username": credentials.username})
    if not admin or not pwd_context.verify(credentials.password, admin["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": credentials.username})
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.post("/admin/create-default")
async def create_default_admin():
    """Create default admin user (username: admin, password: admin123)"""
    existing = await db.admin_users.find_one({"username": "admin"})
    if existing:
        return {"message": "Admin already exists"}
    
    admin = AdminUser(
        username="admin",
        password_hash=pwd_context.hash("admin123")
    )
    await db.admin_users.insert_one(admin.model_dump())
    return {"message": "Default admin created", "username": "admin", "password": "admin123"}

# =========================
# PROFESSIONAL ROUTES
# =========================

@api_router.post("/onboarding/submit", response_model=Professional)
async def submit_professional_application(data: ProfessionalCreate):
    """Public route for expert onboarding"""
    subdomain = generate_subdomain(data.first_name, data.last_name)
    
    # Check if subdomain already exists
    existing = await db.professionals.find_one({"subdomain": subdomain})
    if existing:
        # Add number suffix
        counter = 1
        while existing:
            subdomain = f"{generate_subdomain(data.first_name, data.last_name)}{counter}"
            existing = await db.professionals.find_one({"subdomain": subdomain})
            counter += 1
    
    professional = Professional(**data.model_dump(), subdomain=subdomain, status="pending")
    await db.professionals.insert_one(professional.model_dump())
    return professional

@api_router.get("/professionals", response_model=List[Professional])
async def get_all_professionals(status: Optional[str] = None, _: str = Depends(get_current_admin)):
    """Admin: Get all professionals"""
    query = {"status": status} if status else {}
    professionals = await db.professionals.find(query, {"_id": 0}).to_list(1000)
    return professionals

@api_router.get("/professionals/approved", response_model=List[Professional])
async def get_approved_professionals():
    """Public: Get approved professionals for display"""
    professionals = await db.professionals.find({"status": "approved"}, {"_id": 0}).to_list(1000)
    return professionals

@api_router.get("/professionals/{professional_id}", response_model=Professional)
async def get_professional(professional_id: str, _: str = Depends(get_current_admin)):
    """Admin: Get professional by ID"""
    professional = await db.professionals.find_one({"id": professional_id}, {"_id": 0})
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    return professional

@api_router.get("/public/professional/{subdomain}", response_model=Professional)
async def get_professional_by_subdomain(subdomain: str):
    """Public: Get professional by subdomain"""
    professional = await db.professionals.find_one({"subdomain": subdomain, "status": "approved"}, {"_id": 0})
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    return professional

@api_router.put("/professionals/{professional_id}", response_model=Professional)
async def update_professional(professional_id: str, data: ProfessionalUpdate, _: str = Depends(get_current_admin)):
    """Admin: Update professional"""
    existing = await db.professionals.find_one({"id": professional_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Professional not found")
    
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if update_data:
        await db.professionals.update_one({"id": professional_id}, {"$set": update_data})
    
    updated = await db.professionals.find_one({"id": professional_id}, {"_id": 0})
    return updated

@api_router.post("/professionals", response_model=Professional)
async def create_professional(data: ProfessionalCreate, _: str = Depends(get_current_admin)):
    """Admin: Create new professional"""
    subdomain = generate_subdomain(data.first_name, data.last_name)
    
    existing = await db.professionals.find_one({"subdomain": subdomain})
    if existing:
        counter = 1
        while existing:
            subdomain = f"{generate_subdomain(data.first_name, data.last_name)}{counter}"
            existing = await db.professionals.find_one({"subdomain": subdomain})
            counter += 1
    
    professional = Professional(**data.model_dump(), subdomain=subdomain, status="approved")
    await db.professionals.insert_one(professional.model_dump())
    return professional

# =========================
# APPOINTMENT ROUTES
# =========================

@api_router.post("/appointments", response_model=Appointment)
async def create_appointment(data: AppointmentCreate):
    """Create appointment"""
    # Verify professional exists
    professional = await db.professionals.find_one({"id": data.professional_id, "status": "approved"})
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    
    # Create patient record
    patient = {
        "id": str(uuid.uuid4()),
        "first_name": data.patient_first_name,
        "last_name": data.patient_last_name,
        "phone": data.patient_phone,
        "email": data.patient_email,
        "gender": data.patient_gender,
        "age": data.patient_age,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.patients.insert_one(patient)
    
    appointment = Appointment(**data.model_dump(), patient_id=patient["id"])
    await db.appointments.insert_one(appointment.model_dump())
    return appointment

@api_router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    """Get appointment by ID"""
    appointment = await db.appointments.find_one({"id": appointment_id}, {"_id": 0})
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@api_router.get("/appointments/professional/{professional_id}", response_model=List[Appointment])
async def get_professional_appointments(professional_id: str, _: str = Depends(get_current_admin)):
    """Admin: Get appointments for a professional"""
    appointments = await db.appointments.find({"professional_id": professional_id}, {"_id": 0}).to_list(1000)
    return appointments

@api_router.put("/appointments/{appointment_id}/complete-payment")
async def complete_appointment_payment(appointment_id: str, payment_id: str, razorpay_order_id: str):
    """Complete appointment payment and send notifications"""
    appointment = await db.appointments.find_one({"id": appointment_id})
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    professional = await db.professionals.find_one({"id": appointment["professional_id"]})
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    
    # Update appointment
    meeting_link = generate_google_meet_link(appointment_id)
    await db.appointments.update_one(
        {"id": appointment_id},
        {"$set": {
            "payment_id": payment_id,
            "payment_status": "completed",
            "meeting_link": meeting_link
        }}
    )
    
    # Create payment record
    amount = professional["consulting_fees"]
    platform_fee = amount * 0.10
    doctor_amount = amount * 0.90
    
    payment = Payment(
        appointment_id=appointment_id,
        professional_id=professional["id"],
        razorpay_payment_id=payment_id,
        razorpay_order_id=razorpay_order_id,
        amount=amount,
        platform_fee=platform_fee,
        doctor_amount=doctor_amount,
        status="completed"
    )
    await db.payments.insert_one(payment.model_dump())
    
    # Send WhatsApp notifications
    appointment_time = datetime.fromisoformat(appointment["appointment_datetime"]).strftime("%B %d, %Y at %I:%M %p")
    
    # Patient notification
    patient_message = f"""Hello {appointment['patient_first_name']},\n\nYour appointment with Dr. {professional['first_name']} {professional['last_name']} is confirmed for {appointment_time}.\n\nMeeting Link: {meeting_link}\n\nThank you!"""
    await send_whatsapp_notification(appointment["patient_phone"], patient_message)
    
    # Doctor notification
    doctor_message = f"""Hello Dr. {professional['first_name']},\n\nNew appointment scheduled for {appointment_time}\nPatient: {appointment['patient_first_name']} {appointment['patient_last_name']}\nIssue: {appointment['issue_detail']}\n\nMeeting Link: {meeting_link}"""
    await send_whatsapp_notification(professional["phone"], doctor_message)
    
    await db.appointments.update_one({"id": appointment_id}, {"$set": {"whatsapp_sent": True}})
    
    return {"success": True, "meeting_link": meeting_link}

# =========================
# PAYMENT ROUTES
# =========================

@api_router.post("/payments/create-order")
async def create_razorpay_order(appointment_id: str):
    """Create Razorpay order"""
    appointment = await db.appointments.find_one({"id": appointment_id})
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    professional = await db.professionals.find_one({"id": appointment["professional_id"]})
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    
    # Mock Razorpay order creation
    order_id = f"order_{uuid.uuid4().hex[:12]}"
    amount = int(professional["consulting_fees"] * 100)  # Convert to paise
    
    return {
        "order_id": order_id,
        "amount": amount,
        "currency": "INR",
        "key_id": RAZORPAY_KEY_ID
    }

# =========================
# TESTIMONIAL ROUTES
# =========================

@api_router.post("/testimonials", response_model=Testimonial)
async def create_testimonial(data: TestimonialCreate, _: str = Depends(get_current_admin)):
    """Admin: Create testimonial"""
    testimonial = Testimonial(**data.model_dump())
    await db.testimonials.insert_one(testimonial.model_dump())
    return testimonial

@api_router.get("/testimonials/{professional_id}", response_model=List[Testimonial])
async def get_professional_testimonials(professional_id: str):
    """Get testimonials for a professional"""
    testimonials = await db.testimonials.find({"professional_id": professional_id}, {"_id": 0}).to_list(100)
    return testimonials

# =========================
# ANALYTICS ROUTES
# =========================

@api_router.get("/admin/analytics/{professional_id}")
async def get_professional_analytics(professional_id: str, _: str = Depends(get_current_admin)):
    """Admin: Get analytics for a professional"""
    # Get appointment count
    appointments = await db.appointments.find({"professional_id": professional_id}).to_list(1000)
    total_appointments = len(appointments)
    completed_appointments = len([a for a in appointments if a["status"] == "completed"])
    
    # Get payment data
    payments = await db.payments.find({"professional_id": professional_id}).to_list(1000)
    total_revenue = sum(p["amount"] for p in payments)
    platform_revenue = sum(p["platform_fee"] for p in payments)
    doctor_revenue = sum(p["doctor_amount"] for p in payments)
    
    return {
        "professional_id": professional_id,
        "total_appointments": total_appointments,
        "completed_appointments": completed_appointments,
        "total_revenue": total_revenue,
        "platform_revenue": platform_revenue,
        "doctor_revenue": doctor_revenue
    }

@api_router.get("/admin/analytics/overview")
async def get_platform_analytics(_: str = Depends(get_current_admin)):
    """Admin: Get platform-wide analytics"""
    professionals = await db.professionals.find({}).to_list(1000)
    appointments = await db.appointments.find({}).to_list(1000)
    payments = await db.payments.find({}).to_list(1000)
    
    return {
        "total_professionals": len(professionals),
        "approved_professionals": len([p for p in professionals if p["status"] == "approved"]),
        "pending_professionals": len([p for p in professionals if p["status"] == "pending"]),
        "total_appointments": len(appointments),
        "completed_appointments": len([a for a in appointments if a["status"] == "completed"]),
        "total_revenue": sum(p["amount"] for p in payments),
        "platform_revenue": sum(p["platform_fee"] for p in payments)
    }

# =========================
# ROOT ROUTE
# =========================

@api_router.get("/")
async def root():
    return {"message": "TeleHealthZone API", "version": "1.0.0"}

# Include the router
app.include_router(api_router)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()