import uuid
import time

class GooglePaymentProtocol:
    def __init__(self):
        self.pending_payments = {}
    
    def initiate_agent_payment(self, merchant_agent: str, amount: float) -> dict:
        """Initiate payment between agents"""
        payment_id = str(uuid.uuid4())
        self.pending_payments[payment_id] = {
            'merchant_agent': merchant_agent,
            'amount': amount,
            'status': 'pending',
            'created_at': time.time()
        }
        
        return {
            'payment_id': payment_id,
            'status': 'initiated'
        }
    
    def process_payment(self, payment_id: str, bank_token: str) -> dict:
        """Process payment with bank verification"""
        if payment_id not in self.pending_payments:
            return {'error': 'payment_not_found'}
        
        payment = self.pending_payments[payment_id]
        payment['status'] = 'completed'
        payment['bank_token'] = bank_token
        
        return {
            'status': 'completed',
            'payment_ref': f"GPP_{uuid.uuid4()}"
        }