import abc

from pauchai_scanner.domain.aggregators import AssetBook, MarketBook, PriceBook
from pauchai_scanner.domain.value_objects import Quote, TradingPair



# Базовый интерфейс провайдера бирж

class ExchangeProvider(abc.ABC):
    @abc.abstractmethod
    async def get_price_book(self, pairs: list[TradingPair]) -> PriceBook:
        """Получить агрегат котировок для заданных торговых пар с биржи."""
        pass

    @abc.abstractmethod
    async def get_market_book(self) -> MarketBook:
        """Получить агрегат рынков биржи."""
        pass

    @abc.abstractmethod
    async def get_asset_book(self) -> AssetBook:
        """Получить агрегат активов биржи."""
        pass

    async def close(self):
        pass


class PriceRepository(abc.ABC):
    @abc.abstractmethod
    async def get_pricebook(self, pairs: list[TradingPair] = None) -> PriceBook:
        pass

    async def get_marketbook(self) -> MarketBook:
        pass

    async def get_assetbook(self) -> AssetBook:
        pass

    async def close(self):
        pass