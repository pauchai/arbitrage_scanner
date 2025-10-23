from typing import List, NewType
from pauchai_scanner.domain.value_objects import AssetInfo, ExchangeId, MarketId, MarketInfo, Quote, TradingPair, Asset


class PriceBook(dict[TradingPair, list[Quote]]):
    def add(self, quote: Quote):
        """Добавить котировку."""
        self.setdefault(quote.trading_pair, []).append(quote)

    def get_pairs(self) -> list[TradingPair]:
        """Список всех торговых пар."""
        return list(self.keys())

    def get_quotes(self, pair: TradingPair) -> list[Quote]:
        """Вернуть все котировки по паре."""
        return self.get(pair, [])

class MarketBook(dict[MarketId, MarketInfo]):
    def add(self, market_info: MarketInfo):
        """Добавить информацию о рынке."""
        self[market_info.market_id] = market_info

    def find_by_pair(self, pair: TradingPair) -> list[MarketInfo]:
        """Найти все рынки по конкретной паре."""
        return [
            info for m_id, info in self.items()
            if m_id.pair == pair
        ]

class AssetBook(dict[tuple[Asset, ExchangeId], AssetInfo]):
    def add(self, asset_info: AssetInfo):
        """Добавить информацию об активе."""
        key = (asset_info.asset, asset_info.exchange)
        self[key] = asset_info

    def find_asset(self, asset: Asset) -> list[AssetInfo]:
        """Найти актив на всех биржах."""
        return [
            info for (a, _), info in self.items()
            if a == asset
        ]
