#!/usr/bin/env python3
"""GJH Consulting Blog Agent - Main CLI."""
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

from database import init_db, get_db_session
from agents import (
    ResearchAgent,
    AffiliateAgent,
    ContentAgent,
    PublishingAgent,
    MonitoringAgent
)
from agents.unified_affiliate_agent import UnifiedAffiliateAgent
from models.blog import BlogPost
import models.blog as models

app = typer.Typer(help="GJH Consulting Autonomous Blog Generation System")
console = Console()


@app.command()
def init():
    """Initialize the database and seed sample data."""
    console.print("[bold blue]Initializing GJH Blog Agent...[/bold blue]")

    # Initialize database
    console.print("Creating database tables...")
    init_db()
    console.print("✓ Database initialized")

    # Seed affiliate products
    with get_db_session() as db:
        console.print("Seeding sample affiliate products...")
        affiliate_agent = AffiliateAgent()
        affiliate_agent.seed_sample_products(db)
        console.print("✓ Affiliate products seeded")

    console.print("[bold green]✓ Initialization complete![/bold green]")


@app.command()
def discover(max_topics: int = 10):
    """Discover new trending topics."""
    console.print(f"[bold blue]Discovering up to {max_topics} topics...[/bold blue]")

    with get_db_session() as db:
        research_agent = ResearchAgent()
        topics = research_agent.discover_topics(db, max_topics=max_topics)

        if topics:
            table = Table(title="Discovered Topics")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="white")
            table.add_column("Score", style="green")
            table.add_column("Keywords", style="yellow")

            for topic in topics:
                keywords = ", ".join(topic.keywords[:3]) if topic.keywords else ""
                table.add_row(
                    str(topic.id),
                    topic.title[:60],
                    f"{topic.trend_score:.2f}",
                    keywords
                )

            console.print(table)
            console.print(f"[bold green]✓ Discovered {len(topics)} topics[/bold green]")
        else:
            console.print("[yellow]No new topics discovered[/yellow]")


@app.command()
def generate():
    """Generate a new blog post with dual-network affiliate matching."""
    console.print("[bold blue]Generating new blog post...[/bold blue]")

    with get_db_session() as db:
        # Initialize agents
        research_agent = ResearchAgent()

        # Initialize unified affiliate agent for dual-network matching
        console.print("Initializing dual-network affiliate system...")
        unified_affiliate = UnifiedAffiliateAgent()
        try:
            unified_affiliate.sync_all_programs()
            counts = unified_affiliate.get_stats()["networks"]
            console.print(f"✓ Loaded {counts['partnerstack']} PartnerStack + {counts['impact']} Impact.com programs")
        except Exception as e:
            console.print(f"[yellow]Warning: Affiliate sync failed: {e}[/yellow]")
            unified_affiliate = None

        content_agent = ContentAgent(unified_affiliate_agent=unified_affiliate)

        # Get topic
        console.print("Selecting topic...")
        topic = research_agent.get_unused_topic(db)
        if not topic:
            console.print("[red]✗ No unused topics available. Run 'discover' first.[/red]")
            return

        console.print(f"✓ Topic: [cyan]{topic.title}[/cyan]")

        # Generate content with unified affiliate matching
        console.print("Generating content with intelligent affiliate matching...")
        post = content_agent.generate_post(
            db,
            topic,
            use_unified_affiliates=True,
            max_affiliate_matches=3
        )

        # Mark topic as used
        research_agent.mark_topic_used(db, topic.id)

        # Display result with affiliate info
        affiliate_info = ""
        if post.metadata and "affiliate_matches" in post.metadata:
            matches = post.metadata["affiliate_matches"]
            affiliate_info = f"\n[bold]Affiliate Matches:[/bold] {len(matches)} programs"
            for match in matches:
                affiliate_info += f"\n  • {match['name']} ({match['network']}) - Score: {match['score']:.2f}"

        panel = Panel(
            f"""[bold]Title:[/bold] {post.title}
[bold]Slug:[/bold] {post.slug}
[bold]Word Count:[/bold] {post.word_count}
[bold]Status:[/bold] {post.status}

[bold]Excerpt:[/bold]
{post.excerpt}

[bold]Keywords:[/bold] {", ".join(post.seo_keywords[:5])}{affiliate_info}
""",
            title="Generated Blog Post",
            border_style="green"
        )
        console.print(panel)
        console.print(f"[bold green]✓ Post #{post.id} created successfully![/bold green]")


