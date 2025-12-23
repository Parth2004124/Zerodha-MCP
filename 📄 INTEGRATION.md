
📄 INTEGRATION.md
Purpose:
How APIs connect.
How Claude connects.
Where keys go.
What changes when you move from Mock → Zerodha.
Copy–paste this as-is.

1️⃣ What this project is (in one line)
This is an MCP server that lets Claude or any LLM:
read portfolio state
send trading signals
execute trades via a broker adapter (Mock now, Zerodha later)
Claude never talks to Zerodha directly.
Claude talks to this server.

2️⃣ Current Architecture (Mental Model)
Claude
  ↓ MCP
server.py  (MCP entrypoint)
  ↓
broker.py  (MockBroker / KiteBroker)
  ↓
Zerodha Kite API (future)

Finance logic lives in models.py
Config + secrets live in config.py

3️⃣ How Claude connects (MCP config)
This is what goes into Claude’s MCP config:
{
  "mcpServers": {
    "zerodha": {
      "command": "python",
      "args": ["src/server.py"]
    }
  }
}

What this does:
Claude starts your MCP server locally
Claude discovers tools automatically (execute_trade)
Claude can now send structured trading signals
No REST. No webhooks. No nonsense.

4️⃣ How Claude uses the tool (example)
Claude will internally call:
{
  "name": "execute_trade",
  "arguments": {
    "symbol": "SBIN",
    "action": "BUY",
    "quantity": 10,
    "confidence": 0.82
  }
}

Your server:
validates the signal
places the order via broker
updates portfolio
returns P&L state
Claude never sees API keys. Ever.

5️⃣ Where API keys go (IMPORTANT)
Create a .env file (never commit this):
KITE_API_KEY=xxxxx
KITE_API_SECRET=xxxxx
KITE_ACCESS_TOKEN=xxxxx
BROKER_TYPE=kite

config.py auto-loads this using pydantic-settings.
For now:
BROKER_TYPE=mock

When ready:
BROKER_TYPE=kite

Zero Claude-side changes required.

6️⃣ Switching from Mock → Zerodha Kite
Steps (future):
Create KiteBroker inside broker.py
Implement:
place_order
get_positions
Use official Kite Connect SDK
Toggle BROKER_TYPE=kite
Everything else stays untouched.
This separation is intentional.

7️⃣ What NOT to do
❌ Do not hardcode API keys
❌ Do not let Claude call Zerodha directly
❌ Do not mix strategy logic with broker logic
❌ Do not turn this into a UI project
This is backend Fintech infrastructure.

8️⃣ What this enables later
Risk engine (pre-trade checks)
Strategy marketplace
Multi-broker execution
Paper trading vs live trading toggle
AI-controlled portfolio rebalancing
All without rewriting core logic.

