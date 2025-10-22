from pydantic import BaseModel


class CCXTTickerDTO(BaseModel):
    symbol: str
    bid: float | None
    ask: float | None
    exchange: str

    class ConfigDict:
        extra = "ignore"

class CCXTMarketDTO(BaseModel):
    type: str
    symbol: str
    maker: float | None
    taker: float | None
    percentage: bool | None

    class ConfigDict:
        extra = "ignore"

class CCXTNetworkLimitsDTO(BaseModel):
    withdraw: dict[str, float] | None
    deposit: dict[str, float] | None

    class ConfigDict:
        extra = "ignore"
class CCXTNetworkDTO(BaseModel):
    id: str
    network: str 
    active: bool
    deposit: bool 
    withdraw: bool
    fee: float 
    precision: int 
    limits: CCXTNetworkLimitsDTO 

    class ConfigDict:
        extra = "ignore"

class CCXTCurrencyDTO(BaseModel):
    code: str
    name: str | None
    active: bool | None
    fee: float | None
    precision: int | None
    networks: list[CCXTNetworkDTO] | None

    class ConfigDict:
        extra = "ignore"