import abc

from pauchai_scanner.domain.aggregators import AssetBook, MarketBook, PriceBook
from pauchai_scanner.domain.value_objects import Quote, TradingPair



# Базовый интерфейс провайдера бирж
class ExchangeProvider(abc.ABC):
    @abc.abstractmethod
    async def get_quotes(self, pairs: list[TradingPair]) -> list[Quote]:
        """Получить котировки для заданных торговых пар с биржи."""
        pass


class PriceRepository(abc.ABC):
    @abc.abstractmethod
    async def get_pricebook(self, pairs: list[TradingPair]) -> PriceBook:
        pass

    async def get_marketbook(self) -> MarketBook:
        pass

    async def get_assetbook(self) -> AssetBook:
        pass

    async def close(self):
        pass