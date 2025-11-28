# Impact.com Integration Guide

This guide explains how to set up and use the Impact.com affiliate network integration for the GJH Blog Agent system.

## Overview

Impact.com is a partnership automation platform that connects brands with affiliates. The GJH Blog Agent now supports **dual-network** affiliate management, integrating both:

- **PartnerStack**: 55+ active programs (existing integration)
- **Impact.com**: Additional brand campaigns (new integration)

## Prerequisites

1. Active Impact.com affiliate account
2. API access enabled in your Impact.com account
3. Python environment with required dependencies

## Setup Instructions

### Step 1: Get Your Impact.com Credentials

#### A. Account SID

Your Account SID is visible in your browser URL when logged into Impact.com:

```
https://app.impact.com/secure/mediapartner/YOUR_ACCOUNT_SID/home/...
                                           ^^^^^^^^^^^^^^^^^^
```

**Example**: `IRSCz7UUHKkM5873369fF6fUUFeFHTSsR1`

#### B. Auth Token

1. Log into your Impact.com dashboard
2. Navigate to: **Settings → Technical Settings → API Access**
3. Click **"Create Access Token"**
4. Configure token permissions:
   - ✅ Campaigns (read)
   - ✅ Ads (read/write)
   - ✅ Tracking Links (read/write)
   - ✅ Promo Codes (read)
   - ✅ Reports (read)
