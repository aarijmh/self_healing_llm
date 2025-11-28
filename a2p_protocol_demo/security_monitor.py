#!/usr/bin/env python3
"""Advanced Security Monitoring for A2P Protocol"""
import time
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
import hashlib
import json

class SecurityMonitor:
    def __init__(self):
        self.threat_intelligence = ThreatIntelligence()
        self.anomaly_detector = AnomalyDetector()
        self.incident_response = IncidentResponse()
        self.security_metrics = deque(maxlen=1000)
        
    def analyze_event(self, event):
        threat_level = self.threat_intelligence.assess_threat(event)
        anomaly_score = self.anomaly_detector.detect_anomaly(event)
        
        if threat_level > 70 or anomaly_score > 80:
            self.incident_response.trigger_alert(event, threat_level, anomaly_score)
            
        self.security_metrics.append({
            'timestamp': datetime.now().isoformat(),
            'threat_level': threat_level,
            'anomaly_score': anomaly_score,
            'event_type': event.get('message', 'unknown')
        })

class ThreatIntelligence:
    def __init__(self):
        self.known_threats = {
            'fake_amazon_agent': 95,
            'malicious_payment_bot': 90,
            'credential_harvester': 85
        }
        self.suspicious_patterns = [
            'admin', 'root', 'system', 'bypass', 'exploit'
        ]
        
    def assess_threat(self, event):
        score = 0
        agent_id = event.get('payload', {}).get('agent_id', '')
        message = event.get('message', '').lower()
        
        if agent_id in self.known_threats:
            score += self.known_threats[agent_id]
            
        for pattern in self.suspicious_patterns:
            if pattern in message or pattern in agent_id.lower():
                score += 20
                
        if event.get('status') == 'error':
            score += 15
            
        return min(100, score)

class AnomalyDetector:
    def __init__(self):
        self.baseline_metrics = defaultdict(list)
        self.learning_period = 100
        
    def detect_anomaly(self, event):
        event_type = event.get('message', 'unknown')
        timestamp = datetime.fromisoformat(event['timestamp'])
        
        # Simple statistical anomaly detection
        recent_events = [e for e in self.baseline_metrics[event_type] 
                        if datetime.fromisoformat(e['timestamp']) > timestamp - timedelta(minutes=10)]
        
        if len(recent_events) > 10:  # Potential flooding
            return 80
        elif len(recent_events) > 5:
            return 40
            
        return 10

class IncidentResponse:
    def __init__(self):
        self.active_incidents = []
        self.response_actions = {
            'block_agent': self.block_agent,
            'rate_limit': self.apply_rate_limit,
            'alert_admin': self.alert_admin
        }
        
    def trigger_alert(self, event, threat_level, anomaly_score):
        incident = {
            'id': hashlib.md5(f"{event['id']}{time.time()}".encode()).hexdigest()[:8],
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'threat_level': threat_level,
            'anomaly_score': anomaly_score,
            'status': 'active'
        }
        
        self.active_incidents.append(incident)
        
        if threat_level > 90:
            self.response_actions['block_agent'](event)
        elif threat_level > 70:
            self.response_actions['rate_limit'](event)
            
        self.response_actions['alert_admin'](incident)
        
    def block_agent(self, event):
        agent_id = event.get('payload', {}).get('agent_id')
        print(f"🚫 BLOCKING AGENT: {agent_id}")
        
    def apply_rate_limit(self, event):
        source = event.get('source')
        print(f"⚠️ RATE LIMITING: {source}")
        
    def alert_admin(self, incident):
        print(f"🚨 SECURITY ALERT: Incident {incident['id']} - Threat Level: {incident['threat_level']}")

class ComplianceMonitor:
    def __init__(self):
        self.audit_log = deque(maxlen=10000)
        self.compliance_rules = {
            'pci_dss': PCIDSSCompliance(),
            'gdpr': GDPRCompliance(),
            'sox': SOXCompliance()
        }
        
    def check_compliance(self, event):
        violations = []
        for rule_name, rule in self.compliance_rules.items():
            if not rule.validate(event):
                violations.append(rule_name)
                
        if violations:
            self.audit_log.append({
                'timestamp': datetime.now().isoformat(),
                'event_id': event['id'],
                'violations': violations,
                'severity': 'high' if 'pci_dss' in violations else 'medium'
            })
            
        return violations

class PCIDSSCompliance:
    def validate(self, event):
        # Check for payment card data exposure
        payload = str(event.get('payload', {}))
        sensitive_patterns = ['4[0-9]{12}(?:[0-9]{3})?', '5[1-5][0-9]{14}']
        
        for pattern in sensitive_patterns:
            if pattern in payload:
                return False
        return True

class GDPRCompliance:
    def validate(self, event):
        # Check for personal data handling
        payload = event.get('payload', {})
        if 'user_id' in payload and not payload.get('consent', False):
            return False
        return True

class SOXCompliance:
    def validate(self, event):
        # Check for financial transaction integrity
        if event.get('message') == 'Process Payment':
            payload = event.get('payload', {})
            required_fields = ['amount', 'transaction_id', 'agent_verified']
            return all(field in payload for field in required_fields)
        return True