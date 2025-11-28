#!/usr/bin/env python3
"""Batch generate multiple blog posts with affiliate products."""
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from database import get_db_session
from agents import ResearchAgent, AffiliateAgent, ContentAgent, PublishingAgent

console = Console()

def batch_generate_posts(num_posts: int = 15):
    """Generate multiple blog posts with affiliate products."""
    console.print(f"[bold blue]Generating {num_posts} blog posts with affiliate products...[/bold blue]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        with get_db_session() as db:
            research_agent = ResearchAgent()
            affiliate_agent = AffiliateAgent()
            content_agent = ContentAgent()
            publishing_agent = PublishingAgent()

            # First, discover plenty of topics
            task = progress.add_task(f"[cyan]Discovering {num_posts * 2} topics...", total=None)
            topics = research_agent.discover_topics(db, max_topics=num_posts * 2)
            progress.update(task, completed=True)
            console.print(f"✓ Discovered {len(topics)} topics\n")

            # Generate posts
            successful = 0
            failed = 0

            for i in range(num_posts):
                console.print(f"[bold cyan]Post {i+1}/{num_posts}[/bold cyan]")

                try:
                    # Get unused topic
                    task = progress.add_task(f"[cyan]Selecting topic...", total=None)
                    topic = research_agent.get_unused_topic(db)
                    if not topic:
                        progress.update(task, completed=True)
                        console.print("[yellow]✗ No more topics available[/yellow]\n")
                        break
                    progress.update(task, completed=True)
                    console.print(f"  Topic: {topic.title[:60]}...")

                    # Match affiliate product
                    task = progress.add_task(f"[cyan]Matching affiliate product...", total=None)
                    affiliate_product = affiliate_agent.match_product_to_topic(db, topic)
                    progress.update(task, completed=True)
                    if affiliate_product:
                        console.print(f"  Product: {affiliate_product.name} ({affiliate_product.commission_rate}%)")
                    else:
                        console.print("  Product: None")

                    # Generate content
                    task = progress.add_task(f"[cyan]Generating content...", total=None)
                    post = content_agent.generate_post(db, topic, affiliate_product)
                    progress.update(task, completed=True)
                    console.print(f"  Generated: {post.word_count} words")

                    # Mark topic as used
                    research_agent.mark_topic_used(db, topic.id)

                    # Publish
                    task = progress.add_task(f"[cyan]Publishing...", total=None)
                    success = publishing_agent.publish_post(db, post)
                    progress.update(task, completed=True)

                    if success:
                        console.print(f"  [green]✓ Published: {post.vercel_url}[/green]\n")
                        successful += 1
                    else:
                        console.print(f"  [red]✗ Publishing failed[/red]\n")
                        failed += 1

                except Exception as e:
                    console.print(f"  [red]✗ Error: {e}[/red]\n")
                    failed += 1
                    continue

            # Summary
            console.print(f"\n[bold green]✓ Batch generation complete![/bold green]")
            console.print(f"Successful: {successful}")
            console.print(f"Failed: {failed}")

if __name__ == "__main__":
    batch_generate_posts(15)
