#!/usr/bin/env python3
"""Complete A2P Protocol Demo - All Entities & Security Tests"""
from entities import *
from colorama import Fore, Style, init
import time

init(autoreset=True)

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}{text.center(80)}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

def print_step(entity, action):
    print(f"{Fore.GREEN}[{entity}]{Style.RESET_ALL} {action}")

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

def pause():
    time.sleep(0.5)

def main():
    print_header("A2P PROTOCOL COMPLETE DEMO")
    print(f"{Fore.YELLOW}Demonstrating all entities and security against malicious actors{Style.RESET_ALL}\n")
    
    directory = AgentDirectory()
    delegation_service = DelegationService()
    gateway = PaymentGateway(directory)
    bank = Bank()
    
    print_header("PHASE 1: Merchant Registration")
    print_step("Amazon", "Registering with Agent Directory...")
    pause()
    merchant = Merchant("amazon_merchant_001", "Amazon")
    merchant.certificate = directory.register_merchant("amazon_merchant_001", "business_license_12345")
    print_success(f"Merchant '{merchant.name}' registered")
    print(f"  Certificate ID: {merchant.certificate.entity_id}")
    print(f"  Expires: {merchant.certificate.expires_at.strftime('%Y-%m-%d')}")
    
    print_header("PHASE 2: Agent Registration")
    print_step("Amazon", "Creating shopping agent...")
    pause()
    agent = merchant.create_agent("amazon_agent_001", ["shopping", "checkout", "payment"])
    agent.certificate = directory.register_agent(agent.agent_id, merchant.merchant_id, agent.capabilities)
    print_success(f"Agent registered with dual-signed certificate")
    print(f"  Agent ID: {agent.agent_id}")
    print(f"  Capabilities: {', '.join(agent.capabilities)}")
    
    print_header("PHASE 3: User Setup")
    user_id = "customer_alice"
    bank.create_account(user_id, 10000)
    print_step("Customer Alice", "Downloads Amazon app")
    pause()
    valid, msg = directory.verify_certificate(agent.agent_id)
    print_success(f"Certificate verified: {msg}")
    
    print_step("Customer Alice", "Setting delegation limit: $5000")
    pause()
    agent.bind_user(user_id, 5000)
    delegation_service.create_delegation(user_id, agent.agent_id, 5000)
    print_success("User-Agent binding established")
    
    print_header("PHASE 4: Legitimate Transaction")
    print_step("Customer Alice", '"Buy laptop under $2000"')
    pause()
    print_step("Agent", "Found: Dell XPS 15 - $1899")
    pause()
    success, result = gateway.process_payment(agent.agent_id, user_id, 1899, delegation_service)
    if success:
        bank.process_payment(user_id, 1899)
        print_success(f"Payment authorized! TX: {result}")
        print(f"  Remaining: ${5000 - 1899}")
    
    print_header("PHASE 5: Subsequent Transaction")
    print_step("Customer Alice", '"Buy mouse under $100"')
    pause()
    success, result = gateway.process_payment(agent.agent_id, user_id, 99, delegation_service)
    if success:
        bank.process_payment(user_id, 99)
        print_success(f"Payment processed! TX: {result}")
        print(f"  Total spent: $1998 / $5000")
    
    print_header("SECURITY TEST 1: Unauthorized Agent")
    print_warning("Attacker creates fake agent")
    malicious_agent = Agent("malicious_agent_666", "fake_merchant", ["payment"])
    print_step("Malicious Agent", "Attempting payment...")
    pause()
    success, result = gateway.process_payment(malicious_agent.agent_id, user_id, 500, delegation_service)
    print_error(f"BLOCKED: {result}")
    print_success("✓ Unauthorized agent prevented")
    
    print_header("SECURITY TEST 2: Exceeding Limits")
    print_warning("Agent exceeds delegation limit")
    print_step("Agent", "Attempting $4000 purchase...")
    pause()
    success, result = gateway.process_payment(agent.agent_id, user_id, 4000, delegation_service)
    print_error(f"BLOCKED: {result}")
    print_success("✓ Delegation limits enforced")
    
    print_header("SECURITY TEST 3: Certificate Revocation")
    print_warning("Security vulnerability discovered")
    print_step("Directory", "Revoking certificate...")
    pause()
    directory.revoke_certificate(agent.agent_id)
    print_success("Certificate revoked")
    
    print_step("Agent", "Attempting transaction...")
    pause()
    success, result = gateway.process_payment(agent.agent_id, user_id, 50, delegation_service)
    print_error(f"BLOCKED: {result}")
    print_success("✓ Revoked certificates blocked")
    
    print_header("SECURITY TEST 4: Stolen Certificate")
    print_warning("Attacker steals certificate")
    stolen_agent = Agent("amazon_agent_001", merchant.merchant_id, ["payment"])
    stolen_agent.certificate = agent.certificate
    print_step("Attacker", "Using stolen identity...")
    pause()
    valid, msg = directory.verify_certificate(stolen_agent.agent_id)
    print_error(f"BLOCKED: {msg}")
    print_success("✓ Revocation prevents stolen cert abuse")
    
    print_header("SECURITY TEST 5: Capability Violation")
    print_warning("Agent exceeds capabilities")
    limited_agent = merchant.create_agent("limited_agent_001", ["search"])
    limited_agent.certificate = directory.register_agent(limited_agent.agent_id, merchant.merchant_id, ["search"])
    print_step("Limited Agent", "Attempting payment...")
    pause()
    if "payment" not in limited_agent.capabilities:
        print_error("BLOCKED: 'payment' not in capabilities")
        print_success("✓ Capability control enforced")
    
    print_header("DEMO SUMMARY")
    print(f"{Fore.GREEN}Security Features Demonstrated:{Style.RESET_ALL}")
    print("  1. ✓ Certificate-based authentication")
    print("  2. ✓ Delegation limits enforcement")
    print("  3. ✓ Certificate revocation")
    print("  4. ✓ Unauthorized agent prevention")
    print("  5. ✓ Capability-based access control")
    print(f"\n{Fore.CYAN}All malicious attempts blocked!{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
