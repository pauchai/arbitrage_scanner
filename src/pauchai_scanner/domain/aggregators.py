from typing import List, NewType
from pauchai_scanner.domain.value_objects import AssetInfo, ExchangeId, MarketId, MarketInfo, Quote, TradingPair, Asset


MarketBook =  dict[MarketId, MarketInfo]

PriceBook = dict[TradingPair, List[Quote]]

# AssetBook теперь различает биржи
AssetBook = dict[tuple[Asset, ExchangeId], AssetInfo]