#!/usr/bin/env python3
"""Test script for unified affiliate system (PartnerStack + Impact.com)."""

from agents.unified_affiliate_agent import UnifiedAffiliateAgent
from utils.partnerstack_client import PartnerStackClient
from utils.impact_client import ImpactClient
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def test_connections():
    """Test API connections to both networks."""
    console.print("\n[bold cyan]Testing Network Connections[/bold cyan]")
    console.print("─" * 50)

    agent = UnifiedAffiliateAgent()
    results = agent.test_connections()

    for network, status in results.items():
        if status:
            console.print(f"✓ {network.capitalize()}: [green]Connected[/green]")
        else:
            console.print(f"✗ {network.capitalize()}: [red]Failed[/red]")

    return all(results.values())


def test_sync_programs():
    """Test syncing programs from both networks."""
    console.print("\n[bold cyan]Syncing Programs[/bold cyan]")
    console.print("─" * 50)

    agent = UnifiedAffiliateAgent()
    counts = agent.sync_all_programs()

    console.print(f"PartnerStack: [green]{counts['partnerstack']}[/green] programs")
    console.print(f"Impact.com: [green]{counts['impact']}[/green] programs")
    console.print(f"Total: [bold green]{counts['total']}[/bold green] programs loaded")

    return agent, counts


def test_search():
    """Test searching across both networks."""
    console.print("\n[bold cyan]Testing Search Functionality[/bold cyan]")
    console.print("─" * 50)

    agent = UnifiedAffiliateAgent()
    agent.sync_all_programs()

    # Test searches
    test_queries = ["cybersecurity", "project management", "hr", "wellness"]

    for query in test_queries:
        results = agent.search_programs(query, limit=3)
        if results:
            console.print(f"\n[yellow]Search:[/yellow] '{query}'")
            for i, prog in enumerate(results, 1):
                network_color = "blue" if prog['network'] == 'partnerstack' else "magenta"
                console.print(f"  {i}. {prog['name']} ([{network_color}]{prog['network']}[/{network_color}])")


def test_matching():
    """Test content matching with AI."""
    console.print("\n[bold cyan]Testing Content Matching[/bold cyan]")
    console.print("─" * 50)

    agent = UnifiedAffiliateAgent()
    agent.sync_all_programs()

    # Test content
    test_content = """
    In this comprehensive guide, we'll explore the best project management tools
    for federal contractors and government agencies. We'll cover collaboration
    platforms, task tracking, and team communication solutions.
    """

    matches = agent.find_best_matches(
        content=test_content,
        title="Best Project Management Tools for Government Contractors",
        max_matches=4
    )

    if matches:
        table = Table(title="Top Matches")
        table.add_column("Program", style="cyan")
        table.add_column("Network", style="magenta")
        table.add_column("Score", justify="right", style="green")
        table.add_column("Commission", justify="right", style="yellow")

        for match in matches:
            table.add_row(
                match['name'],
                match['network'],
                f"{match.get('match_score', 0):.2f}",
                f"{match.get('commission_rate', 0):.1f}%"
            )

        console.print(table)
    else:
        console.print("[yellow]No matches found[/yellow]")


def test_link_generation():
    """Test generating affiliate links."""
    console.print("\n[bold cyan]Testing Link Generation[/bold cyan]")
    console.print("─" * 50)

    agent = UnifiedAffiliateAgent()
    agent.sync_all_programs()

    # Get first few programs
    programs = agent.list_all_programs()[:5]

    for prog in programs:
        link = agent.generate_link(
            program_name=prog['name'],
            sub_id="test-blog-post"
        )

        network_color = "blue" if prog['network'] == 'partnerstack' else "magenta"
        console.print(f"\n[{network_color}]{prog['name']}[/{network_color}]")
        console.print(f"  Network: {prog['network']}")
        if link:
            console.print(f"  Link: [dim]{link}[/dim]")
        else:
            console.print(f"  Link: [red]Generation failed[/red]")


