# CallSign Agent Directory Architecture (A2P Protocol)

## Overview
This architecture implements a secure agent-to-payment system based on Google Cloud's A2P protocol, with CallSign Agent Directory as the central trust anchor.

## Key Components

### 1. CallSign Agent Directory (Trust Anchor)
- **Purpose**: Authenticate merchants and sign their agents
- **Responsibilities**:
  - Merchant identity verification
  - Agent certificate issuance (dual-signed)
  - Certificate revocation management
  - Real-time validation endpoint

### 2. Trust Chain
```
CallSign Directory → Merchant (Amazon) → Agent → User
```

## Six-Phase Flow

### Phase 1: Merchant Registration
- Merchant proves identity (business license, domain ownership)
- Directory issues merchant certificate + signing key
- Merchant can now issue agents with Directory's blessing

### Phase 2: Agent Registration & Signing
- Merchant develops agent with defined capabilities
- Directory validates and dual-signs agent certificate
- Certificate contains:
  - Agent ID & Merchant ID
  - Capabilities (payment, search, checkout)
  - Expiration date
  - Revocation endpoint

### Phase 3: User Onboarding
- User downloads merchant app (contains signed agent)
- Agent certificate validated against Directory
- User-agent binding established
- Delegation scope configured ($5,000 limit)

### Phase 4: First Automated Transaction
- User: "Buy laptop under $2000"
- Agent validates certificate with Directory
- Automated search, selection, checkout
- Step-up auth for first payment
- Bank verifies agent certificate

### Phase 5: Subsequent Transactions
- Agent reuses stored token
- Certificate validated in real-time
- No user interaction needed (within delegation)
- Full audit trail maintained

### Phase 6: Revocation
- Directory revokes compromised agent
- All payment capabilities disabled
- User notified to update app

## Security Features

### Agent Certificate Structure
```json
{
  "agent_id": "amazon-shopping-agent-v2",
  "merchant_id": "amazon.com",
  "directory_signature": "...",
  "merchant_signature": "...",
  "capabilities": ["search", "checkout", "payment"],
  "spending_limit": 5000,
  "expiration": "2025-12-31",
  "revocation_endpoint": "https://directory.callsign.com/revoke"
}
```

### Trust Validation Points
1. **App Download**: Certificate embedded in app
2. **First Launch**: Directory validates signatures
3. **User Registration**: User-agent binding created
4. **Every Transaction**: Real-time certificate check
5. **Payment Processing**: Bank validates certificate

## A2P Protocol Alignment

| A2P Concept | Implementation |
|-------------|----------------|
| Agent Registry | CallSign Agent Directory |
| Agent Attestation | Dual-signed certificates |
| Delegation Framework | Spending limits + scopes |
| Payment Instrument Binding | Token vault with agent binding |
| Merchant Trust | Directory-verified merchants |
| Revocation | Real-time certificate revocation |

## Benefits

### For Users
- Automated shopping with safety guardrails
- Explicit delegation control
- Biometric step-up when needed

### For Merchants
- Trusted agent issuance
- Reduced fraud (Directory-verified)
- Faster payment processing

### For Banks
- Verifiable agent authenticity
- Clear delegation audit trail
- Reduced liability (Directory trust)

## Comparison: Before vs After

### Before (Original Diagram)
- Direct agent-to-bank trust
- No centralized agent verification
- Merchant self-signs agents
- Limited revocation capability

### After (With Agent Directory)
- Directory as trust anchor
- Centralized agent authentication
- Dual-signature verification
- Real-time revocation support
- Cross-merchant agent portability (future)

## Future Enhancements

1. **Cross-Merchant Agents**: One agent, multiple merchants
2. **Agent Marketplace**: Directory-verified third-party agents
3. **Capability Tokens**: Fine-grained permission system
4. **Federated Directories**: Multiple directories with trust relationships
5. **Agent Reputation Scoring**: Based on transaction history
