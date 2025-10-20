# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Web Browser                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Frontend (index.html + app.js)                 │ │
│  │  • TailwindCSS UI                                          │ │
│  │  • Socket.IO Client                                        │ │
│  │  • Real-time Updates                                       │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend Server (Flask)                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    REST API Endpoints                       │ │
│  │  • /api/demo/setup                                         │ │
│  │  • /api/demo/delegate                                      │ │
│  │  • /api/demo/purchase                                      │ │
│  │  • /api/account                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                WebSocket Events (Socket.IO)                 │ │
│  │  • step_update (real-time process updates)                │ │
│  │  • connected/disconnected                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Internal Calls
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Mock Services Layer                         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  CallSign    │  │   Bank MCP   │  │     HSM      │         │
│  │    Mock      │  │     Mock     │  │    Mock      │         │
│  │              │  │              │  │              │         │
│  │ • Biometric  │  │ • Agent Reg  │  │ • Tokens     │         │
│  │ • Auth       │  │ • Delegation │  │ • Certs      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Bank Core   │  │  Amazon MCP  │  │  Payment     │         │
│  │    Mock      │  │     Mock     │  │  Protocol    │         │
│  │              │  │              │  │    Mock      │         │
│  │ • KYC        │  │ • Products   │  │ • Agent Pay  │         │
│  │ • Txns       │  │ • Orders     │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ BestBuy MCP  │  │  Target MCP  │                            │
│  │    Mock      │  │     Mock     │                            │
│  │              │  │              │                            │
│  │ • Products   │  │ • Products   │                            │
│  │ • Orders     │  │ • Orders     │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Setup & Registration Flow

```
User → Frontend → Backend API → Mock Services
                                      │
                                      ├─→ BankCore.verify_identity()
                                      ├─→ CallSign.authenticate_biometric()
                                      ├─→ HSM.generate_agent_certificate()
                                      └─→ BankMCP.register_agent()
                                      
Backend → WebSocket → Frontend → UI Update
```

### 2. Delegation Flow

```
User → Frontend → Backend API → Mock Services
                                      │
                                      ├─→ CallSign.validate_delegation()
                                      └─→ BankMCP.register_delegation()
                                      
Backend → WebSocket → Frontend → UI Update
```

### 3. Purchase Flow

```
User → Frontend → Backend API → Mock Services
                                      │
                                      ├─→ CallSign.authenticate_biometric()
                                      ├─→ AmazonMCP.search_products()
                                      ├─→ BestBuyMCP.search_products()
                                      ├─→ TargetMCP.search_products()
                                      ├─→ BankMCP.authorize_purchase()
                                      ├─→ HSM.generate_payment_token()
                                      ├─→ PaymentProtocol.process_payment()
                                      ├─→ BankCore.execute_transaction()
                                      └─→ MerchantMCP.create_order()
                                      
Backend → WebSocket → Frontend → UI Update
```

## Component Details

### Frontend Components

**index.html**
- Header with account balance
- Control panel with demo buttons
- Entity status dashboard
- Process flow panel
- Results panel
- Products display grid
- Transaction summary

**app.js**
- Socket.IO client initialization
- API call functions
- Real-time event handlers
- UI update functions
- State management

### Backend Components

**Flask Application**
- REST API endpoints
- WebSocket server (Socket.IO)
- Request routing
- Error handling

**Mock Services**
- `CallSignMock`: Biometric authentication
- `HSMMock`: Token and certificate generation
- `BankCoreMock`: Identity verification and transactions
- `BankMCPMock`: Agent registration and delegation
- `MerchantMCPMock`: Product search and orders
- `PaymentProtocolMock`: Payment processing

### Data Stores (In-Memory)

```python
sessions = {}        # User sessions
transactions = {}    # Transaction history
delegations = {}     # Delegation records
USER_ACCOUNT = {}    # Account data
PRODUCT_CATALOG = {} # Product inventory
```

## Security Features

### Authentication Layers

1. **Biometric Authentication**
   - Face recognition
   - Voice pattern
   - Behavioral analysis
   - Confidence scoring (95-99%)

2. **Token-Based Security**
   - Auth tokens: 15-minute TTL
   - Payment tokens: 5-minute TTL
   - Encrypted transmission
   - Single-use tokens

3. **Certificate-Based Trust**
   - Dual-signed certificates
   - Public/private key pairs
   - HSM-generated
   - 365-day expiry

4. **Delegation Controls**
   - Spending limits
   - Category restrictions
   - Time-based validity
   - Revocable permissions

### Data Protection

- All tokens are truncated in UI (first 20 chars)
- Sensitive data never logged
- In-memory storage (no persistence)
- CORS enabled for localhost only

## Technology Stack

