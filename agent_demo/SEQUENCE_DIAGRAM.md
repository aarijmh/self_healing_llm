# Visual Sequence Diagrams

## Complete Purchase Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as Web UI
    participant Backend as Flask Backend
    participant CallSign
    participant BankMCP
    participant HSM
    participant Amazon
    participant BestBuy
    participant Target
    participant Payment
    participant Bank

    Note over User,Bank: Complete Purchase Flow Demo

    %% Authentication
    User->>UI: Click "Execute Purchase"
    UI->>Backend: POST /api/demo/purchase
    Backend->>CallSign: authenticate_biometric()
    CallSign-->>Backend: Auth token (15min TTL)
    Backend->>UI: step_update: authentication completed
    
    %% Multi-Merchant Search
    par Search All Merchants
        Backend->>Amazon: search_products("laptop", max=2000)
        Backend->>BestBuy: search_products("laptop", max=2000)
        Backend->>Target: search_products("laptop", max=2000)
    end
    
    Amazon-->>Backend: Dell XPS 15 - $1,899
    BestBuy-->>Backend: MacBook Air M2 - $1,799
    Target-->>Backend: HP Spectre x360 - $1,699
    
    Backend->>UI: step_update: products found
    UI->>User: Display 3 products
    
    %% Transaction Authorization
    Backend->>BankMCP: authorize_purchase(1799, "bestbuy")
    BankMCP->>BankMCP: Check spending limits
    BankMCP-->>Backend: Authorized (txn_id)
    Backend->>UI: step_update: transaction authorized
    
    %% Payment Authentication
    Backend->>CallSign: authenticate_payment()
    CallSign-->>Backend: Payment auth token
    Backend->>UI: step_update: payment authenticated
    
    %% Token Generation
    Backend->>HSM: generate_payment_token(1799)
    HSM-->>Backend: Encrypted token (5min TTL)
    Backend->>UI: step_update: token generated
    
    %% Payment Processing
    Backend->>Payment: process_agent_payment()
    Payment->>BestBuy: payment_request(1799)
    BestBuy-->>Payment: payment_accepted
    Payment->>BankMCP: process_payment()
    BankMCP->>Bank: execute_transaction(1799)
    Bank-->>BankMCP: Transaction completed
    BankMCP-->>Payment: Payment confirmed
    Payment-->>Backend: Payment successful
    Backend->>UI: step_update: payment completed
    
    %% Order Creation
    Backend->>BestBuy: create_order(MacBook Air M2)
    BestBuy-->>Backend: Order confirmed (expedited)
    Backend->>UI: step_update: order created
    
    %% Completion
    Backend->>UI: step_update: purchase complete
    UI->>User: Show success summary
```

## Setup & Registration Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as Web UI
    participant Backend as Flask Backend
    participant Bank
    participant CallSign
    participant HSM
    participant BankMCP

    Note over User,BankMCP: App Download & Agent Registration

    User->>UI: Click "Setup & Registration"
    UI->>Backend: POST /api/demo/setup
    
    %% Identity Verification
    Backend->>Bank: verify_identity(account, ssn)
    Bank->>Bank: KYC validation
    Bank-->>Backend: Identity verified
    Backend->>UI: step_update: identity verified
    
    %% Device Registration
    Backend->>Backend: Register device
    Backend->>UI: step_update: device registered
    
    %% Biometric Enrollment
    Backend->>CallSign: authenticate_biometric("face")
    CallSign->>CallSign: Create biometric template
    CallSign-->>Backend: Enrollment complete
    Backend->>UI: step_update: biometric enrolled
    
    %% Agent Registration
    Backend->>HSM: generate_agent_certificate()
    HSM->>HSM: Create key pair
    HSM-->>Backend: Dual-signed certificate
    Backend->>BankMCP: register_agent()
    BankMCP->>BankMCP: Register MCPs (Amazon, BestBuy, Target)
    BankMCP-->>Backend: Agent registered
    Backend->>UI: step_update: agent ready
    
    UI->>User: "Agent is ready!"
```

## Delegation Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as Web UI
    participant Backend as Flask Backend
    participant CallSign
    participant BankMCP

    Note over User,BankMCP: Delegation of Shopping Authority

    User->>UI: Click "Delegate Authority"
    UI->>Backend: POST /api/demo/delegate
    
    %% Enhanced Authentication
    Backend->>CallSign: validate_delegation()
    CallSign->>CallSign: Biometric + PIN verification
    CallSign-->>Backend: Delegation authorized
    Backend->>UI: step_update: delegation auth complete
    
    %% Register Delegation
    Backend->>BankMCP: register_delegation(limit=5000, categories)
    BankMCP->>BankMCP: Create delegation record
    BankMCP-->>Backend: Delegation active
    Backend->>UI: step_update: delegation registered
    
    UI->>User: "Delegation active - $5,000 limit"
