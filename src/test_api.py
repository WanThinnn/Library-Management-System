#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryManagementSystem.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Create test client
client = Client()

# Login first
user = User.objects.first()
if user:
    print(f"Using user: {user.username}")
    logged_in = client.login(username=user.username, password='241203')
    print(f"Login success: {logged_in}")
    if not logged_in:
        print("Login failed!")
        exit(1)
else:
    print("No users found!")
    exit(1)

# Test API
print("\n[TEST] Calling /api/unreturned-receipts/")
response = client.get('/api/unreturned-receipts/')
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")

if response.status_code == 200:
    try:
        data = json.loads(response.content)
        print(f"Success: {data['success']}")
        print(f"Data count: {len(data['data'])}")
        if data['data']:
            print(f"First receipt: {data['data'][0]}")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Content: {response.content[:500]}")
else:
    print(f"Error: {response.content[:500]}")
