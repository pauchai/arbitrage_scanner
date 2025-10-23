from pauchai_scanner.domain.value_objects import (
    Asset, AssetInfo, AssetNetwork, ExchangeId,
    MarketId, MarketInfo, MarketType, Quote, TradingPair
)
from pauchai_scanner.infrastructure.dtos import CCXTMarketDTO, CCXTCurrencyDTO, CCXTTickerDTO
from decimal import Decimal


def map_market(dto: CCXTMarketDTO, exchange: ExchangeId) -> tuple[MarketId, MarketInfo]:
    """Мэппинг DTO CCXT → доменная структура MarketInfo."""
    pair = TradingPair.from_string(dto.symbol)
    market_id = MarketId(
        pair=pair,
        exchange=exchange,
        market_type=MarketType(dto.type) if dto.type else MarketType.SPOT
    )
    market_info = MarketInfo(
        market_id=market_id,
        maker_fee=Decimal(dto.maker or 0),
        taker_fee=Decimal(dto.taker or 0),
        percentage=bool(dto.percentage)
    )
    return market_id, market_info


def map_asset(dto: CCXTCurrencyDTO, exchange: ExchangeId) -> tuple[tuple[Asset, ExchangeId], AssetInfo]:
    """Мэппинг DTO CCXT → доменная структура AssetInfo."""
    asset = Asset(dto.code)
    networks = []
    if dto.networks:
        for net_name, net_dto in dto.networks.items():
            networks.append(AssetNetwork(
                asset=asset,
                network=net_name,
                withdraw_fee=Decimal(getattr(net_dto, "fee", 0) or 0),
                withdraw_speed=0.0  # у CCXT нет данных
            ))
    asset_info = AssetInfo(
        asset=asset,
        exchange=exchange,
        networks=networks
    )
    return (asset, exchange), asset_info

def map_price(dto: CCXTTickerDTO, exchange: ExchangeId) -> tuple[TradingPair, Quote] | None:
    """Мэппинг ticker DTO → (TradingPair, Quote) — или None если bid/ask отсутствуют"""
    if not dto.bid or not dto.ask:
        return None  # этот тикер не подходит

    pair = TradingPair.from_string(dto.symbol)
    quote = Quote(
        trading_pair=pair,
        bid=Decimal(dto.bid),
        ask=Decimal(dto.ask),
        exchange=exchange,
    )
    return pair, quote