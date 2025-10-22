import pytest
from pauchai_scanner.domain.value_objects import TradingPair, Quote
from pauchai_scanner.infrastructure.providers import MockExchangeProvider
from pauchai_scanner.domain.aggregators import PriceBook
from decimal import Decimal

@pytest.mark.asyncio
async def test_mock_exchange_provider_basic():
    quotes = [
        Quote(TradingPair.from_string("BTC/USDT"), Decimal('30000'), Decimal('30200'), "ExchangeA"),
        Quote(TradingPair.from_string("BTC/USDT"), Decimal('30400'), Decimal('30600'), "ExchangeB"),
        Quote(TradingPair.from_string("ETH/USDT"), Decimal('2000'), Decimal('2020'), "ExchangeA"),
        Quote(TradingPair.from_string("ETH/USDT"), Decimal('2140'), Decimal('2160'), "ExchangeB"),
    ]
    provider = MockExchangeProvider("ExchangeA", quotes)
    pairs = [TradingPair.from_string("BTC/USDT"), TradingPair.from_string("ETH/USDT")]
    price_book = await provider.get_price_book(pairs)
    assert isinstance(price_book, dict)
    assert TradingPair.from_string("BTC/USDT") in price_book
    assert TradingPair.from_string("ETH/USDT") in price_book
    for pair in pairs:
        quotes_for_pair = price_book[pair]
        assert len(quotes_for_pair) == 1
        assert quotes_for_pair[0].exchange == "ExchangeA"

@pytest.mark.asyncio
async def test_mock_exchange_provider_empty():
    provider = MockExchangeProvider("ExchangeA", [])
    pairs = [TradingPair.from_string("BTC/USDT")]
    price_book = await provider.get_price_book(pairs)
    assert price_book == {}
