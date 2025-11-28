#!/usr/bin/env python3
"""Get real affiliate links from PartnerStack API."""
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
import requests

def get_partnerstack_links():
    """Fetch real affiliate links from PartnerStack API."""
    api_key = settings.partnerstack_api_key
    partner_key = settings.partnerstack_partner_key

    if not api_key:
        print("❌ No PartnerStack API key configured in .env")
        return {}

    print(f"🔑 Using Partner Key: {partner_key}")
    print(f"🔑 API Key configured: {'Yes' if api_key else 'No'}\n")

    base_url = "https://api.partnerstack.com/api/v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    print("📡 Fetching partnerships from PartnerStack...\n")

    try:
        response = requests.get(
            f"{base_url}/partnerships",
            headers=headers,
            params={"status": "active", "limit": 100},
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        partnerships = data.get("data", {}).get("items", [])

        print(f"✅ Found {len(partnerships)} active partnerships\n")
        print("="*80)

        links = {}
        for prog in partnerships:
            company = prog.get("company", {})
            link = prog.get("link", {})
            key = prog.get("key", "")
            name = company.get("name", "Unknown")
            affiliate_url = link.get("url", "")
            destination = link.get("destination", "")

            links[name.lower()] = {
                "name": name,
                "key": key,
                "affiliate_url": affiliate_url,
                "destination": destination
            }

            print(f"\n📦 {name}")
            print(f"   Key: {key}")
            print(f"   Affiliate URL: {affiliate_url}")
            print(f"   Destination: {destination}")

        print("\n" + "="*80)
        return links

    except Exception as e:
        print(f"❌ Error fetching partnerships: {e}")
        if hasattr(e, 'response'):
            print(f"   Response: {e.response.text if hasattr(e.response, 'text') else 'No response text'}")
        return {}

if __name__ == "__main__":
    links = get_partnerstack_links()

    print(f"\n\n📋 SUMMARY:")
    print(f"   Total products: {len(links)}")

    # Check which products we need
    needed_products = ["clickup", "gusto", "folk", "aura", "mongodb", "deel", "freshdesk"]

    print(f"\n🔍 Checking for needed products:")
    for product in needed_products:
        if product in links:
            info = links[product]
            print(f"   ✅ {info['name']}: {info['affiliate_url']}")
        else:
            print(f"   ❌ {product}: NOT FOUND")
