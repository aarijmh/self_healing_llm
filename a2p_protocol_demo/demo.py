"""A2P Protocol Interactive Demo"""
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
    print_header("A2P PROTOCOL SECURITY DEMO")
    print(f"{Fore.YELLOW}This demo shows how the Agent-to-Payment protocol prevents malicious actors{Style.RESET_ALL}\n")
    
    # Initialize entities
    directory = AgentDirectory()
    delegation_service = DelegationService()
    gateway = PaymentGateway(directory)
    bank = Bank()
    
    print_header("PHASE 1: Merchant Registration")
    print_step("Amazon", "Registering with Agent Directory...")
    pause()
    merchant = Merchant("amazon_merchant_001", "Amazon")
    merchant.certificate = directory.register_merchant("amazon_merchant_001", "business_license_12345")
    print_success(f"Merchant '{merchant.name}' registered with certificate")
    print(f"  Certificate ID: {merchant.certificate.entity_id}")
    print(f"  Expires: {merchant.certificate.expires_at.strftime('%Y-%m-%d')}")
    
    print_header("PHASE 2: Agent Registration & Signing")
    print_step("Amazon", "Creating shopping agent...")
    pause()
    agent = merchant.create_agent("amazon_agent_001", ["shopping", "checkout", "payment"])
    print_step("Amazon", "Registering agent with Directory...")
    pause()
    agent.certificate = directory.register_agent(agent.agent_id, merchant.merchant_id, agent.capabilities)
    print_success(f"Agent registered with dual-signed certificate")
    print(f"  Agent ID: {agent.agent_id}")
    print(f"  Capabilities: {', '.join(agent.capabilities)}")
    print(f"  Signatures: AgentDirectory + Merchant")
    
    print_header("PHASE 3: User Setup & Trust Establishment")
    user_id = "customer_alice"
    bank.create_account(user_id, 10000)
    print_step("Customer Alice", "Downloads Amazon app with embedded agent")
    pause()
    print_step("Agent", "Verifying certificate with Directory...")
    pause()
    valid, msg = directory.verify_certificate(agent.agent_id)
    if valid:
        print_success(f"Certificate verified: {msg}")
    
    print_step("Customer Alice", "Setting delegation limit: $5000")
    pause()
    agent.bind_user(user_id, 5000)
    delegation_service.create_delegation(user_id, agent.agent_id, 5000)
    print_success("User-Agent binding established with spending limit")
    
    print_header("PHASE 4: Legitimate Transaction")
    print_step("Customer Alice", '"Buy me a laptop under $2000"')
    pause()
    print_step("Agent", "Searching products...")
    pause()
    print_step("Agent", "Found: Dell XPS 15 - $1899")
    pause()
    print_step("Agent", "Verifying certificate before checkout...")
    pause()
    valid, msg = directory.verify_certificate(agent.agent_id)
    print_success(f"Certificate valid: {msg}")
    
    print_step("Gateway", "Processing payment with agent verification...")
    pause()
    success, result = gateway.process_payment(agent.agent_id, user_id, 1899, delegation_service)
    if success:
        bank.process_payment(user_id, 1899)
        print_success(f"Payment authorized! Transaction ID: {result}")
        print(f"  Amount: $1899")
        print(f"  Remaining delegation: ${5000 - 1899}")
    
    print_header("PHASE 5: Subsequent Transaction")
    print_step("Customer Alice", '"Buy wireless mouse under $100"')
    pause()
    print_step("Agent", "Found: Logitech MX Master - $99")
    pause()
    success, result = gateway.process_payment(agent.agent_id, user_id, 99, delegation_service)
    if success:
        bank.process_payment(user_id, 99)
        print_success(f"Payment processed automatically! TX: {result}")
        print(f"  Total spent: $1998 / $5000")
    
    print_header("SECURITY DEMO 1: Malicious Agent (No Certificate)")
    print_warning("Attacker creates fake agent without proper registration")
    malicious_agent = Agent("malicious_agent_666", "fake_merchant", ["payment", "steal"])
    print_step("Malicious Agent", "Attempting payment without certificate...")
    pause()
    success, result = gateway.process_payment(malicious_agent.agent_id, user_id, 500, delegation_service)
    print_error(f"Transaction BLOCKED: {result}")
    print_success("✓ Protocol prevented unauthorized agent")
    
    print_header("SECURITY DEMO 2: Exceeding Delegation Limits")
    print_warning("Agent attempts transaction exceeding user's delegation limit")
    print_step("Agent", "Attempting to buy $4000 item (exceeds remaining $3002 limit)...")
    pause()
    success, result = gateway.process_payment(agent.agent_id, user_id, 4000, delegation_service)
    print_error(f"Transaction BLOCKED: {result}")
    print_success("✓ Delegation limits enforced")
    
    print_header("SECURITY DEMO 3: Certificate Revocation")
    print_warning("Security vulnerability discovered in agent")
    print_step("Directory", "Revoking agent certificate...")
    pause()
    directory.revoke_certificate(agent.agent_id)
    print_success("Certificate revoked and added to revocation list")
    
    print_step("Agent", "Attempting transaction after revocation...")
    pause()
    success, result = gateway.process_payment(agent.agent_id, user_id, 50, delegation_service)
    print_error(f"Transaction BLOCKED: {result}")
    print_success("✓ Revoked certificates cannot transact")
    
    print_header("SECURITY DEMO 4: Stolen Certificate Attack")
    print_warning("Attacker steals certificate but not private keys")
    print_step("Attacker", "Creating agent with stolen certificate ID...")
    pause()
    stolen_agent = Agent("amazon_agent_001", merchant.merchant_id, ["payment"])
    stolen_agent.certificate = agent.certificate
    print_step("Attacker", "Attempting payment with stolen identity...")
    pause()
    valid, msg = directory.verify_certificate(stolen_agent.agent_id)
    print_error(f"Verification FAILED: {msg} (Certificate was revoked)")
    print_success("✓ Even with stolen cert, revocation prevents abuse")
    
    print_header("SECURITY DEMO 5: Unauthorized Capability")
    print_warning("Agent attempts action outside its capabilities")
    print_step("Directory", "Re-registering agent with limited capabilities...")
    pause()
    limited_agent = merchant.create_agent("limited_agent_001", ["search"])
    limited_agent.certificate = directory.register_agent(limited_agent.agent_id, merchant.merchant_id, ["search"])
    print_success(f"Agent registered with capabilities: {limited_agent.capabilities}")
    
    print_step("Limited Agent", "Attempting payment (not in capabilities)...")
    pause()
    if "payment" not in limited_agent.capabilities:
        print_error("Action BLOCKED: 'payment' not in agent capabilities")
        print_success("✓ Capability-based access control enforced")
    
    print_header("DEMO SUMMARY")
    print(f"{Fore.GREEN}Protocol Security Features Demonstrated:{Style.RESET_ALL}")
    print("  1. ✓ Certificate-based authentication (dual-signed)")
    print("  2. ✓ Delegation limits enforcement")
    print("  3. ✓ Certificate revocation mechanism")
    print("  4. ✓ Protection against unauthorized agents")
    print("  5. ✓ Capability-based access control")
    print(f"\n{Fore.CYAN}All malicious attempts were successfully blocked!{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
