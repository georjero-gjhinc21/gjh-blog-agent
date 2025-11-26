"""PartnerStack API client for fetching affiliate programs and generating links."""
import requests
from typing import List, Dict, Optional
from config import settings


class PartnerStackClient:
    """Client for PartnerStack API integration."""

    def __init__(self, api_key: str = None, partner_key: str = None):
        """Initialize PartnerStack client.

        V2 API uses Bearer token authentication.
        """
        self.api_key = api_key or settings.partnerstack_api_key
        self.partner_key = partner_key or settings.partnerstack_partner_key
        self.base_url = "https://api.partnerstack.com/api/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def test_connection(self) -> bool:
        """Test API connection."""
        try:
            response = requests.get(
                f"{self.base_url}/partnerships",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def get_all_programs(self) -> List[Dict]:
        """Fetch all active affiliate programs from PartnerStack (V2 API)."""
        try:
            response = requests.get(
                f"{self.base_url}/partnerships",
                headers=self.headers,
                params={"status": "active", "limit": 100},
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            # V2 API structure: {"data": {"items": [...], "has_more": bool}}
            partnerships = data.get("data", {}).get("items", [])

            # Transform to our format
            transformed = []
            for prog in partnerships:
                company = prog.get("company", {})
                link = prog.get("link", {})
                offers = prog.get("offers", {})
                team = prog.get("team", {})

                # Extract commission rate from offers
                commission_rate = 0.0
                if offers.get("base_rate"):
                    commission_rate = float(offers.get("base_rate", 0))

                transformed.append({
                    "external_id": prog.get("key"),
                    "name": company.get("name", "Unknown"),
                    "description": link.get("destination", ""),
                    "category": team.get("name", "General"),
                    "commission_rate": commission_rate,
                    "base_url": link.get("destination", ""),
                    "affiliate_url": link.get("url", ""),
                    "logo_url": "",
                    "keywords": self._extract_keywords_v2(prog)
                })

            return transformed

        except Exception as e:
            print(f"Error fetching programs: {e}")
            return []

    def get_program_details(self, program_key: str) -> Optional[Dict]:
        """Get detailed information about a specific program."""
        try:
            response = requests.get(
                f"{self.base_url}/partnerships/{program_key}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching program {program_key}: {e}")
            return None

    def generate_affiliate_link(self, program_key: str, path: str = "") -> str:
        """Generate a tracked affiliate link for a program."""
        # PartnerStack link format: https://partnerstack.com/go/{program_key}?ref={partner_key}
        base = f"https://partnerstack.com/go/{program_key}"

        # Add partner reference if available
        if hasattr(settings, 'partnerstack_partner_key'):
            base += f"?ref={settings.partnerstack_partner_key}"

        # Add custom path if provided
        if path:
            separator = "&" if "?" in base else "?"
            base += f"{separator}utm_source=gjhblog&utm_content={path}"

        return base

    def _extract_keywords(self, program: Dict) -> List[str]:
        """Extract relevant keywords from program data (V1 format)."""
        keywords = []

        # From name
        name = program.get("company_name", "")
        keywords.append(name.lower())

        # From category
        category = program.get("category", "")
        if category:
            keywords.append(category.lower())

        # From description
        description = program.get("description", "")
        if description:
            # Extract common business terms
            terms = [
                "crm", "project management", "hr", "payroll", "security",
                "marketing", "sales", "analytics", "communication", "cloud",
                "automation", "integration", "tracking", "reporting", "compliance"
            ]
            desc_lower = description.lower()
            for term in terms:
                if term in desc_lower:
                    keywords.append(term)

        # From tags if available
        tags = program.get("tags", [])
        keywords.extend([tag.lower() for tag in tags])

        return list(set(keywords))  # Remove duplicates

    def _extract_keywords_v2(self, program: Dict) -> List[str]:
        """Extract relevant keywords from program data (V2 API format)."""
        keywords = []

        # From company name
        company = program.get("company", {})
        name = company.get("name", "")
        if name:
            keywords.append(name.lower())

        # From team/category
        team = program.get("team", {})
        team_name = team.get("name", "")
        if team_name:
            keywords.append(team_name.lower())

        # From destination URL - extract domain keywords
        link = program.get("link", {})
        destination = link.get("destination", "")
        if destination:
            # Extract domain name
            import re
            match = re.search(r'https?://(?:www\.)?([^/]+)', destination)
            if match:
                domain = match.group(1).replace('.com', '').replace('.io', '').replace('.co', '')
                keywords.append(domain.lower())

            # Extract common business terms from URL
            terms = [
                "crm", "project", "hr", "payroll", "security",
                "marketing", "sales", "analytics", "communication", "cloud",
                "automation", "integration", "tracking", "reporting", "compliance",
                "software", "saas", "platform", "tool", "app"
            ]
            dest_lower = destination.lower()
            for term in terms:
                if term in dest_lower:
                    keywords.append(term)

        return list(set(keywords))  # Remove duplicates

    def search_programs(self, query: str, limit: int = 10) -> List[Dict]:
        """Search programs by keyword."""
        all_programs = self.get_all_programs()

        query_lower = query.lower()
        scored_programs = []

        for prog in all_programs:
            score = 0

            # Check name
            if query_lower in prog["name"].lower():
                score += 10

            # Check description
            if query_lower in prog["description"].lower():
                score += 5

            # Check category
            if query_lower in prog["category"].lower():
                score += 7

            # Check keywords
            for keyword in prog["keywords"]:
                if query_lower in keyword or keyword in query_lower:
                    score += 3

            if score > 0:
                scored_programs.append((score, prog))

        # Sort by score
        scored_programs.sort(reverse=True, key=lambda x: x[0])

        return [prog for score, prog in scored_programs[:limit]]

    def get_program_categories(self) -> Dict[str, int]:
        """Get all program categories with counts."""
        programs = self.get_all_programs()
        categories = {}

        for prog in programs:
            cat = prog["category"]
            categories[cat] = categories.get(cat, 0) + 1

        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))


