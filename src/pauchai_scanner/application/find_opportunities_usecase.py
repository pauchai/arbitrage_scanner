from decimal import Decimal
import logging
from pauchai_scanner.domain.entities import ArbitrageOpportunity
from pauchai_scanner.domain.interfaces import PriceRepository
from pauchai_scanner.domain.value_objects import Asset, TradingPair
from pauchai_scanner.domain.aggregators import PriceBook, AssetBook, MarketBook
from pauchai_scanner.domain.arbitrage_calculator_service import ArbitrageCalculatorService
        
logging.basicConfig(level=logging.DEBUG)
class FindArbitrageOpportunitiesUseCase:

    def __init__(self, price_repo: PriceRepository):
        self.price_repo = price_repo

    async def execute(self, quoted_asset: Asset, min_profit: Decimal, min_volume: Decimal) -> list[ArbitrageOpportunity]:
        # Получаем котировки и формируем PriceBook
        quotes = [q for q in await self.price_repo.get_quotes() if q.trading_pair.quote == quoted_asset]
        price_book: PriceBook = {q.trading_pair: q for q in quotes}
        asset_book: AssetBook = {}  # Заполнить при необходимости
        market_book: MarketBook = {}  # Заполнить при необходимости
        calculator = ArbitrageCalculatorService(price_book, asset_book, market_book)
        opportunities = calculator.calculate([quoted_asset], min_profit, min_volume)
        return opportunities