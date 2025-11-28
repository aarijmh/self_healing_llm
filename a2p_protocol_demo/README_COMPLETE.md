# A2P Protocol Complete Demo

This demo implements the complete Agent-to-Payment (A2P) protocol from the PlantUML diagram, demonstrating all entities and security mechanisms.

## Architecture Overview

### Entities Implemented

1. **Agent Directory (CallSign Gateway)** - Central trust authority
   - Registers and verifies merchants
   - Issues dual-signed certificates
   - Maintains revocation list
   - Cryptographic signature verification

2. **Merchant (Amazon)** - Service provider
   - Registers with Directory
   - Creates and manages agents
   - Holds merchant certificate

3. **Agent (Amazon Shopping Agent)** - AI assistant
   - Dual-signed certificate (Directory + Merchant)
   - Capability-based permissions
   - User delegation management

4. **Delegation Service** - Authorization manager
   - Creates user-agent bindings
   - Enforces spending limits
   - Tracks transaction history

5. **Payment Gateway** - Transaction processor
   - Verifies agent certificates
   - Checks delegation limits
   - Processes payments securely

6. **Bank** - Financial institution
   - Manages user accounts
   - Processes payments
   - Validates agent attestations

## Security Features

### 1. Certificate-Based Authentication
- Dual-signed certificates (Directory + Merchant)
- Cryptographic verification using RSA-2048
- Certificate expiration enforcement

### 2. Delegation Limits
- User-defined spending limits
- Real-time limit checking
- Transaction tracking

### 3. Certificate Revocation
- Instant revocation capability
- Revocation list checking
- Network-wide broadcast

### 4. Capability-Based Access Control
- Agents limited to specific capabilities
- Capability verification before actions
- Prevents privilege escalation

### 5. Protection Against Attacks
- Unauthorized agents blocked
- Stolen certificates detected
- Limit violations prevented
- Capability violations blocked

## Running the Demo

### Setup
```bash
cd a2p_protocol_demo
source ../.venv/bin/activate
pip install -r requirements.txt
```

### Run Complete Demo
```bash
python complete_demo.py
```

## Demo Phases

### Phase 1: Merchant Registration
- Amazon registers with Agent Directory
- Receives merchant certificate
- Establishes trust relationship

### Phase 2: Agent Registration
- Amazon creates shopping agent
- Agent registered with Directory
- Dual-signed certificate issued

### Phase 3: User Setup
- Customer downloads app
- Certificate verification
- Delegation limit established ($5000)

### Phase 4: First Transaction
- Customer requests laptop purchase
- Agent finds product ($1899)
- Payment processed successfully
- Delegation limit updated

### Phase 5: Subsequent Transaction
- Customer requests mouse purchase
- Automatic processing ($99)
- No step-up authentication needed

## Security Tests

### Test 1: Unauthorized Agent
**Attack**: Malicious agent without certificate
**Result**: ✗ Transaction BLOCKED - Certificate not found

### Test 2: Exceeding Limits
**Attack**: Transaction exceeds delegation limit
**Result**: ✗ Transaction BLOCKED - Exceeds limit

### Test 3: Certificate Revocation
**Attack**: Using revoked certificate
**Result**: ✗ Transaction BLOCKED - Certificate revoked

### Test 4: Stolen Certificate
**Attack**: Attacker uses stolen certificate ID
**Result**: ✗ Transaction BLOCKED - Revocation prevents abuse

### Test 5: Capability Violation
**Attack**: Agent attempts unauthorized action
**Result**: ✗ Action BLOCKED - Not in capabilities

## Protocol Guarantees

1. **Authenticity**: Only Directory-signed agents can transact
2. **Authorization**: Merchants must be registered
3. **Delegation**: User-defined spending limits enforced
4. **Revocation**: Instant certificate invalidation
5. **Capabilities**: Fine-grained permission control

## Key Security Properties

- **No unauthorized agents**: Certificate verification prevents fake agents
- **No limit violations**: Delegation service enforces spending caps
- **No revoked certificates**: Real-time revocation checking
- **No capability escalation**: Strict capability enforcement
- **No replay attacks**: Transaction tracking and validation

## Files

- `entities.py` - Core entity implementations with cryptography
- `complete_demo.py` - Full protocol demonstration
- `requirements.txt` - Python dependencies

## Dependencies

- `cryptography` - RSA signing and verification
- `colorama` - Terminal output formatting
