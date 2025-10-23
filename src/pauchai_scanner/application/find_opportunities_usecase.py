from decimal import Decimal
import logging
from typing import List
from pauchai_scanner.domain.entities import ArbitrageOpportunity
from pauchai_scanner.domain.interfaces import PriceRepository
from pauchai_scanner.domain.value_objects import Asset, TradingPair
from pauchai_scanner.domain.aggregators import PriceBook, AssetBook, MarketBook
from pauchai_scanner.domain.arbitrage_calculator_service import InterExchangeSpotArbitrageService
import logging
        
class FindArbitrageOpportunitiesUseCase:

    def __init__(self, price_repo: PriceRepository):
        self.price_repo = price_repo

    async def execute(self, quoted_asset: Asset , min_profit: Decimal, min_volume: Decimal , trading_pairs: List[TradingPair] = None) -> list[ArbitrageOpportunity]:
        logging.debug(f"[ArbUseCase] Получаем pricebook для пар: {trading_pairs}")
        price_book: PriceBook = await self.price_repo.get_pricebook(trading_pairs)
        logging.debug(f"[ArbUseCase] Получено pricebook: {len(price_book) if price_book else 0} пар, quotes: {sum(len(qs) for qs in price_book.values()) if price_book else 0}")
        asset_book: AssetBook = await self.price_repo.get_assetbook()
        logging.debug(f"[ArbUseCase] Получено assetbook: {len(asset_book) if asset_book else 0} записей")
        market_book: MarketBook = await self.price_repo.get_marketbook()
        logging.debug(f"[ArbUseCase] Получено marketbook: {len(market_book) if market_book else 0} рынков")
        calculator = InterExchangeSpotArbitrageService(price_book, asset_book, market_book)
        opportunities = calculator.calculate([quoted_asset], min_profit, min_volume)
        logging.debug(f"[ArbUseCase] Найдено возможностей: {len(opportunities) if opportunities else 0}")
        return opportunities