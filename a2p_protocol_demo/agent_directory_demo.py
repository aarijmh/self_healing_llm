#!/usr/bin/env python3
"""Agent Directory A2P Protocol Demo with Payload Examples"""
from entities import *
from colorama import Fore, Style, init
import json
import time
import base64
import hashlib

init(autoreset=True)

class PayloadDemo:
    @staticmethod
    def show_http_request(method, endpoint, headers=None, payload=None):
        print(f"\n{Fore.CYAN}📡 {method} {endpoint}{Style.RESET_ALL}")
        if headers:
            print(f"{Fore.YELLOW}Headers:{Style.RESET_ALL}")
            for k, v in headers.items():
                print(f"  {k}: {v}")
        if payload:
            print(f"{Fore.GREEN}Payload:{Style.RESET_ALL}")
            print(json.dumps(payload, indent=2))
    
    @staticmethod
    def show_http_response(status, headers=None, payload=None):
        color = Fore.GREEN if status < 400 else Fore.RED
        print(f"\n{color}📥 Response: {status}{Style.RESET_ALL}")
        if headers:
            print(f"{Fore.YELLOW}Headers:{Style.RESET_ALL}")
            for k, v in headers.items():
                print(f"  {k}: {v}")
        if payload:
            print(f"{Fore.GREEN}Response:{Style.RESET_ALL}")
            print(json.dumps(payload, indent=2))

