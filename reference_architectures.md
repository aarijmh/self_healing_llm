# Reference Architectures and Protocols

## Reference Architectures

### 1. Open Banking Architecture (PSD2/Open Banking UK)
- Multi-party API ecosystem with regulated third-party access
- Strong Customer Authentication (SCA) requirements
- Consent management and delegation frameworks
- Similar to MCP server federation approach

### 2. FIDO Alliance Authentication Framework
- Biometric authentication standards (FIDO2/WebAuthn)
- Hardware security key integration
- Matches CallSign biometric authentication layer

### 3. OAuth 2.0 / OpenID Connect
- Token-based authorization with time-limited access
- Delegation and consent management
- 15-minute TTL tokens follow OAuth patterns

## Relevant Protocols

### 1. Model Context Protocol (MCP)
- Standardizes tool discovery and execution
- Bank/E-commerce MCP servers follow this specification

### 2. Payment Card Industry (PCI) Standards
- **PCI DSS**: Data security for card processing
- **3D Secure 2.0**: Strong authentication for CNP transactions
- **EMV 3DS**: Biometric authentication as SCA method

### 3. ISO 20022 Financial Messaging
- Standard for financial message formats
- Could standardize agent-to-agent payment messages
- Used in real-time payment systems globally

### 4. W3C Payment Request API
- Browser-based payment standardization
- Similar to Google Payment Protocol integration
- Supports multiple payment methods and authentication

## Security Frameworks

### 1. NIST Cybersecurity Framework
- Risk management and authentication controls
- Aligns with HSM and biometric security layers

### 2. Zero Trust Architecture (NIST SP 800-207)
- "Never trust, always verify" principle
- Matches continuous authentication approach

### 3. SWIFT Customer Security Programme (CSP)
- Multi-factor authentication requirements
- Secure messaging between financial institutions
- Relevant for bank-to-merchant communications

## Mobile Security Standards

### 1. OWASP Mobile Security
- Secure storage in device enclaves
- Runtime application self-protection
- Matches SQLCipher and secure enclave usage

### 2. Common Criteria (ISO 15408)
- Security evaluation for HSMs and mobile platforms
- Certification framework for CallSign SDK integration