import time
import uuid
from models import AuthStatus

class CallSignAuth:
    def __init__(self):
        self.active_sessions = {}
    
    def biometric_auth(self, user_id: str) -> dict:
        """Simulate biometric authentication"""
        print("🔐 CallSign: Face scan required...")
        time.sleep(1)
        
        token = str(uuid.uuid4())
        self.active_sessions[token] = {
            'user_id': user_id,
            'expires': time.time() + 900  # 15 min TTL
        }
        
        return {
            'status': AuthStatus.AUTHENTICATED.value,
            'token': token,
            'expires_in': 900
        }
    
    def validate_token(self, token: str) -> bool:
        """Validate authentication token"""
        session = self.active_sessions.get(token)
        if not session:
            return False
        return time.time() < session['expires']
    
    def step_up_auth(self, token: str) -> dict:
        """Step-up authentication for payments"""
        if not self.validate_token(token):
            return {'status': AuthStatus.FAILED.value}
        
        print("🔐 CallSign: Payment confirmation - Face scan...")
        time.sleep(1)
        
        return {
            'status': AuthStatus.AUTHENTICATED.value,
            'payment_authorized': True
        }