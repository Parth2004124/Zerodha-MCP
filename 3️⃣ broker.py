import asyncio
import random
from datetime import datetime
from typing import Dict
from models import Order, Position
from config import logger

class BrokerAdapter:
    async def place_order(self, order: Order):
        raise NotImplementedError

class MockBroker(BrokerAdapter):
    prices = {
        "SBIN": 580.0,
        "RELIANCE": 2850.0,
        "TCS": 3650.0
    }

    async def place_order(self, order: Order):
        await asyncio.sleep(random.uniform(0.1, 0.3))

        price = self.prices.get(order.symbol, 1000.0)
        slip = random.uniform(0.0005, 0.0015)

        fill_price = price * (1 + slip if order.action == "BUY" else 1 - slip)

        order.status = "FILLED"
        order.avg_price = fill_price

        logger.info(
            "order_filled",
            symbol=order.symbol,
            price=fill_price,
            qty=order.quantity
        )

        return Position(
            symbol=order.symbol,
            quantity=order.quantity if order.action == "BUY" else -order.quantity,
            avg_price=fill_price,
            last_price=fill_price
        )
