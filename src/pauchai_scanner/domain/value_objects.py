from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import List

class AssetType(Enum):
    CRYPTO = "CRYPTO"
    #FIAT = "FIAT"

@dataclass(frozen=True)
class Asset:
    symbol: str        # e.g. "ETH"
    asset_type: AssetType = AssetType.CRYPTO  # e.g. AssetType.CRYPTO

@dataclass(frozen=True)
class TradingPair:
    base: Asset   # e.g. ETH
    quote: Asset  # e.g. USD

    # Factory method to create TradingPair from string "BASE/QUOTE"
    @classmethod
    def from_string(cls, pair: str, base_type: AssetType = AssetType.CRYPTO, quote_type: AssetType = AssetType.CRYPTO) -> 'TradingPair':
        base_symbol, quote_symbol = pair.split("/")
        return cls(base=Asset(base_symbol, base_type), quote=Asset(quote_symbol, quote_type))

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
    exchange: str
    bids: List[OrderBookEntry]
    asks: List[OrderBookEntry]