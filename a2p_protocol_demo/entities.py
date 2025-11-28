"""Core entities for A2P Protocol Demo"""
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from datetime import datetime, timedelta
import json
import hashlib

class Certificate:
    def __init__(self, entity_id, entity_type, capabilities=None, issuer=None, expiry_days=365):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.capabilities = capabilities or []
        self.issuer = issuer
        self.issued_at = datetime.now()
        self.expires_at = self.issued_at + timedelta(days=expiry_days)
        self.revoked = False
        self.signatures = []
    
    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "capabilities": self.capabilities,
            "issuer": self.issuer,
            "issued_at": self.issued_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "revoked": self.revoked
        }
    
    def is_valid(self):
        return not self.revoked and datetime.now() < self.expires_at

class AgentDirectory:
    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
        self.merchants = {}
        self.agents = {}
        self.revocation_list = set()
    
    def register_merchant(self, merchant_id, business_license):
        cert = Certificate(merchant_id, "merchant", issuer="AgentDirectory")
        signature = self._sign(cert.to_dict())
        cert.signatures.append(("AgentDirectory", signature))
        self.merchants[merchant_id] = cert
        return cert
    
    def register_agent(self, agent_id, merchant_id, capabilities):
        if merchant_id not in self.merchants:
            raise ValueError("Merchant not registered")
        cert = Certificate(agent_id, "agent", capabilities, issuer=merchant_id)
        signature = self._sign(cert.to_dict())
        cert.signatures.append(("AgentDirectory", signature))
        self.agents[agent_id] = cert
        return cert
    
    def verify_certificate(self, entity_id):
        cert = self.agents.get(entity_id) or self.merchants.get(entity_id)
        if not cert:
            return False, "Certificate not found"
        if entity_id in self.revocation_list:
            return False, "Certificate revoked"
        if not cert.is_valid():
            return False, "Certificate expired"
        return True, "Valid"
    
    def revoke_certificate(self, entity_id):
        self.revocation_list.add(entity_id)
        if entity_id in self.agents:
            self.agents[entity_id].revoked = True
    
    def _sign(self, data):
        message = json.dumps(data, sort_keys=True).encode()
        return self.private_key.sign(message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

class Merchant:
    def __init__(self, merchant_id, name):
        self.merchant_id = merchant_id
        self.name = name
        self.certificate = None
        self.agents = []
    
    def create_agent(self, agent_id, capabilities):
        agent = Agent(agent_id, self.merchant_id, capabilities)
        self.agents.append(agent)
        return agent

class Agent:
    def __init__(self, agent_id, merchant_id, capabilities):
        self.agent_id = agent_id
        self.merchant_id = merchant_id
        self.capabilities = capabilities
        self.certificate = None
        self.user_bindings = {}
        self.delegation_policies = {}
    
    def bind_user(self, user_id, delegation_limit):
        self.user_bindings[user_id] = {"active": True, "limit": delegation_limit, "spent": 0}
        self.delegation_policies[user_id] = {"limit": delegation_limit, "spent": 0}

class DelegationService:
    def __init__(self):
        self.delegations = {}
    
    def create_delegation(self, user_id, agent_id, limit):
        key = f"{user_id}:{agent_id}"
        self.delegations[key] = {"limit": limit, "spent": 0, "active": True}
        return self.delegations[key]
    
    def check_delegation(self, user_id, agent_id, amount):
        key = f"{user_id}:{agent_id}"
        if key not in self.delegations:
            return False, "No delegation found"
        delegation = self.delegations[key]
        if not delegation["active"]:
            return False, "Delegation inactive"
        if delegation["spent"] + amount > delegation["limit"]:
            return False, f"Exceeds limit (${delegation['spent'] + amount} > ${delegation['limit']})"
        return True, "Within limits"
    
    def record_transaction(self, user_id, agent_id, amount):
        key = f"{user_id}:{agent_id}"
        self.delegations[key]["spent"] += amount

class PaymentGateway:
    def __init__(self, directory):
        self.directory = directory
        self.transactions = []
    
    def process_payment(self, agent_id, user_id, amount, delegation_service):
        valid, msg = self.directory.verify_certificate(agent_id)
        if not valid:
            return False, f"Agent verification failed: {msg}"
        
        valid, msg = delegation_service.check_delegation(user_id, agent_id, amount)
        if not valid:
            return False, f"Delegation check failed: {msg}"
        
        tx_id = hashlib.sha256(f"{agent_id}{user_id}{amount}{datetime.now()}".encode()).hexdigest()[:16]
        self.transactions.append({"tx_id": tx_id, "agent_id": agent_id, "user_id": user_id, "amount": amount, "timestamp": datetime.now()})
        delegation_service.record_transaction(user_id, agent_id, amount)
        return True, tx_id

class Bank:
    def __init__(self):
        self.accounts = {}
    
    def create_account(self, user_id, balance):
        self.accounts[user_id] = balance
    
    def process_payment(self, user_id, amount):
        if user_id not in self.accounts:
            return False, "Account not found"
        if self.accounts[user_id] < amount:
            return False, "Insufficient funds"
        self.accounts[user_id] -= amount
        return True, f"Payment processed. New balance: ${self.accounts[user_id]}"
