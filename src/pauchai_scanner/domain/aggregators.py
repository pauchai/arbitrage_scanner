from typing import List
from pauchai_scanner.domain.value_objects import AssetInfo, ExchangeId, MarketId, MarketInfo, Quote, TradingPair, Asset


MarketBook =  dict[MarketId, MarketInfo]

PriceBook = dict[TradingPair, List[Quote]]

AssetBook = dict[Asset, AssetInfo]