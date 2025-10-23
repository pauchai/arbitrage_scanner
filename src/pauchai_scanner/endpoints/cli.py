import argparse
import logging
from pauchai_scanner.config.exchanges import config, config_credentials
import asyncio
from pauchai_scanner.application.find_opportunities_usecase import FindArbitrageOpportunitiesUseCase
from pauchai_scanner.domain.value_objects import Asset, TradingPair
from pauchai_scanner.infrastructure.providers import CCXTExchangeProvider
from pauchai_scanner.infrastructure.repositories import PriceRepositoryImpl

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("ccxt").setLevel(logging.WARNING)

merged_config = {
    name: {**config[name], **config_credentials.get(name, {})}
    for name in config
}

def main():
    parser = argparse.ArgumentParser(description="Arbitrage CLI")
    parser.add_argument("--show-config", action="store_true", help="Показать merged_config")
    parser.add_argument("--exchange", type=str, help="Биржа для вывода информации")
    parser.add_argument("--find-arb", action="store_true", help="Поиск арбитражных возможностей")
    parser.add_argument("--quoted-asset", type=str, help="Актив для арбитража (например USDT)")
    parser.add_argument("--min-profit", type=float, default=0, help="Минимальная прибыль")
    parser.add_argument("--min-volume", type=float, default=0.01, help="Минимальный объём")
    parser.add_argument("--pairs", type=str, nargs="*", default=None, help="Торговые пары через пробел (например BTC/USDT ETH/USDT)")
    parser.add_argument("--interval", type=float, default=10.0, help="Задержка между циклами арбитража (сек)")
    args = parser.parse_args()

    if args.show_config:
        import pprint
        pprint.pprint(merged_config)
        return

    if args.exchange:
        exch = args.exchange.lower()
        if exch in merged_config:
            print(f"Config for {exch}:")
            import pprint
            pprint.pprint(merged_config[exch])
        else:
            print(f"Exchange '{exch}' not found in config.")
        return

    if args.find_arb or (not args.show_config and not args.exchange):        
        # Выбираем только включённые биржи
        enabled_exchanges = [name for name, cfg in merged_config.items() if cfg.get('enabled')]
        providers = []
        for name in enabled_exchanges:
            ccxt_kwargs = merged_config[name].get('ccxt', {})
            credentials = merged_config[name].get('credentials', {})
            ccxt_kwargs = {**ccxt_kwargs, **credentials}
            logging.info(f"Инициализация провайдера для биржи {name} с параметрами: {ccxt_kwargs}")
            try:
                providers.append(CCXTExchangeProvider(name, ccxt_kwargs))
            except Exception as e:
                print(f"Ошибка инициализации провайдера {name}: {e}")
        repo = PriceRepositoryImpl(providers)
        quoted_asset = Asset(args.quoted_asset) if args.quoted_asset else Asset("USDT")
        min_profit = args.min_profit
        min_volume = args.min_volume
        if args.pairs:
            pairs = [TradingPair.from_string(p) for p in args.pairs]
        else:
            pairs = None
        async def run():
            usecase = FindArbitrageOpportunitiesUseCase(repo)
            try:
                while True:
                    opportunities = await usecase.execute(
                        quoted_asset=quoted_asset,
                        min_profit=min_profit,
                        min_volume=min_volume,
                        trading_pairs=pairs
                    )
                    if not opportunities:
                        print("Арбитражные возможности не найдены.")
                    for opp in opportunities:
                        print(f"{opp.pair.symbol()}: {opp.buy_exchange} -> {opp.sell_exchange}, profit={opp.estimated_profit:.2f}")
                    await asyncio.sleep(args.interval)
            finally:
                # Закрытие всех провайдеров
                for provider in providers:
                    if hasattr(provider, "close") and callable(provider.close):
                        await provider.close()
        asyncio.run(run())
        return

    parser.print_help()

if __name__ == "__main__":
    main()
