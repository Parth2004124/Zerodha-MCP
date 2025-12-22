from fastmcp import MCPServer
from models import TradingSignal, Portfolio, Order
from broker import MockBroker
from config import logger

server = MCPServer("zerodha-mcp")
portfolio = Portfolio()
broker = MockBroker()

@server.tool()
async def execute_trade(signal: TradingSignal):
    """
    Execute a trade from an AI signal
    """
    logger.info("signal_received", signal=signal.dict())

    order = Order(
        symbol=signal.symbol,
        action=signal.action,
        quantity=signal.quantity,
        order_type=signal.order_type,
        price=signal.price
    )

    position = await broker.place_order(order)
    portfolio.update_position(position)

    return {
        "status": "success",
        "portfolio_pnl": portfolio.total_pnl(),
        "positions": list(portfolio.positions.keys())
    }

if __name__ == "__main__":
    server.run()