@app.command()
def publish(post_id: int):
    """Publish a blog post."""
    console.print(f"[bold blue]Publishing post #{post_id}...[/bold blue]")

    with get_db_session() as db:
        post = db.query(BlogPost).filter_by(id=post_id).first()
        if not post:
            console.print(f"[red]✗ Post #{post_id} not found[/red]")
            return

        publishing_agent = PublishingAgent()
        success = publishing_agent.publish_post(db, post)

        if success:
            console.print(f"[bold green]✓ Published: {post.vercel_url}[/bold green]")
        else:
            console.print("[red]✗ Publishing failed[/red]")


@app.command()
def list_posts(status: Optional[str] = None, limit: int = 20):
    """List blog posts."""
    with get_db_session() as db:
        query = db.query(BlogPost)

        if status:
            query = query.filter_by(status=status)

        posts = query.order_by(BlogPost.created_at.desc()).limit(limit).all()

        if posts:
            table = Table(title=f"Blog Posts ({status or 'all'})")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="white")
            table.add_column("Status", style="yellow")
            table.add_column("Word Count", style="green")
            table.add_column("Created", style="blue")

            for post in posts:
                table.add_row(
                    str(post.id),
                    post.title[:50],
                    post.status,
                    str(post.word_count),
                    post.created_at.strftime("%Y-%m-%d")
                )

            console.print(table)
        else:
            console.print("[yellow]No posts found[/yellow]")


@app.command()
def stats():
    """Show performance statistics."""
    console.print("[bold blue]Generating performance report...[/bold blue]\n")

    with get_db_session() as db:
        monitoring_agent = MonitoringAgent()

        # Get summary
        summary = monitoring_agent.get_performance_summary(db, days=30)

        # Create summary panel
        summary_panel = Panel(
            f"""[bold cyan]30-Day Performance Summary[/bold cyan]

Total Posts Published: [green]{summary['total_posts']}[/green]
Total Page Views: [green]{summary['total_views']:,}[/green]
Total Affiliate Clicks: [green]{summary['total_affiliate_clicks']}[/green]
Total Revenue: [green]${summary['total_revenue']:.2f}[/green]

Avg Views per Post: [yellow]{summary['avg_views_per_post']:.0f}[/yellow]
Avg Revenue per Post: [yellow]${summary['avg_revenue_per_post']:.2f}[/yellow]
Click-Through Rate: [yellow]{summary['click_through_rate']:.2f}%[/yellow]
""",
            border_style="blue"
        )
        console.print(summary_panel)

        # Top posts
        top_posts = monitoring_agent.get_top_performing_posts(db, limit=5)
        if top_posts:
            console.print("\n[bold cyan]Top 5 Posts by Traffic[/bold cyan]")
            for i, post in enumerate(top_posts, 1):
                console.print(f"{i}. {post['title'][:60]} - {post['views']:,} views")

        # Revenue posts
        revenue_posts = monitoring_agent.get_top_revenue_posts(db, limit=5)
        if revenue_posts:
            console.print("\n[bold cyan]Top 5 Posts by Revenue[/bold cyan]")
            for i, post in enumerate(revenue_posts, 1):
                console.print(f"{i}. {post['title'][:60]} - ${post['revenue']:.2f}")


