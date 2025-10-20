"""
Banking Agent Demo - Backend API
Complete mock implementation of all entities for visual demonstration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ============================================================================
# MOCK DATA STORES
# ============================================================================

# User session store
sessions = {}

# Transaction store
transactions = {}

# Delegation store
delegations = {}

# Product catalog
PRODUCT_CATALOG = {
	"amazon": [
		{"id": "AMZ001", "name": "Dell XPS 15", "price": 1899, "category": "electronics", "rating": 4.5},
		{"id": "AMZ002", "name": "Lenovo ThinkPad X1", "price": 1699, "category": "electronics", "rating": 4.7},
		{"id": "AMZ003", "name": "ASUS ROG Gaming Laptop", "price": 1999, "category": "electronics", "rating": 4.6},
	],
	"bestbuy": [
		{"id": "BB001", "name": "MacBook Air M2", "price": 1799, "category": "electronics", "rating": 4.8},
		{"id": "BB002", "name": "HP Envy 17", "price": 1599, "category": "electronics", "rating": 4.4},
		{"id": "BB003", "name": "Microsoft Surface Laptop 5", "price": 1699, "category": "electronics", "rating": 4.6},
	],
	"target": [
		{"id": "TGT001", "name": "HP Spectre x360", "price": 1699, "category": "electronics", "rating": 4.5},
		{"id": "TGT002", "name": "Acer Swift 3", "price": 899, "category": "electronics", "rating": 4.3},
		{"id": "TGT003", "name": "Samsung Galaxy Book Pro", "price": 1499, "category": "electronics", "rating": 4.4},
	]
}

# User account data
USER_ACCOUNT = {
	"account_number": "****1234",
	"balance": 15000.00,
	"daily_limit": 5000.00,
	"spent_today": 0.00,
	"name": "John Doe"
}

# ============================================================================
# MOCK SERVICES
# ============================================================================

class CallSignMock:
	"""Mock CallSign Authentication Service"""
	
	@staticmethod
	def authenticate_biometric(user_id: str, biometric_type: str) -> Dict[str, Any]:
		"""Simulate biometric authentication"""
		time.sleep(0.5)  # Simulate processing time
		return {
			"success": True,
			"token": f"AUTH_{uuid.uuid4().hex[:8]}",
			"ttl": 900,  # 15 minutes
			"biometric_type": biometric_type,
			"confidence": random.uniform(0.95, 0.99)
		}
	
	@staticmethod
	def validate_delegation(user_id: str) -> Dict[str, Any]:
		"""Validate delegation authority"""
		time.sleep(0.3)
		return {
			"success": True,
			"delegation_token": f"DEL_{uuid.uuid4().hex[:8]}",
			"authorized": True
		}

class HSMMock:
	"""Mock Hardware Security Module"""
	
	@staticmethod
	def generate_payment_token(amount: float, merchant: str) -> Dict[str, Any]:
		"""Generate secure payment token"""
		time.sleep(0.4)
		return {
			"token": f"PAY_{uuid.uuid4().hex[:12]}",
			"encrypted": True,
			"ttl": 300,  # 5 minutes
			"amount": amount,
			"merchant": merchant,
			"timestamp": datetime.now().isoformat()
		}
	
	@staticmethod
	def generate_agent_certificate() -> Dict[str, Any]:
		"""Generate agent certificate"""
		time.sleep(0.5)
		return {
			"certificate": f"CERT_{uuid.uuid4().hex[:16]}",
			"public_key": f"PUB_{uuid.uuid4().hex[:32]}",
			"private_key": f"PRIV_{uuid.uuid4().hex[:32]}",
			"dual_signed": True,
			"expiry": (datetime.now() + timedelta(days=365)).isoformat()
		}

class BankCoreMock:
	"""Mock Bank Core System"""
	
	@staticmethod
	def verify_identity(account_number: str, ssn: str) -> Dict[str, Any]:
		"""Verify customer identity"""
		time.sleep(0.6)
		return {
			"verified": True,
			"kyc_status": "approved",
			"risk_level": "low",
			"account_status": "active"
		}
	
	@staticmethod
	def execute_transaction(amount: float, merchant: str) -> Dict[str, Any]:
		"""Execute payment transaction"""
		time.sleep(0.7)
		
		if USER_ACCOUNT["balance"] >= amount:
			USER_ACCOUNT["balance"] -= amount
			USER_ACCOUNT["spent_today"] += amount
			
			return {
				"success": True,
				"transaction_id": f"TXN_{uuid.uuid4().hex[:12]}",
				"amount": amount,
				"merchant": merchant,
				"new_balance": USER_ACCOUNT["balance"],
				"timestamp": datetime.now().isoformat()
			}
		else:
			return {
				"success": False,
				"error": "insufficient_funds",
				"available_balance": USER_ACCOUNT["balance"]
			}

class BankMCPMock:
	"""Mock Bank MCP Server"""
	
	@staticmethod
	def register_agent() -> Dict[str, Any]:
		"""Register shopping agent"""
		time.sleep(0.5)
		cert = HSMMock.generate_agent_certificate()
		return {
			"agent_id": f"AGENT_{uuid.uuid4().hex[:8]}",
			"certificate": cert,
			"registered_mcps": ["amazon", "bestbuy", "target"],
			"capabilities": ["shopping", "payment", "delegation"]
		}
	
	@staticmethod
	def register_delegation(spending_limit: float, categories: List[str]) -> Dict[str, Any]:
		"""Register delegation authority"""
		time.sleep(0.4)
		delegation_id = f"DEL_{uuid.uuid4().hex[:8]}"
		delegations[delegation_id] = {
			"spending_limit": spending_limit,
			"categories": categories,
			"created_at": datetime.now().isoformat(),
			"active": True
		}
		return {
			"delegation_id": delegation_id,
			"spending_limit": spending_limit,
			"categories": categories,
			"status": "active"
		}
	
	@staticmethod
	def authorize_purchase(amount: float, merchant: str) -> Dict[str, Any]:
		"""Authorize purchase transaction"""
		time.sleep(0.5)
		
		available = USER_ACCOUNT["daily_limit"] - USER_ACCOUNT["spent_today"]
		
		if amount > available:
			return {
				"authorized": False,
				"reason": "exceeds_daily_limit",
				"available": available,
				"requested": amount
			}
		
		return {
			"authorized": True,
			"txn_id": f"AUTH_{uuid.uuid4().hex[:8]}",
			"amount": amount,
			"merchant": merchant,
			"timestamp": datetime.now().isoformat()
		}

class MerchantMCPMock:
	"""Mock Merchant MCP Servers (Amazon, BestBuy, Target)"""
	
	@staticmethod
	def search_products(merchant: str, query: str, max_price: float) -> List[Dict[str, Any]]:
		"""Search products in merchant catalog"""
		time.sleep(0.6)
		products = PRODUCT_CATALOG.get(merchant, [])
		return [p for p in products if p["price"] <= max_price]
	
	@staticmethod
	def create_order(merchant: str, product_id: str, amount: float) -> Dict[str, Any]:
		"""Create order with merchant"""
		time.sleep(0.8)
		return {
			"order_id": f"{merchant.upper()[:3]}_{uuid.uuid4().hex[:8]}",
			"product_id": product_id,
			"amount": amount,
			"status": "confirmed",
			"estimated_delivery": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
			"bank_verified": True,
			"expedited_processing": True
		}

class PaymentProtocolMock:
	"""Mock Google Payment Protocol"""
	
	@staticmethod
	def process_agent_payment(merchant: str, amount: float, bank_token: str) -> Dict[str, Any]:
		"""Process agent-to-agent payment"""
		time.sleep(0.7)
		return {
			"payment_id": f"GPP_{uuid.uuid4().hex[:12]}",
			"status": "completed",
			"merchant": merchant,
			"amount": amount,
			"bank_guaranteed": True,
			"timestamp": datetime.now().isoformat()
		}

# ============================================================================
# WEBSOCKET EVENTS FOR REAL-TIME UPDATES
# ============================================================================

def emit_step(step_name: str, status: str, data: Dict[str, Any] = None):
	"""Emit step update to frontend"""
	socketio.emit('step_update', {
		'step': step_name,
		'status': status,
		'data': data or {},
		'timestamp': datetime.now().isoformat()
	})

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
	"""Health check endpoint"""
	return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/demo/setup', methods=['POST'])
def setup_demo():
	"""Initialize demo with app download and setup"""
	try:
		emit_step("app_download", "started")
		time.sleep(1)
		emit_step("app_download", "completed", {"app_name": "SecureBank AI Agent"})
		
		emit_step("identity_verification", "started")
		result = BankCoreMock.verify_identity("1234", "***-**-1234")
		emit_step("identity_verification", "completed", result)
		
		emit_step("device_registration", "started")
		time.sleep(0.8)
		emit_step("device_registration", "completed", {"device_id": f"DEV_{uuid.uuid4().hex[:8]}"})
		
		emit_step("biometric_enrollment", "started")
		face_result = CallSignMock.authenticate_biometric("user1", "face")
		emit_step("biometric_enrollment", "completed", face_result)
		
		emit_step("agent_registration", "started")
		agent_result = BankMCPMock.register_agent()
		emit_step("agent_registration", "completed", agent_result)
		
		return jsonify({
			"success": True,
			"message": "Demo setup completed",
			"agent_id": agent_result["agent_id"]
		})
	except Exception as e:
		return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/demo/delegate', methods=['POST'])
def delegate_authority():
	"""Delegate shopping authority to agent"""
	try:
		data = request.json
		spending_limit = data.get('spending_limit', 5000)
		categories = data.get('categories', ['electronics', 'home'])
		
		emit_step("delegation_auth", "started")
		auth_result = CallSignMock.validate_delegation("user1")
		emit_step("delegation_auth", "completed", auth_result)
		
		emit_step("delegation_registration", "started")
		delegation_result = BankMCPMock.register_delegation(spending_limit, categories)
		emit_step("delegation_registration", "completed", delegation_result)
		
		return jsonify({
			"success": True,
			"delegation": delegation_result
		})
	except Exception as e:
		return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/demo/purchase', methods=['POST'])
def execute_purchase():
	"""Execute complete purchase flow"""
	try:
		data = request.json
		query = data.get('query', 'laptop')
		max_price = data.get('max_price', 2000)
		
		# Authentication
		emit_step("authentication", "started")
		auth_result = CallSignMock.authenticate_biometric("user1", "face")
		emit_step("authentication", "completed", auth_result)
		
		# Multi-shopper search
		emit_step("product_search", "started")
		amazon_products = MerchantMCPMock.search_products("amazon", query, max_price)
		emit_step("search_amazon", "completed", {"products": amazon_products})
		
		bestbuy_products = MerchantMCPMock.search_products("bestbuy", query, max_price)
		emit_step("search_bestbuy", "completed", {"products": bestbuy_products})
		
		target_products = MerchantMCPMock.search_products("target", query, max_price)
		emit_step("search_target", "completed", {"products": target_products})
		
		# Select best option (for demo, pick BestBuy MacBook)
		selected_product = bestbuy_products[0] if bestbuy_products else None
		selected_merchant = "bestbuy"
		
		emit_step("product_search", "completed", {
			"total_found": len(amazon_products) + len(bestbuy_products) + len(target_products),
			"selected": selected_product,
			"merchant": selected_merchant
		})
		
		# Transaction authorization
		emit_step("transaction_auth", "started")
		auth_result = BankMCPMock.authorize_purchase(selected_product["price"], selected_merchant)
		emit_step("transaction_auth", "completed", auth_result)
		
		if not auth_result["authorized"]:
			return jsonify({"success": False, "error": auth_result["reason"]})
		
		# Payment authentication
		emit_step("payment_auth", "started")
		payment_auth = CallSignMock.authenticate_biometric("user1", "face")
		emit_step("payment_auth", "completed", payment_auth)
		
		# Generate payment token
		emit_step("payment_token", "started")
		token_result = HSMMock.generate_payment_token(selected_product["price"], selected_merchant)
		emit_step("payment_token", "completed", token_result)
		
		# Process payment
		emit_step("payment_processing", "started")
		payment_result = PaymentProtocolMock.process_agent_payment(
			selected_merchant,
			selected_product["price"],
			token_result["token"]
		)
		emit_step("payment_processing", "completed", payment_result)
		
		# Execute bank transaction
		emit_step("bank_transaction", "started")
		bank_result = BankCoreMock.execute_transaction(selected_product["price"], selected_merchant)
		emit_step("bank_transaction", "completed", bank_result)
		
		# Create order
		emit_step("order_creation", "started")
		order_result = MerchantMCPMock.create_order(
			selected_merchant,
			selected_product["id"],
			selected_product["price"]
		)
		emit_step("order_creation", "completed", order_result)
		
		# Complete
		emit_step("purchase_complete", "completed", {
			"product": selected_product,
			"order": order_result,
			"transaction": bank_result,
			"new_balance": USER_ACCOUNT["balance"]
		})
		
		return jsonify({
			"success": True,
			"product": selected_product,
			"order": order_result,
			"transaction": bank_result
		})
		
	except Exception as e:
		emit_step("error", "failed", {"error": str(e)})
		return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/account', methods=['GET'])
def get_account():
	"""Get current account status"""
	return jsonify(USER_ACCOUNT)

@app.route('/api/products/<merchant>', methods=['GET'])
def get_products(merchant):
	"""Get products from specific merchant"""
	max_price = request.args.get('max_price', 10000, type=float)
	products = MerchantMCPMock.search_products(merchant, "", max_price)
	return jsonify({"merchant": merchant, "products": products})

# ============================================================================
# WEBSOCKET HANDLERS
# ============================================================================

@socketio.on('connect')
def handle_connect():
	"""Handle client connection"""
	print('Client connected')
	emit('connected', {'message': 'Connected to Banking Agent Demo'})

@socketio.on('disconnect')
def handle_disconnect():
	"""Handle client disconnection"""
	print('Client disconnected')

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
	print("🚀 Banking Agent Demo Backend Starting...")
	print("📡 Server running on http://localhost:5000")
	socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
