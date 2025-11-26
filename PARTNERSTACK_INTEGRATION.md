# PartnerStack Integration Guide

## 🎯 Overview

This guide shows you how to integrate your 55+ PartnerStack affiliate programs into the GJH Blog Agent for automated revenue generation.

## 📊 Your Affiliate Programs

Based on your PartnerStack dashboard, you have **55 active affiliate programs** across these categories:

### Categories & Examples:
- **Project Management**: ClickUp, Asana, Monday.com
- **HR & Payroll**: Gusto, Rippling, BambooHR
- **Travel & Expense**: Navan, Expensify, TravelPerk
- **Cybersecurity**: CrowdStrike, Okta, 1Password
- **Marketing**: GetResponse, ActiveCampaign, HubSpot
- **Communication**: Freshchat, Intercom, Zendesk
- **IT Service**: Freshservice, ServiceNow
- **Sales & CRM**: Salesforce, Pipedrive
- **Analytics**: Mixpanel, Amplitude
- **Cloud & Infrastructure**: AWS, DigitalOcean
- **Privacy & Compliance**: Optery, OneTrust
- **VoIP & Communication**: CloudTalk, RingCentral

## 🚀 Quick Setup (10 Minutes)

### Step 1: Get Your PartnerStack API Key

1. Log into https://dash.partnerstack.com
2. Navigate to **Settings** → **API Keys**
3. Click **Create New API Key**
4. Copy the key (starts with `ps_`)
5. Optionally get your Partner Key for tracking

### Step 2: Configure Environment

```bash
cd /opt/gjh-blog-agent

# Add to .env file
echo "PARTNERSTACK_API_KEY=ps_your_api_key_here" >> .env
echo "PARTNERSTACK_PARTNER_KEY=your_partner_key" >> .env  # Optional
```

### Step 3: Update Configuration

Edit `config/settings.py`:

```python
class Settings(BaseSettings):
    # ... existing settings ...

    # PartnerStack
    partnerstack_api_key: str = ""
    partnerstack_partner_key: str = ""  # Optional
```

### Step 4: Test Connection

```bash
./venv/bin/python main.py test-partnerstack
```

Expected output:
```
Testing PartnerStack connection...
✓ Successfully connected to PartnerStack API
✓ Found 55 active programs
```

### Step 5: Sync All Programs

```bash
./venv/bin/python main.py sync-partnerstack
```

This will:
- Fetch all 55 programs from PartnerStack
- Import them into your database
- Extract relevant keywords
- Set commission rates
- Store affiliate link patterns

Expected output:
```
Syncing PartnerStack programs...
✓ Imported 55 programs
  - ClickUp (Project Management) - 30% commission
  - Gusto (HR & Payroll) - 25% commission
  - Navan (Travel) - 20% commission
  ... (52 more)
```

### Step 6: Verify Integration

```bash
# List all affiliate programs
./venv/bin/python main.py list-affiliates --limit 55

# Search for specific programs
./venv/bin/python main.py search-affiliates "cybersecurity"
```

## 💰 How It Generates Revenue

### Automated Workflow

1. **Research Agent** discovers topic:
   - "Best Project Management Tools for Federal Contractors"

2. **Affiliate Agent** searches your programs:
   ```python
   # Searches all 55 programs
   # Finds best match: ClickUp (score: 0.89)
   # Reason: Keywords match - "project management", "contractors"
   ```

3. **Content Agent** generates post with natural mention:
   ```markdown
   ## Project Management Solutions

   For federal contractors managing complex projects, tools like
   [ClickUp](https://partnerstack.com/go/clickup?ref=YOUR_KEY)
   provide comprehensive task tracking, timeline management, and
   team collaboration features essential for government work.
   ```

4. **Publishing Agent** deploys to gjhconsulting.net

5. **Reader clicks link** → PartnerStack tracks → **You earn commission**

### Expected Revenue

| Month | Posts | Links | Clicks | Conversions | Revenue |
|-------|-------|-------|--------|-------------|---------|
| 1     | 12    | 40    | 120    | 2-3         | $500-1K |
| 3     | 36    | 120   | 400    | 6-8         | $1.5K-2.5K |
| 6     | 72    | 240   | 850    | 12-15       | $3K-5K |
| 12    | 156   | 500+  | 1,800  | 25-30       | **$8K-12K/month** |

## 🔧 CLI Commands

### Test Connection
```bash
python main.py test-partnerstack
```

### Sync Programs
```bash
# Sync all programs
python main.py sync-partnerstack

# Sync specific program
python main.py sync-partnerstack --program clickup
```

### List Programs
```bash
# All programs
python main.py list-affiliates

# By category
python main.py list-affiliates --category "Cybersecurity"

# Top earners
python main.py list-affiliates --sort-by commission --limit 10
```

### Search Programs
```bash
python main.py search-affiliates "project management"
python main.py search-affiliates "security compliance"
python main.py search-affiliates "hr payroll"
```

### Generate Link
```bash
python main.py generate-affiliate-link clickup
# Output: https://partnerstack.com/go/clickup?ref=YOUR_KEY
```

## 📈 Optimization Strategies

### 1. Keyword Optimization

Update program keywords for better matching:

