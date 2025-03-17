import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

# Test user credentials
TEST_USER = {
    "email": "user@example.com",
    "username": "testuser",
    "phone": "1234567890",
    "is_active": True,
    "membership_rank": "STANDARD",
    "password": "testpassword123"
}

# Test admin credentials (for creating coaches)
TEST_ADMIN = {
    "email": "admin@example.com",
    "username": "testadmin",
    "phone": "1234567899",
    "is_active": True,
    "role": "ADMIN",
    "password": "adminpassword123"
}

def get_auth_token(user_data=None):
    """Get authentication token for API requests"""
    if user_data is None:
        user_data = TEST_USER
        
    try:
        # Try to login first
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }
        print(f"Trying to login with: {login_data}")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"accept": "application/json"}
        )
        
        print(f"Login response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()["access_token"]
        
        # If login fails, try to register
        print(f"Login failed for {user_data['email']}, attempting to register user...")
        print(f"Registration data: {json.dumps(user_data)}")
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Registration response status: {response.status_code}")
        if response.status_code == 200 or response.status_code == 201:
            print(f"User {user_data['email']} registered successfully.")
            # Try login again
            response = requests.post(
                f"{BASE_URL}/auth/login",
                data=login_data,
                headers={"accept": "application/json"}
            )
            print(f"Second login attempt response status: {response.status_code}")
            if response.status_code == 200:
                return response.json()["access_token"]
        else:
            print(f"Registration failed: {response.text}")
    except Exception as e:
        print(f"Error getting auth token: {e}")
    
    return None

def setup_test_data():
    """Set up test data for the API tests"""
    # First get admin token for creating coaches
    admin_token = get_auth_token(TEST_ADMIN)
    if not admin_token:
        print("Failed to get admin authentication token.")
        return False
        
    # Then get regular user token
    user_token = get_auth_token()
    if not user_token:
        print("Failed to get user authentication token.")
        return False
    
    admin_headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    user_headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    # Create test venue
    venue_data = {
        "venue_name": "Test Venue",
        "address": "123 Test Street",
        "description": "A test venue for API testing",
        "access_info": "Parking available",
        "thumbnail_url": "https://example.com/venue.jpg"
    }
    
    try:
        # Check if venue exists first (to prevent duplicate errors)
        venues_response = requests.get(f"{BASE_URL}/venues/", headers=user_headers)
        venues = venues_response.json() if venues_response.status_code == 200 else []
        
        venue_exists = any(v.get("venue_name") == venue_data["venue_name"] for v in venues)
        
        if not venue_exists:
            print("Creating test venue...")
            response = requests.post(
                f"{BASE_URL}/venues/",
                json=venue_data,
                headers=admin_headers
            )
            
            if response.status_code in (201, 200):
                print("Test venue created successfully.")
                venue_id = response.json().get("venue_id")
            else:
                print(f"Failed to create venue: {response.status_code} - {response.text}")
                venue_id = None
        else:
            # Find the venue ID if it already exists
            venue_id = next((v.get("venue_id") for v in venues if v.get("venue_name") == venue_data["venue_name"]), None)
            print(f"Venue already exists with ID: {venue_id}")
    except Exception as e:
        print(f"Error creating venue: {e}")
        venue_id = None
    
    # Create test coach
    coach_data = {
        "name": "Test Coach",
        "email": "coach@example.com",
        "phone": "9876543210",
        "password": "coachpassword123",
        "bio": "Experienced coach for testing",
        "specialization": "Tennis",
        "hourly_rate": 50.0,
        "profile_image": "https://example.com/coach.jpg",
        "is_active": True
    }
    
    try:
        # Check if coaches exist first
        coaches_response = requests.get(f"{BASE_URL}/coaches/", headers=user_headers)
        coaches = coaches_response.json() if coaches_response.status_code == 200 else []
        
        coach_exists = any(c.get("email") == coach_data["email"] for c in coaches)
        
        if not coach_exists:
            print("Creating test coach...")
            response = requests.post(
                f"{BASE_URL}/coaches/",
                json=coach_data,
                headers=admin_headers  # Only admin can create coaches
            )
            
            if response.status_code in (201, 200):
                print("Test coach created successfully.")
                coach_id = response.json().get("user_id")  # Now using user_id instead of coach_id
            else:
                print(f"Failed to create coach: {response.status_code} - {response.text}")
                coach_id = None
        else:
            # Find the coach ID if it already exists
            coach_id = next((c.get("user_id") for c in coaches if c.get("email") == coach_data["email"]), None)
            print(f"Coach already exists with ID: {coach_id}")
    except Exception as e:
        print(f"Error creating coach: {e}")
        coach_id = None
    
    # Create test lesson type
    lesson_type_data = {
        "name": "Standard Training",  # Changed from type_name to name
        "description": "60-minute standard training session",
        "base_price": 45.00,
        "duration_minutes": 60
    }
    
    try:
        # Check if lesson types exist first
        lesson_types_response = requests.get(f"{BASE_URL}/lesson-types/", headers=user_headers)
        
        if lesson_types_response.status_code == 200:
            lesson_types = lesson_types_response.json()
            lesson_type_exists = any(lt.get("name") == lesson_type_data["name"] for lt in lesson_types)
            
            if not lesson_type_exists:
                print("Creating test lesson type...")
                response = requests.post(
                    f"{BASE_URL}/lesson-types/",
                    json=lesson_type_data,
                    headers=admin_headers
                )
                
                if response.status_code in (201, 200):
                    print("Test lesson type created successfully.")
                    lesson_type_id = response.json().get("lesson_type_id")
                else:
                    print(f"Failed to create lesson type: {response.status_code} - {response.text}")
                    lesson_type_id = 1  # Default to 1 if creation fails
            else:
                # Find the lesson type ID if it already exists
                lesson_type_id = next((lt.get("lesson_type_id") for lt in lesson_types if lt.get("name") == lesson_type_data["name"]), 1)
                print(f"Lesson type already exists with ID: {lesson_type_id}")
        else:
            print(f"Failed to get lesson types: {lesson_types_response.status_code} - {lesson_types_response.text}")
            lesson_type_id = 1  # Default to 1 if API fails
    except Exception as e:
        print(f"Error creating lesson type: {e}")
        lesson_type_id = 1  # Default to 1 if exception occurs
    
    # Create test booking if venue and coach exist
    if venue_id and coach_id:
        # Tomorrow at 2 PM
        tomorrow = datetime.now() + timedelta(days=1)
        booking_date = tomorrow.strftime("%Y-%m-%d")
        start_time = "14:00:00"
        end_time = "15:00:00"
        
        # Note: user_id is automatically extracted from the authentication token
        booking_data = {
            "venue_id": venue_id,
            "coach_id": coach_id,
            "lesson_type_id": lesson_type_id,
            "booking_date": booking_date,
            "start_time": start_time,
            "end_time": end_time,
            "lesson_price": 50.00,
            "facility_fee": 10.00,
            "service_fee": 5.00,
            "total_price": 65.00,
            "notes": "Test booking"
        }
        
        try:
            print("Creating test booking...")
            response = requests.post(
                f"{BASE_URL}/bookings/",
                json=booking_data,
                headers=user_headers  # Regular user creates booking
            )
            
            if response.status_code in (201, 200):
                print("Test booking created successfully.")
                booking_id = response.json().get("booking_id")
                
                # Create test review for the booking
                review_data = {
                    "booking_id": booking_id,
                    "coach_id": coach_id,
                    "score": 5.0,
                    "comment": "Great session!"
                }
                
                print("Creating test review...")
                response = requests.post(
                    f"{BASE_URL}/reviews/",
                    json=review_data,
                    headers=user_headers
                )
                
                if response.status_code in (201, 200):
                    print("Test review created successfully.")
                else:
                    print(f"Failed to create review: {response.status_code} - {response.text}")
            else:
                print(f"Failed to create booking: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error creating booking or review: {e}")
    
    return True

if __name__ == "__main__":
    print("Setting up test data...")
    if setup_test_data():
        print("Test data setup complete!")
    else:
        print("Failed to set up test data.") 