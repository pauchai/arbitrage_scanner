from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import List, NewType


ExchangeId = str  # e.g. "binance"
NetworkId = str  # e.g. "ERC20"
ContractAdress = str  # e.g. "0x..."

@dataclass(frozen=True)
class Asset:
    symbol: str        # e.g. "ETH"
#    network: NetworkId | None = None  # e.g. "ERC20"
#    contract_address: ContractAddress | None = None  # e.g. "0x..."

@dataclass(frozen=True)
class TradingPair:
    base: Asset   # e.g. ETH    
    quote: Asset  # e.g. USD

    # Factory method to create TradingPair from string "BASE/QUOTE"
    @classmethod
    def from_string(cls, pair: str) -> 'TradingPair':
        base_symbol, quote_symbol = pair.split("/")
        return cls(base=Asset(base_symbol), quote=Asset(quote_symbol))

    # Method to get string representation "BASE/QUOTE"
    def symbol(self) -> str:
        return f"{self.base.symbol}/{self.quote.symbol}"


@dataclass(frozen=True)
class Quote:
    trading_pair: TradingPair
    bid: Decimal
    ask: Decimal
    exchange: str
    

@dataclass(frozen=True)
class OrderBookEntry:
    price: Decimal
    volume: Decimal

@dataclass(frozen=True)
class OrderBook:
    pair: TradingPair
    exchange: ExchangeId
    bids: List[OrderBookEntry]
    asks: List[OrderBookEntry]

@dataclass(frozen=True)
class MarketType(Enum):
    SPOT = "spot"
    FUTURES = "futures"
    PERPETUAL = "perpetual"
    MARGIN = "margin"
    OPTION = "option"

@dataclass(frozen=True)
class MarketId:
    pair: TradingPair
    exchange: ExchangeId
    market_type: MarketType


@dataclass(frozen=True)
class MarketInfo:
    market_id: MarketId
    maker_fee: Decimal
    taker_fee: Decimal
    percentage: bool

@dataclass(frozen=True)
class AssetNetwork:
    asset: Asset
    exchange: ExchangeId
    network: NetworkId
    withdraw_fee: Decimal
    withdraw_speed: float  # in hours

@dataclass(frozen=True)
class AssetInfo:
    asset: Asset
    exchange: ExchangeId
    networks: list[AssetNetwork]