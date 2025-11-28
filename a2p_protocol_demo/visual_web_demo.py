#!/usr/bin/env python3
"""Enhanced Visual Web Demo for A2P Protocol with Real-time Features"""
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from entities import *
import json
import time
import threading
import uuid
from datetime import datetime, timedelta
import psutil
import random
from collections import defaultdict, deque

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a2p_demo_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

class VisualDemo:
    def __init__(self):
        self.directory = AgentDirectory()
        self.delegation_service = DelegationService()
        self.gateway = PaymentGateway(self.directory)
        self.bank = Bank()
        self.events = deque(maxlen=1000)
        self.security_events = deque(maxlen=100)
        self.performance_metrics = deque(maxlen=50)
        self.rate_limiter = defaultdict(list)
        self.fraud_detector = FraudDetector()
        self.network_topology = NetworkTopology()
        self.entities = {
            'directory': {'name': 'Agent Directory', 'status': 'active', 'color': '#4CAF50', 'load': 0, 'connections': 0},
            'gateway': {'name': 'Payment Gateway', 'status': 'active', 'color': '#2196F3', 'load': 0, 'connections': 0},
            'bank': {'name': 'Bank', 'status': 'active', 'color': '#FF9800', 'load': 0, 'connections': 0},
            'merchant': {'name': 'Merchant', 'status': 'inactive', 'color': '#9C27B0', 'load': 0, 'connections': 0},
            'agent': {'name': 'Agent', 'status': 'inactive', 'color': '#00BCD4', 'load': 0, 'connections': 0},
            'malicious': {'name': 'Malicious Agent', 'status': 'blocked', 'color': '#F44336', 'load': 0, 'connections': 0}
        }
        self.start_monitoring()
        
    def add_event(self, source, target, message, payload=None, status='success', security_level='low'):
        event = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'target': target,
            'message': message,
            'payload': payload or {},
            'status': status,
            'security_level': security_level
        }
        self.events.append(event)
        
        if security_level in ['high', 'critical']:
            self.security_events.append(event)
            
        # Update entity load
        if source in self.entities:
            self.entities[source]['load'] = min(100, self.entities[source]['load'] + 10)
        if target in self.entities:
            self.entities[target]['load'] = min(100, self.entities[target]['load'] + 5)
            
        # Emit real-time update
        socketio.emit('new_event', event)
        return event
        
    def check_rate_limit(self, source_ip, limit=10, window=60):
        now = time.time()
        self.rate_limiter[source_ip] = [t for t in self.rate_limiter[source_ip] if now - t < window]
        if len(self.rate_limiter[source_ip]) >= limit:
            return False
        self.rate_limiter[source_ip].append(now)
        return True
        
    def start_monitoring(self):
        def monitor():
            while True:
                cpu = psutil.cpu_percent()
                memory = psutil.virtual_memory().percent
                self.performance_metrics.append({
                    'timestamp': datetime.now().isoformat(),
                    'cpu': cpu,
                    'memory': memory,
                    'events_per_sec': len([e for e in self.events if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(seconds=1)])
                })
                
                # Decay entity load
                for entity in self.entities.values():
                    entity['load'] = max(0, entity['load'] - 2)
                    
                socketio.emit('performance_update', {
                    'cpu': cpu, 'memory': memory,
                    'entities': self.entities
                })
                time.sleep(2)
        threading.Thread(target=monitor, daemon=True).start()

class FraudDetector:
    def __init__(self):
        self.suspicious_patterns = []
        self.blacklist = set()
        
    def analyze_transaction(self, agent_id, amount, user_id):
        risk_score = 0
        if agent_id in self.blacklist:
            risk_score += 100
        if amount > 10000:
            risk_score += 30
        if amount < 1:
            risk_score += 20
        return min(100, risk_score)
        
    def add_to_blacklist(self, agent_id):
        self.blacklist.add(agent_id)

class NetworkTopology:
    def __init__(self):
        self.connections = defaultdict(set)
        self.traffic = defaultdict(int)
        
    def add_connection(self, source, target):
        self.connections[source].add(target)
        self.traffic[(source, target)] += 1

demo = VisualDemo()

@app.route('/')
def index():
    return render_template('visual_demo.html')

@app.route('/api/entities')
def get_entities():
    return jsonify(demo.entities)

@app.route('/api/events')
def get_events():
    return jsonify(demo.events[-20:])  # Last 20 events

@app.route('/api/clear')
def clear_events():
    demo.events.clear()
    return jsonify({'status': 'cleared'})

