#!/usr/bin/env python3
"""Generate blog posts for remaining affiliate product batches."""
import sys
import os
from pathlib import Path
from datetime import datetime
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
import requests

USED_PRODUCTS = {
    "clickup", "gusto", "folk", "aura", "drip",
    "blackbox ai", "reclaim.ai", "adcreative.ai", "mongodb",
    "1password", "deel", "hive", "knowledgenet.ai", "trainual", "alli ai"
}

# Blog post templates mapped to products
BATCH_POSTS = [
    # Batch 1 - Marketing & Sales Tools
    {
        "product_name": "GetResponse",
        "title": "Complete Email Marketing Platform for Government Contractors: GetResponse Guide",
        "slug": "getresponse-email-marketing-government-contractors",
        "excerpt": "Discover how GetResponse's all-in-one email marketing platform helps government contractors build campaigns, create landing pages, and convert more leads into contracts.",
        "category": "Email Marketing & Automation",
        "keywords": ["email marketing", "GetResponse", "marketing automation", "landing pages", "lead generation", "government contractors"],
    },
    {
        "product_name": "Apollo.io",
        "title": "Sales Intelligence for GovCon: How Apollo.io Helps You Find Federal Opportunities",
        "slug": "apollo-sales-intelligence-government-contractors",
        "excerpt": "Learn how Apollo.io's powerful sales intelligence platform helps government contractors identify decision-makers, research agencies, and build targeted outreach campaigns.",
        "category": "Sales Intelligence & Prospecting",
        "keywords": ["sales intelligence", "Apollo.io", "prospecting", "lead generation", "B2G sales", "government contractors"],
    },
    {
        "product_name": "Close",
        "title": "Close CRM: Sales-Focused Customer Relationship Management for Federal Contractors",
        "slug": "close-crm-sales-government-contractors",
        "excerpt": "Explore how Close CRM's sales-focused features help government contractors manage pipelines, track communications, and close more federal contracts efficiently.",
        "category": "CRM & Sales Management",
        "keywords": ["CRM", "Close", "sales management", "pipeline", "government contractors", "customer relationship management"],
    },
    {
        "product_name": "Brand24",
        "title": "Monitor Your GovCon Brand Reputation with Brand24: Social Listening Guide",
        "slug": "brand24-social-listening-government-contractors",
        "excerpt": "Understand how Brand24's social listening tools help government contractors monitor their brand reputation, track mentions, and engage with opportunities in real-time.",
        "category": "Social Media Monitoring",
        "keywords": ["social listening", "Brand24", "reputation management", "social media monitoring", "brand tracking", "government contractors"],
    },
    {
        "product_name": "Brevo",
        "title": "Brevo Marketing Automation: Streamline Your GovCon Email Campaigns",
        "slug": "brevo-marketing-automation-government-contractors",
        "excerpt": "See how Brevo (formerly Sendinblue) provides government contractors with powerful email marketing, SMS campaigns, and marketing automation at scale.",
        "category": "Marketing Automation",
        "keywords": ["Brevo", "Sendinblue", "marketing automation", "email campaigns", "SMS marketing", "government contractors"],
    },
    {
        "product_name": "Closely",
        "title": "LinkedIn Automation for Government Contractors: Scale Your Outreach with Closely",
        "slug": "closely-linkedin-automation-government-contractors",
        "excerpt": "Discover how Closely helps government contractors automate LinkedIn prospecting, build professional networks, and generate qualified leads through social selling.",
        "category": "Social Selling Automation",
        "keywords": ["LinkedIn automation", "Closely", "social selling", "prospecting", "lead generation", "government contractors"],
    },

    # Batch 2 - Communication & Collaboration
    {
        "product_name": "Freshdesk by Freshworks",
        "title": "Customer Support Excellence: Freshdesk for Government Contractor Service Teams",
        "slug": "freshdesk-customer-support-government-contractors",
        "excerpt": "Learn how Freshdesk's helpdesk software helps government contractors deliver exceptional customer support, manage tickets, and maintain high client satisfaction.",
        "category": "Customer Support & Helpdesk",
        "keywords": ["Freshdesk", "customer support", "helpdesk", "ticketing system", "client service", "government contractors"],
    },
    {
        "product_name": "CloudTalk",
        "title": "Cloud-Based Phone System for GovCon Teams: CloudTalk Communication Platform",
        "slug": "cloudtalk-phone-system-government-contractors",
        "excerpt": "Explore how CloudTalk's cloud phone system helps government contractors manage calls, track conversations, and improve team communication from anywhere.",
        "category": "Cloud Communications",
        "keywords": ["CloudTalk", "cloud phone system", "VoIP", "business communications", "call management", "government contractors"],
    },
    {
        "product_name": "Freshchat",
        "title": "Live Chat for Government Contractors: Engage Clients with Freshchat",
        "slug": "freshchat-live-chat-government-contractors",
        "excerpt": "See how Freshchat's messaging platform helps government contractors provide instant support, qualify leads, and engage with clients through modern chat channels.",
        "category": "Live Chat & Messaging",
        "keywords": ["Freshchat", "live chat", "messaging", "customer engagement", "instant support", "government contractors"],
    },
    {
        "product_name": "Wati.io",
        "title": "WhatsApp Business for GovCon: Scale Client Communication with Wati.io",
        "slug": "wati-whatsapp-business-government-contractors",
        "excerpt": "Discover how Wati.io enables government contractors to leverage WhatsApp Business for client communications, notifications, and support at scale.",
        "category": "WhatsApp Business Platform",
        "keywords": ["Wati", "WhatsApp Business", "messaging", "client communication", "notifications", "government contractors"],
    },

    # Batch 3 - Business Operations
    {
        "product_name": "Synder",
        "title": "Automated Accounting for Government Contractors: Synder Bookkeeping Platform",
        "slug": "synder-automated-accounting-government-contractors",
        "excerpt": "Learn how Synder automates accounting reconciliation for government contractors, syncing transactions and streamlining financial management.",
        "category": "Accounting Automation",
        "keywords": ["Synder", "accounting automation", "bookkeeping", "reconciliation", "financial management", "government contractors"],
    },
    {
        "product_name": "WhatConverts",
        "title": "Track Lead Sources & ROI: WhatConverts for Government Contractor Marketing",
        "slug": "whatconverts-lead-tracking-government-contractors",
        "excerpt": "Discover how WhatConverts helps government contractors track which marketing channels generate leads and contracts, optimizing your marketing ROI.",
        "category": "Conversion Tracking & Analytics",
        "keywords": ["WhatConverts", "conversion tracking", "lead tracking", "marketing ROI", "analytics", "government contractors"],
    },

    # Batch 4 - Development & Design
    {
        "product_name": "Webflow",
        "title": "Build Professional GovCon Websites: Webflow No-Code Platform Guide",
        "slug": "webflow-website-builder-government-contractors",
        "excerpt": "See how Webflow's powerful no-code platform helps government contractors build professional, compliant websites without extensive development resources.",
        "category": "Website Development",
        "keywords": ["Webflow", "website builder", "no-code", "web design", "professional websites", "government contractors"],
    },
    {
        "product_name": "GoFormz",
        "title": "Digital Forms & Mobile Data Collection: GoFormz for Federal Contractors",
        "slug": "goformz-digital-forms-government-contractors",
        "excerpt": "Learn how GoFormz transforms paper forms into digital workflows, helping government contractors collect data, automate processes, and stay compliant.",
        "category": "Digital Forms & Workflow",
        "keywords": ["GoFormz", "digital forms", "mobile forms", "data collection", "workflow automation", "government contractors"],
    },
    {
        "product_name": "LearnWorlds - Top User-rated  Online Course Platform & LMS",
        "title": "Create Training Programs for GovCon Teams: LearnWorlds LMS Platform",
        "slug": "learnworlds-lms-training-government-contractors",
        "excerpt": "Discover how LearnWorlds' online course platform helps government contractors create training programs, onboard employees, and ensure compliance through eLearning.",
        "category": "Learning Management System",
        "keywords": ["LearnWorlds", "LMS", "online training", "eLearning", "course platform", "government contractors"],
    },
    {
        "product_name": "webAI",
        "title": "AI Website Agents for Government Contractors: Enhance Your Site with webAI",
        "slug": "webai-website-agents-government-contractors",
        "excerpt": "Explore how webAI's artificial intelligence agents help government contractors enhance website functionality, improve user experience, and automate interactions.",
        "category": "AI Website Enhancement",
        "keywords": ["webAI", "AI agents", "website automation", "user experience", "AI assistants", "government contractors"],
    },

    # Batch 5 - Security & Infrastructure
    {
        "product_name": "CrowdStrike",
        "title": "Enterprise Endpoint Security: CrowdStrike for Government Contractor Protection",
        "slug": "crowdstrike-endpoint-security-government-contractors",
        "excerpt": "Learn how CrowdStrike's industry-leading endpoint protection helps government contractors defend against cyber threats and meet stringent security requirements.",
        "category": "Endpoint Security",
        "keywords": ["CrowdStrike", "endpoint security", "cybersecurity", "threat protection", "EDR", "government contractors"],
    },
    {
        "product_name": "Tresorit",
        "title": "Secure Cloud Storage for Federal Contractors: Tresorit End-to-End Encryption",
        "slug": "tresorit-secure-cloud-storage-government-contractors",
        "excerpt": "Discover how Tresorit's end-to-end encrypted cloud storage helps government contractors protect sensitive data and maintain compliance with federal security standards.",
        "category": "Secure Cloud Storage",
        "keywords": ["Tresorit", "secure storage", "cloud encryption", "data protection", "file sharing", "government contractors"],
    },
    {
        "product_name": "Druva",
        "title": "Cloud Data Protection & Backup: Druva for Government Contractor Resilience",
        "slug": "druva-cloud-backup-government-contractors",
        "excerpt": "See how Druva's cloud-native data protection platform helps government contractors backup critical data, ensure business continuity, and meet compliance requirements.",
        "category": "Cloud Backup & Recovery",
        "keywords": ["Druva", "cloud backup", "data protection", "disaster recovery", "business continuity", "government contractors"],
    },
    {
        "product_name": "Auvik",
        "title": "Network Monitoring & Management: Auvik for GovCon IT Infrastructure",
        "slug": "auvik-network-monitoring-government-contractors",
        "excerpt": "Learn how Auvik's network management platform helps government contractors monitor infrastructure, troubleshoot issues, and maintain optimal network performance.",
        "category": "Network Monitoring",
        "keywords": ["Auvik", "network monitoring", "IT management", "infrastructure", "network performance", "government contractors"],
    },
    {
        "product_name": "Tenable",
        "title": "Vulnerability Management for Federal Contractors: Tenable Security Platform",
        "slug": "tenable-vulnerability-management-government-contractors",
        "excerpt": "Understand how Tenable's vulnerability management solutions help government contractors identify security risks, prioritize remediation, and maintain compliance.",
        "category": "Vulnerability Management",
        "keywords": ["Tenable", "vulnerability management", "security scanning", "risk assessment", "compliance", "government contractors"],
    },
    {
        "product_name": "Plesk",
        "title": "Web Hosting Control Panel: Plesk for Government Contractor Websites",
        "slug": "plesk-hosting-control-panel-government-contractors",
        "excerpt": "Explore how Plesk's web hosting platform helps government contractors manage websites, ensure security, and maintain reliable online presence with ease.",
        "category": "Web Hosting & Management",
        "keywords": ["Plesk", "web hosting", "control panel", "website management", "hosting platform", "government contractors"],
    },
]

