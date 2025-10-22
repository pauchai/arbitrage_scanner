import abc

from pauchai_scanner.domain.value_objects import Quote, TradingPair


class PriceRepository:
    @abc.abstractmethod
    async def get_quotes(self, pairs: list[TradingPair]) -> list[Quote]:
        pass