@app.route('/api/demo/merchant_registration')
def merchant_registration():
    demo.add_event('merchant', 'directory', 'Register Merchant', {
        'merchant_id': 'amazon_us',
        'business_license': 'BL-123456789',
        'domain': 'amazon.com'
    })
    
    merchant = Merchant("amazon_us", "Amazon")
    merchant.certificate = demo.directory.register_merchant("amazon_us", "BL-123456789")
    demo.entities['merchant']['status'] = 'active'
    
    demo.add_event('directory', 'merchant', 'Certificate Issued', {
        'cert_id': 'CERT_AMZ_001',
        'status': 'registered'
    })
    
    return jsonify({'status': 'success', 'merchant_id': 'amazon_us'})

@app.route('/api/demo/agent_registration')
def agent_registration():
    merchant = Merchant("amazon_us", "Amazon")
    
    demo.add_event('merchant', 'directory', 'Register Agent', {
        'agent_id': 'amazon_shopping_agent_v2.1',
        'capabilities': ['payment', 'search', 'checkout']
    })
    
    agent = merchant.create_agent("amazon_shopping_agent_v2.1", ["payment", "search", "checkout"])
    agent.certificate = demo.directory.register_agent(agent.agent_id, merchant.merchant_id, agent.capabilities)
    demo.entities['agent']['status'] = 'active'
    
    demo.add_event('directory', 'merchant', 'Agent Certificate Issued', {
        'agent_id': 'amazon_shopping_agent_v2.1',
        'status': 'certified'
    })
    
    return jsonify({'status': 'success', 'agent_id': 'amazon_shopping_agent_v2.1'})

@app.route('/api/demo/malicious_agent')
def malicious_agent_demo():
    source_ip = request.remote_addr
    if not demo.check_rate_limit(source_ip):
        return jsonify({'error': 'Rate limit exceeded'}), 429
        
    # Malicious agent attempts registration
    demo.add_event('malicious', 'directory', 'Attempt Registration', {
        'agent_id': 'fake_amazon_agent',
        'merchant_id': 'fake_merchant',
        'capabilities': ['payment', 'admin'],
        'source_ip': source_ip
    }, 'warning', 'high')
    
    demo.add_event('directory', 'malicious', 'Registration REJECTED', {
        'reason': 'Invalid merchant certificate',
        'status': 'blocked'
    }, 'error', 'high')
    
    # Add to fraud detector blacklist
    demo.fraud_detector.add_to_blacklist('fake_amazon_agent')
    
    # Malicious agent tries to bypass
    demo.add_event('malicious', 'gateway', 'Direct Payment Request', {
        'amount': 5000,
        'fake_cert': 'invalid_certificate'
    }, 'warning', 'critical')
    
    demo.add_event('gateway', 'directory', 'Verify Certificate', {
        'agent_id': 'fake_amazon_agent'
    })
    
    demo.add_event('directory', 'gateway', 'Certificate INVALID', {
        'status': 'not_found',
        'threat_level': 'high'
    }, 'error', 'critical')
    
    demo.add_event('gateway', 'malicious', 'Transaction BLOCKED', {
        'reason': 'Invalid certificate',
        'action': 'IP_BLOCKED'
    }, 'error', 'critical')
    
    return jsonify({'status': 'blocked', 'threat_detected': True})

@app.route('/api/demo/legitimate_transaction')
def legitimate_transaction():
    # User delegation
    user_id = "user_12345"
    amount = 1899
    demo.bank.create_account(user_id, 10000)
    
    # Fraud analysis
    risk_score = demo.fraud_detector.analyze_transaction("amazon_shopping_agent_v2.1", amount, user_id)
    
    demo.add_event('agent', 'gateway', 'Request User Delegation', {
        'user_id': user_id,
        'spending_limit': 5000,
        'risk_score': risk_score
    })
    
    demo.delegation_service.create_delegation(user_id, "amazon_shopping_agent_v2.1", 5000)
    
    demo.add_event('gateway', 'agent', 'Delegation Granted', {
        'delegation_id': 'DEL_456XYZ',
        'limit': 5000
    })
    
    # Transaction with network topology tracking
    demo.network_topology.add_connection('agent', 'gateway')
    demo.add_event('agent', 'gateway', 'Process Payment', {
        'amount': amount,
        'transaction_id': 'TXN_789DEF',
        'risk_score': risk_score
    })
    
    demo.add_event('gateway', 'directory', 'Verify Agent Certificate', {
        'agent_id': 'amazon_shopping_agent_v2.1'
    })
    
    demo.add_event('directory', 'gateway', 'Certificate Valid', {
        'status': 'active',
        'trust_score': 0.98
    })
    
    demo.add_event('gateway', 'bank', 'Authorize Payment', {
        'amount': amount,
        'agent_verified': True
    })
    
    success, tx_id = demo.gateway.process_payment("amazon_shopping_agent_v2.1", user_id, amount, demo.delegation_service)
    if success:
        demo.bank.process_payment(user_id, amount)
        demo.add_event('bank', 'gateway', 'Payment Successful', {
            'transaction_id': tx_id,
            'remaining_balance': 8101
        })
        
        demo.add_event('gateway', 'agent', 'Transaction Complete', {
            'status': 'success',
            'transaction_id': tx_id
        })
    
    return jsonify({'status': 'success', 'transaction_id': tx_id, 'risk_score': risk_score})

