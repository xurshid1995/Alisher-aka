"""
Test: Real API response'ni tekshirish
"""
import requests
import json

# Login qilish
login_url = "http://165.232.81.142/api/login"
locations_url = "http://165.232.81.142/api/locations"

print("\n" + "="*80)
print("TEST: Real API response - sotuvchi user bilan")
print("="*80)

# Session yaratish
session = requests.Session()

# Login
login_data = {
    "username": "sotuvchi",
    "password": "sotuvchi123"  # Parolni to'g'rilang
}

print("\n1. Logging in as sotuvchi...")
try:
    login_response = session.post(login_url, json=login_data)
    print(f"   Login status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        print("   ✅ Login successful!")
        
        # Get locations
        print("\n2. Fetching /api/locations...")
        locations_response = session.get(locations_url)
        print(f"   Response status: {locations_response.status_code}")
        
        if locations_response.status_code == 200:
            locations = locations_response.json()
            print(f"   ✅ Got {len(locations)} locations")
            print("\n   Locations returned:")
            for loc in locations:
                print(f"      - {loc}")
        else:
            print(f"   ❌ Error: {locations_response.text}")
    else:
        print(f"   ❌ Login failed: {login_response.text}")
        
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print("\n" + "="*80)
