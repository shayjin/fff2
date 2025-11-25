"""
Quick test script to verify your deployed API is working
Run this with: python test_api.py
"""
import requests

API_BASE = "https://s-aof7.onrender.com"

print("Testing API at:", API_BASE)
print("-" * 50)

# Test 1: Check if API is alive
print("\n1. Testing GET /server (should return current server)...")
try:
    response = requests.get(f"{API_BASE}/server")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Set a patient ID
print("\n2. Testing POST /patient (set patient ID)...")
try:
    response = requests.post(
        f"{API_BASE}/patient",
        json={"patient_id": "test-patient-123"}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Get patient ID
print("\n3. Testing GET /patient (get current patient ID)...")
try:
    response = requests.get(f"{API_BASE}/patient")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 4: Ask a question
print("\n4. Testing POST /ask (ask a medical question)...")
try:
    response = requests.post(
        f"{API_BASE}/ask",
        json={"query": "What is diabetes?"},
        timeout=60  # Medical queries might take longer
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "-" * 50)
print("Testing complete!")



