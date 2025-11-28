#!/usr/bin/env python3
"""Main Demo Runner - Interactive Menu System"""
from colorama import Fore, Style, init
import sys
import subprocess

init(autoreset=True)

def print_banner():
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║                    A2P PROTOCOL DEMONSTRATION SUITE                         ║")
    print(f"║                   Agent-to-Payment with CallSign Gateway                    ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

def print_menu():
    print(f"{Fore.YELLOW}Select a demo mode:{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Quick Demo (Automated)")
    print(f"   → Fast-paced demonstration of all protocol phases")
    print(f"   → Shows legitimate transactions and security blocks")
    print(f"   → Duration: ~2 minutes\n")
    
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Interactive Demo (Step-by-step)")
    print(f"   → Press Enter to advance through each phase")
    print(f"   → Detailed security metrics and attack simulations")
    print(f"   → Duration: ~5-10 minutes (user-paced)\n")
    
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} Security Test Suite")
    print(f"   → Comprehensive automated security tests")
    print(f"   → Validates all security mechanisms")
    print(f"   → Duration: ~1 minute\n")
    
    print(f"{Fore.GREEN}4.{Style.RESET_ALL} Complete Walkthrough (All Demos)")
    print(f"   → Runs all demos in sequence")
    print(f"   → Best for presentations and full demonstrations")
    print(f"   → Duration: ~10-15 minutes\n")
    
    print(f"{Fore.GREEN}5.{Style.RESET_ALL} View Protocol Documentation")
    print(f"   → Display README with protocol details\n")
    
    print(f"{Fore.RED}0.{Style.RESET_ALL} Exit\n")

def run_script(script_name):
    """Run a Python script and handle errors"""
    try:
        result = subprocess.run([sys.executable, script_name], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n{Fore.RED}Error running {script_name}: {e}{Style.RESET_ALL}")
        return False
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Demo interrupted by user{Style.RESET_ALL}")
        return False

def show_documentation():
    """Display README content"""
    try:
        with open('README.md', 'r') as f:
            content = f.read()
            print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
            print(content)
            print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    except FileNotFoundError:
        print(f"{Fore.RED}README.md not found{Style.RESET_ALL}")

def main():
    while True:
        print_banner()
        print_menu()
        
        try:
            choice = input(f"{Fore.CYAN}Enter your choice (0-5): {Style.RESET_ALL}").strip()
            
            if choice == '0':
                print(f"\n{Fore.CYAN}Thank you for exploring the A2P Protocol!{Style.RESET_ALL}\n")
                sys.exit(0)
            
            elif choice == '1':
                print(f"\n{Fore.YELLOW}Starting Quick Demo...{Style.RESET_ALL}\n")
                run_script('demo.py')
                input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
            
            elif choice == '2':
                print(f"\n{Fore.YELLOW}Starting Interactive Demo...{Style.RESET_ALL}\n")
                run_script('interactive_demo.py')
                input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
            
            elif choice == '3':
                print(f"\n{Fore.YELLOW}Running Security Test Suite...{Style.RESET_ALL}\n")
                run_script('security_tests.py')
                input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
            
            elif choice == '4':
                print(f"\n{Fore.YELLOW}Starting Complete Walkthrough...{Style.RESET_ALL}\n")
                print(f"{Fore.CYAN}Part 1: Quick Demo{Style.RESET_ALL}")
                run_script('demo.py')
                input(f"\n{Fore.YELLOW}Press Enter to continue to Interactive Demo...{Style.RESET_ALL}")
                
                print(f"\n{Fore.CYAN}Part 2: Interactive Demo{Style.RESET_ALL}")
                run_script('interactive_demo.py')
                input(f"\n{Fore.YELLOW}Press Enter to continue to Security Tests...{Style.RESET_ALL}")
                
                print(f"\n{Fore.CYAN}Part 3: Security Test Suite{Style.RESET_ALL}")
                run_script('security_tests.py')
                
                print(f"\n{Fore.GREEN}✓ Complete walkthrough finished!{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
            
            elif choice == '5':
                show_documentation()
                input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
            
            else:
                print(f"\n{Fore.RED}Invalid choice. Please enter 0-5.{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.CYAN}Thank you for exploring the A2P Protocol!{Style.RESET_ALL}\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
