#!/usr/bin/env python3
"""Analyze remaining unused products and create batches."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
import requests

# Products already in use (updated list)
USED_PRODUCTS = {
    "clickup", "gusto", "folk", "aura", "drip",
    "blackbox ai", "reclaim.ai", "adcreative.ai", "mongodb",
    "1password", "deel", "hive", "knowledgenet.ai", "trainual", "alli ai"
}

def get_all_products():
    """Fetch all products from PartnerStack."""
    api_key = settings.partnerstack_api_key
    base_url = "https://api.partnerstack.com/api/v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.get(
        f"{base_url}/partnerships",
        headers=headers,
        params={"status": "active", "limit": 100},
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    partnerships = data.get("data", {}).get("items", [])

    products = []
    for prog in partnerships:
        company = prog.get("company", {})
        link = prog.get("link", {})
        team = prog.get("team", {})

        name = company.get("name", "Unknown")
        key = prog.get("key", "")

        if name.lower() not in USED_PRODUCTS:
            products.append({
                "name": name,
                "key": key,
                "url": link.get("url", ""),
                "destination": link.get("destination", ""),
                "category": team.get("name", "General"),
                "name_lower": name.lower()
            })

    return products

def create_batches(products):
    """Create themed batches of products."""
    batches = {
        "Batch 1 - Marketing & Sales Tools": {
            "theme": "Marketing automation, email marketing, CRM, and sales tools",
            "products": []
        },
        "Batch 2 - Communication & Collaboration": {
            "theme": "Chat, video, messaging, customer support tools",
            "products": []
        },
        "Batch 3 - Business Operations": {
            "theme": "Accounting, analytics, conversion tracking, business intelligence",
            "products": []
        },
        "Batch 4 - Development & Design": {
            "theme": "Website builders, forms, developer tools, design platforms",
            "products": []
        },
        "Batch 5 - Security & Infrastructure": {
            "theme": "Security, monitoring, cloud, backup, compliance tools",
            "products": []
        },
        "Batch 6 - Specialized Industry Tools": {
            "theme": "Niche tools for specific industries and use cases",
            "products": []
        }
    }

    # Keywords for each batch
    marketing_kw = ["marketing", "email", "campaign", "sales", "crm", "lead", "brand", "getresponse", "brevo", "apollo", "close"]
    comm_kw = ["chat", "communication", "messaging", "collaboration", "meeting", "video", "support", "freshchat", "freshdesk", "cloudtalk", "wati"]
    ops_kw = ["accounting", "analytics", "tracking", "conversion", "business", "synder", "whatconverts"]
    dev_kw = ["website", "web", "form", "developer", "design", "code", "webflow", "goformz", "webydo"]
    security_kw = ["security", "monitor", "cloud", "backup", "infrastructure", "network", "protect", "tresorit", "auvik", "crowdstrike", "tenable", "druva", "plesk"]

    for product in products:
        name_lower = product["name_lower"]

        # Marketing & Sales
        if any(kw in name_lower for kw in marketing_kw):
            batches["Batch 1 - Marketing & Sales Tools"]["products"].append(product)
        # Communication
        elif any(kw in name_lower for kw in comm_kw):
            batches["Batch 2 - Communication & Collaboration"]["products"].append(product)
        # Business Operations
        elif any(kw in name_lower for kw in ops_kw):
            batches["Batch 3 - Business Operations"]["products"].append(product)
        # Development & Design
        elif any(kw in name_lower for kw in dev_kw):
            batches["Batch 4 - Development & Design"]["products"].append(product)
        # Security & Infrastructure
        elif any(kw in name_lower for kw in security_kw):
            batches["Batch 5 - Security & Infrastructure"]["products"].append(product)
        # Specialized/Other
        else:
            batches["Batch 6 - Specialized Industry Tools"]["products"].append(product)

    return batches

def main():
    print("="*80)
    print("REMAINING AFFILIATE PRODUCTS - BATCH ANALYSIS")
    print("="*80)

    products = get_all_products()
    print(f"\n📊 Total unused products: {len(products)}")
    print(f"📊 Products already in use: {len(USED_PRODUCTS)}")

    batches = create_batches(products)

    total_in_batches = 0
    for batch_name, batch_data in batches.items():
        count = len(batch_data["products"])
        total_in_batches += count

        if count > 0:
            print(f"\n{'='*80}")
            print(f"📦 {batch_name}")
            print(f"   Theme: {batch_data['theme']}")
            print(f"   Products: {count}")
            print(f"{'='*80}")

            for i, prod in enumerate(batch_data["products"][:8], 1):  # Show first 8
                print(f"\n  {i}. {prod['name']}")
                print(f"     URL: {prod['url'][:65]}...")

            if count > 8:
                print(f"\n  ... and {count - 8} more products")

    print(f"\n\n{'='*80}")
    print(f"📊 BATCH SUMMARY")
    print(f"{'='*80}")

    for batch_name, batch_data in batches.items():
        count = len(batch_data["products"])
        if count > 0:
            print(f"{batch_name}: {count} products")

    print(f"\nTotal products to be posted: {total_in_batches}")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
