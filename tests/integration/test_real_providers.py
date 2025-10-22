import asyncio
from pauchai_scanner.infrastructure.providers import CCXTExchangeProvider
from pauchai_scanner.infrastructure.repositories import PriceRepositoryImpl
from pauchai_scanner.application.find_opportunities_usecase import FindArbitrageOpportunitiesUseCase
from pauchai_scanner.domain.value_objects import TradingPair, Asset
from decimal import Decimal

# Пример: используем две биржи и реальные пары
EXCHANGES = [
    ('binance', {}),
    ('bybit', {}),
]
TRADING_PAIRS = [
    TradingPair.from_string('BTC/USDT'),
    TradingPair.from_string('ETH/USDT'),
]

async def main():
    providers = [CCXTExchangeProvider(exchange_id, **params) for exchange_id, params in EXCHANGES]
    repo = PriceRepositoryImpl(providers)
    usecase = FindArbitrageOpportunitiesUseCase(repo)
    opportunities = await usecase.execute(
        quoted_asset=Asset('USDT'),
        min_profit=Decimal('10'),
        min_volume=Decimal('0.001'),
        trading_pairs=TRADING_PAIRS
    )
    for opp in opportunities:
        print(f"Arbitrage: {opp.pair.symbol()} | Buy: {opp.buy_exchange} | Sell: {opp.sell_exchange} | Profit: {opp.estimated_profit}")
    for provider in providers:
        await provider.close()
    await repo.close()

if __name__ == "__main__":
    asyncio.run(main())
