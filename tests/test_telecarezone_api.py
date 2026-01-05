"""
TeleCareZone API Tests
Tests for: Professionals API, Admin Authentication, Static Pages
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://carebridge-39.preview.emergentagent.com')

class TestHealthCheck:
    """Health check and API root tests"""
    
    def test_api_root(self):
        """Test API root endpoint returns operational status"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'operational'
        assert data['version'] == '2.0.0'
        assert 'endpoints' in data
        print(f"✓ API root: {data['message']}")


class TestProfessionalsAPI:
    """Tests for /api/professionals endpoints"""
    
    def test_get_approved_professionals(self):
        """Test GET /api/professionals/approved returns 3 doctors"""
        response = requests.get(f"{BASE_URL}/api/professionals/approved")
        assert response.status_code == 200
        
        professionals = response.json()
        assert isinstance(professionals, list)
        assert len(professionals) == 3, f"Expected 3 professionals, got {len(professionals)}"
        
        # Verify all 3 doctors are present
        names = [f"{p['first_name']} {p['last_name']}" for p in professionals]
        assert "Priya Sharma" in names, "Dr. Priya Sharma not found"
        assert "Rajesh Kumar" in names, "Dr. Rajesh Kumar not found"
        assert "Ananya Desai" in names, "Dr. Ananya Desai not found"
        print(f"✓ Found {len(professionals)} approved professionals: {names}")
    
    def test_professional_data_structure(self):
        """Test that professional data has required fields"""
        response = requests.get(f"{BASE_URL}/api/professionals/approved")
        assert response.status_code == 200
        
        professionals = response.json()
        required_fields = ['id', 'first_name', 'last_name', 'speciality', 
                          'consulting_fees', 'experience_years', 'theme_color', 'status']
        
        for prof in professionals:
            for field in required_fields:
                assert field in prof, f"Missing field '{field}' in professional {prof.get('first_name', 'unknown')}"
            assert prof['status'] == 'approved'
        print("✓ All professionals have required fields")
    
    def test_dr_priya_sharma_details(self):
        """Test Dr. Priya Sharma's details"""
        response = requests.get(f"{BASE_URL}/api/professionals/approved")
        professionals = response.json()
        
        priya = next((p for p in professionals if p['first_name'] == 'Priya'), None)
        assert priya is not None, "Dr. Priya Sharma not found"
        
        assert priya['speciality'] == 'General Physician'
        assert priya['experience_years'] == 12
        assert float(priya['consulting_fees']) == 500.0
        assert priya['theme_color'] == '#667eea'
        print(f"✓ Dr. Priya Sharma: {priya['speciality']}, {priya['experience_years']} years, ₹{priya['consulting_fees']}")
    
    def test_dr_rajesh_kumar_details(self):
        """Test Dr. Rajesh Kumar's details"""
        response = requests.get(f"{BASE_URL}/api/professionals/approved")
        professionals = response.json()
        
        rajesh = next((p for p in professionals if p['first_name'] == 'Rajesh'), None)
        assert rajesh is not None, "Dr. Rajesh Kumar not found"
        
        assert rajesh['speciality'] == 'Dermatologist'
        assert rajesh['experience_years'] == 8
        assert float(rajesh['consulting_fees']) == 700.0
        assert rajesh['theme_color'] == '#10b981'
        print(f"✓ Dr. Rajesh Kumar: {rajesh['speciality']}, {rajesh['experience_years']} years, ₹{rajesh['consulting_fees']}")
    
    def test_dr_ananya_desai_details(self):
        """Test Dr. Ananya Desai's details"""
        response = requests.get(f"{BASE_URL}/api/professionals/approved")
        professionals = response.json()
        
        ananya = next((p for p in professionals if p['first_name'] == 'Ananya'), None)
        assert ananya is not None, "Dr. Ananya Desai not found"
        
        assert ananya['speciality'] == 'Psychiatrist'
        assert ananya['experience_years'] == 10
        assert float(ananya['consulting_fees']) == 800.0
        assert ananya['theme_color'] == '#8b5cf6'
        print(f"✓ Dr. Ananya Desai: {ananya['speciality']}, {ananya['experience_years']} years, ₹{ananya['consulting_fees']}")


class TestAdminAuthentication:
    """Tests for admin login API"""
    
    def test_admin_login_success(self):
        """Test admin login with valid credentials"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "teleadmin", "password": "teleadm@2026"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert 'access_token' in data
        assert data['token_type'] == 'bearer'
        assert len(data['access_token']) > 0
        print(f"✓ Admin login successful, token received")
    
    def test_admin_login_invalid_credentials(self):
        """Test admin login with invalid credentials"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "wronguser", "password": "wrongpass"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 401
        
        data = response.json()
        assert 'error' in data
        print(f"✓ Invalid credentials rejected: {data['error']}")
    
    def test_admin_login_missing_fields(self):
        """Test admin login with missing fields"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "teleadmin"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400
        print("✓ Missing password field rejected")


class TestPublicProfessionalAPI:
    """Tests for public professional lookup by subdomain"""
    
    def test_get_professional_by_subdomain(self):
        """Test GET /api/public/professional/:subdomain"""
        response = requests.get(f"{BASE_URL}/api/public/professional/priya-sharma")
        assert response.status_code == 200
        
        prof = response.json()
        assert prof['first_name'] == 'Priya'
        assert prof['last_name'] == 'Sharma'
        assert prof['subdomain'] == 'priya-sharma'
        print(f"✓ Found professional by subdomain: Dr. {prof['first_name']} {prof['last_name']}")
    
    def test_get_professional_invalid_subdomain(self):
        """Test GET /api/public/professional/:subdomain with invalid subdomain"""
        response = requests.get(f"{BASE_URL}/api/public/professional/nonexistent-doctor")
        assert response.status_code == 404
        print("✓ Invalid subdomain returns 404")


class TestFrontendPages:
    """Tests for frontend page accessibility"""
    
    def test_homepage_loads(self):
        """Test homepage loads successfully"""
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        assert 'TeleCareZone' in response.text or 'telecare' in response.text.lower()
        print("✓ Homepage loads successfully")
    
    def test_about_page_loads(self):
        """Test about page loads"""
        response = requests.get(f"{BASE_URL}/about")
        assert response.status_code == 200
        print("✓ About page loads successfully")
    
    def test_blogs_page_loads(self):
        """Test blogs page loads"""
        response = requests.get(f"{BASE_URL}/blogs")
        assert response.status_code == 200
        print("✓ Blogs page loads successfully")
    
    def test_contact_page_loads(self):
        """Test contact page loads"""
        response = requests.get(f"{BASE_URL}/contact")
        assert response.status_code == 200
        print("✓ Contact page loads successfully")
    
    def test_privacy_policy_page_loads(self):
        """Test privacy policy page loads"""
        response = requests.get(f"{BASE_URL}/privacy-policy")
        assert response.status_code == 200
        print("✓ Privacy Policy page loads successfully")
    
    def test_terms_page_loads(self):
        """Test terms of service page loads"""
        response = requests.get(f"{BASE_URL}/terms")
        assert response.status_code == 200
        print("✓ Terms of Service page loads successfully")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
