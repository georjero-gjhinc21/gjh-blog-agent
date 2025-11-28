#!/usr/bin/env python3
"""Quick verification test for dual-network affiliate system."""

from agents.unified_affiliate_agent import UnifiedAffiliateAgent

def main():
    print("🔍 GJH Affiliate System - Quick Test\n" + "="*50)

    # Initialize agent
    print("\n1. Initializing agent...")
    agent = UnifiedAffiliateAgent()
    print("   ✓ Agent initialized")

    # Test connections
    print("\n2. Testing connections...")
    status = agent.test_connections()
    for network, connected in status.items():
        icon = "✓" if connected else "✗"
        print(f"   {icon} {network.capitalize()}: {'Connected' if connected else 'Failed'}")

    if not all(status.values()):
        print("\n❌ Connection failed. Check credentials.")
        return

    # Sync programs
    print("\n3. Syncing programs...")
    counts = agent.sync_all_programs()
    print(f"   ✓ PartnerStack: {counts['partnerstack']} programs")
    print(f"   ✓ Impact.com: {counts['impact']} programs")
    print(f"   ✓ Total: {counts['total']} programs")

    # Test search
    print("\n4. Testing search...")
    results = agent.search_programs("cybersecurity", limit=3)
    print(f"   ✓ Found {len(results)} cybersecurity programs:")
    for prog in results[:3]:
        print(f"      - {prog['name']} ({prog['network']})")

    # Test link generation
    print("\n5. Testing link generation...")
    if results:
        test_prog = results[0]
        link = agent.generate_link(test_prog['name'], sub_id="test")
        if link:
            print(f"   ✓ Generated link for {test_prog['name']}")
            print(f"      {link[:60]}...")
        else:
            print(f"   ✗ Link generation failed")

    # Get stats
    print("\n6. System statistics...")
    stats = agent.get_stats()
    print(f"   ✓ Networks: {stats['networks']['total']} programs total")
    print(f"   ✓ Categories: {len(stats['categories'])} different categories")

    print("\n" + "="*50)
    print("✅ All systems operational!\n")
    print(f"Your affiliate system has {counts['total']} programs ready to use.")
    print(f"PartnerStack: {counts['partnerstack']} | Impact.com: {counts['impact']}")

if __name__ == "__main__":
    main()
