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

### Contacts
- Telegram: [@montepauk](https://t.me/montepauk)

---
If you have any questions or suggestions, feel free to contact via Telegram!