def run_agent_directory_demo():
    print(f"\n{Fore.MAGENTA}{'='*80}")
    print("AGENT DIRECTORY A2P PROTOCOL DEMO WITH PAYLOADS")
    print(f"{'='*80}{Style.RESET_ALL}\n")
    
    # Initialize entities
    directory = AgentDirectory()
    delegation_service = DelegationService()
    gateway = PaymentGateway(directory)
    bank = Bank()
    
    print(f"{Fore.CYAN}== PHASE 1: MERCHANT REGISTRATION =={Style.RESET_ALL}")
    
    # Merchant registration with detailed payload
    PayloadDemo.show_http_request("POST", "/register/merchant", 
        headers={
            "Content-Type": "application/json",
            "X-API-Version": "2.0"
        },
        payload={
            "merchant_id": "amazon_us",
            "business_license": "BL-123456789",
            "domain": "amazon.com",
            "public_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...",
            "proof_of_domain": "dns_txt_record_hash"
        }
    )
    
    merchant = Merchant("amazon_us", "Amazon")
    merchant.certificate = directory.register_merchant("amazon_us", "BL-123456789")
    
    PayloadDemo.show_http_response(200,
        headers={
            "Content-Type": "application/json",
            "X-Certificate-Chain": "base64_encoded_chain"
        },
        payload={
            "status": "registered",
            "merchant_cert": {
                "cert_id": "CERT_AMZ_001",
                "public_key": "merchant_public_key",
                "signature": "gateway_signature_of_cert",
                "expires_at": "2025-12-31T23:59:59Z"
            },
            "signing_key": "merchant_private_key_encrypted"
        }
    )
    
    input(f"\n{Fore.YELLOW}Press Enter to continue to Phase 2...{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}== PHASE 2: AGENT REGISTRATION & SIGNING =={Style.RESET_ALL}")
    
    PayloadDemo.show_http_request("POST", "/register/agent",
        headers={
            "Authorization": "Bearer merchant_jwt_token",
            "X-Merchant-Signature": "HMAC-SHA256(payload)"
        },
        payload={
            "agent_id": "amazon_shopping_agent_v2.1",
            "merchant_id": "amazon_us",
            "capabilities": ["payment", "search", "checkout"],
            "scopes": ["user_delegation", "transaction_processing"],
            "agent_hash": "sha256_of_agent_binary",
            "merchant_signature": "RSA_signature_by_merchant"
        }
    )
    
    agent = merchant.create_agent("amazon_shopping_agent_v2.1", ["payment", "search", "checkout"])
    agent.certificate = directory.register_agent(agent.agent_id, merchant.merchant_id, agent.capabilities)
    
    PayloadDemo.show_http_response(200,
        headers={
            "X-Agent-Certificate": "base64_encoded_cert",
            "X-Revocation-Endpoint": "https://gateway.callsign.com/revoke"
        },
        payload={
            "agent_cert": {
                "agent_id": "amazon_shopping_agent_v2.1",
                "merchant_id": "amazon_us",
                "capabilities": ["payment", "search", "checkout"],
                "issued_at": "2024-01-15T10:00:00Z",
                "expires_at": "2025-01-15T10:00:00Z",
                "merchant_signature": "merchant_rsa_signature",
                "gateway_signature": "gateway_ecdsa_signature",
                "revocation_endpoint": "/revoke/agent/amazon_shopping_agent_v2.1"
            }
        }
    )
    
    input(f"\n{Fore.YELLOW}Press Enter to continue to Phase 3...{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}== PHASE 3: TRUST ESTABLISHMENT =={Style.RESET_ALL}")
    
    # Certificate validation
    PayloadDemo.show_http_request("GET", "/validate/certificate",
        headers={
            "X-Agent-Certificate": "base64_encoded_cert",
            "X-Agent-ID": "amazon_shopping_agent_v2.1"
        }
    )
    
    PayloadDemo.show_http_response(200, payload={
        "status": "valid",
        "cert_status": "active",
        "revocation_check": "passed",
        "timestamp": "2024-01-20T14:30:00Z"
    })
    
    # Signature chain validation
    PayloadDemo.show_http_request("POST", "/validate/signature_chain", payload={
        "agent_cert": "base64_agent_certificate",
        "challenge": "random_nonce_12345",
        "signatures": {
            "merchant_sig": "merchant_rsa_signature",
            "gateway_sig": "gateway_ecdsa_signature"
        }
    })
    
    PayloadDemo.show_http_response(200, payload={
        "validation_result": "authentic",
        "signature_chain_valid": True,
        "trust_score": 0.98
    })
    
    # User-agent binding
    PayloadDemo.show_http_request("POST", "/bind/user_agent",
        headers={
            "Authorization": "Bearer user_session_token",
            "X-Agent-Certificate": "base64_encoded_cert"
        },
        payload={
            "user_id": "user_12345",
            "agent_id": "amazon_shopping_agent_v2.1",
            "biometric_hash": "sha256_face_template",
            "device_fingerprint": "device_unique_id"
        }
    )
    
    PayloadDemo.show_http_response(200, payload={
        "binding_id": "BIND_789ABC",
        "trust_token": "eyJhbGciOiJFUzI1NiJ9...",
        "expires_at": "2024-02-20T14:30:00Z"
    })
    
    # Delegation setup
    user_id = "user_12345"
    bank.create_account(user_id, 10000)
    agent.bind_user(user_id, 5000)
    delegation_service.create_delegation(user_id, agent.agent_id, 5000)
    
    PayloadDemo.show_http_request("POST", "/delegate/permissions",
        headers={
            "Authorization": "Bearer trust_token",
            "X-User-Consent": "signed_consent_hash"
        },
        payload={
            "delegation_scope": {
                "spending_limit": 5000.00,
                "currency": "USD",
                "categories": ["electronics", "books", "home"],
                "duration": "30_days"
            },
            "user_signature": "biometric_consent_signature"
        }
    )
    
    PayloadDemo.show_http_response(200, payload={
        "delegation_id": "DEL_456XYZ",
        "status": "active",
        "remaining_limit": 5000.00,
        "policy_token": "eyJkZWxlZ2F0aW9uX2lkIjoi..."
    })
    
    input(f"\n{Fore.YELLOW}Press Enter to continue to Phase 4...{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}== PHASE 4: AUTOMATED SHOPPING TRANSACTION =={Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}Customer: \"Buy me a laptop under $2000\"{Style.RESET_ALL}")
    
    # Session validation
    PayloadDemo.show_http_request("GET", "/session/validate",
        headers={
            "Authorization": "Bearer policy_token",
            "X-Session-ID": "session_12345"
        }
    )
    
    PayloadDemo.show_http_response(200, payload={
        "session_valid": True,
        "certificate_status": "active",
        "remaining_delegation": 5000.00
    })
    
    print(f"{Fore.GREEN}Agent: Found Dell XPS 15 - $1,899{Style.RESET_ALL}")
    
    # Transaction initiation
    PayloadDemo.show_http_request("POST", "/transaction/initiate",
        headers={
            "X-Agent-Certificate": "base64_encoded_cert",
            "X-Transaction-Type": "agent_automated",
            "Content-Type": "application/json"
        },
        payload={
            "transaction_id": "TXN_789DEF",
            "amount": 1899.00,
            "currency": "USD",
            "merchant_id": "amazon_us",
            "agent_attestation": {
                "agent_id": "amazon_shopping_agent_v2.1",
                "delegation_id": "DEL_456XYZ",
                "user_consent_hash": "sha256_consent"
            }
        }
    )
    
    # Agent transaction verification
    PayloadDemo.show_http_request("POST", "/verify/agent_transaction", payload={
        "agent_cert": "base64_certificate",
        "transaction_amount": 1899.00,
        "delegation_check": True
    })
    
    PayloadDemo.show_http_response(200, payload={
        "certificate_valid": True,
        "merchant_trusted": True,
        "delegation_sufficient": True,
        "risk_score": 0.15
    })
    
    # Biometric step-up authentication
    print(f"\n{Fore.YELLOW}🔐 Biometric Authentication Required{Style.RESET_ALL}")
    PayloadDemo.show_http_request("POST", "/auth/stepup", payload={
        "challenge_type": "biometric_face",
        "nonce": "random_challenge_67890",
        "timeout": 30
    })
    
    PayloadDemo.show_http_response(200, payload={
        "biometric_template": "encrypted_face_data",
        "challenge_response": "signed_nonce_67890",
        "device_attestation": "tpm_signature"
    })
    
    # Payment authorization
    PayloadDemo.show_http_request("POST", "/payment/authorize",
        headers={
            "Authorization": "Bearer auth_token",
            "X-Agent-Attestation": "agent_signature"
        },
        payload={
            "transaction_id": "TXN_789DEF",
            "amount": 1899.00,
            "payment_method": "stored_card_token",
            "agent_certificate": "base64_agent_cert",
            "delegation_proof": "signed_delegation_token"
        }
    )
    
    # Bank processing
    PayloadDemo.show_http_request("POST", "/bank/process", payload={
        "amount": 1899.00,
        "merchant_id": "amazon_us",
        "agent_context": {
            "agent_certified": True,
            "gateway_verified": True,
            "delegation_valid": True
        },
        "risk_indicators": {
            "automated_transaction": True,
            "user_authenticated": True
        }
    })
    
    success, tx_id = gateway.process_payment(agent.agent_id, user_id, 1899, delegation_service)
    if success:
        bank.process_payment(user_id, 1899)
        print(f"\n{Fore.GREEN}✅ Payment successful! Transaction ID: {tx_id}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue to Phase 6...{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}== PHASE 6: CERTIFICATE REVOCATION SCENARIO =={Style.RESET_ALL}")
    
    print(f"{Fore.RED}🚨 Security incident detected: Agent vulnerability discovered{Style.RESET_ALL}")
    
    # Certificate revocation
    PayloadDemo.show_http_request("POST", "/revoke/certificate", payload={
        "cert_id": "CERT_AMZ_001",
        "agent_id": "amazon_shopping_agent_v2.1",
        "revocation_reason": "security_vulnerability",
        "effective_immediately": True,
        "revoked_at": "2024-01-25T09:15:00Z"
    })
    
    directory.revoke_certificate(agent.agent_id)
    
    # Revocation notification
    PayloadDemo.show_http_request("POST", "/notify/revocation", payload={
        "event_type": "agent_revoked",
        "agent_id": "amazon_shopping_agent_v2.1",
        "revocation_reason": "security_vulnerability",
        "action_required": "immediate_update",
        "new_agent_version": "amazon_shopping_agent_v2.2"
    })
    
    # Revocation broadcast to banks
    PayloadDemo.show_http_request("POST", "/broadcast/revocation", payload={
        "revoked_certificates": [{
            "agent_id": "amazon_shopping_agent_v2.1",
            "merchant_id": "amazon_us",
            "revoked_at": "2024-01-25T09:15:00Z"
        }],
        "block_transactions": True
    })
    
    print(f"\n{Fore.GREEN}Customer: \"Buy headphones\"{Style.RESET_ALL}")
    
    # Validation attempt after revocation
    PayloadDemo.show_http_request("GET", "/validate/certificate")
    
    PayloadDemo.show_http_response(403, payload={
        "status": "REVOKED",
        "revocation_reason": "security_vulnerability",
        "revoked_at": "2024-01-25T09:15:00Z",
        "update_required": True
    })
    
    success, result = gateway.process_payment(agent.agent_id, user_id, 200, delegation_service)
    print(f"\n{Fore.RED}❌ Transaction BLOCKED: {result}{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}{'='*80}")
    print("DEMO COMPLETE - ALL SECURITY FEATURES DEMONSTRATED")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}✅ Key Features Demonstrated:{Style.RESET_ALL}")
    features = [
        "Detailed HTTP payloads and headers",
        "Certificate-based authentication",
        "Dual-signature verification",
        "Biometric step-up authentication",
        "Real-time certificate revocation",
        "Agent capability enforcement",
        "Delegation limit controls"
    ]
    
    for feature in features:
        print(f"  • {feature}")
    
    print(f"\n{Fore.CYAN}The A2P Protocol successfully prevents unauthorized agents")
    print(f"from accessing payment systems through cryptographic verification{Style.RESET_ALL}")

if __name__ == "__main__":
    run_agent_directory_demo()