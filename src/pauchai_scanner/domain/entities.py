from dataclasses import dataclass
from decimal import Decimal

from pauchai_scanner.domain.value_objects import  TradingPair


@dataclass
class ArbitrageOpportunity:
    pair: TradingPair
    buy_exchange: str
    sell_exchange: str
    estimated_profit: Decimal
    #real_profit: Money | None = None
    #status: str = "candidate"
    #buy_url: str | None = None
    #sell_url: str | None = None
    #network: str | None = None
    #withdraw_fee: Money | None = None
    #withdraw_speed: float | None = None