import uuid
from typing import List, Dict
from models import Product, Transaction, TransactionStatus

class AmazonMCP:
    def __init__(self):
        self.products = [
            Product("amz_001", "Dell XPS 15", 1899.0, "amazon", "High-performance laptop"),
            Product("amz_002", "MacBook Pro 14", 1999.0, "amazon", "Apple M2 Pro laptop"),
            Product("amz_003", "ThinkPad X1 Carbon", 1699.0, "amazon", "Business ultrabook")
        ]
    
    def search_products(self, query: str, max_price: float) -> List[Product]:
        return [p for p in self.products if query.lower() in p.name.lower() and p.price <= max_price]

class BestBuyMCP:
    def __init__(self):
        self.products = [
            Product("bb_001", "MacBook Air M2", 1799.0, "bestbuy", "Apple M2 laptop"),
            Product("bb_002", "Surface Laptop 5", 1599.0, "bestbuy", "Microsoft laptop"),
            Product("bb_003", "ASUS ZenBook", 1299.0, "bestbuy", "Ultrabook laptop")
        ]
    
    def search_products(self, query: str, max_price: float) -> List[Product]:
        return [p for p in self.products if query.lower() in p.name.lower() and p.price <= max_price]

class TargetMCP:
    def __init__(self):
        self.products = [
            Product("tgt_001", "HP Spectre x360", 1699.0, "target", "2-in-1 laptop"),
            Product("tgt_002", "Lenovo IdeaPad", 899.0, "target", "Budget laptop"),
            Product("tgt_003", "Acer Swift 3", 799.0, "target", "Lightweight laptop")
        ]
    
    def search_products(self, query: str, max_price: float) -> List[Product]:
        return [p for p in self.products if query.lower() in p.name.lower() and p.price <= max_price]

class BankMCP:
    def __init__(self):
        self.transactions = {}
        self.user_limits = {"user_001": 5000.0}
    
    def authorize_purchase(self, user_id: str, amount: float, merchant: str) -> dict:
        """Authorize purchase transaction"""
        limit = self.user_limits.get(user_id, 0)
        if amount > limit:
            return {'status': 'denied', 'reason': 'exceeds_spending_limit'}
        
        txn_id = str(uuid.uuid4())
        self.transactions[txn_id] = Transaction(
            id=txn_id,
            user_id=user_id,
            amount=amount,
            merchant=merchant,
            product_id="",
            status=TransactionStatus.AUTHORIZED
        )
        
        return {'status': 'approved', 'txn_id': txn_id}
    
    def get_payment_credentials(self, txn_id: str) -> dict:
        """Generate secure payment credentials"""
        if txn_id not in self.transactions:
            return {'error': 'transaction_not_found'}
        
        return {
            'payment_token': f"pay_{uuid.uuid4()}",
            'expires_in': 300  # 5 min TTL
        }
    
    def process_payment(self, txn_id: str) -> dict:
        """Process the payment"""
        if txn_id not in self.transactions:
            return {'error': 'transaction_not_found'}
        
        self.transactions[txn_id].status = TransactionStatus.COMPLETED
        return {'status': 'completed', 'txn_ref': f"PAY_{uuid.uuid4()}"}