5. Click **"Generate Token"**
6. **Copy the token immediately** (you won't see it again)

**Example**: `dbrWjq_mbJ8vEcmiN7pvcNu-LGevosCh`

### Step 2: Configure Environment Variables

Add your Impact.com credentials to `.env`:

```bash
# Impact.com Integration
IMPACT_ACCOUNT_SID=your_account_sid_here
IMPACT_AUTH_TOKEN=your_auth_token_here
```

Your complete `.env` should include both networks:

```bash
# PartnerStack
PARTNERSTACK_API_KEY=your_partnerstack_key
PARTNERSTACK_PARTNER_KEY=gjh-consulting

# Impact.com
IMPACT_ACCOUNT_SID=your_impact_sid
IMPACT_AUTH_TOKEN=your_impact_token
```

### Step 3: Install Dependencies

No additional dependencies needed - the Impact.com client uses the existing `requests` library.

### Step 4: Test the Connection

```bash
python test_unified_affiliate.py
```

Expected output:
```
Testing network connections...
✓ PartnerStack: Connected
✓ Impact.com: Connected

Syncing programs...
✓ PartnerStack: 55 programs
✓ Impact.com: X programs
Total: XX programs loaded
```

## Usage Examples

### Basic Usage

```python
from agents.unified_affiliate_agent import UnifiedAffiliateAgent

# Initialize the agent
agent = UnifiedAffiliateAgent()

# Test connections
status = agent.test_connections()
print(f"PartnerStack: {'✓' if status['partnerstack'] else '✗'}")
print(f"Impact.com: {'✓' if status['impact'] else '✗'}")

# Sync all programs from both networks
counts = agent.sync_all_programs()
print(f"Loaded {counts['total']} programs total")
```

### Finding Matches for Blog Content

```python
# Match affiliate programs to blog content
blog_title = "Best Cybersecurity Tools for Federal Contractors"
blog_content = """
In this guide, we'll explore the top cybersecurity solutions
that help federal contractors achieve CMMC compliance...
"""

matches = agent.find_best_matches(
    content=blog_content,
    title=blog_title,
    max_matches=3,
    min_score=0.2
)

for match in matches:
    print(f"{match['name']} ({match['network']})")
    print(f"  Score: {match['match_score']:.2f}")
    print(f"  Commission: {match['commission_rate']}%")
```

### Generating Affiliate Links

```python
# Generate a tracked affiliate link
link = agent.generate_link(
    program_name="CrowdStrike",
    sub_id="blog-post-slug-here"
)

print(f"Affiliate link: {link}")
```

### Searching Programs

```python
# Search across both networks
results = agent.search_programs("cybersecurity", limit=5)

for program in results:
    print(f"{program['name']} - {program['network']}")
```

### Getting Statistics

```python
# View statistics across all networks
stats = agent.get_stats()

print("Network Distribution:")
for network, count in stats['networks'].items():
    print(f"  {network}: {count}")

print("\nTop Categories:")
for category, count in list(stats['categories'].items())[:5]:
    print(f"  {category}: {count}")
```

### Formatting Affiliate Sections

```python
# Generate formatted affiliate section for blog post
matches = agent.find_best_matches(content, title)
affiliate_section = agent.format_affiliate_section(
    matches,
    section_title="Recommended Tools & Services"
)

# Add disclosure
disclosure = agent.format_affiliate_disclosure()

# Append to blog post
full_post = f"{blog_content}\n\n{affiliate_section}\n\n{disclosure}"
```

## API Reference

### UnifiedAffiliateAgent

The main class for managing multi-network affiliate programs.

#### Methods

**`__init__(partnerstack_client=None, impact_client=None)`**
- Initialize the agent with optional custom clients

**`test_connections() -> Dict[str, bool]`**
- Test API connections to both networks
- Returns: `{"partnerstack": bool, "impact": bool}`

**`sync_all_programs() -> Dict[str, int]`**
- Fetch and sync programs from both networks
- Returns: `{"partnerstack": int, "impact": int, "total": int}`

**`find_best_matches(content, title="", max_matches=3, min_score=0.15) -> List[Dict]`**
- Find best matching programs for content using AI
- Uses Ollama for intelligent matching
- Returns: List of programs with match scores

**`generate_link(program_name, sub_id=None, path="") -> str`**
- Generate tracked affiliate link for a program
- Automatically uses correct network (PartnerStack or Impact.com)
- Returns: Tracking URL

**`search_programs(query, limit=10) -> List[Dict]`**
- Search across all networks by keyword
- Returns: List of matching programs

**`get_stats() -> Dict`**
- Get comprehensive statistics
- Returns: Network counts, categories, top programs

**`format_affiliate_section(matches, section_title) -> str`**
- Format matched programs as markdown section
- Returns: Formatted markdown string

**`format_affiliate_disclosure() -> str`**
- Generate standard affiliate disclosure
- Returns: Formatted disclosure text

**`list_all_programs(network=None) -> List[Dict]`**
- List all programs, optionally filtered by network
- Returns: List of program dictionaries

**`export_programs(format="dict") -> List[Dict]`**
- Export programs in various formats (dict, json, csv)
- Returns: Exported data in requested format

## Impact.com Specific Features

### Promo Codes

```python
from utils.impact_client import ImpactClient

client = ImpactClient()
promo_codes = client.get_promo_codes(campaign_id="12345")

for code in promo_codes:
    print(f"Code: {code['Code']}, Discount: {code['Discount']}")
```

### Performance Statistics

```python
# Get last 30 days of performance data
stats = client.get_stats(days=30)
print(f"Clicks: {stats.get('clicks', 0)}")
print(f"Revenue: ${stats.get('revenue', 0):.2f}")
```

## Integration with Blog Generation

To automatically add affiliate links to generated blog posts:

```python
from agents.unified_affiliate_agent import UnifiedAffiliateAgent
from agents.blog_agent import BlogAgent

# Initialize agents
affiliate_agent = UnifiedAffiliateAgent()
blog_agent = BlogAgent()

# Generate blog post
post_content = blog_agent.generate_post(topic)

# Find and add affiliate links
matches = affiliate_agent.find_best_matches(
    content=post_content,
    title=topic.title,
    max_matches=3
)

# Format affiliate section
affiliate_section = affiliate_agent.format_affiliate_section(matches)
disclosure = affiliate_agent.format_affiliate_disclosure()

# Combine
final_post = f"{post_content}\n\n{affiliate_section}\n\n{disclosure}"
```

## Troubleshooting

### Connection Issues

**Problem**: `Impact.com connection test failed`

**Solutions**:
1. Verify Account SID is correct (check URL)
2. Ensure Auth Token is valid (not expired)
3. Check API permissions include required scopes
4. Verify network connectivity

### No Campaigns Returned

**Problem**: `sync_all_programs()` returns 0 Impact campaigns

**Solutions**:
1. Check if you've joined any campaigns in Impact.com dashboard
2. Navigate to: **Marketplace → Find Brands** to join campaigns
3. Ensure campaigns are in "ACTIVE" status
4. Wait 5-10 minutes after joining for API to update

### Link Generation Fails

**Problem**: `generate_link()` returns empty string

**Solutions**:
1. Verify program name is exact match
2. Check if campaign allows affiliate link creation
3. Try using `search_programs()` to find correct program name
4. Check API token has "Ads" write permission

## Best Practices

### 1. Regular Syncing

Sync programs daily to get latest campaigns and commission rates:

```python
# In your automation script
agent.sync_all_programs()
```

### 2. Match Score Threshold

Adjust `min_score` based on content quality:

- **High-quality, targeted content**: `min_score=0.3`
- **General content**: `min_score=0.2`
- **Broad topics**: `min_score=0.15`

### 3. Network Diversification

Aim for mix of both networks to maximize revenue:

```python
matches = agent.find_best_matches(content, max_matches=4)

# Ensure both networks represented
ps_matches = [m for m in matches if m['network'] == 'partnerstack']
impact_matches = [m for m in matches if m['network'] == 'impact']

# Use 2 from each network when possible
balanced_matches = ps_matches[:2] + impact_matches[:2]
```

### 4. SubId Tracking

Always use `sub_id` for detailed tracking:

```python
link = agent.generate_link(
    program_name="ProductName",
    sub_id=f"{blog_post_slug}-{datetime.now().strftime('%Y%m%d')}"
)
```

## Revenue Tracking

Monitor performance in both dashboards:

- **PartnerStack**: https://dash.partnerstack.com
- **Impact.com**: https://app.impact.com/secure/mediapartner/{YOUR_SID}/home

## Support Resources

- **Impact.com API Docs**: https://developer.impact.com/
- **Impact.com Support**: support@impact.com
- **PartnerStack Docs**: https://docs.partnerstack.com/

## Next Steps

1. ✅ Complete setup and test connections
2. ✅ Sync programs from both networks
3. ✅ Test link generation
4. ✅ Integrate with blog post generation workflow
5. ✅ Monitor revenue in both dashboards
6. ✅ Join additional campaigns to expand program inventory

---

**Ready to maximize your affiliate revenue with dual-network integration!**
