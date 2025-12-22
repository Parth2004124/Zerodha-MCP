from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict
from datetime import datetime
from enum import Enum
import uuid

class TradingSignal(BaseModel):
    symbol: str
    action: Literal["BUY", "SELL"]
    quantity: int = Field(gt=0)
    order_type: Literal["MARKET", "LIMIT"] = "MARKET"
    price: Optional[float] = None
    confidence: float = 1.0
    source: str = "ai"
    timestamp: datetime = Field(default_factory=datetime.now)

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    symbol: str
    action: Literal["BUY", "SELL"]
    quantity: int
    order_type: str
    price: Optional[float]
    status: OrderStatus = OrderStatus.PENDING
    avg_price: Optional[float] = None

class Position(BaseModel):
    symbol: str
    quantity: int
    avg_price: float
    last_price: float

    @property
    def unrealized_pnl(self):
        return (self.last_price - self.avg_price) * self.quantity

class Portfolio(BaseModel):
    positions: Dict[str, Position] = {}
    cash: float = 1_000_000.0

    def update_position(self, pos: Position):
        self.positions[pos.symbol] = pos

    def total_pnl(self):
        return sum(p.unrealized_pnl for p in self.positions.values())
