from dataclasses import dataclass
from decimal import Decimal

from pauchai_scanner.domain.value_objects import  TradingPair


@dataclass
class ArbitrageOpportunity:
    pair: TradingPair
    buy_exchange: str
    sell_exchange: str
    estimated_profit: Decimal
    # Новые поля для расширенного сервиса:
    #real_profit: Decimal | None = None  # Фактическая прибыль
    #status: str = "candidate"          # Статус возможности
    #buy_url: str | None = None          # Ссылка на торговую страницу покупки
    #sell_url: str | None = None         # Ссылка на торговую страницу продажи
    buy_network: str | None = None      # Сеть для ввода на биржу покупки
    sell_network: str | None = None     # Сеть для вывода с биржи продажи
    withdraw_fee: Decimal | None = None # Комиссия сети на вывод
    withdraw_speed: float | None = None # Скорость вывода (часы)