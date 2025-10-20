#!/usr/bin/env python3

import sys
import time
from mobile_agent import MobileAgent

def print_banner():
    print("=" * 60)
    print("🏦 SecureBank AI Agent - Purchase Demo")
    print("=" * 60)

def print_products(results):
    """Display search results"""
    print("\n📋 Search Results:")
    for merchant, products in results.items():
        if products:
            print(f"\n{merchant.upper()}:")
            for i, product in enumerate(products, 1):
                print(f"  {i}. {product.name} - ${product.price}")
                print(f"     {product.description}")

def main():
    print_banner()
    
    # Initialize agent
    agent = MobileAgent()
    
    # Step 1: Authentication
    print("\n🔐 Step 1: User Authentication")
    if not agent.authenticate_user():
        print("❌ Authentication failed")
        return
    
    time.sleep(1)
    
    # Step 2: User request
    print(f"\n👤 User: 'I need a laptop for work under $2000'")
    print("📱 Agent: 'Let me search across all retailers for you...'")
    
    time.sleep(1)
    
    # Step 3: Multi-retailer search
    print("\n🛍️ Step 2: Multi-Retailer Product Search")
    results = agent.search_products("laptop", 2000.0)
    print_products(results)
    
    time.sleep(2)
    
    # Step 4: AI recommendation
    print("\n🤖 Step 3: AI Analysis & Recommendation")
    recommended = agent.recommend_product(results)
    
    if not recommended:
        print("❌ No products found matching criteria")
        return
    
    print(f"📱 Agent: 'Based on value analysis, I recommend:'")
    print(f"   🏆 {recommended.name} - ${recommended.price} from {recommended.merchant.upper()}")
    print(f"   📝 {recommended.description}")
    
    time.sleep(2)
    
    # Step 5: User confirmation
    print(f"\n👤 User: 'Yes, buy the {recommended.name}'")
    
    # Step 6: Purchase execution
    print("\n💳 Step 4: Secure Purchase Execution")
    result = agent.purchase_product(recommended)
    
    if 'error' in result:
        print(f"❌ Purchase failed: {result['error']}")
        return
    
    # Step 7: Success confirmation
    print(f"\n🎉 Purchase Complete!")
    print(f"✅ {result['product'].name} ordered from {result['product'].merchant.upper()}")
    print(f"💰 Amount: ${result['product'].price}")
    print(f"📦 Order ID: {result['order_id']}")
    print(f"🧾 Transaction Ref: {result['txn_ref']}")
    print(f"🚚 Bank-verified payment = Expedited processing!")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully! 🎊")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)