@app.route('/api/demo/certificate_revocation')
def certificate_revocation():
    demo.add_event('directory', 'gateway', 'Security Alert', {
        'agent_id': 'amazon_shopping_agent_v2.1',
        'vulnerability': 'CVE-2024-001'
    }, 'warning')
    
    demo.add_event('directory', 'bank', 'Revoke Certificate', {
        'agent_id': 'amazon_shopping_agent_v2.1',
        'reason': 'security_vulnerability'
    }, 'warning')
    
    demo.directory.revoke_certificate("amazon_shopping_agent_v2.1")
    demo.entities['agent']['status'] = 'revoked'
    
    # Agent tries to make transaction
    demo.add_event('agent', 'gateway', 'Attempt Payment', {
        'amount': 200,
        'agent_id': 'amazon_shopping_agent_v2.1'
    }, 'warning')
    
    demo.add_event('gateway', 'directory', 'Verify Certificate', {
        'agent_id': 'amazon_shopping_agent_v2.1'
    })
    
    demo.add_event('directory', 'gateway', 'Certificate REVOKED', {
        'status': 'revoked',
        'revoked_at': datetime.now().isoformat()
    }, 'error')
    
    demo.add_event('gateway', 'agent', 'Transaction DENIED', {
        'reason': 'Certificate revoked',
        'action_required': 'Update agent'
    }, 'error')
    
    return jsonify({'status': 'revoked', 'agent_blocked': True})

@app.route('/api/demo/full_scenario')
def full_scenario():
    """Run complete demo scenario"""
    threading.Thread(target=run_full_demo).start()
    return jsonify({'status': 'started'})

def run_full_demo():
    time.sleep(1)
    merchant_registration()
    time.sleep(2)
    agent_registration()
    time.sleep(2)
    malicious_agent_demo()
    time.sleep(3)
    legitimate_transaction()
    time.sleep(3)
    certificate_revocation()

# New API endpoints
@app.route('/api/security/events')
def get_security_events():
    return jsonify(list(demo.security_events))

@app.route('/api/performance/metrics')
def get_performance_metrics():
    return jsonify(list(demo.performance_metrics))

@app.route('/api/network/topology')
def get_network_topology():
    return jsonify({
        'connections': {k: list(v) for k, v in demo.network_topology.connections.items()},
        'traffic': dict(demo.network_topology.traffic)
    })

@app.route('/api/demo/ddos_attack')
def ddos_attack_demo():
    for i in range(20):
        demo.add_event('malicious', 'gateway', f'DDoS Request #{i+1}', {
            'request_id': f'REQ_{i+1}',
            'payload_size': random.randint(1000, 5000)
        }, 'warning', 'high')
        time.sleep(0.1)
    
    demo.add_event('gateway', 'malicious', 'DDoS Protection Activated', {
        'blocked_requests': 20,
        'protection_level': 'maximum'
    }, 'success', 'high')
    
    return jsonify({'status': 'blocked', 'attack_mitigated': True})

@app.route('/api/demo/multi_agent_scenario')
def multi_agent_scenario():
    agents = ['shopping_agent', 'payment_agent', 'delivery_agent']
    for i, agent in enumerate(agents):
        demo.add_event(agent, 'gateway', f'Concurrent Transaction', {
            'agent_id': agent,
            'amount': random.randint(100, 2000),
            'concurrent_id': i
        })
        demo.network_topology.add_connection(agent, 'gateway')
    
    return jsonify({'status': 'success', 'concurrent_agents': len(agents)})

# WebSocket events
@socketio.on('connect')
def handle_connect():
    emit('connected', {'status': 'Connected to A2P Demo'})

@socketio.on('request_update')
def handle_update_request():
    emit('entities_update', demo.entities)
    emit('events_update', list(demo.events)[-10:])

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, host='0.0.0.0')