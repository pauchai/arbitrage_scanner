from decimal import Decimal
import pytest

from pauchai_scanner.domain.arbitrage_calculator_service import ArbitrageCalculatorService
from pauchai_scanner.domain.value_objects import Asset, TradingPair, Quote, MarketId, MarketType, MarketInfo
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

market_book = {
    MarketId(pair=TradingPair.from_string("BTC/USDT"), exchange="ExchangeA", market_type=MarketType.SPOT): MarketInfo(market_id=MarketId(TradingPair.from_string("BTC/USDT"), "ExchangeA", MarketType.SPOT), maker_fee=Decimal("0.0005"), taker_fee=Decimal("0.001"), percentage=True),
    MarketId(pair=TradingPair.from_string("BTC/USDT"), exchange="ExchangeB", market_type=MarketType.SPOT): MarketInfo(market_id=MarketId(TradingPair.from_string("BTC/USDT"), "ExchangeB", MarketType.SPOT), maker_fee=Decimal("0.0005"), taker_fee=Decimal("0.001"), percentage=True),
    MarketId(pair=TradingPair.from_string("ETH/USDT"), exchange="ExchangeA", market_type=MarketType.SPOT): MarketInfo(market_id=MarketId(TradingPair.from_string("ETH/USDT"), "ExchangeA", MarketType.SPOT), maker_fee=Decimal("0.0005"), taker_fee=Decimal("0.001"), percentage=True),
    MarketId(pair=TradingPair.from_string("ETH/USDT"), exchange="ExchangeB", market_type=MarketType.SPOT): MarketInfo(market_id=MarketId(TradingPair.from_string("ETH/USDT"), "ExchangeB", MarketType.SPOT), maker_fee=Decimal("0.0005"), taker_fee=Decimal("0.001"), percentage=True),
}

@pytest.mark.asyncio
async def test_arbitrage_calculator_service_basic():
    asset_usdt = Asset("USDT")
    price_book = prices_with_arbitrage
    asset_book = {}

    service = ArbitrageCalculatorService(price_book, asset_book, market_book)
    opportunities = service.calculate([asset_usdt], min_profit=Decimal('90'), min_volume=Decimal('0.01'))
    assert isinstance(opportunities, list)
    assert len(opportunities) == 2
    # Ожидаемая прибыль с учетом комиссий
    expected_profits = {
        ("ExchangeA", "ExchangeB", "BTC/USDT"): Decimal('30400') - Decimal('30200') - Decimal('30200')*Decimal('0.001') - Decimal('30400')*Decimal('0.001'),
        ("ExchangeA", "ExchangeB", "ETH/USDT"): Decimal('2140') - Decimal('2020') - Decimal('2020')*Decimal('0.001') - Decimal('2140')*Decimal('0.001'),
    }
    for opp in opportunities:
        key = (opp.buy_exchange, opp.sell_exchange, opp.pair.symbol())
        assert abs(opp.estimated_profit - expected_profits[key]) < Decimal('0.01')
