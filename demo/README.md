# Agentic Purchase Workflow Demo

Interactive demonstration of the secure banking agent purchase sequence.

## Quick Start

```bash
cd demo
python demo_cli.py
```

## Demo Flow

1. **Authentication**: CallSign biometric simulation
2. **Product Search**: Multi-retailer search (Amazon, BestBuy, Target)
3. **AI Recommendation**: Value-based product analysis
4. **Secure Purchase**: Bank authorization + payment processing
5. **Order Confirmation**: Bank-verified expedited processing

## Architecture

- `mobile_agent.py` - Main orchestrator
- `mcp_servers.py` - Mock retailer & bank MCPs
- `auth_service.py` - CallSign authentication
- `payment_protocol.py` - Google Payment Protocol
- `models.py` - Data structures

## Key Features

- Biometric authentication simulation
- Multi-retailer product comparison
- Spending limit validation
- Step-up payment authentication
- Bank-verified trusted payments