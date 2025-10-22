import asyncio
from typing import List
import ccxt.async_support as ccxt
from pauchai_scanner.domain.aggregators import AssetBook, MarketBook, PriceBook
from pauchai_scanner.domain.value_objects import Quote, TradingPair
from pauchai_scanner.domain.interfaces import  ExchangeProvider, PriceRepository



class PriceRepositoryImpl(PriceRepository):
    def __init__(self, providers: list[ExchangeProvider]):
        self.providers = {type(provider).__name__: provider for provider in providers}

    async def get_pricebook(self, pairs: list[TradingPair]) -> PriceBook:
        quotes = []
        tasks = [
            provider.get_price_book(pairs)
            for provider in self.providers.values()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, dict):
                for pair, qs in result.items():
                    quotes.extend(qs)
            elif isinstance(result, list):
                quotes.extend(result)
            else:
                pass

        pricebook = {}
        for q in quotes:
            pricebook.setdefault(q.trading_pair, []).append(q)
        return pricebook



class InMemoryPriceRepository(PriceRepository):
    def __init__(self, quotes: List[Quote], market_book: MarketBook = None, asset_book: AssetBook = None):
        self._quotes = quotes
        self._market_book = market_book or {}
        self._asset_book = asset_book or {}

    async def get_pricebook(self, pairs: List[TradingPair] = None) -> PriceBook:
        pricebook = {}
        for q in self._quotes:
            if pairs is None or q.trading_pair in pairs:
                pricebook.setdefault(q.trading_pair, []).append(q)
        return pricebook

    async def get_marketbook(self) -> MarketBook:
        return self._market_book

    async def get_assetbook(self) -> AssetBook:
        return self._asset_book

    async def close(self):
        pass