#!/usr/bin/env python3

from test_runner import PlaywrightTestRunner
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <test_file.json>")
        sys.exit(1)
    
    test_file = sys.argv[1]
    
    print(f"🚀 Running test: {test_file}")
    print("📋 Selector healing enabled with Ollama")
    
    runner = PlaywrightTestRunner(test_file)
    runner.run_test()
    
    print("✅ Test execution completed")

if __name__ == "__main__":
    main()