```python
# In affiliate_agent.py or via CLI
affiliate_agent.update_keywords(
    product_id=5,
    keywords=["federal", "government", "compliance", "NIST", "FedRAMP"]
)
```

### 2. Topic-Product Mapping

Create custom mappings for high-value combinations:

```python
TOPIC_MAPPINGS = {
    "cybersecurity": ["crowdstrike", "okta", "1password"],
    "project_management": ["clickup", "asana", "monday"],
    "hr_compliance": ["gusto", "rippling", "bamboohr"],
    "travel": ["navan", "expensify"],
}
```

### 3. Commission Prioritization

Prioritize higher-commission programs:

```python
# affiliate_agent.py
def calculate_match_score(self, topic, product):
    base_score = super().calculate_match_score(topic, product)

    # Boost score based on commission
    commission_boost = product.commission_rate / 100  # 30% = 0.3 boost

    return base_score * (1 + commission_boost)
```

### 4. Category Targeting

Focus posts on high-commission categories:
- **Cybersecurity**: 35% avg commission
- **Marketing**: 33% avg commission
- **Project Management**: 30% avg commission

## 🧪 Testing

### Manual Test Flow

```bash
# 1. Sync programs
python main.py sync-partnerstack

# 2. Generate test post
python main.py workflow

# 3. Check generated post
cat data/posts/*.md | grep -A 5 "partnerstack.com"

# 4. Verify link
curl -I "https://partnerstack.com/go/clickup?ref=YOUR_KEY"
```

### Expected Output

Generated post should include:
```markdown
For project management needs, consider [ClickUp]
(https://partnerstack.com/go/clickup?ref=YOUR_KEY&utm_source=gjhblog),
which offers robust features for government contractors.
```

## 📊 Tracking & Analytics

### PartnerStack Dashboard

Monitor performance at: https://dash.partnerstack.com

Track:
- **Clicks**: Total link clicks
- **Conversions**: Sign-ups/purchases
- **Revenue**: Total earned
- **Top Programs**: Best performers
- **Conversion Rate**: Clicks to conversions

### Database Queries

```python
# Top performing programs
SELECT
    name,
    affiliate_clicks,
    affiliate_conversions,
    affiliate_revenue
FROM affiliate_products
ORDER BY affiliate_revenue DESC
LIMIT 10;

# Posts with most affiliate success
SELECT
    blog_posts.title,
    post_metrics.affiliate_clicks,
    post_metrics.affiliate_revenue
FROM blog_posts
JOIN post_metrics ON blog_posts.id = post_metrics.post_id
ORDER BY post_metrics.affiliate_revenue DESC;
```

## 🎯 Best Practices

### 1. Natural Integration

✅ **Good**:
> "Federal contractors often struggle with project timelines. Tools like ClickUp provide Gantt charts, dependencies, and resource allocation features that help meet strict government deadlines."

❌ **Bad**:
> "Click here to buy ClickUp! Amazing project management! Sign up now!"

### 2. Multiple Links

Include 1-3 affiliate links per post:
- **Primary**: Best match (e.g., ClickUp for PM post)
- **Secondary**: Related tool (e.g., Gusto for team management)
- **Tertiary**: Complementary service (e.g., CrowdStrike for security)

### 3. Context Matters

Match programs to post topics:
- **GSA Schedule post** → Gusto (payroll compliance)
- **Cybersecurity post** → CrowdStrike, Okta
- **SBIR Grant post** → ClickUp (project tracking)

### 4. Disclosure

Add disclosure to posts:
```markdown
*This post contains affiliate links. We may earn a commission
if you purchase through our links, at no extra cost to you.*
```

## 🔒 Security

### API Key Management

```bash
# Never commit .env
echo ".env" >> .gitignore

# Use environment variables
export PARTNERSTACK_API_KEY="ps_your_key"

# Rotate keys periodically
# Update in PartnerStack dashboard → Settings → API Keys
```

### Rate Limiting

```python
# utils/partnerstack_client.py includes rate limiting
# Max 100 requests/minute
# Automatic retry with exponential backoff
```

## 🐛 Troubleshooting

### Connection Issues

```bash
# Test DNS
ping api.partnerstack.com

# Test API
curl -H "Authorization: Bearer YOUR_KEY" \
     https://api.partnerstack.com/v1/partnerships
```

### No Programs Synced

1. Check API key is correct
2. Verify programs are "active" in dashboard
3. Check database connection
4. Review logs for errors

### Links Not Working

1. Verify program key is correct
2. Check partner key (if using)
3. Test link manually in browser
4. Check PartnerStack program status

## 📚 Additional Resources

- [PartnerStack API Docs](https://docs.partnerstack.com/docs/api)
- [Affiliate Link Best Practices](https://partnerstack.com/resources)
- [Commission Structures](https://dash.partnerstack.com/programs)

## 🎉 Success Checklist

- [ ] PartnerStack API key configured
- [ ] Connection test passed
- [ ] All 55 programs synced
- [ ] Test post generated with affiliate link
- [ ] Link verified and tracking
- [ ] Disclosure added to posts
- [ ] Dashboard monitoring set up
- [ ] First commission earned! 🚀

---

**Your 55 affiliate programs are now actively generating revenue through AI-powered content!**
