from typing import List, Dict
from models import Product, User
from auth_service import CallSignAuth
from mcp_servers import AmazonMCP, BestBuyMCP, TargetMCP, BankMCP
from payment_protocol import GooglePaymentProtocol

class MobileAgent:
    def __init__(self):
        self.auth = CallSignAuth()
        self.amazon = AmazonMCP()
        self.bestbuy = BestBuyMCP()
        self.target = TargetMCP()
        self.bank = BankMCP()
        self.payment_protocol = GooglePaymentProtocol()
        self.current_user = User("user_001", "John Doe", 5000.0, 10000.0)
        self.auth_token = None
    
    def authenticate_user(self) -> bool:
        """Authenticate user with biometric"""
        print("📱 Mobile Agent: Authentication required")
        auth_result = self.auth.biometric_auth(self.current_user.id)
        
        if auth_result['status'] == 'authenticated':
            self.auth_token = auth_result['token']
            print(f"✅ Authentication successful. Session expires in {auth_result['expires_in']}s")
            return True
        return False
    
    def search_products(self, query: str, max_price: float) -> Dict[str, List[Product]]:
        """Search products across all retailers"""
        print(f"🔍 Searching for '{query}' under ${max_price}...")
        
        results = {
            'amazon': self.amazon.search_products(query, max_price),
            'bestbuy': self.bestbuy.search_products(query, max_price),
            'target': self.target.search_products(query, max_price)
        }
        
        return results
    
    def recommend_product(self, results: Dict[str, List[Product]]) -> Product:
        """Analyze and recommend best product"""
        all_products = []
        for products in results.values():
            all_products.extend(products)
        
        # Simple recommendation: best value (lowest price)
        if all_products:
            return min(all_products, key=lambda p: p.price)
        return None
    
    def purchase_product(self, product: Product) -> dict:
        """Execute purchase workflow"""
        if not self.auth_token or not self.auth.validate_token(self.auth_token):
            return {'error': 'authentication_required'}
        
        print(f"💳 Processing purchase: {product.name} for ${product.price}")
        
        # Step 1: Authorize purchase
        auth_result = self.bank.authorize_purchase(
            self.current_user.id, product.price, product.merchant
        )
        
        if auth_result['status'] != 'approved':
            return {'error': 'authorization_failed', 'reason': auth_result.get('reason')}
        
        txn_id = auth_result['txn_id']
        print(f"✅ Purchase authorized (txn_id: {txn_id})")
        
        # Step 2: Step-up authentication
        step_up = self.auth.step_up_auth(self.auth_token)
        if not step_up.get('payment_authorized'):
            return {'error': 'payment_auth_failed'}
        
        # Step 3: Get payment credentials
        credentials = self.bank.get_payment_credentials(txn_id)
        if 'error' in credentials:
            return credentials
        
        print("🔐 Secure payment credentials obtained")
        
        # Step 4: Process payment
        payment_result = self.bank.process_payment(txn_id)
        if 'error' in payment_result:
            return payment_result
        
        print(f"✅ Payment completed! Transaction ref: {payment_result['txn_ref']}")
        
        return {
            'status': 'success',
            'product': product,
            'txn_ref': payment_result['txn_ref'],
            'order_id': f"ORD_{txn_id[:8]}"
        }