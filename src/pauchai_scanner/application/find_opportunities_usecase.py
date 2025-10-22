from decimal import Decimal
import logging
from typing import List
from pauchai_scanner.domain.entities import ArbitrageOpportunity
from pauchai_scanner.domain.interfaces import PriceRepository
from pauchai_scanner.domain.value_objects import Asset, TradingPair
from pauchai_scanner.domain.aggregators import PriceBook, AssetBook, MarketBook
from pauchai_scanner.domain.arbitrage_calculator_service import InterExchangeSpotArbitrageService
        
logging.basicConfig(level=logging.DEBUG)
class FindArbitrageOpportunitiesUseCase:

    def __init__(self, price_repo: PriceRepository):
        self.price_repo = price_repo

    async def execute(self, quoted_asset: Asset , min_profit: Decimal, min_volume: Decimal , trading_pairs: List[TradingPair] = None) -> list[ArbitrageOpportunity]:
        # Получаем котировки и формируем PriceBook
        price_book: PriceBook = await self.price_repo.get_pricebook(trading_pairs)
        asset_book: AssetBook = await self.price_repo.get_assetbook()
        market_book: MarketBook = await self.price_repo.get_marketbook()
        calculator = InterExchangeSpotArbitrageService(price_book, asset_book, market_book)
        opportunities = calculator.calculate([quoted_asset], min_profit, min_volume)
        return opportunities