@app.command()
def workflow():
    """Run complete blog generation workflow (discover → generate → publish)."""
    console.print("[bold blue]Running complete blog generation workflow...[/bold blue]\n")

    with get_db_session() as db:
        # 1. Discover topics
        console.print("[1/4] Discovering topics...")
        research_agent = ResearchAgent()
        topics = research_agent.discover_topics(db, max_topics=5)
        console.print(f"✓ Discovered {len(topics)} topics\n")

        # 2. Get best topic
        console.print("[2/4] Selecting best topic...")
        topic = research_agent.get_unused_topic(db)
        if not topic:
            console.print("[red]✗ No topics available[/red]")
            return
        console.print(f"✓ Selected: {topic.title}\n")

        # 3. Generate post
        console.print("[3/4] Generating blog post...")
        affiliate_agent = AffiliateAgent()
        content_agent = ContentAgent()

        affiliate_product = affiliate_agent.match_product_to_topic(db, topic)
        post = content_agent.generate_post(db, topic, affiliate_product)
        research_agent.mark_topic_used(db, topic.id)

        # Enhance generated post with affiliate links
        try:
            from utils.blog_affiliate_integration import BlogAffiliateIntegration
            integrator = BlogAffiliateIntegration()
            result = integrator.enhance_post(
                title=post.title,
                content=post.content,
                slug=post.slug
            )
            enhanced_content = result.get('content', post.content)
            post.content = enhanced_content
            console.print(f"✓ Added {result.get('affiliate_count', 0)} affiliate links to post")
        except Exception as e:
            console.print(f"[yellow]Warning: Affiliate integration failed: {e}[/yellow]")

        # Attempt to auto-fix known broken links in generated post
        try:
            from utils.link_fixer import fix_links_in_post, validate_links_in_post
            # Create post file so fixer can operate on a consistent path
            publishing_agent = PublishingAgent()
            post_file = publishing_agent._create_post_file(post)

            fixed_count = fix_links_in_post(str(post_file))
            if fixed_count:
                # reload fixed content into post
                post.content = post_file.read_text()
                # update DB
                db.commit()
                console.print(f"[green]✓ Auto-fixed {fixed_count} links in post[/green]")

            # Validate links
            broken = validate_links_in_post(str(post_file))
            if broken:
                console.print(f"[yellow]Warning: {len(broken)} links still broken after auto-fix[/yellow]")
                for u, code in broken:
                    console.print(f"  - {u} -> {code}")
        except Exception as e:
            console.print(f"[yellow]Warning: Link fixer failed: {e}[/yellow]")

        console.print(f"✓ Generated: {post.title} ({post.word_count} words)\n")

        # 4. Publish
        console.print("[4/4] Publishing post...")
        publishing_agent = PublishingAgent()
        success = publishing_agent.publish_post(db, post)

        if success:
            console.print(f"\n[bold green]✓ Workflow complete![/bold green]")
            console.print(f"Published: {post.vercel_url}")
        else:
            console.print("\n[red]✗ Publishing failed[/red]")


@app.command()
def add_product(
    name: str,
    description: str,
    category: str,
    affiliate_link: str,
    commission_rate: float = 0.0
):
    """Add a new affiliate product."""
    with get_db_session() as db:
        affiliate_agent = AffiliateAgent()
        product = affiliate_agent.add_product(
            db,
            name=name,
            description=description,
            category=category,
            affiliate_link=affiliate_link,
            commission_rate=commission_rate
        )

        console.print(f"[bold green]✓ Added product: {product.name}[/bold green]")


@app.command()
def enqueue_affiliate_integration(limit: int = 0):
    """Enqueue background task to integrate affiliates into posts.

    limit: optional number of posts to process (0 = all)
    """
    try:
        from tasks.integrate_affiliates import integrate_affiliates_task
        job = integrate_affiliates_task.delay(limit)
        console.print(f"[green]✓ Enqueued affiliate integration task: {job.id}[/green]")
    except Exception as e:
        console.print(f"[red]✗ Failed to enqueue task: {e}[/red]")


