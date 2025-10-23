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
