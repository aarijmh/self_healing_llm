#!/usr/bin/env python3
"""
Complete demo runner that starts server and runs healing demo
"""

import time
import subprocess
import sys
from simple_server import DemoServer
from healing_demo import run_healing_demo

def main():
    print("🎭 Playwright Test Healing - Complete Demo")
    print("=" * 50)
    
    # Start the demo server
    server = DemoServer(port=8080)
    
    try:
        server.start()
        
        print("\n📋 Demo pages available at:")
        print("   Original: http://localhost:8080/demo_page_original.html")
        print("   Modified: http://localhost:8080/demo_page_modified.html")
        
        input("\n⏸️  Press Enter to start the healing demo...")
        
        # Run the healing demonstration
        run_healing_demo()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
    finally:
        server.stop()

if __name__ == "__main__":
    main()