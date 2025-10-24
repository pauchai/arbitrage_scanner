# Arbitrage Scanner

> **Ведётся разработка PRO-версии!**
> Подробнее: https://github.com/arbitrage-scanner-pro
> Вопросы и предложения — Telegram: [@montepauk](https://t.me/montepauk)

## Описание
Arbitrage Scanner — сервис для поиска межбиржевых арбитражных возможностей на криптовалютных биржах. Проект реализован на принципах DDD/TDD, поддерживает интеграцию с CCXT, покрыт тестами, имеет CLI и легко расширяется.

### Основные возможности
- Поиск арбитражных возможностей между биржами
- Интеграция с реальными провайдерами через CCXT
- Гибкая работа с торговыми парами (pairs=None)
- Устойчивость к ошибкам парсинга тикеров
- Корректная работа DTO (Pydantic v2)
- CLI для запуска и анализа арбитража
- Мэпперы для преобразования DTO → агрегаторы
- Полное покрытие unit и integration тестами

### Поддерживаемые биржи

[![Binance](https://github.com/user-attachments/assets/e9419b93-ccb0-46aa-9bff-c883f096274b)](https://www.binance.com/activity/referral-entry/CPA?ref=CPA_00JM9DOEP3)
[![Bybit](https://github.com/user-attachments/assets/97a5d0b3-de10-423d-90e1-6620960025ed)](https://www.bybit.com/invite?ref=ZL4WLP8)
[![BingX](https://github-production-user-asset-6210df.s3.amazonaws.com/1294454/253675376-6983b72e-4999-4549-b177-33b374c195e3.jpg)](https://bingx.com/invite/GJKWDY/)
[![KuCoin](https://user-images.githubusercontent.com/51840849/87295558-132aaf80-c50e-11ea-9801-a2fb0c57c799.jpg)](https://www.kucoin.com/r/rf/CX8XUX73)
![OKX](https://user-images.githubusercontent.com/1294454/152485636-38b19e4a-bece-4dec-979a-5982859ffc04.jpg)
[![MEXC](https://user-images.githubusercontent.com/1294454/137283979-8b2a818d-8633-461b-bfca-de89e8c446b2.jpg)](https://promote.mexc.com/r/QpfKQfw8)
[![HTX](https://user-images.githubusercontent.com/1294454/76137448-22748a80-604e-11ea-8069-6e389271911d.jpg)](https://www.htx.com/invite/ru-ru/1f?invite_code=4g7jd223)
[![BitMart](https://github.com/user-attachments/assets/0623e9c4-f50e-48c9-82bd-65c3908c3a14)](https://www.bitmart.com/invite/cVxrKu)

### Структура проекта
- `src/` — исходный код
- `tests/` — тесты (unit/integration)
- `notebooks/` — примеры и эксперименты (Pydantic, CCXT)
- `.env.example` — шаблон переменных окружения для API ключей

### Быстрый старт
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/pauchai/arbitrage_scanner.git
   cd arbitrage_scanner
   ```
2. Создайте и настройте `.env` на основе `.env.example`.
3. Установите зависимости:
   ```bash
   poetry install
   ```
4. Запустите тесты:
   ```bash
   poetry run pytest
   ```
5. Запустите CLI:
   ```bash
   poetry run python src/pauchai_scanner/endpoints/cli.py --find-arb --quoted-asset USDT
   ```

### Контакты
- Telegram: [@montepauk](https://t.me/montepauk)

---
Если у вас есть вопросы или предложения — пишите в Telegram!
