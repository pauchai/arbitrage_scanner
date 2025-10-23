import ccxt.async_support as ccxt
from pauchai_scanner.domain.aggregators import AssetBook, MarketBook, PriceBook
from pauchai_scanner.domain.exceptions import ExchangeUnavailable
from pauchai_scanner.domain.interfaces import ExchangeProvider
from pauchai_scanner.domain.value_objects import Quote, Quote, TradingPair
from pauchai_scanner.infrastructure.adapters.ccxt.mappers import map_asset, map_market, map_price
from pauchai_scanner.infrastructure.dtos import CCXTCurrencyDTO, CCXTMarketDTO, CCXTNetworkDTO, CCXTTickerDTO
import logging


class CCXTExchangeProvider(ExchangeProvider):
    exchange: ccxt.Exchange
    def __init__(self, exchange_id: str, ccxt_kwargs: dict):
        self.exchange_id = exchange_id
        self.exchange = getattr(ccxt, exchange_id)(ccxt_kwargs)

    #async def _ensure_markets_loaded(self):
    #    if not getattr(self, "_markets_loaded", False):
    #        await self.exchange.load_markets()
    #        self._markets_loaded = True

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

        for symbol, ticker_raw in tickers_raw.items():
            try:
                dto = CCXTTickerDTO(**ticker_raw)
                # CCXT иногда не возвращает 'symbol' внутри payload — гарантируем
                if not getattr(dto, "symbol", None):
                    dto.symbol = symbol

                mapped = map_price(dto, self.exchange_id)
            except Exception as e:
                logging.warning(f"[{self.exchange_id}] Ошибка парсинга тикера {symbol}: {e}")
                continue

            if mapped:
                pair, quote = mapped
                price_book.setdefault(pair, []).append(quote)

        return price_book

    async def get_market_book(self) -> MarketBook:
        try:
            await self.exchange.load_markets()
            markets_raw = await self.exchange.fetch_markets()
        except Exception as e:
            raise ExchangeUnavailable(f"Ошибка CCXT у биржи {self.exchange_id}") from e

        market_book: MarketBook = {}
        for market_raw in markets_raw:
            try:
                dto = CCXTMarketDTO(**market_raw)
                market_id, market_info = map_market(dto, self.exchange_id)
                market_book[market_id] = market_info
            except Exception as e:
                logging.warning(f"[{self.exchange_id}] Ошибка мэппинга market {market_raw.get('symbol', 'unknown')}: {e}")
        return market_book

    
    async def get_asset_book(self) -> AssetBook:
        try:
            assets_raw = await self.exchange.fetch_currencies()
        except Exception as e:
            raise ExchangeUnavailable(f"Ошибка CCXT у биржи {self.exchange_id}") from e

        asset_book: AssetBook = {}
        for asset_symbol, asset_raw in assets_raw.items():
            try:
                dto = CCXTCurrencyDTO(**asset_raw)
                key, asset_info = map_asset(dto, self.exchange_id)
                asset_book[key] = asset_info
            except Exception as e:
                logging.warning(f"[{self.exchange_id}] Ошибка мэппинга актива {asset_symbol}: {e}")
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