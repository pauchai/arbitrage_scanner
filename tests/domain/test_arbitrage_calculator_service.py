from decimal import Decimal
import pytest

from pauchai_scanner.domain.arbitrage_calculator_service import ArbitrageCalculatorService
from pauchai_scanner.domain.value_objects import Asset, TradingPair, Quote
from pauchai_scanner.domain.entities import ArbitrageOpportunity

prices_with_arbitrage = {
    TradingPair.from_string("BTC/USDT"): [
        Quote(TradingPair.from_string("BTC/USDT"), Decimal('30000'), Decimal('30200'), "ExchangeA"),
        Quote(TradingPair.from_string("BTC/USDT"), Decimal('30400'), Decimal('30600'), "ExchangeB"),
    ],
    TradingPair.from_string("ETH/USDT"): [
        Quote(TradingPair.from_string("ETH/USDT"), Decimal('2000'), Decimal('2020'), "ExchangeA"),
        Quote(TradingPair.from_string("ETH/USDT"), Decimal('2140'), Decimal('2160'), "ExchangeB"),
    ],
}

@pytest.mark.asyncio
async def test_arbitrage_calculator_service_basic():
    asset_usdt = Asset("USDT")
    price_book = prices_with_arbitrage
    asset_book = {}
    market_book = {}
    service = ArbitrageCalculatorService(price_book, asset_book, market_book)
    opportunities = service.calculate([asset_usdt], min_profit=Decimal('100'), min_volume=Decimal('0.01'))
    assert isinstance(opportunities, list)
    assert len(opportunities) == 2
    expected_profits = {
        ("ExchangeA", "ExchangeB", "BTC/USDT"): Decimal('200'),
        ("ExchangeA", "ExchangeB", "ETH/USDT"): Decimal('120'),
    }
    for opp in opportunities:
        key = (opp.buy_exchange, opp.sell_exchange, opp.pair.symbol())
        assert opp.estimated_profit == expected_profits[key]