@app.command()
def test_partnerstack():
    """Test PartnerStack API connection."""
    console.print("[bold blue]Testing PartnerStack connection...[/bold blue]")

    try:
        from utils.partnerstack_client import PartnerStackClient

        client = PartnerStackClient()
        if client.test_connection():
            console.print("[green]✓ Successfully connected to PartnerStack API[/green]")

            programs = client.get_all_programs()
            console.print(f"[green]✓ Found {len(programs)} active programs[/green]")

            if programs:
                console.print("\n[bold]Sample programs:[/bold]")
                for prog in programs[:5]:
                    console.print(f"  - {prog['name']} ({prog['category']})")
        else:
            console.print("[red]✗ Connection failed - check your API key[/red]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def sync_partnerstack(program: Optional[str] = None):
    """Sync PartnerStack programs to database."""
    console.print("[bold blue]Syncing PartnerStack programs...[/bold blue]")

    try:
        from utils.partnerstack_client import PartnerStackClient

        client = PartnerStackClient()
        programs = client.get_all_programs()

        if not programs:
            console.print("[yellow]No programs found[/yellow]")
            return

        with get_db_session() as db:
            affiliate_agent = AffiliateAgent()
            imported = 0

            for prog in programs:
                # Check if already exists
                existing = db.query(models.AffiliateProduct).filter_by(
                    name=prog['name']
                ).first()

                if not existing:
                    # Use real affiliate URL from PartnerStack API
                    affiliate_link = prog.get('affiliate_url', prog.get('base_url', ''))

                    # Import program
                    affiliate_agent.add_product(
                        db,
                        name=prog['name'],
                        description=prog['description'],
                        category=prog['category'],
                        affiliate_link=affiliate_link,
                        commission_rate=prog['commission_rate'],
                        relevance_keywords=prog['keywords']
                    )
                    imported += 1

                    console.print(f"  ✓ {prog['name']} ({prog['category']}) - {prog['commission_rate']}%")

            console.print(f"\n[bold green]✓ Imported {imported} programs[/bold green]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def list_affiliates(category: str = None, limit: int = 20, sort_by: str = "name"):
    """List affiliate programs.

    sort_by: 'name' (default) or 'commission'
    """
    with get_db_session() as db:
        query = db.query(models.AffiliateProduct).filter_by(active=True)

        if category:
            query = query.filter_by(category=category)

        # Robust ordering: some test mocks may not provide SQLAlchemy Column objects
        if sort_by == "commission":
            col = getattr(models.AffiliateProduct, 'commission_rate', None)
        else:
            col = getattr(models.AffiliateProduct, 'name', None)

        if col is None:
            # fallback: order by the model (no-op for our test QueryMock)
            query = query.order_by(models.AffiliateProduct)
        else:
            # if column supports .desc(), prefer that for commission sorting
            if sort_by == "commission" and hasattr(col, 'desc'):
                try:
                    query = query.order_by(col.desc())
                except Exception:
                    query = query.order_by(col)
            else:
                query = query.order_by(col)

        programs = query.limit(limit).all()

        if programs:
            table = Table(title=f"Affiliate Programs ({category or 'all'})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="white")
            table.add_column("Category", style="yellow")
            table.add_column("Commission", style="green")

            for prog in programs:
                table.add_row(
                    str(prog.id),
                    prog.name,
                    prog.category,
                    f"{prog.commission_rate}%"
                )

            console.print(table)
        else:
            console.print("[yellow]No programs found[/yellow]")


@app.command()
def search_affiliates(query: str, limit: int = 10):
    """Search affiliate programs by keyword."""
    console.print(f"[bold blue]Searching for: {query}[/bold blue]\n")

    try:
        from utils.partnerstack_client import PartnerStackClient

        client = PartnerStackClient()
        results = client.search_programs(query, limit)

        if results:
            for prog in results:
                console.print(f"[bold]{prog['name']}[/bold] ({prog['category']})")
                console.print(f"  {prog['description'][:100]}...")
                console.print(f"  Commission: [green]{prog['commission_rate']}%[/green]\n")
        else:
            console.print("[yellow]No matching programs found[/yellow]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def generate_affiliate_link(program_key: str, path: Optional[str] = None):
    """Generate an affiliate link for a program."""
    try:
        from utils.partnerstack_client import PartnerStackClient

        client = PartnerStackClient()
        link = client.generate_affiliate_link(program_key, path)

        console.print(f"[bold]Affiliate Link:[/bold]")
        console.print(f"[cyan]{link}[/cyan]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def test_unified():
    """Test unified affiliate system (PartnerStack + Impact.com)."""
    console.print("[bold blue]Testing Unified Affiliate System...[/bold blue]\n")

    try:
        from agents.unified_affiliate_agent import UnifiedAffiliateAgent

        agent = UnifiedAffiliateAgent()
        status = agent.test_connections()

        for network, connected in status.items():
            icon = "✓" if connected else "✗"
            color = "green" if connected else "red"
            console.print(f"[{color}]{icon} {network.capitalize()}: {'Connected' if connected else 'Failed'}[/{color}]")

        if all(status.values()):
            console.print("\n[bold green]✓ All networks operational![/bold green]")
        else:
            console.print("\n[yellow]⚠ Some connections failed. Check credentials.[/yellow]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def sync_unified():
    """Sync programs from both PartnerStack and Impact.com."""
    console.print("[bold blue]Syncing from all networks...[/bold blue]\n")

    try:
        from agents.unified_affiliate_agent import UnifiedAffiliateAgent

        agent = UnifiedAffiliateAgent()
        counts = agent.sync_all_programs()

        console.print(f"[green]✓ PartnerStack: {counts['partnerstack']} programs[/green]")
        console.print(f"[green]✓ Impact.com: {counts['impact']} programs[/green]")
        console.print(f"\n[bold green]✓ Total: {counts['total']} programs loaded[/bold green]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def search_unified(query: str, limit: int = 10):
    """Search affiliate programs across all networks."""
    console.print(f"[bold blue]Searching all networks for: {query}[/bold blue]\n")

    try:
        from agents.unified_affiliate_agent import UnifiedAffiliateAgent

        agent = UnifiedAffiliateAgent()
        results = agent.search_programs(query, limit)

        if results:
            table = Table(title=f"Search Results: '{query}'")
            table.add_column("Name", style="cyan")
            table.add_column("Network", style="magenta")
            table.add_column("Category", style="yellow")
            table.add_column("Commission", style="green")

            for prog in results:
                network_display = prog.get('network', 'unknown')
                table.add_row(
                    prog['name'],
                    network_display,
                    prog.get('category', 'N/A'),
                    f"{prog.get('commission_rate', 0):.1f}%"
                )

            console.print(table)
            console.print(f"\n[green]Found {len(results)} programs[/green]")
        else:
            console.print("[yellow]No matching programs found[/yellow]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def link_unified(program_name: str, sub_id: Optional[str] = None):
    """Generate affiliate link for a program (auto-detects network)."""
    console.print(f"[bold blue]Generating link for: {program_name}[/bold blue]\n")

    try:
        from agents.unified_affiliate_agent import UnifiedAffiliateAgent

        agent = UnifiedAffiliateAgent()
        link = agent.generate_link(program_name, sub_id=sub_id)

        if link:
            console.print(f"[bold]Affiliate Link:[/bold]")
            console.print(f"[cyan]{link}[/cyan]")
        else:
            console.print(f"[red]✗ Program '{program_name}' not found[/red]")
            console.print("[yellow]Try searching first: python main.py search-unified <keyword>[/yellow]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def stats_unified():
    """Show unified affiliate system statistics."""
    console.print("[bold blue]Unified Affiliate System Statistics[/bold blue]\n")

    try:
        from agents.unified_affiliate_agent import UnifiedAffiliateAgent

        agent = UnifiedAffiliateAgent()
        stats = agent.get_stats()

        # Network distribution
        console.print("[bold cyan]Network Distribution:[/bold cyan]")
        for network, count in stats['networks'].items():
            if network != 'total':
                console.print(f"  {network.capitalize()}: {count}")
        console.print(f"  [bold]Total: {stats['networks']['total']}[/bold]\n")

        # Top categories
        console.print("[bold cyan]Top Categories:[/bold cyan]")
        for i, (category, count) in enumerate(list(stats['categories'].items())[:10], 1):
            console.print(f"  {i}. {category}: {count}")

        # Top commission programs
        if stats.get('top_commission_programs'):
            console.print("\n[bold cyan]Top Commission Programs:[/bold cyan]")
            for i, prog in enumerate(stats['top_commission_programs'][:5], 1):
                console.print(f"  {i}. {prog['name']} ({prog['network']}): {prog['commission']:.1f}%")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def match_content(title: str, content: Optional[str] = None, max_matches: int = 3):
    """Find best affiliate matches for content."""
    console.print("[bold blue]Finding affiliate matches...[/bold blue]\n")

    try:
        from agents.unified_affiliate_agent import UnifiedAffiliateAgent

        agent = UnifiedAffiliateAgent()
        matches = agent.find_best_matches(
            content=content or title,
            title=title,
            max_matches=max_matches
        )

        if matches:
            table = Table(title=f"Top {len(matches)} Matches")
            table.add_column("Program", style="cyan")
            table.add_column("Network", style="magenta")
            table.add_column("Score", style="green")
            table.add_column("Commission", style="yellow")

            for match in matches:
                table.add_row(
                    match['name'],
                    match.get('network', 'N/A'),
                    f"{match.get('match_score', 0):.2f}",
                    f"{match.get('commission_rate', 0):.1f}%"
                )

            console.print(table)
        else:
            console.print("[yellow]No relevant matches found[/yellow]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def version():
    """Show version information."""
    console.print(Panel(
        """[bold cyan]GJH Consulting Blog Agent[/bold cyan]
Version: 1.0.0
Author: GJH Consulting
Description: Autonomous blog generation system with AI agents

Components:
- Research Agent: Topic discovery
- Affiliate Agent: Product matching
- Content Agent: Blog generation
- Publishing Agent: Vercel deployment
- Monitoring Agent: Analytics tracking

Affiliate Networks:
- PartnerStack: 70+ programs
- Impact.com: 100+ campaigns
- Unified Agent: AI-powered matching

Infrastructure:
- PostgreSQL: Data storage
- Redis: Task queue
- Milvus: Vector database
- Celery: Job scheduling
- Ollama: Local LLM (llama3.1:8b)
""",
        title="About",
        border_style="cyan"
    ))


if __name__ == "__main__":
    app()
