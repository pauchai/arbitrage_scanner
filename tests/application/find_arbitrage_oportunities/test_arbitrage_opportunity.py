from decimal import Decimal
from unittest.mock import AsyncMock, Mock
import pytest

from pauchai_scanner.application.find_opportunities_usecase import FindArbitrageOpportunitiesUseCase
from pauchai_scanner.domain.repository import PriceRepository
from pauchai_scanner.domain.value_objects import Asset, Quote, TradingPair

prices_with_arbitrage = [
    # ExchangeA
    Quote(TradingPair.from_string("BTC/USDT"), Decimal('30000'), Decimal('30200'), "ExchangeA"),
    Quote(TradingPair.from_string("ETH/USDT"), Decimal('2000'), Decimal('2020'), "ExchangeA"),
    # ExchangeB
    Quote(TradingPair.from_string("BTC/USDT"), Decimal('30400'), Decimal('30600'), "ExchangeB"),
    Quote(TradingPair.from_string("ETH/USDT"), Decimal('2140'), Decimal('2160'), "ExchangeB"),
]

prices_one_exchange = [
    Quote(TradingPair.from_string("BTC/USDT"), Decimal('30000'), Decimal('30200'), "ExchangeA"),
    Quote(TradingPair.from_string("ETH/USDT"), Decimal('2000'), Decimal('2020'), "ExchangeA"),
]


@pytest.fixture
def mock_price_repository():
    repo = PriceRepository()
    repo.get_quotes = AsyncMock(return_value=prices_with_arbitrage)
    return repo

@pytest.mark.asyncio
async def test_find_arbitrage_opportunities(mock_price_repository):
    finder = FindArbitrageOpportunitiesUseCase(mock_price_repository)
    opportunities = await finder.execute(quoted_asset=Asset("USDT"), min_profit=Decimal('100'), min_volume=Decimal('0.01'))
    assert isinstance(opportunities, list)
    assert len(opportunities) == 2  
    # Ожидаемая прибыль должна быть корректной
    expected_profits = {
        ("ExchangeA", "ExchangeB", "BTC/USDT"): Decimal('200'),  # Buy on A at 30000, sell on B at 30400
        ("ExchangeA", "ExchangeB", "ETH/USDT"): Decimal('120'),  # Buy on A at 2020, sell on B at 2140
    }
    for opp in opportunities:   
        key = (opp.buy_exchange, opp.sell_exchange, opp.pair.symbol())
        assert opp.estimated_profit == expected_profits[key]



@pytest.mark.asyncio
async def test_no_arbitrage_within_one_exchange(mock_price_repository):
    # Все quotes только с одной биржи
 
    repo = PriceRepository()
    repo.get_quotes = AsyncMock(return_value=prices_one_exchange)
    finder = FindArbitrageOpportunitiesUseCase(repo)
    opportunities = await finder.execute(Asset("USDT"), Decimal('100'), Decimal('0.01'))
    assert isinstance(opportunities, list)
    assert len(opportunities) == 0  # Не должно быть арбитража внутри одной биржи