# Sample fallback data for testing without API key
SAMPLE_PROGRAMS = [
    {
        "external_id": "clickup",
        "name": "ClickUp",
        "description": "All-in-one project management and productivity platform for teams",
        "category": "Project Management",
        "commission_rate": 30.0,
        "base_url": "https://clickup.com",
        "keywords": ["project management", "productivity", "collaboration", "tasks", "agile"]
    },
    {
        "external_id": "gusto",
        "name": "Gusto",
        "description": "Modern payroll, benefits, and HR platform for small businesses",
        "category": "HR & Payroll",
        "commission_rate": 25.0,
        "base_url": "https://gusto.com",
        "keywords": ["payroll", "hr", "benefits", "compliance", "small business"]
    },
    {
        "external_id": "navan",
        "name": "Navan",
        "description": "Corporate travel and expense management platform",
        "category": "Travel & Expense",
        "commission_rate": 20.0,
        "base_url": "https://navan.com",
        "keywords": ["travel", "expense", "corporate", "booking", "management"]
    },
    {
        "external_id": "crowdstrike",
        "name": "CrowdStrike",
        "description": "Cloud-native endpoint security and threat intelligence platform",
        "category": "Cybersecurity",
        "commission_rate": 35.0,
        "base_url": "https://crowdstrike.com",
        "keywords": ["cybersecurity", "endpoint", "threat", "protection", "security"]
    },
    {
        "external_id": "getresponse",
        "name": "GetResponse",
        "description": "Email marketing, automation, and landing page platform",
        "category": "Marketing",
        "commission_rate": 33.0,
        "base_url": "https://getresponse.com",
        "keywords": ["email marketing", "automation", "landing pages", "marketing"]
    }
]


def get_sample_programs() -> List[Dict]:
    """Return sample programs for testing."""
    return SAMPLE_PROGRAMS
