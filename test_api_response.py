#!/usr/bin/env python3
"""Test to see actual API response structure."""
from utils.partnerstack_client import PartnerStackClient
import json

client = PartnerStackClient()

try:
    import requests
    response = requests.get(
        f"{client.base_url}/partnerships",
        headers=client.headers,
        params={"limit": 10},
        timeout=30
    )
    print(f"Status: {response.status_code}")
    print(f"\nRaw response text (first 500 chars):\n{response.text[:500]}")
    print(f"\nJSON response:")
    data = response.json()
    print(json.dumps(data, indent=2)[:1000])
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
