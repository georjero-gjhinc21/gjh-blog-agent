#!/usr/bin/env python3
"""Detailed PartnerStack API test."""
from utils.partnerstack_client import PartnerStackClient
from config import settings
import requests

print(f"API Key configured: {bool(settings.partnerstack_api_key)}")
print(f"API Key length: {len(settings.partnerstack_api_key) if settings.partnerstack_api_key else 0}")
print(f"API Key (first 10 chars): {settings.partnerstack_api_key[:10] if settings.partnerstack_api_key else 'None'}...")

client = PartnerStackClient()

# Test connection with details
try:
    print("\nTesting connection to PartnerStack API...")
    response = requests.get(
        f"{client.base_url}/partnerships",
        headers=client.headers,
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")

    if response.status_code == 200:
        print("✓ Connection successful!")
        data = response.json()
        print(f"Response data keys: {data.keys() if isinstance(data, dict) else 'Not a dict'}")
    else:
        print(f"✗ Connection failed")
        print(f"Response: {response.text[:500]}")

except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