def test_stats():
    """Test getting statistics."""
    console.print("\n[bold cyan]System Statistics[/bold cyan]")
    console.print("─" * 50)

    agent = UnifiedAffiliateAgent()
    agent.sync_all_programs()
    stats = agent.get_stats()

    # Network stats
    console.print("\n[bold]Network Distribution:[/bold]")
    for network, count in stats['networks'].items():
        if network != 'total':
            console.print(f"  {network.capitalize()}: {count}")
    console.print(f"  [bold]Total: {stats['networks']['total']}[/bold]")

    # Category stats
    console.print("\n[bold]Top Categories:[/bold]")
    for i, (category, count) in enumerate(list(stats['categories'].items())[:10], 1):
        console.print(f"  {i}. {category}: {count}")

    # Top commission programs
    console.print("\n[bold]Top Commission Programs:[/bold]")
    for i, prog in enumerate(stats['top_commission_programs'][:5], 1):
        console.print(f"  {i}. {prog['name']} ({prog['network']}): {prog['commission']:.1f}%")


def test_impact_specific():
    """Test Impact.com specific features."""
    console.print("\n[bold cyan]Testing Impact.com Specific Features[/bold cyan]")
    console.print("─" * 50)

    client = ImpactClient()

    # Get campaigns
    campaigns = client.get_all_campaigns()
    console.print(f"\nImpact.com campaigns: {len(campaigns)}")

    if campaigns:
        # Test first campaign
        campaign = campaigns[0]
        console.print(f"\nTest Campaign: [cyan]{campaign['name']}[/cyan]")
        console.print(f"  Category: {campaign.get('category')}")
        console.print(f"  Commission: {campaign.get('commission_rate', 0)}%")

        # Try getting promo codes
        promo_codes = client.get_promo_codes(campaign['external_id'])
        if promo_codes:
            console.print(f"\n  Promo Codes Available: {len(promo_codes)}")
            for code in promo_codes[:3]:
                console.print(f"    - {code.get('Code', 'N/A')}")
        else:
            console.print("  No promo codes available")


def test_export():
    """Test exporting programs."""
    console.print("\n[bold cyan]Testing Export Functionality[/bold cyan]")
    console.print("─" * 50)

    agent = UnifiedAffiliateAgent()
    agent.sync_all_programs()

    # Export as dict
    programs = agent.export_programs(format="dict")
    console.print(f"Exported {len(programs)} programs as dict")

    # Export as CSV
    csv_data = agent.export_programs(format="csv")
    lines = csv_data.split('\n')
    console.print(f"Exported as CSV: {len(lines)} lines")
    console.print(f"\nFirst 3 lines:")
    for line in lines[:3]:
        console.print(f"  {line[:80]}...")


def main():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]GJH Unified Affiliate System Test Suite[/bold cyan]\n"
        "Testing PartnerStack + Impact.com Integration",
        border_style="cyan"
    ))

    try:
        # Test 1: Connections
        if not test_connections():
            console.print("\n[red]⚠ Connection test failed. Check your API credentials.[/red]")
            return

        # Test 2: Sync
        agent, counts = test_sync_programs()

        if counts['total'] == 0:
            console.print("\n[yellow]⚠ No programs synced. Check API access.[/yellow]")
            return

        # Test 3: Search
        test_search()

        # Test 4: Matching
        test_matching()

        # Test 5: Link Generation
        test_link_generation()

        # Test 6: Statistics
        test_stats()

        # Test 7: Impact.com specific
        test_impact_specific()

        # Test 8: Export
        test_export()

        # Success summary
        console.print("\n" + "─" * 50)
        console.print(Panel.fit(
            "[bold green]✓ All tests completed successfully![/bold green]\n"
            f"Total programs available: {counts['total']}\n"
            f"PartnerStack: {counts['partnerstack']} | Impact.com: {counts['impact']}",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"\n[red]Error during testing: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
