#!/usr/bin/env python3
"""Analyze unused affiliate products and categorize them."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
import requests

# Products already in use
USED_PRODUCTS = {
    "clickup", "gusto", "folk", "aura", "drip",
    # partner.link products (not in PartnerStack)
    # "cybersecurity-compliance-kit", "fedbiz-pro"
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

        products.append({
            "name": name,
            "key": key,
            "url": link.get("url", ""),
            "destination": link.get("destination", ""),
            "category": team.get("name", "General"),
            "name_lower": name.lower()
        })

    return products

def categorize_products(products):
    """Categorize products by theme."""
    categories = {
        "AI & Automation": [],
        "Database & Infrastructure": [],
        "Marketing & Sales": [],
        "Security & Compliance": [],
        "HR & Payroll": [],
        "Project Management": [],
        "Communication & Collaboration": [],
        "Development Tools": [],
        "Other": []
    }

    ai_keywords = ["ai", "artificial", "machine learning", "automation", "intelligent", "smart"]
    db_keywords = ["database", "mongodb", "storage", "cloud", "infrastructure"]
    marketing_keywords = ["marketing", "email", "campaign", "sales", "crm", "lead"]
    security_keywords = ["security", "password", "auth", "compliance", "encryption", "protect"]
    hr_keywords = ["hr", "payroll", "hiring", "recruitment", "employee", "workforce", "deel", "gusto"]
    pm_keywords = ["project", "task", "workflow", "management", "planning", "hive"]
    comm_keywords = ["chat", "communication", "messaging", "collaboration", "meeting", "video"]
    dev_keywords = ["code", "developer", "api", "github", "programming"]

    for product in products:
        name_lower = product["name_lower"]
        category_lower = product.get("category", "").lower()
        combined = name_lower + " " + category_lower

        if product["name_lower"] in USED_PRODUCTS:
            continue

        # AI & Automation
        if any(kw in combined for kw in ai_keywords):
            categories["AI & Automation"].append(product)
        # Database
        elif any(kw in combined for kw in db_keywords):
            categories["Database & Infrastructure"].append(product)
        # Marketing & Sales
        elif any(kw in combined for kw in marketing_keywords):
            categories["Marketing & Sales"].append(product)
        # Security
        elif any(kw in combined for kw in security_keywords):
            categories["Security & Compliance"].append(product)
        # HR
        elif any(kw in combined for kw in hr_keywords):
            categories["HR & Payroll"].append(product)
        # Project Management
        elif any(kw in combined for kw in pm_keywords):
            categories["Project Management"].append(product)
        # Communication
        elif any(kw in combined for kw in comm_keywords):
            categories["Communication & Collaboration"].append(product)
        # Development
        elif any(kw in combined for kw in dev_keywords):
            categories["Development Tools"].append(product)
        else:
            categories["Other"].append(product)

    return categories

def main():
    print("="*80)
    print("UNUSED AFFILIATE PRODUCTS ANALYSIS")
    print("="*80)

    products = get_all_products()
    print(f"\n📊 Total products available: {len(products)}")
    print(f"📊 Products already in use: {len(USED_PRODUCTS)}")
    print(f"📊 Unused products: {len(products) - len(USED_PRODUCTS)}\n")

    categories = categorize_products(products)

    for category, prods in categories.items():
        if prods:
            print(f"\n{'='*80}")
            print(f"📁 {category} ({len(prods)} products)")
            print(f"{'='*80}")

            for prod in prods[:10]:  # Show top 10 per category
                print(f"\n  🔹 {prod['name']}")
                print(f"     Key: {prod['key']}")
                print(f"     URL: {prod['url'][:70]}..." if len(prod['url']) > 70 else f"     URL: {prod['url']}")
                print(f"     Category: {prod['category']}")

    # Suggest blog post topics
    print(f"\n\n{'='*80}")
    print("📝 SUGGESTED BLOG POST TOPICS")
    print(f"{'='*80}\n")

    suggestions = [
        {
            "category": "AI & Automation",
            "topics": [
                "AI Tools Transforming Government Contracting in 2025",
                "Automate Your GovCon Business: Top AI Solutions for Federal Contractors",
                "Smart Automation: How AI is Revolutionizing Government Contract Management",
                "AI-Powered Solutions for Streamlining Federal Procurement Processes"
            ]
        },
        {
            "category": "Database & Infrastructure",
            "topics": [
                "Modern Database Solutions for Government Contractors: Cloud vs On-Premise",
                "Scalable Infrastructure for Growing GovCon Businesses",
                "Data Management Best Practices for Federal Contractors in 2025"
            ]
        },
        {
            "category": "Marketing & Sales",
            "topics": [
                "Advanced Sales Intelligence Tools for Government Contractors",
                "CRM Solutions Built for Federal Contracting Success",
                "Lead Generation Strategies for GovCon Businesses in the Digital Era"
            ]
        },
        {
            "category": "Security & Compliance",
            "topics": [
                "Password Management Best Practices for Government Contractors",
                "Secure Cloud Storage Solutions for Federal Contract Data",
                "Identity Protection Tools Every GovCon Business Needs"
            ]
        },
        {
            "category": "Communication & Collaboration",
            "topics": [
                "Modern Communication Tools for Distributed GovCon Teams",
                "Video Collaboration Solutions for Federal Contractors",
                "Chatbots and AI Assistants: The Future of GovCon Customer Service"
            ]
        }
    ]

    for suggestion in suggestions:
        if categories.get(suggestion["category"]):
            print(f"\n🎯 {suggestion['category']}")
            for i, topic in enumerate(suggestion["topics"], 1):
                print(f"   {i}. {topic}")

    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