```

## Security Checkpoints

```mermaid
graph TD
    A[User Request] --> B{Biometric Auth}
    B -->|Success| C{Delegation Check}
    B -->|Fail| Z[Reject]
    
    C -->|Authorized| D{Spending Limit}
    C -->|Not Authorized| Z
    
    D -->|Within Limit| E{Step-up Auth}
    D -->|Exceeds Limit| Z
    
    E -->|Confirmed| F{Generate Token}
    E -->|Fail| Z
    
    F --> G{Process Payment}
    G -->|Success| H[Order Created]
    G -->|Fail| Z
    
    H --> I[Complete]
    Z --> J[User Notified]
    
    style B fill:#e1f5ff
    style C fill:#e1f5ff
    style D fill:#e1f5ff
    style E fill:#e1f5ff
    style F fill:#fff4e1
    style G fill:#e8f5e9
    style H fill:#e8f5e9
    style I fill:#c8e6c9
    style Z fill:#ffebee
```

## Data Flow Architecture

```mermaid
graph LR
    subgraph Frontend
        A[Web Browser]
        B[Socket.IO Client]
    end
    
    subgraph Backend
        C[Flask API]
        D[WebSocket Server]
        E[Mock Services]
    end
    
    subgraph Mocks
        F[CallSign]
        G[Bank MCP]
        H[HSM]
        I[Bank Core]
        J[Merchants]
        K[Payment]
    end
    
    A -->|HTTP| C
    B -->|WebSocket| D
    C --> E
    D --> E
    E --> F
    E --> G
    E --> H
    E --> I
    E --> J
    E --> K
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#f3e5f5
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#fff3e0
    style G fill:#fff3e0
    style H fill:#fff3e0
    style I fill:#fff3e0
    style J fill:#fff3e0
    style K fill:#fff3e0
```

## Entity Interaction Map

```mermaid
graph TB
    User[User/Client]
    
    subgraph Authentication Layer
        CS[CallSign Auth]
    end
    
    subgraph Coordination Layer
        BM[Bank MCP Server]
    end
    
    subgraph Security Layer
        HSM[Hardware Security Module]
    end
    
    subgraph Banking Layer
        BC[Bank Core System]
    end
    
    subgraph Merchant Layer
        AM[Amazon MCP]
        BB[BestBuy MCP]
        TG[Target MCP]
    end
    
    subgraph Payment Layer
        PP[Payment Protocol]
    end
    
    User --> CS
    User --> BM
    CS --> BM
    BM --> HSM
    BM --> BC
    BM --> AM
    BM --> BB
    BM --> TG
    BM --> PP
    PP --> AM
    PP --> BB
    PP --> TG
    PP --> BC
    
    style User fill:#e1f5fe
    style CS fill:#f3e5f5
    style BM fill:#e8f5e9
    style HSM fill:#fff3e0
    style BC fill:#fce4ec
    style AM fill:#ffebee
    style BB fill:#e3f2fd
    style TG fill:#ffebee
    style PP fill:#f1f8e9
```

## Token Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Requested: User initiates payment
    Requested --> Generated: HSM creates token
    Generated --> Active: Token issued (5min TTL)
    Active --> Used: Payment processed
    Active --> Expired: 5 minutes elapsed
    Used --> Logged: Audit trail
    Expired --> Logged: Audit trail
    Logged --> [*]
    
    note right of Generated
        Encrypted token
        Time-limited
        Single-use
    end note
    
    note right of Active
        Valid for 5 minutes
        Cannot be reused
        Merchant-specific
    end note
```

## Demo State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle: Page loaded
    Idle --> Setup: Click "Setup & Registration"
    Setup --> SetupComplete: All steps done
    SetupComplete --> Idle: Reset
    
    Idle --> Delegation: Click "Delegate Authority"
    Delegation --> DelegationComplete: Delegation registered
    DelegationComplete --> Idle: Reset
    
    Idle --> Purchase: Click "Execute Purchase"
    Purchase --> Searching: Multi-merchant search
    Searching --> Authorizing: Products found
    Authorizing --> Processing: Transaction approved
    Processing --> Completing: Payment successful
    Completing --> PurchaseComplete: Order created
    PurchaseComplete --> Idle: Reset
    
    Idle --> CompleteDemo: Click "Run Complete Demo"
    CompleteDemo --> Setup
    SetupComplete --> Delegation
    DelegationComplete --> Purchase
    
    note right of Setup
        8 seconds
        6 steps
    end note
    
    note right of Purchase
        10 seconds
        9 steps
    end note
```

---

## How to Use These Diagrams

### During Presentation

1. **Show Complete Purchase Flow** first
   - Demonstrates end-to-end process
   - Highlights all entities
   - Shows parallel processing

2. **Explain Security Checkpoints**
   - Visual representation of security layers
   - Easy for non-technical audience

3. **Show Entity Interaction Map**
   - Architecture overview
   - System components
   - Integration points

### For Technical Discussions

1. **Data Flow Architecture**
   - Frontend/Backend separation
   - WebSocket real-time updates
   - Mock service layer

2. **Token Lifecycle**
   - Security model
   - Time-limited credentials
   - Audit trail

3. **State Machine**
   - Demo flow logic
   - User interactions
   - State transitions

---

## Rendering Options

### In Markdown Viewers
- GitHub
- GitLab
- VS Code (with Mermaid extension)
- Obsidian

### Export to Images
```bash
# Using mermaid-cli
npm install -g @mermaid-js/mermaid-cli
mmdc -i SEQUENCE_DIAGRAM.md -o diagrams.pdf
```

### Live Rendering
- Mermaid Live Editor: https://mermaid.live
- Copy/paste diagrams for editing

---

**Use these diagrams to enhance your client presentation!**
