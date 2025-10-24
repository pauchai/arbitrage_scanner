# Arbitrage Scanner

[Русская версия README](./README_RU.md)

> **PRO version is under development!**
> See: https://github.com/arbitrage-scanner-pro
> For inquiries, contact Telegram: [@montepauk](https://t.me/montepauk)

## Description
Arbitrage Scanner is a service for searching inter-exchange arbitrage opportunities on cryptocurrency exchanges. The project is built with DDD/TDD principles, integrates with CCXT, is fully tested, features a CLI, and is easily extensible.

### Features
- Search for arbitrage opportunities between exchanges
- Integration with real providers via CCXT
- Flexible trading pairs support (pairs=None)
- Robust error handling for ticker parsing
- Correct DTO handling (Pydantic v2)
- CLI for running and analyzing arbitrage
- Mappers for DTO → aggregator conversion
- Full unit and integration test coverage

### Project Structure
- `src/` — source code
- `tests/` — unit/integration tests
- `notebooks/` — examples and experiments (Pydantic, CCXT)
- `.env.example` — environment variable template for API keys

### Quick Start
1. Clone the repository:
	```bash
	git clone https://github.com/pauchai/arbitrage_scanner.git
	cd arbitrage_scanner
	```
2. Create and configure `.env` based on `.env.example`.
3. Install dependencies:
	```bash
	poetry install
	```
4. Run tests:
	```bash
	poetry run pytest
	```
5. Run CLI:
	```bash
	poetry run python src/pauchai_scanner/endpoints/cli.py --find-arb --quoted-asset USDT
	```

### Supported Exchanges

| Exchange | Logo & Referral |
|----------|----------------|
| Binance  | <a href="https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00JM9DOEP3" target="_blank"><img src="https://github.com/user-attachments/assets/e9419b93-ccb0-46aa-9bff-c883f096274b" alt="Binance" height="32"/></a> |
| Bybit    | <a href="https://www.bybit.com/invite?ref=ZL4WLP8" target="_blank"><img src="https://github.com/user-attachments/assets/97a5d0b3-de10-423d-90e1-6620960025ed" alt="Bybit" height="32"/></a> |
| BingX    | <a href="https://bingx.com/invite/GJKWDY/" target="_blank"><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/1294454/253675376-6983b72e-4999-4549-b177-33b374c195e3.jpg" alt="BingX" height="32"/></a> |
| KuCoin   | <a href="https://www.kucoin.com/r/rf/CX8XUX73" target="_blank"><img src="https://user-images.githubusercontent.com/51840849/87295558-132aaf80-c50e-11ea-9801-a2fb0c57c799.jpg" alt="KuCoin" height="32"/></a> |
| OKX      | <img src="https://user-images.githubusercontent.com/1294454/152485636-38b19e4a-bece-4dec-979a-5982859ffc04.jpg" alt="OKX" height="32"/> |
| MEXC     | <a href="https://promote.mexc.com/r/QpfKQfw8" target="_blank"><img src="https://user-images.githubusercontent.com/1294454/137283979-8b2a818d-8633-461b-bfca-de89e8c446b2.jpg" alt="MEXC" height="32"/></a> |
| HTX      | <a href="https://www.htx.com/invite/ru-ru/1f?invite_code=4g7jd223" target="_blank"><img src="https://user-images.githubusercontent.com/1294454/76137448-22748a80-604e-11ea-8069-6e389271911d.jpg" alt="HTX" height="32"/></a> |
| BitMart  | <a href="https://www.bitmart.com/invite/cVxrKu" target="_blank"><img src="https://github.com/user-attachments/assets/0623e9c4-f50e-48c9-82bd-65c3908c3a14" alt="BitMart" height="32"/></a> |

### Features
