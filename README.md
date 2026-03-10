# OSINT Tool

Локальный CLI-инструмент для сбора публичной информации о человеке из VK, Telegram и веб-поиска.

## Установка

```bash
cd osint_tool
pip install -r requirements.txt
```

## Настройка

1. Скопируй `.env.example` в `.env`:
   ```bash
   cp .env.example .env
   ```

2. Заполни `.env`:
   - **VK_TOKEN** — сервисный ключ приложения VK: https://vk.com/apps (создай standalone-приложение)
   - **TG_API_ID / TG_API_HASH** — получи на https://my.telegram.org → API development tools

## Запуск

```bash
python main.py "Иван Петров"
```

или без аргумента — программа спросит сама:

```bash
python main.py
```

При первом запуске Telegram попросит авторизацию по номеру телефона — это нормально, сессия сохранится локально.

## Тесты

```bash
pytest tests/ -v
```