def get_product_url(product_name):
    """Fetch product URL from PartnerStack."""
    api_key = settings.partnerstack_api_key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.get(
        "https://api.partnerstack.com/api/v2/partnerships",
        headers=headers,
        params={"status": "active", "limit": 100},
        timeout=30
    )

    data = response.json()
    partnerships = data.get("data", {}).get("items", [])

    for prog in partnerships:
        company = prog.get("company", {})
        if company.get("name", "").lower() == product_name.lower():
            link = prog.get("link", {})
            return link.get("url", "")

    return ""

def generate_post_content(post_data, product_url):
    """Generate blog post content."""
    content = f"""---
{{
  "title": "{post_data['title']}",
  "slug": "{post_data['slug']}",
  "excerpt": "{post_data['excerpt']}",
  "date": "{datetime.now().isoformat()}",
  "keywords": {json.dumps(post_data['keywords'])},
  "description": "{post_data['excerpt'][:150]}"
}}
---

{post_data['excerpt']}

## The Modern Government Contracting Landscape

Today's government contractors face unprecedented challenges in managing complex operations, maintaining compliance, and staying competitive in a rapidly evolving digital marketplace. Success requires not just expertise in your domain, but also the right technology stack to support efficient operations and scalable growth.

## Why the Right Tools Matter

Federal contracting demands precision, accountability, and efficiency at every step. The right software solutions can:

- **Streamline Operations**: Automate repetitive tasks and free up your team for high-value work
- **Improve Compliance**: Maintain accurate records and meet federal requirements consistently
- **Enhance Communication**: Keep teams, clients, and stakeholders aligned and informed
- **Boost Productivity**: Enable your team to do more with existing resources
- **Support Growth**: Scale your operations without proportionally increasing overhead

## Common Challenges Government Contractors Face

### 1. Operational Complexity
Managing multiple contracts, deliverables, and stakeholder relationships requires robust systems that can handle complexity without creating bottlenecks.

### 2. Compliance Requirements
Federal contracts come with strict compliance obligations. The right tools help you track requirements, maintain documentation, and demonstrate adherence during audits.

### 3. Resource Constraints
Small to mid-sized contractors must maximize efficiency with limited budgets and personnel. Technology investments should deliver clear ROI and require minimal overhead to maintain.

### 4. Communication Gaps
Effective communication across distributed teams, with clients, and among stakeholders is critical. Modern tools enable seamless collaboration regardless of location.

### 5. Data Security
Protecting sensitive information isn't optional for government contractors. Your technology stack must include robust security measures that meet or exceed federal standards.

## Key Features to Prioritize

When evaluating solutions for your government contracting business, look for:

- **Ease of Use**: Intuitive interfaces that minimize training time and encourage adoption
- **Integration Capabilities**: Seamless connectivity with your existing tools and workflows
- **Scalability**: Solutions that grow with your business without requiring complete replacements
- **Security & Compliance**: Built-in features that support federal security requirements
- **Reliable Support**: Responsive customer service and comprehensive documentation
- **Proven Track Record**: Established vendors with strong reputations in the business software space

## Implementation Best Practices

Successfully integrating new tools into your government contracting operations requires:

1. **Clear Objectives**: Define specific goals and success metrics before implementation
2. **Stakeholder Buy-In**: Involve team members in evaluation and selection processes
3. **Phased Rollout**: Start with pilot programs before full deployment
4. **Comprehensive Training**: Invest in proper onboarding for all users
5. **Ongoing Optimization**: Regularly review usage and adjust configurations for maximum value

## Measuring Success

Track these key performance indicators to evaluate your technology investments:

- Time saved on administrative tasks
- Reduction in errors and rework
- Improvement in compliance metrics
- Team productivity gains
- Client satisfaction scores
- ROI on software investments

## Looking Forward

The government contracting industry continues to evolve, with increasing emphasis on digital capabilities, data-driven decision making, and operational efficiency. Contractors who invest wisely in modern tools position themselves for long-term success and competitive advantage.

## Recommended Tool

**{post_data['product_name']}** - {post_data['excerpt'].split(':')[1].strip() if ':' in post_data['excerpt'] else post_data['excerpt']}

🔗 [Try {post_data['product_name']} Today]({product_url})

*Category: {post_data['category']}*

---

## Conclusion

Choosing the right tools for your government contracting business is a strategic decision that impacts every aspect of your operations. By focusing on solutions that address your specific challenges, integrate well with existing systems, and support your growth objectives, you can build a technology stack that delivers real value.

Remember that the best tools are those your team will actually use. Prioritize solutions that offer intuitive interfaces, strong support, and clear benefits. Start with high-impact areas, measure results carefully, and continuously optimize your approach.

What tools will transform your government contracting operations in 2025?
"""
    return content

def main():
    posts_dir = Path("frontend/posts")
    posts_dir.mkdir(exist_ok=True)

    print("="*80)
    print("GENERATING BATCH BLOG POSTS (Batches 1-5)")
    print("="*80)

    generated = 0
    skipped = 0

    for i, post_data in enumerate(BATCH_POSTS, 1):
        product_name = post_data["product_name"]

        print(f"\n[{i}/{len(BATCH_POSTS)}] Processing: {product_name}")

        # Get product URL from PartnerStack
        product_url = get_product_url(product_name)

        if not product_url:
            print(f"  ⚠️  Skipped: No URL found in PartnerStack")
            skipped += 1
            continue

        filename = f"{post_data['slug']}.md"
        filepath = posts_dir / filename

        content = generate_post_content(post_data, product_url)
        filepath.write_text(content)

        generated += 1
        print(f"  ✅ Generated: {filename}")
        print(f"     Product: {product_name}")
        print(f"     Category: {post_data['category']}")

    print(f"\n{'='*80}")
    print(f"📊 GENERATION SUMMARY")
    print(f"   Posts generated: {generated}")
    print(f"   Posts skipped: {skipped}")
    print(f"   Location: frontend/posts/")
    print("="*80)

if __name__ == "__main__":
    main()