### Backend
- **Python 3.8+**: Core language
- **Flask 3.0.0**: Web framework
- **Flask-CORS 4.0.0**: Cross-origin support
- **Flask-SocketIO 5.3.5**: WebSocket support
- **Eventlet 0.33.3**: Async processing

### Frontend
- **HTML5**: Structure
- **TailwindCSS**: Styling (CDN)
- **Vanilla JavaScript**: Logic
- **Socket.IO Client 4.5.4**: WebSocket (CDN)
- **Font Awesome 6.4.0**: Icons (CDN)

### Communication
- **REST API**: HTTP/JSON
- **WebSocket**: Real-time updates
- **CORS**: Cross-origin requests

## Scalability Considerations

### Current Implementation (Demo)
- Single-threaded Flask server
- In-memory data storage
- No persistence
- Localhost only

### Production Recommendations
- **Backend**: Gunicorn/uWSGI with multiple workers
- **Database**: PostgreSQL for persistence
- **Cache**: Redis for session management
- **Queue**: Celery for async tasks
- **Load Balancer**: Nginx/HAProxy
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK stack

## Performance Metrics

### Simulated Delays (Realistic)
- Biometric auth: 500ms
- Identity verification: 600ms
- Product search: 600ms per merchant
- Token generation: 400ms
- Transaction processing: 700ms

### Real-World Targets
- Total setup time: <2 minutes
- Delegation: <5 seconds
- Purchase flow: <10 seconds
- API response: <100ms
- WebSocket latency: <50ms

## Deployment Architecture (Production)

```
                    ┌─────────────┐
                    │   CDN       │
                    │  (Static)   │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Load        │
                    │ Balancer    │
                    └─────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Backend  │    │ Backend  │    │ Backend  │
    │ Server 1 │    │ Server 2 │    │ Server 3 │
    └──────────┘    └──────────┘    └──────────┘
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    ┌─────────────┐
                    │  Database   │
                    │ (PostgreSQL)│
                    └─────────────┘
                           │
                    ┌─────────────┐
                    │   Redis     │
                    │  (Cache)    │
                    └─────────────┘
```

## File Structure

```
agent_demo/
├── backend/
│   ├── app.py                 # Main Flask application
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html            # Main UI
│   └── app.js                # Frontend logic
├── README.md                 # Full documentation
├── QUICK_START.md            # Quick start guide
├── PRESENTATION_GUIDE.md     # Client presentation guide
├── ARCHITECTURE.md           # This file
├── start_demo.bat            # Windows launcher
└── start_demo.sh             # Linux/Mac launcher
```

## API Reference

### REST Endpoints

#### GET /api/health
Health check endpoint
```json
Response: {
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### POST /api/demo/setup
Initialize demo with app download and setup
```json
Response: {
  "success": true,
  "message": "Demo setup completed",
  "agent_id": "AGENT_abc123"
}
```

#### POST /api/demo/delegate
Delegate shopping authority
```json
Request: {
  "spending_limit": 5000,
  "categories": ["electronics", "home"]
}
Response: {
  "success": true,
  "delegation": {
    "delegation_id": "DEL_xyz789",
    "spending_limit": 5000,
    "categories": ["electronics", "home"],
    "status": "active"
  }
}
```

#### POST /api/demo/purchase
Execute purchase flow
```json
Request: {
  "query": "laptop",
  "max_price": 2000
}
Response: {
  "success": true,
  "product": {...},
  "order": {...},
  "transaction": {...}
}
```

#### GET /api/account
Get account status
```json
Response: {
  "account_number": "****1234",
  "balance": 15000.00,
  "daily_limit": 5000.00,
  "spent_today": 0.00,
  "name": "John Doe"
}
```

### WebSocket Events

#### Client → Server
- `connect`: Initial connection
- `disconnect`: Client disconnect

#### Server → Client
- `connected`: Connection confirmation
- `step_update`: Process step update
  ```json
  {
    "step": "authentication",
    "status": "completed",
    "data": {...},
    "timestamp": "2024-01-01T12:00:00"
  }
  ```

## Extension Points

### Adding New Merchants
1. Add products to `PRODUCT_CATALOG` in `app.py`
2. Add entity box in `index.html`
3. Add search step in purchase flow
4. Update entity highlighting in `app.js`

### Adding New Authentication Methods
1. Add method to `CallSignMock` class
2. Add step in setup/purchase flow
3. Update UI to display new method

### Adding Error Scenarios
1. Add error conditions in mock services
2. Emit error events via WebSocket
3. Handle in frontend with error UI

### Persistence Layer
1. Replace in-memory dicts with database models
2. Add SQLAlchemy ORM
3. Create migration scripts
4. Update mock services to use DB

---

**Last Updated**: 2024
**Version**: 1.0.0
