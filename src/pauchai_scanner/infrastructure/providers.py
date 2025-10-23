import ccxt.async_support as ccxt
from pauchai_scanner.domain.aggregators import AssetBook, MarketBook, PriceBook
from pauchai_scanner.domain.exceptions import ExchangeUnavailable
from pauchai_scanner.domain.interfaces import ExchangeProvider
from pauchai_scanner.domain.value_objects import Quote, Quote, TradingPair
from pauchai_scanner.infrastructure.dtos import CCXTCurrencyDTO, CCXTMarketDTO, CCXTTickerDTO


class CCXTExchangeProvider(ExchangeProvider):
    def __init__(self, exchange_id: str, ccxt_kwargs: dict):
        self.exchange_id = exchange_id
        self.exchange = getattr(ccxt, exchange_id)(ccxt_kwargs)

    async def get_price_book(self, pairs: list[TradingPair]) -> PriceBook:
        if not pairs:
            symbols = None
        else:
            symbols = [pair.symbol() for pair in pairs]
            
        if not self.exchange.has.get('fetchTickers', False):
            raise ExchangeUnavailable(f"Exchange {self.exchange_id} не поддерживает fetchTickers().")

        try:
            await self.exchange.load_markets()
            tickers_raw = await self.exchange.fetch_tickers(symbols)
        except Exception as e:
            raise ExchangeUnavailable(f"Ошибка CCXT у биржи {self.exchange_id}") from e

        price_book = PriceBook()
        pairs_map = {p.symbol(): p for p in pairs}  # O(1) lookup

        for symbol, ticker_raw in tickers_raw.items():
            ticker_dto = CCXTTickerDTO(**ticker_raw)
            pair = pairs_map.get(symbol)
            bid = ticker_dto.bid
            ask = ticker_dto.ask
            if pair and bid and ask:
                price_book[self.exchange_id][pair] = Quote(trading_pair=pair, bid=bid, ask=ask, exchange=self.exchange_id)

        return price_book
    async def get_market_book(self) -> MarketBook:
        try:
            await self.exchange.load_markets()
            markets_raw = await self.exchange.fetch_markets()
        except Exception as e:
            raise ExchangeUnavailable(f"Ошибка CCXT у биржи {self.exchange_id}") from e

        market_book: MarketBook = {}
        for market_raw in markets_raw:
            market_dto = CCXTMarketDTO(**market_raw)
            market_book[market_dto.symbol] = market_dto

        return market_book
    
    async def get_asset_book(self) -> AssetBook:
        try:
            await self.exchange.load_markets()
            assets_raw = await self.exchange.fetch_currencies()
        except Exception as e:
            raise ExchangeUnavailable(f"Ошибка CCXT у биржи {self.exchange_id}") from e

        asset_book: AssetBook = {}
        for asset_symbol, asset_raw in assets_raw.items():
            asset_dto = CCXTCurrencyDTO(**asset_raw)
            asset_book[(asset_symbol, self.exchange_id)] = asset_dto

        return asset_book
    async def close(self):
        if hasattr(self.exchange, "close") and callable(self.exchange.close):
            await self.exchange.close()




class MockExchangeProvider(ExchangeProvider):
    def __init__(self, exchange_id: str, quotes: list[Quote], market_book: MarketBook = None, asset_book: AssetBook = None):
        self.exchange_id = exchange_id
        self._quotes = quotes
        self._market_book = market_book or {}
        self._asset_book = asset_book or {}

    async def get_price_book(self, pairs: list[TradingPair]) -> PriceBook:
        price_book = {}
        for q in self._quotes:
            if q.trading_pair in pairs and q.exchange == self.exchange_id:
                price_book.setdefault(q.trading_pair, []).append(q)
        return price_book

    async def get_market_book(self) -> MarketBook:
        return self._market_book

    async def get_asset_book(self) -> AssetBook:
        return self._asset_book

    async def close(self):
        pass