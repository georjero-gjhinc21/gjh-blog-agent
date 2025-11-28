"""Impact.com API client for fetching affiliate campaigns and generating links."""
import requests
import base64
from typing import List, Dict, Optional
from config import settings


class ImpactClient:
    """Client for Impact.com API integration."""

    def __init__(self, account_sid: str = None, auth_token: str = None):
        """Initialize Impact.com client.

        Args:
            account_sid: Impact.com Account SID (from URL when logged in)
            auth_token: Impact.com Auth Token (from Settings → API Access)
        """
        self.account_sid = account_sid or settings.impact_account_sid
        self.auth_token = auth_token or settings.impact_auth_token
        self.base_url = f"https://api.impact.com/Mediapartners/{self.account_sid}"

        # Encode credentials for Basic Auth
        credentials = f"{self.account_sid}:{self.auth_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def test_connection(self) -> bool:
        """Test API connection by fetching account info."""
        try:
            response = requests.get(
                f"{self.base_url}/Campaigns",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Impact.com connection test failed: {e}")
            return False

    def get_all_campaigns(self) -> List[Dict]:
        """Fetch all active campaigns (brands) from Impact.com."""
        try:
            response = requests.get(
                f"{self.base_url}/Campaigns",
                headers=self.headers,
                params={
                    "PageSize": 100,
                    "CampaignState": "ACTIVE"
                },
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            campaigns = data.get("Campaigns", [])

            # Transform to our standard format
            transformed = []
            for campaign in campaigns:
                transformed.append({
                    "external_id": str(campaign.get("Id")),
                    "name": campaign.get("Name", "Unknown"),
                    "description": campaign.get("Description", ""),
                    "category": campaign.get("Category", "General"),
                    "commission_rate": self._extract_commission_rate(campaign),
                    "base_url": campaign.get("Url", ""),
                    "affiliate_url": "",  # Will be generated on-demand
                    "logo_url": campaign.get("LogoUrl", ""),
                    "network": "impact",
                    "keywords": self._extract_keywords(campaign)
                })

            return transformed

        except Exception as e:
            print(f"Error fetching Impact.com campaigns: {e}")
            return []

    def get_campaign_details(self, campaign_id: str) -> Optional[Dict]:
        """Get detailed information about a specific campaign."""
        try:
            response = requests.get(
                f"{self.base_url}/Campaigns/{campaign_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching campaign {campaign_id}: {e}")
            return None

    def generate_affiliate_link(
        self,
        campaign_id: str,
        url: str = None,
        sub_id: str = None
    ) -> str:
        """Generate a tracked affiliate link for a campaign.

        Args:
            campaign_id: The Impact.com campaign ID
            url: Optional destination URL (if not provided, uses campaign default)
            sub_id: Optional SubId for tracking (e.g., blog post slug)

        Returns:
            Tracked affiliate link
        """
        try:
            # Create ad via API
            payload = {
                "CampaignId": int(campaign_id),
                "AdType": "TEXT_LINK"
            }

            if url:
                payload["DestinationUrl"] = url

            if sub_id:
                payload["SubId1"] = sub_id

            response = requests.post(
                f"{self.base_url}/Ads",
                headers=self.headers,
                json=payload,
                timeout=10
            )

            if response.status_code in [200, 201]:
                data = response.json()
                return data.get("TrackingLink", "")

            # Fallback: construct manual link
            return self._construct_tracking_link(campaign_id, url, sub_id)

        except Exception as e:
            print(f"Error generating link: {e}")
            # Fallback to manual construction
            return self._construct_tracking_link(campaign_id, url, sub_id)

    def _construct_tracking_link(
        self,
        campaign_id: str,
        url: str = None,
        sub_id: str = None
    ) -> str:
        """Construct a tracking link manually (fallback method)."""
        # Impact.com tracking link format
        base = f"https://impact.com/campaign-promo-code/{self.account_sid}/{campaign_id}"

        params = []
        if url:
            params.append(f"u={url}")
        if sub_id:
            params.append(f"subId1={sub_id}")

        if params:
            base += "?" + "&".join(params)

        return base

    def get_promo_codes(self, campaign_id: str) -> List[Dict]:
        """Get available promo codes for a campaign."""
        try:
            response = requests.get(
                f"{self.base_url}/Campaigns/{campaign_id}/PromoCodes",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return data.get("PromoCodes", [])

        except Exception as e:
            print(f"Error fetching promo codes: {e}")
            return []

    def get_stats(self, days: int = 30) -> Dict:
        """Get performance statistics for the last N days."""
        try:
            response = requests.get(
                f"{self.base_url}/Reports/mp_clicks",
                headers=self.headers,
                params={
                    "MONTH_START_DATE": f"-{days}d",
                    "MONTH_END_DATE": "today"
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return {}

    def search_campaigns(self, query: str, limit: int = 10) -> List[Dict]:
        """Search campaigns by keyword."""
        all_campaigns = self.get_all_campaigns()

        query_lower = query.lower()
        scored_campaigns = []

        for campaign in all_campaigns:
            score = 0

            # Check name
            if query_lower in campaign["name"].lower():
                score += 10

            # Check description
            if query_lower in campaign["description"].lower():
                score += 5

            # Check category
            if query_lower in campaign["category"].lower():
                score += 7

            # Check keywords
            for keyword in campaign["keywords"]:
                if query_lower in keyword or keyword in query_lower:
                    score += 3

            if score > 0:
                scored_campaigns.append((score, campaign))

        # Sort by score
        scored_campaigns.sort(reverse=True, key=lambda x: x[0])

        return [campaign for score, campaign in scored_campaigns[:limit]]

    def _extract_commission_rate(self, campaign: Dict) -> float:
        """Extract commission rate from campaign data."""
        # Impact.com campaigns may have different commission structures
        # Try to extract from common fields

        # Check for payout rate
        payout = campaign.get("DefaultPayout", {})
        if isinstance(payout, dict):
            amount = payout.get("Amount", 0)
            if amount:
                return float(amount)

        # Check for percentage
        commission_percent = campaign.get("CommissionPercent", 0)
        if commission_percent:
            return float(commission_percent)

        return 0.0

    def _extract_keywords(self, campaign: Dict) -> List[str]:
        """Extract relevant keywords from campaign data."""
        keywords = []

        # From name
        name = campaign.get("Name", "")
        if name:
            keywords.append(name.lower())

        # From category
        category = campaign.get("Category", "")
        if category:
            keywords.append(category.lower())

        # From URL - extract domain
        url = campaign.get("Url", "")
        if url:
            import re
            match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            if match:
                domain = match.group(1).replace('.com', '').replace('.io', '').replace('.co', '')
                keywords.append(domain.lower())

        # From description - extract common business terms
        description = campaign.get("Description", "")
        if description:
            terms = [
                "crm", "project management", "hr", "payroll", "security",
                "marketing", "sales", "analytics", "communication", "cloud",
                "automation", "integration", "tracking", "reporting", "compliance",
                "software", "saas", "platform", "tool", "app", "health", "wellness",
                "fitness", "nutrition", "supplements"
            ]
            desc_lower = description.lower()
            for term in terms:
                if term in desc_lower:
                    keywords.append(term)

        # Remove duplicates
        return list(set(keywords))

    def get_campaign_categories(self) -> Dict[str, int]:
        """Get all campaign categories with counts."""
        campaigns = self.get_all_campaigns()
        categories = {}

        for campaign in campaigns:
            cat = campaign["category"]
            categories[cat] = categories.get(cat, 0) + 1

        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))


# Sample fallback data for testing
SAMPLE_IMPACT_CAMPAIGNS = [
    {
        "external_id": "1stphorm",
        "name": "1st Phorm",
        "description": "Premium sports nutrition and wellness supplements",
        "category": "Health & Wellness",
        "commission_rate": 10.0,
        "base_url": "https://1stphorm.com",
        "network": "impact",
        "keywords": ["supplements", "fitness", "nutrition", "wellness", "sports"]
    }
]


def get_sample_impact_campaigns() -> List[Dict]:
    """Return sample Impact.com campaigns for testing."""
    return SAMPLE_IMPACT_CAMPAIGNS
