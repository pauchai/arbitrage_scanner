import asyncio
import ccxt.async_support as ccxt
from pauchai_scanner.domain.value_objects import Quote, TradingPair
from pauchai_scanner.domain.interfaces import  ExchangeProvider, PriceRepository



class PriceRepositoryImpl(PriceRepository):
    def __init__(self, providers: list[ExchangeProvider]):
        self.providers = {type(provider).__name__: provider for provider in providers}

    async def get_pricebook(self, pairs: list[TradingPair]) -> list[Quote]:
        quotes = []
        
        tasks = [
            provider.get_pricebook(pairs)
            for provider in self.providers.values()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, list):
                quotes.extend(result)
            else:
                pass

        return quotes
