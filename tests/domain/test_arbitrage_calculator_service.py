from decimal import Decimal
import pytest

from pauchai_scanner.domain.arbitrage_calculator_service import InterExchangeSpotArbitrageService
from pauchai_scanner.domain.value_objects import Asset, TradingPair, Quote, MarketId, MarketType, MarketInfo, AssetInfo, AssetNetwork
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


asset_book = {
    (Asset("BTC"), "ExchangeA"): AssetInfo(
        asset=Asset("BTC"),
        exchange="ExchangeA",
        networks=[
            AssetNetwork(asset=Asset("BTC"), network="BTC", withdraw_fee=Decimal("0.0005"), withdraw_speed=1.0),
        ]
    ),
    (Asset("BTC"), "ExchangeB"): AssetInfo(
        asset=Asset("BTC"),
        exchange="ExchangeB",
        networks=[
            AssetNetwork(asset=Asset("BTC"), network="BTC", withdraw_fee=Decimal("0.0004"), withdraw_speed=0.5),
        ]
    ),
    (Asset("ETH"), "ExchangeA"): AssetInfo(
        asset=Asset("ETH"),
        exchange="ExchangeA",
        networks=[
            AssetNetwork(asset=Asset("ETH"), network="ERC20", withdraw_fee=Decimal("0.005"), withdraw_speed=2.0),
        ]
    ),
    (Asset("ETH"), "ExchangeB"): AssetInfo(
        asset=Asset("ETH"),
        exchange="ExchangeB",
        networks=[
            AssetNetwork(asset=Asset("ETH"), network="ERC20", withdraw_fee=Decimal("0.004"), withdraw_speed=1.5),
        ]
    ),
    (Asset("USDT"), "ExchangeA"): AssetInfo(
        asset=Asset("USDT"),
        exchange="ExchangeA",
        networks=[
            AssetNetwork(asset=Asset("USDT"), network="ERC20", withdraw_fee=Decimal("5"), withdraw_speed=1.0),
        ]
    ),
    (Asset("USDT"), "ExchangeB"): AssetInfo(
        asset=Asset("USDT"),
        exchange="ExchangeB",
        networks=[
            AssetNetwork(asset=Asset("USDT"), network="TRC20", withdraw_fee=Decimal("1"), withdraw_speed=0.5),
        ]
    ),
}

@pytest.mark.asyncio
async def test_arbitrage_calculator_service_basic():
    asset_usdt = Asset("USDT")
    price_book = prices_with_arbitrage

    service = InterExchangeSpotArbitrageService(price_book, asset_book, market_book)
    opportunities = service.calculate([asset_usdt], min_profit=Decimal('90'), min_volume=Decimal('0.01'))
    assert isinstance(opportunities, list)
    assert len(opportunities) == 2
    # Ожидаемая прибыль с учетом комиссий
    expected_profits = {
        # BTC/USDT:
        # sell_bid (ExchangeB) - buy_ask (ExchangeA)
        # - taker_fee на покупку (ExchangeA)
        # - taker_fee на продажу (ExchangeB)
        # - минимальная withdraw_fee для USDT на ExchangeB (TRC20 = 1)
        ("ExchangeA", "ExchangeB", "BTC/USDT"): Decimal('30400')  # sell_bid
            - Decimal('30200')                                         # buy_ask
            - Decimal('30200')*Decimal('0.001')                        # taker_fee ExchangeA
            - Decimal('30400')*Decimal('0.001')                        # taker_fee ExchangeB
            - Decimal('1'),                                            # withdraw_fee USDT ExchangeB (TRC20)
        # ETH/USDT:
        # sell_bid (ExchangeB) - buy_ask (ExchangeA)
        # - taker_fee на покупку (ExchangeA)
        # - taker_fee на продажу (ExchangeB)
        # - минимальная withdraw_fee для USDT на ExchangeB (TRC20 = 1)
        ("ExchangeA", "ExchangeB", "ETH/USDT"): Decimal('2140')   # sell_bid
            - Decimal('2020')                                         # buy_ask
            - Decimal('2020')*Decimal('0.001')                        # taker_fee ExchangeA
            - Decimal('2140')*Decimal('0.001')                        # taker_fee ExchangeB
            - Decimal('1'),                                            # withdraw_fee USDT ExchangeB (TRC20)
    }
    expected_fields = {
        ("ExchangeA", "ExchangeB", "BTC/USDT"): {
            "buy_network": "ERC20",   # USDT на ExchangeA: ERC20 (выбор по withdraw_fee, но только для USDT)
            "sell_network": "TRC20",  # USDT на ExchangeB: TRC20 (минимальная комиссия)
            "withdraw_fee": Decimal("1"),
            "withdraw_speed": 0.5,
        },
        ("ExchangeA", "ExchangeB", "ETH/USDT"): {
            "buy_network": "ERC20",
            "sell_network": "TRC20",
            "withdraw_fee": Decimal("1"),
            "withdraw_speed": 0.5,
        },
    }
    for opp in opportunities:
        key = (opp.buy_exchange, opp.sell_exchange, opp.pair.symbol())
        fields = expected_fields[key]
        assert opp.buy_network == fields["buy_network"], f"buy_network mismatch for {key}: {opp.buy_network} != {fields['buy_network']}"
        assert opp.sell_network == fields["sell_network"], f"sell_network mismatch for {key}: {opp.sell_network} != {fields['sell_network']}"
        assert opp.withdraw_fee == fields["withdraw_fee"], f"withdraw_fee mismatch for {key}: {opp.withdraw_fee} != {fields['withdraw_fee']}"
        assert opp.withdraw_speed == fields["withdraw_speed"], f"withdraw_speed mismatch for {key}: {opp.withdraw_speed} != {fields['withdraw_speed']}"