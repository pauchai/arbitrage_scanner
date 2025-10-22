import ccxt
from pauchai_scanner.domain.aggregators import AssetBook, MarketBook, PriceBook
from pauchai_scanner.domain.exceptions import ExchangeUnavailable
from pauchai_scanner.domain.interfaces import ExchangeProvider
from pauchai_scanner.domain.value_objects import Quote, Quote, TradingPair
from pauchai_scanner.infrastructure.dtos import CCXTCurrencyDTO, CCXTMarketDTO, CCXTTickerDTO


class CCXTExchangeProvider(ExchangeProvider):
    def __init__(self, exchange_id: str, **kwargs):
        self.exchange_id = exchange_id
        self.exchange = getattr(ccxt, exchange_id)(**kwargs)

    async def get_price_book(self, pairs: list[TradingPair]) -> PriceBook:
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
    async def get_market_book(self)->MarketBook:
        try:
            await self.exchange.load_markets()
            markets_raw = await self.exchange.fetch_markets()
        except Exception as e:
            raise ExchangeUnavailable(f"Ошибка CCXT у биржи {self.exchange_id}") from e

        market_book: MarketBook = {}
        for market_raw in markets_raw:
            market_dto = CCXTMarketDTO(**market_raw)
            market_book[self.exchange_id][market_dto.symbol] = ..

        return market_book
    
    async def get_asset_book(self)->AssetBook:
        try:
            await self.exchange.load_markets()
            assets_raw = await self.exchange.fetch_currencies()
        except Exception as e:
            raise ExchangeUnavailable(f"Ошибка CCXT у биржи {self.exchange_id}") from e

        asset_book: AssetBook = {}
        for asset_symbol, asset_raw in assets_raw.items():
            asset_dto = CCXTCurrencyDTO(**asset_raw)
            asset_book[self.exchange_id][asset_symbol] = ..

        return asset_book
    async def close(self):
        await self.exchange.close()