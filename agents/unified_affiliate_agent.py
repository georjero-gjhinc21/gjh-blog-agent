"""Unified Affiliate Agent - Manages multiple affiliate networks (PartnerStack + Impact.com)."""
from typing import List, Dict, Optional
from utils.partnerstack_client import PartnerStackClient
from utils.impact_client import ImpactClient
from utils.ollama_client import OllamaClient


class UnifiedAffiliateAgent:
    """Manages affiliate programs across multiple networks for intelligent content matching."""

    def __init__(
        self,
        partnerstack_client: PartnerStackClient = None,
        impact_client: ImpactClient = None
    ):
        """Initialize unified affiliate agent with multiple network clients."""
        self.ps_client = partnerstack_client or PartnerStackClient()
        self.impact_client = impact_client or ImpactClient()
        self.ollama = OllamaClient()
        self.all_programs = []
        self.programs_by_network = {
            "partnerstack": [],
            "impact": []
        }

    def test_connections(self) -> Dict[str, bool]:
        """Test connections to all affiliate networks."""
        results = {
            "partnerstack": self.ps_client.test_connection(),
            "impact": self.impact_client.test_connection()
        }
        return results

    def sync_all_programs(self) -> Dict[str, int]:
        """Sync programs from all affiliate networks.

        Returns:
            Dict with count of programs from each network
        """
        # Fetch from PartnerStack
        ps_programs = self.ps_client.get_all_programs()
        for prog in ps_programs:
            prog["network"] = "partnerstack"
        self.programs_by_network["partnerstack"] = ps_programs

        # Fetch from Impact.com
        impact_programs = self.impact_client.get_all_campaigns()
        for prog in impact_programs:
            prog["network"] = "impact"
        self.programs_by_network["impact"] = impact_programs

        # Combine all programs
        self.all_programs = ps_programs + impact_programs

        return {
            "partnerstack": len(ps_programs),
            "impact": len(impact_programs),
            "total": len(self.all_programs)
        }

    def find_best_matches(
        self,
        content: str,
        title: str = "",
        max_matches: int = 3,
        min_score: float = 0.15
    ) -> List[Dict]:
        """Find the best matching affiliate programs for given content.

        Args:
            content: Blog post content
            title: Blog post title
            max_matches: Maximum number of matches to return
            min_score: Minimum match score (0.0-1.0)

        Returns:
            List of matched programs with scores
        """
        if not self.all_programs:
            self.sync_all_programs()

        # Combine title and content for matching
        full_text = f"{title}\n\n{content}"

        # Score each program
        scored_programs = []
        for program in self.all_programs:
            score = self._calculate_match_score(full_text, program)
            if score >= min_score:
                program_with_score = program.copy()
                program_with_score["match_score"] = score
                scored_programs.append(program_with_score)

        # Sort by score and return top matches
        scored_programs.sort(key=lambda x: x["match_score"], reverse=True)
        return scored_programs[:max_matches]

    def _calculate_match_score(self, content: str, program: Dict) -> float:
        """Calculate how well a program matches content using AI.

        Args:
            content: The blog content to match against
            program: The affiliate program

        Returns:
            Match score between 0.0 and 1.0
        """
        # Prepare program description
        program_text = f"""
Name: {program['name']}
Description: {program['description']}
Category: {program['category']}
Keywords: {', '.join(program.get('keywords', []))}
Network: {program.get('network', 'unknown')}
"""

        system = """You are an affiliate marketing expert. Return ONLY a single number between 0.0 and 1.0. No explanations."""

        prompt = f"""Rate this match as ONE NUMBER ONLY (0.0-1.0). NO TEXT.

Content: {content[:300]}
Program: {program_text[:200]}

Score:"""

        try:
            response = self.ollama.generate(prompt, system, temperature=0.2)
            score = float(response.strip())
            return max(0.0, min(1.0, score))
        except Exception as e:
            print(f"AI scoring failed for {program['name']}: {e}")
            # Fallback to keyword matching
            return self._keyword_match_score(content, program)

    def _keyword_match_score(self, content: str, program: Dict) -> float:
        """Fallback keyword-based matching when AI is unavailable."""
        content_lower = content.lower()
        program_keywords = [k.lower() for k in program.get("keywords", [])]

        if not program_keywords:
            return 0.0

        matches = sum(1 for kw in program_keywords if kw in content_lower)
        return min(1.0, matches / len(program_keywords))

    def generate_link(
        self,
        program_name: str,
        sub_id: str = None,
        path: str = ""
    ) -> Optional[str]:
        """Generate an affiliate link for a program by name.

        Args:
            program_name: Name of the affiliate program
            sub_id: Optional tracking ID (e.g., blog post slug)
            path: Optional path/URL parameter

        Returns:
            Tracked affiliate link or None if program not found
        """
        # Find program
        program = None
        for p in self.all_programs:
            if p["name"].lower() == program_name.lower():
                program = p
                break

        if not program:
            print(f"Program '{program_name}' not found")
            return None

        # Generate link based on network
        network = program.get("network", "partnerstack")

        if network == "partnerstack":
            return self.ps_client.generate_affiliate_link(
                program["external_id"],
                path=path or sub_id
            )
        elif network == "impact":
            return self.impact_client.generate_affiliate_link(
                program["external_id"],
                url=program.get("base_url"),
                sub_id=sub_id
            )
        else:
            print(f"Unknown network: {network}")
            return None

    def search_programs(self, query: str, limit: int = 10) -> List[Dict]:
        """Search across all networks for matching programs.

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            List of matching programs
        """
        if not self.all_programs:
            self.sync_all_programs()

        query_lower = query.lower()
        scored_programs = []

        for program in self.all_programs:
            score = 0

            # Check name
            if program.get("name") and query_lower in program["name"].lower():
                score += 10

            # Check description
            description = program.get("description", "")
            if description and query_lower in description.lower():
                score += 5

            # Check category
            category = program.get("category", "")
            if category and query_lower in category.lower():
                score += 7

            # Check keywords
            for keyword in program.get("keywords", []):
                if keyword and (query_lower in keyword or keyword in query_lower):
                    score += 3

            if score > 0:
                scored_programs.append((score, program))

        # Sort by score
        scored_programs.sort(reverse=True, key=lambda x: x[0])

        return [prog for score, prog in scored_programs[:limit]]

    def get_stats(self) -> Dict:
        """Get statistics across all networks.

        Returns:
            Dict with program counts, categories, networks, etc.
        """
        if not self.all_programs:
            self.sync_all_programs()

        # Count by network
        network_counts = {
            "partnerstack": len(self.programs_by_network["partnerstack"]),
            "impact": len(self.programs_by_network["impact"]),
            "total": len(self.all_programs)
        }

        # Count by category
        categories = {}
        for program in self.all_programs:
            cat = program.get("category", "Unknown")
            categories[cat] = categories.get(cat, 0) + 1

        # Top programs by commission
        top_commission = sorted(
            self.all_programs,
            key=lambda x: x.get("commission_rate", 0),
            reverse=True
        )[:10]

        return {
            "networks": network_counts,
            "categories": dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)),
            "top_commission_programs": [
                {
                    "name": p["name"],
                    "network": p.get("network"),
                    "commission": p.get("commission_rate", 0)
                }
                for p in top_commission
            ]
        }

    def format_affiliate_section(
        self,
        matches: List[Dict],
        section_title: str = "Recommended Tools & Services"
    ) -> str:
        """Format matched programs as a blog post section.

        Args:
            matches: List of matched programs with scores
            section_title: Title for the affiliate section

        Returns:
            Formatted markdown section
        """
        if not matches:
            return ""

        section = f"\n## {section_title}\n\n"

        for i, match in enumerate(matches, 1):
            # Generate link
            link = self.generate_link(match["name"])

            section += f"### {i}. {match['name']}\n\n"
            section += f"{match['description']}\n\n"

            if link:
                section += f"[Learn more about {match['name']}]({link})\n\n"

            # Add match score in comment for debugging (optional)
            # section += f"<!-- Match score: {match.get('match_score', 0):.2f} -->\n\n"

        return section

    def format_affiliate_disclosure(self) -> str:
        """Generate standard affiliate disclosure text.

        Returns:
            Formatted markdown disclosure
        """
        return """
---

**Affiliate Disclosure**: This post may contain affiliate links. If you click through and make a purchase, we may earn a commission at no additional cost to you. We only recommend products and services we genuinely believe will benefit our readers in their government contracting journey.

---
"""

    def get_program_by_name(self, name: str) -> Optional[Dict]:
        """Get a program by exact or partial name match.

        Args:
            name: Program name to search for

        Returns:
            Program dict or None
        """
        if not self.all_programs:
            self.sync_all_programs()

        name_lower = name.lower()

        # Try exact match first
        for program in self.all_programs:
            if program["name"].lower() == name_lower:
                return program

        # Try partial match
        for program in self.all_programs:
            if name_lower in program["name"].lower():
                return program

        return None

    def list_all_programs(self, network: str = None) -> List[Dict]:
        """List all programs, optionally filtered by network.

        Args:
            network: Optional network filter ('partnerstack' or 'impact')

        Returns:
            List of programs
        """
        if not self.all_programs:
            self.sync_all_programs()

        if network:
            return [p for p in self.all_programs if p.get("network") == network]

        return self.all_programs

    def export_programs(self, format: str = "dict") -> List[Dict]:
        """Export all programs in a specific format.

        Args:
            format: Export format ('dict', 'json', 'csv')

        Returns:
            List of programs in requested format
        """
        if not self.all_programs:
            self.sync_all_programs()

        if format == "dict":
            return self.all_programs
        elif format == "json":
            import json
            return json.dumps(self.all_programs, indent=2)
        elif format == "csv":
            # Simplified CSV export
            csv_lines = ["Name,Description,Category,Network,Commission"]
            for p in self.all_programs:
                csv_lines.append(
                    f'"{p["name"]}","{p.get("description", "")}","{p.get("category", "")}","{p.get("network", "")}",{p.get("commission_rate", 0)}'
                )
            return "\n".join(csv_lines)
        else:
            return self.all_programs
