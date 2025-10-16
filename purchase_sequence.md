# Complete User Lifecycle: App Download to Purchase

## Full Lifecycle Flow

```mermaid
sequenceDiagram
    participant User
    participant AppStore as App Store
    participant MobileApp as Mobile Banking App
    participant CallSign as CallSign Auth
    participant BankMCP as Bank MCP Server
    participant HSM as Hardware Security Module
    participant Bank as Bank Core System
    participant AmazonMCP as Amazon MCP Server
    participant BestBuyMCP as BestBuy MCP Server
    participant TargetMCP as Target MCP Server
    participant PaymentProtocol as Google Payment Protocol

    Note over User, PaymentProtocol: Complete Lifecycle: Download → Authentication → Delegation → Multi-Shopper Purchase

    %% App Download & Installation
    User->>AppStore: Search "SecureBank AI Agent"
    AppStore-->>User: App listing with bank verification badge
    User->>AppStore: Download & Install app
    AppStore->>MobileApp: Install banking app with CallSign SDK
    MobileApp-->>User: "Welcome to SecureBank AI Agent"

    %% Initial Setup & Identity Verification
    User->>MobileApp: "Set up my account"
    MobileApp->>User: "Please enter your account number and SSN"
    User->>MobileApp: Provide account credentials
    MobileApp->>Bank: Verify customer identity
    Bank->>Bank: KYC validation & risk assessment
    Bank-->>MobileApp: Identity verified

    %% Device Registration & Biometric Enrollment
    MobileApp->>CallSign: Initialize device fingerprinting
    CallSign->>CallSign: Collect device characteristics
    CallSign-->>MobileApp: Device fingerprint created
    MobileApp->>User: "Please complete biometric enrollment"
    User->>CallSign: Face scan enrollment
    User->>CallSign: Voice pattern enrollment
    CallSign->>CallSign: Create biometric templates
    CallSign-->>MobileApp: Biometric enrollment complete

    %% Agent Registration & MCP Discovery
    MobileApp->>BankMCP: Request agent registration
    BankMCP->>BankMCP: Register shopping MCPs (Amazon, BestBuy, Target, etc.)
    BankMCP->>HSM: Generate agent certificate with shopping capabilities
    HSM->>HSM: Create public/private key pair
    HSM-->>BankMCP: Agent certificate with dual signatures
    BankMCP-->>MobileApp: Agent credentials & registered MCP endpoints
    MobileApp->>MobileApp: Store credentials in secure enclave
    MobileApp-->>User: "✅ Your SecureBank AI Agent is ready with shopping capabilities!"

    %% User Delegation to Agent
    User->>MobileApp: "I want to delegate shopping decisions to you"
    MobileApp->>CallSign: Enhanced delegation authentication
    CallSign->>User: "Confirm delegation with biometric + PIN"
    User->>CallSign: Face scan + PIN entry
    CallSign-->>MobileApp: Delegation authorized
    MobileApp->>BankMCP: register_delegation(spending_limit=5000, categories=["electronics", "home"])
    BankMCP-->>MobileApp: Delegation registered with limits
    MobileApp-->>User: "✅ Delegation active. I can shop for electronics up to $5000 on your behalf"

    Note over User, PaymentProtocol: === 30 Days Later: User Makes First Purchase ===

    %% Daily Authentication
    User->>MobileApp: Open app
    MobileApp->>CallSign: Continuous authentication check
    CallSign->>CallSign: Validate face, voice, behavior patterns
    CallSign-->>MobileApp: Authentication successful
    MobileApp-->>User: "Good morning! How can I help you today?"

    %% User Instructions to Banking Agent
    User->>MobileApp: "I need a laptop for work under $2000"
    MobileApp->>MobileApp: Parse intent & check delegation authority
    MobileApp->>BankMCP: Validate session & get fresh token
    BankMCP-->>MobileApp: Session token (15min TTL)

    %% Multi-Shopper Recommendations
    MobileApp->>AmazonMCP: search_products(query="work laptop", max_price=2000)
    MobileApp->>BestBuyMCP: search_products(query="work laptop", max_price=2000)
    MobileApp->>TargetMCP: search_products(query="work laptop", max_price=2000)
    
    AmazonMCP-->>MobileApp: Dell XPS 15 - $1,899
    BestBuyMCP-->>MobileApp: MacBook Air M2 - $1,799
    TargetMCP-->>MobileApp: HP Spectre x360 - $1,699
    
    MobileApp->>MobileApp: Analyze options & user preferences
    MobileApp-->>User: "I found 3 great options:\n1. Dell XPS 15 ($1,899) - Amazon\n2. MacBook Air M2 ($1,799) - BestBuy\n3. HP Spectre ($1,699) - Target\nBased on your work needs, I recommend the MacBook Air. Shall I proceed?"
    User->>MobileApp: "Yes, get the MacBook from BestBuy"

    %% Transaction Authorization
    MobileApp->>BankMCP: authorize_purchase(amount=1899, merchant="amazon")
    BankMCP->>BankMCP: Validate dual-signed certificate
    BankMCP->>BankMCP: Check spending limits & fraud rules
    BankMCP-->>MobileApp: Pre-authorization approved

    %% Step-up Authentication for Payment
    MobileApp->>CallSign: Request payment authentication
    CallSign->>User: "Please confirm payment with face scan"
    User->>CallSign: Face scan for payment confirmation
    CallSign->>CallSign: Enhanced biometric validation
    CallSign-->>MobileApp: Payment authorization granted

    %% Secure Payment Processing
    MobileApp->>BankMCP: get_payment_credentials(txn_id)
    BankMCP->>HSM: Generate payment token
    HSM-->>BankMCP: Encrypted payment token (5min TTL)
    BankMCP-->>MobileApp: Secure payment credentials

    %% Trusted Banking Agent Payment
    Note over MobileApp, Bank: Banking agent provides trusted payment channel
    MobileApp->>BankMCP: initiate_trusted_payment(merchant="bestbuy", amount=1799)
    BankMCP->>BankMCP: Validate delegation authority & spending limits
    BankMCP->>PaymentProtocol: secure_agent_payment(bank_guaranteed=true)
    PaymentProtocol->>BestBuyMCP: payment_request(amount=1799, bank_verified=true)
    BestBuyMCP->>BestBuyMCP: Accept payment (higher trust due to bank agent)
    BestBuyMCP-->>PaymentProtocol: payment_accepted
    PaymentProtocol->>BankMCP: process_payment
    BankMCP->>Bank: Execute transaction with agent delegation
    Bank->>Bank: Debit account & transfer funds
    Bank-->>BankMCP: Transaction completed

    %% Order Completion with Banking Trust
    BankMCP-->>PaymentProtocol: Payment confirmed
    PaymentProtocol-->>BestBuyMCP: Payment successful
    BestBuyMCP->>BestBuyMCP: Create order with expedited processing
    BestBuyMCP-->>MobileApp: Order confirmation with bank trust benefits
    MobileApp-->>User: "✅ MacBook Air M2 ordered from BestBuy! Bank-verified payment = faster processing. Delivery tomorrow! Order #BB_456"

    %% Post-Transaction
    BankMCP->>BankMCP: Update user spending patterns
    BankMCP->>BankMCP: Log transaction for compliance
    MobileApp->>User: Push notification with receipt
```

