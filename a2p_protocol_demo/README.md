# A2P Protocol Security Demo

Complete demonstration of the Agent-to-Payment (A2P) Protocol with CallSign Gateway, showing how each entity works and how the protocol prevents malicious actors.

## Overview

This demo implements the complete A2P Protocol flow from the PlantUML diagram, demonstrating:
- All 6 phases of the protocol
- Role of each entity (Directory, Merchant, Agent, Gateway, Bank, User)
- Security mechanisms that prevent malicious attacks

## Entities

1. **Agent Directory**: Certificate authority that registers and validates merchants and agents
2. **Merchant**: Business (e.g., Amazon) that creates and deploys agents
3. **Agent**: AI assistant with specific capabilities (shopping, payment, etc.)
4. **Payment Gateway**: Validates transactions and enforces security policies
5. **Delegation Service**: Manages user-agent spending limits
6. **Bank**: Processes actual payments

## Setup

1. Activate the virtual environment:
```bash
source ../.venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Demo

### Option 1: Quick Demo (Automated)
```bash
python demo.py
```
Shows all phases with automatic progression and security demonstrations.

### Option 2: Interactive Demo (Step-by-step)
```bash
python interactive_demo.py
```
Press Enter to advance through each phase, with detailed security metrics.

### Option 3: Security Test Suite
```bash
python security_tests.py
```
Runs comprehensive unit tests validating all security mechanisms.

### Option 4: Complete Demo Runner
```bash
python run_demo.py
```
Interactive menu to choose which demo to run.

## Security Features Demonstrated

1. **Certificate-based Authentication**: Dual-signed certificates (Directory + Merchant)
2. **Delegation Limits**: User-defined spending limits enforced by protocol
3. **Certificate Revocation**: Real-time revocation list prevents compromised agents
4. **Capability-based Access Control**: Agents can only perform authorized actions
5. **Protection Against Unregistered Agents**: Only certified agents can transact
6. **Privilege Escalation Prevention**: Capabilities are cryptographically bound
7. **Replay Attack Resistance**: Unique transaction IDs and timestamps
8. **Man-in-the-Middle Protection**: Cryptographic signatures ensure integrity

## Attack Scenarios Blocked

- ❌ Malicious agents without certificates
- ❌ Certificate forgery attempts
- ❌ Delegation limit bypass
- ❌ Privilege escalation
- ❌ Revoked certificate usage
- ❌ Expired certificate usage
- ❌ Unauthorized capability execution
- ❌ Session hijacking
- ❌ Credential stuffing
- ❌ Transaction replay attacks

## Protocol Phases

### Phase 1: Merchant Registration
Merchant registers with Agent Directory and receives certificate

### Phase 2: Agent Registration & Signing
Merchant creates agent, Directory signs with dual signatures

### Phase 3: User Setup & Trust Establishment
User downloads app, establishes trust via CallSign, sets delegation limits

### Phase 4: Automated Shopping Transaction
Agent makes first purchase with full verification

### Phase 5: Subsequent Automated Transaction
Agent makes follow-up purchase with cached trust

### Phase 6: Agent Revocation Scenario
Security incident triggers certificate revocation, blocking all future transactions

## Files

- `entities.py`: Core protocol entities and cryptographic operations
- `demo.py`: Automated demonstration of all phases
- `interactive_demo.py`: Step-by-step interactive demo with metrics
- `security_tests.py`: Comprehensive security test suite
- `run_demo.py`: Main menu for running different demo modes
- `requirements.txt`: Python dependencies

## Requirements

- Python 3.8+
- cryptography library (for RSA signatures)
- colorama library (for colored terminal output)
