# SecureBank AI Agent - Live Demo

A comprehensive visual demonstration of the Banking AI Agent with complete purchase flow, featuring mocked entities and real-time process visualization.

## 🎯 Overview

This demo showcases the complete lifecycle of a banking AI agent from app download to purchase completion, including:

- **Authentication**: CallSign biometric authentication
- **Agent Registration**: Bank MCP server with HSM security
- **Delegation**: User delegation of shopping authority
- **Multi-Shopper Search**: Amazon, BestBuy, and Target integration
- **Secure Payment**: Google Payment Protocol with bank guarantees
- **Order Completion**: Bank-verified expedited processing

## 🏗️ Architecture

### Entities (All Mocked)

1. **CallSign Auth** - Biometric authentication service
2. **Bank MCP Server** - Central agent coordination
3. **HSM** - Hardware Security Module for token generation
4. **Bank Core System** - Transaction processing
5. **Amazon MCP** - Product search and ordering
6. **BestBuy MCP** - Product search and ordering
7. **Target MCP** - Product search and ordering
8. **Google Payment Protocol** - Agent-to-agent payment

### Technology Stack

**Backend:**
- Python 3.8+
- Flask (REST API)
- Flask-SocketIO (Real-time communication)
- Eventlet (Async processing)

**Frontend:**
- HTML5 / CSS3
- TailwindCSS (Modern UI framework)
- Vanilla JavaScript
- Socket.IO Client
- Font Awesome Icons

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip3 package manager
- Modern web browser (Chrome, Firefox, Edge)

### Installation

1. **Navigate to the demo folder:**
   ```bash
   cd agent_demo
   ```

2. **Activate your Python environment:**
   ```bash
   # Windows
   ..\.venv\Scripts\activate
   
   # Linux/Mac
   source ../.venv/bin/activate
   ```

3. **Install backend dependencies:**
   ```bash
   cd backend
   pip3 install -r requirements.txt
   ```

### Running the Demo

#### Option 1: Using the Startup Script (Recommended)

**Windows:**
```bash
.\start_demo.bat
```

**Linux/Mac:**
```bash
chmod +x start_demo.sh
./start_demo.sh
```

#### Option 2: Manual Start

**Terminal 1 - Backend Server:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend Server:**
```bash
cd frontend
python -m http.server 8000
```

### Access the Demo

Open your browser and navigate to:
```
http://localhost:8000
```

The backend API will be running on:
```
http://localhost:5000
```

## 🎮 Using the Demo

### Demo Control Panel

The interface provides three main demo flows:

1. **Setup & Registration**
   - App download and installation
   - Identity verification (KYC)
   - Device registration
   - Biometric enrollment (face/voice)
   - Agent registration with MCP endpoints

2. **Delegate Authority**
   - Enhanced biometric authentication
   - Delegation registration with spending limits
   - Category-based permissions

3. **Execute Purchase**
   - User authentication
   - Multi-shopper product search
   - Transaction authorization
   - Payment authentication
   - Secure payment processing
   - Order creation and confirmation

### Complete Demo Flow

Click **"Run Complete Demo"** to execute all three flows sequentially with automatic delays for better visualization.

## 📊 Features

### Real-Time Visualization

- **Process Flow Panel**: Shows each step with status (In Progress, Completed, Failed)
- **Entity Dashboard**: Highlights active entities during processing
- **Live Results**: Displays detailed JSON responses from each service
- **Product Display**: Shows products from all merchants with pricing and ratings
- **Transaction Summary**: Beautiful completion screen with order details

### Mock Services

All services are fully mocked with realistic:
- Processing delays
- Authentication tokens
- Transaction IDs
- Product catalogs
- Payment confirmations
- Order tracking

### Security Features Demonstrated

1. **Biometric Authentication**: Face and voice recognition
2. **Dual-Signed Certificates**: Agent credentials with bank verification
3. **Time-Limited Tokens**: 5-15 minute TTL for security
4. **Spending Limits**: Daily and per-transaction limits
5. **Step-Up Authentication**: Additional verification for payments
6. **HSM Token Generation**: Secure payment credential creation
7. **Audit Trail**: Complete transaction logging

## 🎨 UI Features

- **Modern Gradient Design**: Professional purple gradient theme
- **Responsive Layout**: Works on desktop and mobile
- **Smooth Animations**: Slide-in effects and transitions
- **Real-Time Updates**: WebSocket-based live updates
- **Entity Highlighting**: Visual feedback for active services
- **Status Indicators**: Color-coded step completion
- **Product Cards**: Beautiful product display with merchant branding

## 📁 Project Structure

```
agent_demo/
├── backend/
│   ├── app.py              # Flask backend with all mock services
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main UI
│   └── app.js             # Frontend logic and WebSocket handling
├── README.md              # This file
└── start_demo.bat/sh      # Startup scripts
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/app.py` to modify:

- **User Account**: `USER_ACCOUNT` dictionary (balance, limits)
- **Product Catalog**: `PRODUCT_CATALOG` dictionary
- **Processing Delays**: `time.sleep()` values in mock services
- **Port**: Default is 5000

### Frontend Configuration

Edit `frontend/app.js` to modify:

- **API URL**: `API_URL` constant (default: http://localhost:5000)
- **Demo Delays**: `sleep()` values in `runCompleteDemo()`

## 🎯 Demo Scenarios

### Scenario 1: Successful Purchase
- User requests laptop under $2000
- Agent searches 3 merchants
- Finds MacBook Air M2 at BestBuy for $1799
- Completes purchase with bank verification
- Order confirmed with expedited delivery

### Scenario 2: Spending Limit (Modify code to test)
- User requests $5000 laptop
- Exceeds daily limit of $2000
- Transaction denied
- Shows available balance

### Scenario 3: Multi-Merchant Comparison
- Searches Amazon, BestBuy, and Target
- Displays all options with pricing
- Agent recommends best option
- User confirms selection

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Activate virtual environment
- Install dependencies: `pip3 install -r requirements.txt`
- Check port 5000 is not in use

### Frontend won't connect
- Ensure backend is running first
- Check browser console for errors
- Verify API_URL in app.js matches backend
- Try disabling browser extensions

### WebSocket connection fails
- Check CORS settings in backend
- Ensure Socket.IO versions match
- Try different browser

## 🎓 For Client Presentation

### Key Talking Points

1. **Security First**: Multi-layer authentication with biometrics
2. **Bank Trust**: Dual-signed certificates enable faster processing
3. **User Control**: Delegation with spending limits and categories
4. **Multi-Merchant**: Searches multiple stores for best deals
5. **Seamless UX**: Complete flow from search to delivery
6. **Compliance**: Full audit trail and transaction logging

### Demo Tips

1. Start with "Run Complete Demo" for full flow
2. Highlight entity dashboard during processing
3. Show product comparison across merchants
4. Emphasize security checkpoints (biometric, tokens)
5. Point out bank-verified expedited processing
6. Show transaction summary with new balance

## 📝 Notes

- All services are mocked - no real transactions occur
- Product data is static for demonstration purposes
- Authentication always succeeds in demo mode
- Balances reset when page is refreshed
- WebSocket provides real-time updates without polling

## 🚀 Future Enhancements

- Add error scenarios (insufficient funds, network failures)
- Implement approval workflow for high-value purchases
- Add fraud detection visualization
- Include transaction history
- Add voice command interface
- Mobile app version

## 📄 License

This is a demonstration project for client presentation purposes.

## 👥 Support

For questions or issues with the demo, contact the development team.

---

**Built with ❤️ for SecureBank AI Agent Demonstration**
