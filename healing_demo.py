#!/usr/bin/env python3
"""
Demo script showing Playwright test healing in action.

This script demonstrates:
1. Running a test that works on the original page
2. Switching to a modified page where selectors fail
3. Using LLM-powered healing to fix the test
"""

import os
import json
import shutil
from test_runner import PlaywrightTestRunner

def run_healing_demo():
    """Run the complete healing demonstration"""
    
    print("🎭 Playwright Test Healing Demo")
    print("=" * 50)
    
    # Paths
    test_file = "/Users/aarij.hussaan/development/ollama_tester/demo_test.json"
    original_url = "http://localhost:8080/demo_page_original.html"
    modified_url = "http://localhost:8080/demo_page_modified.html"
    
    # Step 1: Test with original page (should pass)
    print("\n📋 Step 1: Running test on ORIGINAL page")
    print("-" * 40)
    
    runner = PlaywrightTestRunner(test_file)
    print(f"✅ Test loaded: {runner.test_data['name']}")
    print(f"📄 Target URL: {runner.test_data['url']}")
    
    print("\n🚀 Executing test...")
    runner.run_test()
    
    import time
    print("\n⏳ Waiting 3 seconds so you can see the original page...")
    time.sleep(3)
    
    input("\n⏸️  Press Enter to continue to Step 2...")
    
    # Step 2: Switch to modified page and show failure
    print("\n📋 Step 2: Switching to MODIFIED page (selectors will fail)")
    print("-" * 40)
    
    # Update test file to point to modified page
    with open(test_file, 'r') as f:
        test_data = json.load(f)
    
    test_data['url'] = modified_url
    
    with open(test_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"🔄 Updated test URL to: {test_data['url']}")
    
    # Run test again (should fail and heal)
    print("\n🚀 Executing test with healing...")
    runner = PlaywrightTestRunner(test_file)
    runner.run_test()
    
    print("\n📋 Step 3: Checking healed test file")
    print("-" * 40)
    
    # Show the updated selectors
    with open(test_file, 'r') as f:
        healed_data = json.load(f)
    
    print("🔧 Healed selectors:")
    for i, step in enumerate(healed_data['steps']):
        original_selector = step['selectors'][1] if len(step['selectors']) > 1 else step['selectors'][0]
        healed_selector = step['selectors'][0]
        
        if healed_selector != original_selector:
            print(f"  Step {i+1}: {step['description']}")
            print(f"    Original: {original_selector}")
            print(f"    Healed:   {healed_selector}")
    
    # Step 4: Restore original test file
    print("\n📋 Step 4: Restoring original test configuration")
    print("-" * 40)
    
    test_data['url'] = original_url
    with open(test_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print("✅ Demo completed! Test file restored to original state.")
    print("\n💡 Key takeaways:")
    print("   • Original selectors failed on modified page")
    print("   • LLM analyzed DOM and suggested new selectors")
    print("   • Test was automatically healed and continued")
    print("   • Healed selectors were saved for future runs")

if __name__ == "__main__":
    # Check if Ollama is running
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Ollama is not running. Please start Ollama first:")
            print("   ollama serve")
            exit(1)
    except:
        print("❌ Cannot connect to Ollama. Please ensure it's running:")
        print("   ollama serve")
        exit(1)
    
    run_healing_demo()