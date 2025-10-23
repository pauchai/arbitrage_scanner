from pydantic import BaseModel, ConfigDict


class CCXTTickerDTO(BaseModel):
    symbol: str
    bid: float | None
    ask: float | None

    model_config = ConfigDict(extra="ignore")

class CCXTMarketDTO(BaseModel):
    type: str
    symbol: str
    maker: float | None
    taker: float | None
    percentage: bool | None = None

    model_config = ConfigDict(extra="ignore")


class CCXTNetworkLimitsDTO(BaseModel):
    withdraw: dict[str, float | None] | None = None
    deposit: dict[str, float | None] | None = None

    model_config = ConfigDict(extra="ignore")

class CCXTNetworkDTO(BaseModel):
    id: str
    active: bool
    deposit: bool 
    withdraw: bool
    fee: float | None = None         # ← иногда приходит строка или null
    limits: CCXTNetworkLimitsDTO | None = None  # ← иногда вообще отсутствует
    model_config = ConfigDict(extra="ignore")


class CCXTCurrencyDTO(BaseModel):
    code: str
    name: str | None
    active: bool | None
    fee: float | None
    precision: float | None = None
    networks: dict[str, CCXTNetworkDTO] | None = None

    model_config = ConfigDict(extra="ignore")
