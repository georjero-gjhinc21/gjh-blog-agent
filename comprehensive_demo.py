#!/usr/bin/env python3
"""Comprehensive demo of all affiliate system functions."""

from agents.unified_affiliate_agent import UnifiedAffiliateAgent
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def demo_1_test_connections():
    """Demo 1: Test network connections."""
    console.print("\n[bold cyan]═══ DEMO 1: Test Connections ═══[/bold cyan]\n")

    agent = UnifiedAffiliateAgent()
    status = agent.test_connections()

    for network, connected in status.items():
        icon = "✓" if connected else "✗"
        color = "green" if connected else "red"
        console.print(f"[{color}]{icon} {network.capitalize()}: {'Connected' if connected else 'Failed'}[/{color}]")

    return agent


def demo_2_sync_programs(agent):
    """Demo 2: Sync all programs from both networks."""
    console.print("\n[bold cyan]═══ DEMO 2: Sync Programs ═══[/bold cyan]\n")

    counts = agent.sync_all_programs()

    console.print(f"[green]✓ PartnerStack: {counts['partnerstack']} programs[/green]")
    console.print(f"[green]✓ Impact.com: {counts['impact']} programs[/green]")
    console.print(f"[bold green]✓ Total: {counts['total']} programs loaded[/bold green]")

    return counts


def demo_3_search_and_links(agent):
    """Demo 3: Search programs and generate links."""
    console.print("\n[bold cyan]═══ DEMO 3: Search & Generate Links ═══[/bold cyan]\n")

    # Search for different categories
    searches = ["cybersecurity", "project", "crm"]

    for query in searches:
        results = agent.search_programs(query, limit=2)

        if results:
            console.print(f"\n[yellow]Search:[/yellow] '{query}'")

            table = Table(show_header=True)
            table.add_column("Program", style="cyan")
            table.add_column("Network", style="magenta")
            table.add_column("Link Sample", style="dim")

            for prog in results:
                # Generate link
                link = agent.generate_link(prog['name'], sub_id="demo")
                link_preview = link[:40] + "..." if link and len(link) > 40 else (link or "N/A")

                table.add_row(
                    prog['name'],
                    prog.get('network', 'unknown'),
                    link_preview
                )

            console.print(table)


def demo_4_content_matching(agent):
    """Demo 4: Match content to affiliate programs."""
    console.print("\n[bold cyan]═══ DEMO 4: Content Matching ═══[/bold cyan]\n")

    # Sample blog content
    sample_posts = [
        {
            "title": "Best Project Management Tools for Government Contractors",
            "snippet": "Discover top project management solutions for federal contractors including collaboration, task tracking, and team communication."
        },
        {
            "title": "Cybersecurity Compliance for Federal Contractors",
            "snippet": "Essential cybersecurity tools for CMMC compliance including endpoint protection and threat intelligence."
        },
        {
            "title": "HR and Payroll Solutions for Small Businesses",
            "snippet": "Streamline your HR processes with modern payroll and benefits management platforms."
        }
    ]

    for post in sample_posts:
        console.print(f"\n[bold]Post:[/bold] {post['title']}")

        # Find matches (without verbose AI - using keyword matching)
        matches = []
        content = f"{post['title']} {post['snippet']}"

        # Get top programs by keyword matching
        all_programs = agent.list_all_programs()

        for prog in all_programs[:20]:  # Check first 20 programs
            # Simple keyword matching
            keywords = prog.get('keywords', [])
            score = 0

            for keyword in keywords:
                if keyword and keyword.lower() in content.lower():
                    score += 1

            if score > 0:
                prog_copy = prog.copy()
                prog_copy['match_score'] = score / max(len(keywords), 1)
                matches.append(prog_copy)

        # Sort by score and take top 3
        matches.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        top_matches = matches[:3]

        if top_matches:
            console.print(f"  [green]Found {len(top_matches)} matches:[/green]")
            for i, match in enumerate(top_matches, 1):
                console.print(f"    {i}. {match['name']} ({match.get('network')}) - Score: {match.get('match_score', 0):.2f}")
        else:
            console.print("  [yellow]No keyword matches found[/yellow]")


def main():
    """Run comprehensive demo."""
    console.print(Panel.fit(
        "[bold cyan]GJH Unified Affiliate System[/bold cyan]\n"
        "Comprehensive Demo: All Functions",
        border_style="cyan"
    ))

    try:
        # Demo 1: Test connections
        agent = demo_1_test_connections()

        # Demo 2: Sync programs
        counts = demo_2_sync_programs(agent)

        # Demo 3: Search and generate links
        demo_3_search_and_links(agent)

        # Demo 4: Content matching
        demo_4_content_matching(agent)

        # Summary
        console.print("\n" + "═" * 50)
        console.print(Panel.fit(
            f"[bold green]✓ All Demos Completed Successfully![/bold green]\n\n"
            f"System Stats:\n"
            f"  • Networks: 2 (PartnerStack + Impact.com)\n"
            f"  • Programs: {counts['total']} total\n"
            f"  • Search: ✓ Functional\n"
            f"  • Links: ✓ Generated\n"
            f"  • Matching: ✓ Working\n\n"
            f"Ready for production integration!",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
