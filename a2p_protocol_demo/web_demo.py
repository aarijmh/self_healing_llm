#!/usr/bin/env python3
"""Web-based Visual A2P Protocol Demo"""
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from entities import *
import json
import time
import threading
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a2p_demo_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

class WebDemo:
    def __init__(self):
        self.directory = AgentDirectory()
        self.delegation_service = DelegationService()
        self.gateway = PaymentGateway(self.directory)
        self.bank = Bank()
        self.merchant = None
        self.agent = None
        self.message_log = []
        self.current_step = 0
        
    def log_message(self, sender, receiver, message_type, payload, status="success"):
        """Log a message exchange between entities"""
        msg = {
            "id": len(self.message_log),
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "type": message_type,
            "payload": payload,
            "status": status
        }
        self.message_log.append(msg)
        socketio.emit('new_message', msg)
        return msg
    
    def run_demo_step(self, step):
        """Execute a specific demo step"""
        if step == 1:
            return self.merchant_registration()
        elif step == 2:
            return self.agent_registration()
        elif step == 3:
            return self.trust_establishment()
        elif step == 4:
            return self.payment_transaction()
        elif step == 5:
            return self.certificate_revocation()
        return {"error": "Invalid step"}
    
    def merchant_registration(self):
        """Step 1: Merchant Registration"""
        self.log_message("Merchant", "AgentDirectory", "REGISTER_REQUEST", {
            "merchant_id": "amazon_us",
            "business_license": "BL-123456789",
            "domain": "amazon.com",
            "public_key": "-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..."
        })
        
        self.merchant = Merchant("amazon_us", "Amazon")
        self.merchant.certificate = self.directory.register_merchant("amazon_us", "BL-123456789")
        
        self.log_message("AgentDirectory", "Merchant", "REGISTER_RESPONSE", {
            "status": "registered",
            "merchant_cert": {
                "cert_id": "CERT_AMZ_001",
                "issued_at": self.merchant.certificate.issued_at.isoformat(),
                "expires_at": self.merchant.certificate.expires_at.isoformat()
            }
        })
        
        return {"status": "completed", "step": 1}
    
    def agent_registration(self):
        """Step 2: Agent Registration"""
        if not self.merchant:
            return {"error": "Merchant must be registered first"}
            
        self.log_message("Merchant", "AgentDirectory", "AGENT_REGISTER_REQUEST", {
            "agent_id": "amazon_shopping_agent_v2.1",
            "merchant_id": "amazon_us",
            "capabilities": ["payment", "search", "checkout"],
            "agent_hash": "sha256_of_agent_binary"
        })
        
        self.agent = self.merchant.create_agent("amazon_shopping_agent_v2.1", ["payment", "search", "checkout"])
        self.agent.certificate = self.directory.register_agent(self.agent.agent_id, self.merchant.merchant_id, self.agent.capabilities)
        
        self.log_message("AgentDirectory", "Merchant", "AGENT_REGISTER_RESPONSE", {
            "agent_cert": {
                "agent_id": "amazon_shopping_agent_v2.1",
                "capabilities": ["payment", "search", "checkout"],
                "issued_at": self.agent.certificate.issued_at.isoformat(),
                "expires_at": self.agent.certificate.expires_at.isoformat()
            }
        })
        
        return {"status": "completed", "step": 2}
    
    def trust_establishment(self):
        """Step 3: Trust Establishment & User Binding"""
        if not self.agent:
            return {"error": "Agent must be registered first"}
            
        # Certificate validation
        self.log_message("PaymentGateway", "AgentDirectory", "VALIDATE_CERTIFICATE", {
            "agent_id": "amazon_shopping_agent_v2.1",
            "challenge": "random_nonce_12345"
        })
        
        valid, msg = self.directory.verify_certificate(self.agent.agent_id)
        self.log_message("AgentDirectory", "PaymentGateway", "VALIDATION_RESPONSE", {
            "status": "valid" if valid else "invalid",
            "message": msg,
            "trust_score": 0.98 if valid else 0.0
        })
        
        # User binding and delegation
        user_id = "user_12345"
        self.bank.create_account(user_id, 10000)
        self.agent.bind_user(user_id, 5000)
        self.delegation_service.create_delegation(user_id, self.agent.agent_id, 5000)
        
        self.log_message("User", "DelegationService", "CREATE_DELEGATION", {
            "user_id": user_id,
            "agent_id": "amazon_shopping_agent_v2.1",
            "spending_limit": 5000.00,
            "duration": "30_days"
        })
        
        self.log_message("DelegationService", "User", "DELEGATION_CREATED", {
            "delegation_id": "DEL_456XYZ",
            "status": "active",
            "remaining_limit": 5000.00
        })
        
        return {"status": "completed", "step": 3}
    
    def payment_transaction(self):
        """Step 4: Payment Transaction"""
        if not self.agent:
            return {"error": "Setup incomplete"}
            
        user_id = "user_12345"
        amount = 1899.00
        
        # Transaction initiation
        self.log_message("Agent", "PaymentGateway", "TRANSACTION_REQUEST", {
            "transaction_id": "TXN_789DEF",
            "amount": amount,
            "currency": "USD",
            "agent_id": "amazon_shopping_agent_v2.1",
            "user_id": user_id
        })
        
        # Certificate verification
        self.log_message("PaymentGateway", "AgentDirectory", "VERIFY_AGENT", {
            "agent_id": "amazon_shopping_agent_v2.1",
            "transaction_amount": amount
        })
        
        valid, msg = self.directory.verify_certificate(self.agent.agent_id)
        self.log_message("AgentDirectory", "PaymentGateway", "VERIFICATION_RESULT", {
            "certificate_valid": valid,
            "message": msg
        })
        
        # Delegation check
        self.log_message("PaymentGateway", "DelegationService", "CHECK_DELEGATION", {
            "user_id": user_id,
            "agent_id": "amazon_shopping_agent_v2.1",
            "amount": amount
        })
        
        delegation_valid, delegation_msg = self.delegation_service.check_delegation(user_id, self.agent.agent_id, amount)
        self.log_message("DelegationService", "PaymentGateway", "DELEGATION_RESULT", {
            "valid": delegation_valid,
            "message": delegation_msg
        })
        
        # Process payment
        if valid and delegation_valid:
            success, tx_id = self.gateway.process_payment(self.agent.agent_id, user_id, amount, self.delegation_service)
            if success:
                self.bank.process_payment(user_id, amount)
                self.log_message("PaymentGateway", "Bank", "PROCESS_PAYMENT", {
                    "transaction_id": tx_id,
                    "amount": amount,
                    "user_id": user_id
                })
                
                self.log_message("Bank", "PaymentGateway", "PAYMENT_RESULT", {
                    "status": "success",
                    "transaction_id": tx_id,
                    "new_balance": self.bank.accounts[user_id]
                })
        
        return {"status": "completed", "step": 4}
    
    def certificate_revocation(self):
        """Step 5: Certificate Revocation"""
        if not self.agent:
            return {"error": "Agent not found"}
            
        # Revoke certificate
        self.log_message("SecurityTeam", "AgentDirectory", "REVOKE_CERTIFICATE", {
            "agent_id": "amazon_shopping_agent_v2.1",
            "reason": "security_vulnerability",
            "effective_immediately": True
        })
        
        self.directory.revoke_certificate(self.agent.agent_id)
        
        self.log_message("AgentDirectory", "PaymentGateway", "REVOCATION_NOTICE", {
            "agent_id": "amazon_shopping_agent_v2.1",
            "revoked_at": datetime.now().isoformat(),
            "reason": "security_vulnerability"
        })
        
        # Attempt transaction after revocation
        self.log_message("Agent", "PaymentGateway", "TRANSACTION_REQUEST", {
            "transaction_id": "TXN_BLOCKED",
            "amount": 200.00,
            "agent_id": "amazon_shopping_agent_v2.1"
        })
        
        valid, msg = self.directory.verify_certificate(self.agent.agent_id)
        self.log_message("PaymentGateway", "Agent", "TRANSACTION_BLOCKED", {
            "status": "BLOCKED",
            "reason": msg,
            "revoked": True
        })
        
        return {"status": "completed", "step": 5}

# Global demo instance
demo = WebDemo()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run_step/<int:step>')
def run_step(step):
    result = demo.run_demo_step(step)
    return jsonify(result)

@app.route('/api/messages')
def get_messages():
    return jsonify(demo.message_log)

@app.route('/api/reset')
def reset_demo():
    global demo
    demo = WebDemo()
    return jsonify({"status": "reset"})

@app.route('/api/status')
def get_status():
    return jsonify({
        "merchant_registered": demo.merchant is not None,
        "agent_registered": demo.agent is not None,
        "total_messages": len(demo.message_log)
    })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)