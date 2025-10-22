from pauchai_scanner.domain.aggregators import PriceBook, AssetBook, MarketBook
from pauchai_scanner.domain.value_objects import TradingPair, Asset
from pauchai_scanner.domain.entities import ArbitrageOpportunity
from decimal import Decimal
from typing import List

class ArbitrageCalculatorService:
    """
    Доменный сервис для расчета арбитражных возможностей между биржами.
    Входные данные: агрегаты PriceBook, AssetBook, MarketBook
    Выход: список ArbitrageOpportunity
    """
    def __init__(self, price_book: PriceBook, asset_book: AssetBook, market_book: MarketBook):
        self.price_book = price_book
        self.asset_book = asset_book
        self.market_book = market_book

    def calculate(self, quoted_assets: List[Asset], min_profit: Decimal, min_volume: Decimal) -> List[ArbitrageOpportunity]:
        opportunities = []
        from pauchai_scanner.domain.value_objects import MarketId, MarketType
        # Новый перебор: для каждой пары сравниваем все котировки между биржами
        for pair, quotes in self.price_book.items():
            if pair.quote not in quoted_assets:
                continue
            for buy_quote in quotes:
                for sell_quote in quotes:
                    if buy_quote.exchange == sell_quote.exchange:
                        continue
                    # Получаем комиссии
                    market_id_buy = MarketId(pair=pair, exchange=buy_quote.exchange, market_type=MarketType.SPOT)
                    market_id_sell = MarketId(pair=pair, exchange=sell_quote.exchange, market_type=MarketType.SPOT)
                    fee_buy = self.market_book.get(market_id_buy, None)
                    fee_sell = self.market_book.get(market_id_sell, None)
                    buy_fee = (buy_quote.ask * fee_buy.taker_fee) if (fee_buy and fee_buy.percentage) else (fee_buy.taker_fee if fee_buy else Decimal("0"))
                    sell_fee = (sell_quote.bid * fee_sell.taker_fee) if (fee_sell and fee_sell.percentage) else (fee_sell.taker_fee if fee_sell else Decimal("0"))
                    profit = sell_quote.bid - buy_quote.ask - buy_fee - sell_fee
                    if profit >= min_profit:
                        opportunity = ArbitrageOpportunity(
                            pair=pair,
                            buy_exchange=buy_quote.exchange,
                            sell_exchange=sell_quote.exchange,
                            estimated_profit=profit
                        )
                        opportunities.append(opportunity)
        return opportunities