# Purchase Transaction Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant MobileAgent as Mobile Agent
    participant CallSign as CallSign Auth
    participant BankMCP as Bank MCP Server
    participant AmazonMCP as Amazon MCP Server
    participant PaymentProtocol as Google Payment Protocol
    participant HSM as Hardware Security Module
    participant Bank as Bank Core System

    Note over User, Bank: User Purchase Request: "Buy a laptop under $2000 from Amazon"

    %% Authentication Phase
    User->>MobileAgent: "Buy laptop under $2000 from Amazon"
    MobileAgent->>CallSign: Biometric authentication request
    CallSign->>CallSign: Face/voice/behavior validation
    CallSign-->>MobileAgent: Authentication token (15min TTL)
    
    %% Product Search Phase
    MobileAgent->>AmazonMCP: search_products(query="laptop", max_price=2000)
    AmazonMCP->>AmazonMCP: Search product catalog
    AmazonMCP-->>MobileAgent: Product list with prices
    MobileAgent-->>User: "Found 5 laptops. Dell XPS 15 for $1,899?"
    User->>MobileAgent: "Yes, buy the Dell XPS"
    
    %% Transaction Authorization Phase
    MobileAgent->>BankMCP: authorize_purchase(amount=1899, merchant="amazon")
    BankMCP->>BankMCP: Validate dual-signed certificate
    BankMCP->>BankMCP: Check spending limits & merchant whitelist
    BankMCP-->>MobileAgent: Authorization approved (txn_id: AUTH_456)
    
    %% Payment Processing Phase
    MobileAgent->>CallSign: Step-up authentication for payment
    CallSign->>User: Additional biometric confirmation
    User->>CallSign: Biometric confirmation
    CallSign-->>MobileAgent: Payment authorization token
    
    %% Secure Credential Retrieval
    MobileAgent->>BankMCP: get_payment_credentials(txn_id=AUTH_456)
    BankMCP->>HSM: Generate time-limited payment token
    HSM-->>BankMCP: Encrypted payment token (5min TTL)
    BankMCP-->>MobileAgent: Secure payment credentials
    
    %% Agent-to-Agent Payment Protocol
    MobileAgent->>PaymentProtocol: initiate_agent_payment(merchant_agent="amazon_agent")
    PaymentProtocol->>AmazonMCP: payment_request(amount=1899, currency="USD")
    AmazonMCP-->>PaymentProtocol: payment_accepted
    PaymentProtocol->>BankMCP: process_agent_payment(google_payment_token)
    
    %% Bank Processing
    BankMCP->>Bank: Execute payment transaction
    Bank->>Bank: Debit user account
    Bank->>Bank: Transfer to Amazon merchant account
    Bank-->>BankMCP: Transaction completed (txn_ref: PAY_789)
    
    %% Order Completion
    BankMCP-->>PaymentProtocol: Payment confirmed
    PaymentProtocol-->>AmazonMCP: Payment successful
    AmazonMCP->>AmazonMCP: Create order & initiate shipping
    AmazonMCP-->>MobileAgent: Order confirmation (order_id: ORD_123)
    
    %% User Notification
    MobileAgent-->>User: "✅ Purchase complete! Dell XPS 15 ordered for $1,899. Order #ORD_123. Estimated delivery: 2 days"
    
    %% Audit & Compliance
    Note over BankMCP, Bank: All transactions logged for compliance
    BankMCP->>BankMCP: Log transaction details
    BankMCP->>BankMCP: Update spending limits
    BankMCP->>BankMCP: Fraud monitoring check
