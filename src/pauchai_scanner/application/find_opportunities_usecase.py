from decimal import Decimal
import logging
from pauchai_scanner.domain.entities import ArbitrageOpportunity
from pauchai_scanner.domain.repository import PriceRepository
from pauchai_scanner.domain.value_objects import Asset, TradingPair

logging.basicConfig(level=logging.DEBUG)
class FindArbitrageOpportunitiesUseCase:

    def __init__(self, price_repo: PriceRepository):
        self.price_repo = price_repo

    async def execute(self, quoted_asset: Asset, min_profit: Decimal, min_volume: Decimal) -> list[ArbitrageOpportunity]:
        # Implementation of the use case to find arbitrage opportunities
        quotes = [q for q in await self.price_repo.get_quotes() if q.trading_pair.quote == quoted_asset]
        logging.debug(f"Found {len(quotes)} quotes for {quoted_asset}")
        opportunities = []
        # Logic to find arbitrage opportunities based on quotes
        trading_pairs = set(quote.trading_pair for quote in quotes)
        for pair in trading_pairs:
            # Filter quotes for the current trading pair
            pair_quotes = [q for q in quotes if q.trading_pair == pair]
            # Check for arbitrage opportunities between different exchanges
            if len(pair_quotes) < 2:
                continue  # Need at least two exchanges to find arbitrage
            lowest_ask = min(pair_quotes, key=lambda q: q.ask)
            highest_bid = max(pair_quotes, key=lambda q: q.bid)

            if lowest_ask.exchange == highest_bid.exchange:
                continue  # No arbitrage if both prices are from the same exchange

            buy_price = lowest_ask.ask # Минимальная цена по которой продавец готов продать
            sell_price = highest_bid.bid # Максимальная цена которую покупатель готов заплатить
            potential_profit = sell_price - buy_price
            logging.debug(f"Evaluated pair {pair.symbol()}: Buy on {lowest_ask.exchange} at {lowest_ask.ask}, "
                          f"Sell on {highest_bid.exchange} at {highest_bid.bid}, Potential Profit: {potential_profit}") 
            if potential_profit >= min_profit:
                opportunity = ArbitrageOpportunity(
                    pair=pair,
                    buy_exchange=lowest_ask.exchange,
                    sell_exchange=highest_bid.exchange,
                    estimated_profit=potential_profit
                )
                opportunities.append(opportunity)
        return opportunities