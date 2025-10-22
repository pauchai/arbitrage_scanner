import pytest
from pauchai_scanner.domain.value_objects import Asset, TradingPair, Quote
from pauchai_scanner.infrastructure.repositories import InMemoryPriceRepository
from pauchai_scanner.domain.aggregators import PriceBook
from decimal import Decimal

@pytest.mark.asyncio
async def test_inmemory_price_repository_basic():
    quotes = [
        Quote(TradingPair.from_string("BTC/USDT"), Decimal('30000'), Decimal('30200'), "ExchangeA"),
        Quote(TradingPair.from_string("BTC/USDT"), Decimal('30400'), Decimal('30600'), "ExchangeB"),
        Quote(TradingPair.from_string("ETH/USDT"), Decimal('2000'), Decimal('2020'), "ExchangeA"),
        Quote(TradingPair.from_string("ETH/USDT"), Decimal('2140'), Decimal('2160'), "ExchangeB"),
    ]
    repo = InMemoryPriceRepository(quotes)
    pairs = [TradingPair.from_string("BTC/USDT"), TradingPair.from_string("ETH/USDT")]
    pricebook = await repo.get_pricebook(pairs)
    assert isinstance(pricebook, dict)
    assert TradingPair.from_string("BTC/USDT") in pricebook
    assert TradingPair.from_string("ETH/USDT") in pricebook
    assert len(pricebook[TradingPair.from_string("BTC/USDT")]) == 2
    assert len(pricebook[TradingPair.from_string("ETH/USDT")]) == 2
