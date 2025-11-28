#!/usr/bin/env python3
"""
Script to help discover and join more Impact.com campaigns.

This script helps you:
1. Browse available campaigns on Impact.com by category
2. Get recommendations for GovCon-relevant programs
3. Track which campaigns to apply to
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.impact_client import ImpactClient
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


# High-value keywords for GovCon audience
GOVCON_KEYWORDS = [
    "project management", "crm", "collaboration", "productivity",
    "security", "cybersecurity", "compliance", "cloud", "saas",
    "analytics", "automation", "communication", "hr", "payroll",
    "accounting", "training", "certification", "consulting"
]


# Recommended programs to pursue (manually curated)
RECOMMENDED_PROGRAMS = [
    {
        "name": "Monday.com",
        "category": "Project Management",
        "why": "Popular PM tool, government contractors need",
        "commission": "20-30%",
        "priority": "HIGH"
    },
    {
        "name": "HubSpot",
        "category": "CRM & Marketing",
        "why": "Industry-standard CRM for B2B",
        "commission": "100% first month recurring",
        "priority": "HIGH"
    },
    {
        "name": "DocuSign",
        "category": "Business Tools",
        "why": "Essential for contract signing",
        "commission": "15-25%",
        "priority": "HIGH"
    },
    {
        "name": "QuickBooks",
        "category": "Accounting",
        "why": "Required for government contractors",
        "commission": "20%+",
        "priority": "HIGH"
    },
    {
        "name": "Zoom",
        "category": "Communication",
        "why": "Standard for remote meetings",
        "commission": "20%",
        "priority": "MEDIUM"
    },
    {
        "name": "Norton/McAfee",
        "category": "Cybersecurity",
        "why": "Compliance requirements",
        "commission": "40%+",
        "priority": "HIGH"
    },
    {
        "name": "Coursera/Udemy",
        "category": "Training",
        "why": "Professional development for contractors",
        "commission": "20-45%",
        "priority": "MEDIUM"
    },
    {
        "name": "AWS Activate",
        "category": "Cloud",
        "why": "Government cloud services",
        "commission": "Varies",
        "priority": "MEDIUM"
    }
]


def show_recommended_programs():
    """Display recommended programs to pursue."""
    console.print("\n[bold cyan]═══ Recommended Programs to Join ═══[/bold cyan]\n")

    table = Table(title="High-Priority Programs for GovCon Blog")
    table.add_column("Program", style="cyan")
    table.add_column("Category", style="yellow")
    table.add_column("Why Important", style="white")
    table.add_column("Commission", style="green")
    table.add_column("Priority", style="magenta")

    for prog in RECOMMENDED_PROGRAMS:
        priority_color = "red" if prog["priority"] == "HIGH" else "yellow"
        table.add_row(
            prog["name"],
            prog["category"],
            prog["why"],
            prog["commission"],
            f"[{priority_color}]{prog['priority']}[/{priority_color}]"
        )

    console.print(table)


def show_search_strategy():
    """Display search strategy for Impact.com Marketplace."""
    console.print("\n[bold cyan]═══ Search Strategy ═══[/bold cyan]\n")

    console.print("[bold]Step 1: Access Impact.com Marketplace[/bold]")
    console.print("  1. Log into https://app.impact.com")
    console.print("  2. Navigate to: Marketplace → Find Brands")
    console.print("  3. Use filters and search\n")

    console.print("[bold]Step 2: Use These Search Terms:[/bold]")

    # Group keywords by category
    categories = {
        "Software & Tools": ["project management", "crm", "collaboration", "productivity"],
        "Security": ["cybersecurity", "security", "compliance"],
        "Business Services": ["hr", "payroll", "accounting", "consulting"],
        "Training": ["training", "certification", "education"],
        "Cloud & Tech": ["cloud", "saas", "automation", "analytics"]
    }

    for category, keywords in categories.items():
        console.print(f"\n  [yellow]{category}:[/yellow]")
        for kw in keywords:
            console.print(f"    • {kw}")


def show_application_checklist():
    """Display checklist for applying to programs."""
    console.print("\n[bold cyan]═══ Application Checklist ═══[/bold cyan]\n")

    checklist = [
        ("✓ Profile Complete", "Ensure your Impact.com profile is 100% filled out"),
        ("✓ Website Listed", "Add gjhconsulting.net to your profile"),
        ("✓ Traffic Data", "Be ready to share monthly pageviews"),
        ("✓ Content Examples", "Have sample blog posts ready to show"),
        ("✓ Apply in Batches", "Apply to 10-20 programs at once"),
        ("✓ Follow Up", "Check status after 2-3 days"),
        ("✓ Sync After Approval", "Run 'python main.py sync-unified' after approvals")
    ]

    for item, description in checklist:
        console.print(f"[green]{item}[/green]")
        console.print(f"  {description}\n")


def show_current_status():
    """Show current Impact.com campaign status."""
    console.print("\n[bold cyan]═══ Current Status ═══[/bold cyan]\n")

    try:
        client = ImpactClient()

        # Test connection
        if not client.test_connection():
            console.print("[red]✗ Cannot connect to Impact.com API[/red]")
            console.print("[yellow]Check your credentials in .env[/yellow]")
            return

        # Get current campaigns
        campaigns = client.get_all_campaigns()

        console.print(f"[green]✓ Connected to Impact.com[/green]")
        console.print(f"[green]✓ Current campaigns: {len(campaigns)}[/green]\n")

        if campaigns:
            console.print("[bold]Active Campaigns:[/bold]")
            for camp in campaigns[:10]:  # Show first 10
                console.print(f"  • {camp['name']} ({camp.get('category', 'Unknown')})")

            if len(campaigns) > 10:
                console.print(f"  ... and {len(campaigns) - 10} more")
        else:
            console.print("[yellow]No active campaigns yet. Time to join some![/yellow]")

    except Exception as e:
        console.print(f"[red]Error checking status: {e}[/red]")


def show_goal_tracker():
    """Display goal tracking for campaign expansion."""
    console.print("\n[bold cyan]═══ Expansion Goals ═══[/bold cyan]\n")

    try:
        client = ImpactClient()
        campaigns = client.get_all_campaigns()
        current_count = len(campaigns)

        # Goals
        goals = [
            {"target": 150, "timeframe": "Week 1", "action": "Apply to 50 programs"},
            {"target": 200, "timeframe": "Week 2", "action": "Apply to 50 more programs"},
            {"target": 250, "timeframe": "Month 1", "action": "Reach 250 total programs"},
        ]

        console.print(f"[bold]Current: {current_count} campaigns[/bold]\n")

        for goal in goals:
            remaining = max(0, goal["target"] - current_count)
            progress = min(100, (current_count / goal["target"]) * 100)

            status = "✓" if current_count >= goal["target"] else "○"
            color = "green" if current_count >= goal["target"] else "yellow"

            console.print(f"[{color}]{status} {goal['timeframe']}:[/{color}] Target {goal['target']} ({goal['action']})")
            console.print(f"  Progress: {progress:.0f}% | Remaining: {remaining}\n")

    except Exception as e:
        console.print(f"[yellow]Could not fetch current count: {e}[/yellow]")


def show_quick_wins():
    """Display quick-win opportunities."""
    console.print("\n[bold cyan]═══ Quick Wins ═══[/bold cyan]\n")

    quick_wins = [
        {
            "category": "Auto-Approve Programs",
            "tip": "Look for programs with 'Auto-Approve' or 'Instant Approval' badges",
            "benefit": "Start promoting immediately"
        },
        {
            "category": "High Commission",
            "tip": "Filter by commission > 20%",
            "benefit": "Better revenue per conversion"
        },
        {
            "category": "Recurring Commissions",
            "tip": "Look for SaaS products with recurring payouts",
            "benefit": "Ongoing passive income"
        },
        {
            "category": "Free Trials",
            "tip": "Programs offering free trials convert better",
            "benefit": "Lower barrier for readers"
        }
    ]

    for win in quick_wins:
        console.print(f"[bold yellow]{win['category']}[/bold yellow]")
        console.print(f"  💡 {win['tip']}")
        console.print(f"  ✨ Benefit: {win['benefit']}\n")


def main():
    """Run the campaign expansion helper."""
    console.print(Panel.fit(
        "[bold cyan]Impact.com Campaign Expansion Helper[/bold cyan]\n"
        "Grow from 100 → 200+ affiliate programs",
        border_style="cyan"
    ))

    # Show all sections
    show_current_status()
    show_goal_tracker()
    show_recommended_programs()
    show_search_strategy()
    show_quick_wins()
    show_application_checklist()

    # Next steps
    console.print("\n" + "═" * 50)
    console.print(Panel.fit(
        "[bold green]Next Steps[/bold green]\n\n"
        "1. Log into Impact.com Marketplace\n"
        "2. Search for recommended programs above\n"
        "3. Apply to 10-20 high-priority programs\n"
        "4. Wait 1-3 days for approvals\n"
        "5. Run: python main.py sync-unified\n"
        "6. Repeat weekly until you reach 200+ programs!",
        border_style="green"
    ))


if __name__ == "__main__":
    main()
