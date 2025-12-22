# Zerodha-MCP
Repo for Zerodha mcp server
# 📈 MCP Trading Server for Zerodha Kite Connect

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

Production-ready MCP-compliant trading server for Zerodha Kite Connect API integration. Developed in Google Colab, deployable anywhere, with complete mock broker for development without API keys.

## ✨ Features

- 🤖 **MCP Protocol** - Works seamlessly with Claude and other MCP clients
- 📊 **Complete Order Management** - Full lifecycle tracking from signal to execution
- 🛡️ **Risk Management** - Configurable limits, circuit breakers, position controls
- 💼 **Portfolio Tracking** - Real-time P&L calculation and position management
- 🎭 **Mock Broker** - Realistic simulation for development without API access
- 🔌 **Kite Connect Ready** - Drop-in adapter with detailed integration guide
- 📝 **Structured Logging** - JSON logs for orders, risk events, and system operations
- ✅ **Comprehensive Tests** - 80%+ coverage with unit and integration tests

## 🚀 Quick Start

### Option 1: Google Colab (Recommended for Development)

1. **Open the Colab Notebook:**
   - [Open in Colab](https://colab.research.google.com/) and paste the notebook from `colab_notebook.md`

2. **Run Setup Cell:**
   ```python
   !pip install fastmcp pydantic sqlalchemy structlog
   # Run all cells in order
   ```

3. **Test the System:**
   ```python
   # Quick test included in notebook
   await test_system()
   ```

4. **Download & Push to GitHub:**
   ```python
   !zip -r trading-server.zip src/ tests/ docs/
   # Download ZIP and push to your GitHub repo
   ```

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/zerodha-trading-mcp.git
cd zerodha-trading-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run tests
pytest tests/ -v

# Start MCP server
python src/server.py
```

## 📁 Project Structure

```
zerodha-trading-mcp/
├── src/
│   ├── server.py              # MCP server entry point
│   ├── config.py              # Configuration management
│   ├── mcp/                   # MCP protocol handlers
│   ├── core/                  # Trading engine
│   │   ├── risk_manager.py
│   │   ├── order_manager.py
│   │   └── portfolio_tracker.py
│   ├── adapters/              # Broker adapters
│   │   ├── base.py
│   │   ├── mock_broker.py
│   │   └── kite_adapter.py    # Placeholder for Kite Connect
│   ├── models/                # Data models
│   │   ├── signal.py
│   │   ├── order.py
│   │   ├── position.py
│   │   └── portfolio.py
│   └── utils/                 # Utilities
│       └── logger.py
├── tests/                     # Test suite
│   ├── unit/
│   └── integration/
├── docs/                      # Documentation
│   ├── API.md
│   ├── SETUP.md
│   └── KITE_INTEGRATION.md
├── logs/                      # Log files (gitignored)
├── data/                      # Database (gitignored)
├── .env.example               # Environment template
├── requirements.txt
└── README.md
```

## 🎯 Usage with MCP Client

### Example: Trading with Claude

```
User: Buy 10 shares of SBIN at market price

Claude: I'll place that order for you.
[Calls place_order tool with symbol=SBIN, action=BUY, quantity=10]

Server Response:
✅ Order Submitted Successfully
- Symbol: SBIN
- Action: BUY
- Quantity: 10
- Status: SUBMITTED
Order ID: abc-123-def
```

### Available MCP Tools

1. **place_order** - Submit trading orders (BUY/SELL)
2. **get_positions** - View all open positions with P&L
3. **get_portfolio** - Complete portfolio summary
4. **cancel_order** - Cancel pending orders
5. **get_order_status** - Check specific order status
6. **get_order_history** - View past orders
7. **get_risk_metrics** - Current risk exposure and limits

## ⚙️ Configuration

Edit `.env` file to configure:

```bash
# Environment
ENVIRONMENT=development
DEBUG=true
DRY_RUN=false           # Set to true for testing without real orders

# Broker
BROKER_TYPE=mock        # Change to 'kite' when ready

# Risk Limits
MAX_POSITION_SIZE=500000.0       # ₹5 lakhs per position
MAX_TOTAL_EXPOSURE=2000000.0     # ₹20 lakhs total
MAX_POSITIONS=10                 # Max concurrent positions
MAX_DAILY_LOSS_PCT=5.0          # Circuit breaker at -5%

# Kite Connect (fill when ready)
KITE_API_KEY=your_key_here
KITE_API_SECRET=your_secret_here
KITE_ACCESS_TOKEN=
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_trading.py -v

# Run integration tests only
pytest tests/integration/ -v
```

## 📊 Mock Broker Features

The mock broker simulates realistic trading behavior:

- ✅ Random order delays (50-200ms)
- ✅ Slippage simulation (0.05-0.15%)
- ✅ Partial fill scenarios
- ✅ Order rejection cases (5% rate)
- ✅ Market price movements
- ✅ Bid-ask spreads

Perfect for development and testing without API access!

## 🔌 Kite Connect Integration

### Prerequisites

1. Zerodha trading account
2. Kite Connect API subscription (₹2000/month)
3. Create app in [Kite Connect Dashboard](https://kite.trade/)

### Integration Steps

```bash
# 1. Get API credentials
KITE_API_KEY=your_key
KITE_API_SECRET=your_secret

# 2. Update .env
BROKER_TYPE=kite

# 3. Install kiteconnect
pip install kiteconnect

# 4. Uncomment Kite adapter code
# See src/adapters/kite_adapter.py for detailed instructions

# 5. Authenticate
# Run authentication flow to get access_token

# 6. Start with dry-run
DRY_RUN=true

# 7. Test with small orders
# Place 1-share orders first

# 8. Go live
DRY_RUN=false
```

See [docs/KITE_INTEGRATION.md](docs/KITE_INTEGRATION.md) for complete guide.

## 📈 Risk Management

Built-in risk controls:

| Control | Default | Description |
|---------|---------|-------------|
| Max Position Size | ₹5,00,000 | Per symbol limit |
| Max Total Exposure | ₹20,00,000 | Portfolio limit |
| Max Positions | 10 | Concurrent positions |
| Daily Loss Limit | -5% | Circuit breaker |
| Position Concentration | 25% | Max % in single stock |

All limits are configurable via `.env`.

## 📝 Logging

Structured JSON logs in `logs/` directory:

- `orders_{date}.jsonl` - All order activity
- `risk_{date}.jsonl` - Risk check results
- `system_{date}.jsonl` - System events
- `errors_{date}.jsonl` - Error tracking

## 🛠️ Development Workflow

### Phase 1: Mock Trading (Current)
- ✅ Develop in Google Colab
- ✅ Test with mock broker
- ✅ Perfect your strategy
- ✅ Store in GitHub

### Phase 2: API Integration
- 🔶 Get Kite Connect credentials
- 🔶 Implement authentication
- 🔶 Test with paper trading
- 🔶 Small real orders

### Phase 3: Production
- ⏳ Scale up gradually
- ⏳ Monitor performance
- ⏳ Add enhancements
- ⏳ Optimize strategy

## 🚦 Status

- ✅ **Complete**: Mock trading, risk management, portfolio tracking
- 🔶 **Pending**: Kite Connect integration (requires API keys)
- ⏳ **Future**: Dashboard, advanced analytics, AI signal integration

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational purposes. Trading involves risk. Always:
- Start with small positions
- Use proper risk management
- Test thoroughly before live trading
- Never trade more than you can afford to lose

## 📧 Support

- 📖 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/YOUR_USERNAME/zerodha-trading-mcp/issues)
- 💬 [Discussions](https://github.com/YOUR_USERNAME/zerodha-trading-mcp/discussions)

## 🙏 Acknowledgments

- Built for [Model Context Protocol](https://modelcontextprotocol.io/)
- Designed for [Zerodha Kite Connect](https://kite.trade/)
- Developed with [Claude](https://claude.ai/)

---

**Ready to start trading with AI? Clone, configure, and go! 🚀**