```

## Key Security Checkpoints

1. **Initial Authentication**: CallSign biometric validation
2. **Transaction Authorization**: Dual-signed certificate + spending limits
3. **Payment Confirmation**: Step-up biometric authentication
4. **Credential Security**: HSM-generated time-limited tokens
5. **Agent Protocol**: Google Payment Protocol for secure agent communication
6. **Audit Trail**: Complete transaction logging for compliance

## Error Handling Scenarios

```mermaid
sequenceDiagram
    participant User
    participant MobileAgent as Mobile Agent
    participant BankMCP as Bank MCP Server
    
    Note over User, BankMCP: Error Scenario: Spending Limit Exceeded
    
    User->>MobileAgent: "Buy a $5000 laptop"
    MobileAgent->>BankMCP: authorize_purchase(amount=5000)
    BankMCP->>BankMCP: Check spending limits (daily: $2000)
    BankMCP-->>MobileAgent: Authorization denied (reason: "exceeds_daily_limit")
    MobileAgent-->>User: "❌ Purchase denied. Daily limit is $2000. Current available: $1,200"
    
    Note over User, BankMCP: Alternative: Request Approval
    
    User->>MobileAgent: "Request approval for $5000 purchase"
    MobileAgent->>BankMCP: request_approval(amount=5000, reason="laptop_purchase")
    BankMCP-->>MobileAgent: Approval request submitted (approval_id: APR_789)
    MobileAgent-->>User: "📋 Approval requested. You'll receive SMS confirmation within 5 minutes"
```