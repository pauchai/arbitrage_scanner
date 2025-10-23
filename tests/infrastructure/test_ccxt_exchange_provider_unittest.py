import pytest
from pauchai_scanner.infrastructure.providers import CCXTExchangeProvider
from pauchai_scanner.domain.value_objects import TradingPair, Asset, MarketId, MarketType
from pauchai_scanner.infrastructure.adapters.ccxt.dtos import CCXTCurrencyDTO, CCXTMarketDTO
import pauchai_scanner.infrastructure.providers as providers

@pytest.mark.asyncio
async def test_get_asset_book_with_mocks(monkeypatch):
    class DummyExchange:
        def __init__(self):
            self.has = {'fetchTickers': True}
        async def load_markets(self):
            return None
        async def fetch_currencies(self):
            return {
                'BTC': {
                    'code': 'BTC',
                    'name': 'Bitcoin',
                    'active': True,
                    'fee': 0.00001,
                    'precision': None,
                    'networks': {
                        'BTC': {
                            'id': 'BTC',
                            'network': 'BTC',
                            'active': True,
                            'deposit': True,
                            'withdraw': True,
                            'fee': 0.0001,
                            'precision': 8,
                            'limits': {'withdraw': {'min': 0.0003}, 'deposit': {'min': 0.00000001}}
                        }
                    }
                }
            }
        async def close(self):
            pass
    class DummyCCXT:
        def __getattr__(self, name):
            return lambda kwargs: DummyExchange()
    monkeypatch.setattr(providers, 'ccxt', DummyCCXT())
    provider = CCXTExchangeProvider('binance', {})
    asset_book = await provider.get_asset_book()
    assert isinstance(asset_book, dict)
    key = (Asset('BTC'), 'binance')
    assert key in asset_book
    asset_info = asset_book[key]
    assert asset_info.asset.symbol == 'BTC'
    assert asset_info.exchange == 'binance'
    assert asset_info.networks[0].network == 'BTC'
    assert asset_info.networks[0].withdraw_fee > 0
    await provider.close()

@pytest.mark.asyncio
async def test_get_market_book_with_mocks(monkeypatch):
    class DummyExchange:
        def __init__(self):
            self.has = {'fetchTickers': True}
        async def load_markets(self):
            return None
        async def fetch_markets(self):
            return [
                {
                    'type': 'spot',
                    'symbol': 'BTC/USDT',
                    'maker': 0.001,
                    'taker': 0.001,
                    'percentage': True
                },
                {
                    'type': 'spot',
                    'symbol': 'ETH/USDT',
                    'maker': 0.002,
                    'taker': 0.002,
                    'percentage': True
                }
            ]
        async def close(self):
            pass
    class DummyCCXT:
        def __getattr__(self, name):
            return lambda kwargs: DummyExchange()
    monkeypatch.setattr(providers, 'ccxt', DummyCCXT())
    provider = CCXTExchangeProvider('binance', {})
    market_book = await provider.get_market_book()
    assert isinstance(market_book, dict)
    pair_btc = TradingPair.from_string('BTC/USDT')
    market_id_btc = MarketId(pair=pair_btc, exchange='binance', market_type=MarketType.SPOT)
    assert market_id_btc in market_book
    btc_market = market_book[market_id_btc]
    assert btc_market.market_id == market_id_btc
    assert btc_market.maker_fee == 0.001
    assert btc_market.taker_fee == 0.001
    assert btc_market.percentage is True
    await provider.close()
