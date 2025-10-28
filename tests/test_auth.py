"""
Simple script to test authentication endpoints
Run this after starting the Flask server
"""
import requests
import json

BASE_URL = "http://localhost:8001"

def test_auth():
    print("🧪 Testing Authentication API\n")
    
    # 1. Register a new user
    print("1️⃣ Registering new user...")
    register_data = {
        "email": "test@gatech.edu",
        "password": "password123",
        "name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    # 2. Login
    print("2️⃣ Logging in...")
    login_data = {
        "email": "test@gatech.edu",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result}\n")
    
    if result.get('success'):
        token = result.get('token')
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Get current user (protected route)
        print("3️⃣ Getting current user profile...")
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        
        # 4. Add favorite club
        print("4️⃣ Adding favorite club...")
        response = requests.post(f"{BASE_URL}/favorites/Robotics Club", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        
        # 5. Get favorites
        print("5️⃣ Getting favorites...")
        response = requests.get(f"{BASE_URL}/favorites", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        
        # 6. Test without token (should fail)
        print("6️⃣ Testing protected route without token...")
        response = requests.get(f"{BASE_URL}/favorites")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        
        print("✅ All tests completed!")

if __name__ == "__main__":
    try:
        test_auth()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Flask server.")
        print("Make sure the server is running: python hello.py")
    except Exception as e:
        print(f"❌ Error: {e}")


