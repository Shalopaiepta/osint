import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.functions.contacts import SearchRequest
from telethon.errors import FloodWaitError, UsernameInvalidError, UsernameNotOccupiedError
from config import TG_API_ID, TG_API_HASH, TG_SESSION_NAME
from utils.models import PersonResult

SOURCE_NAME = "telegram"


async def fetch(query: str) -> PersonResult:
    errors = []
    data = {}

    try:
        skip = input("Telegram — пропустить? (Enter = пропустить, n = войти): ").strip().lower()
        if skip != "n":
            return PersonResult(source=SOURCE_NAME, found=False, data={"skipped": True}, errors=[], timestamp=datetime.now())

        client = TelegramClient(TG_SESSION_NAME, int(TG_API_ID), TG_API_HASH)
        await client.start(phone=lambda: input("Введи номер телефона (например +79001234567): "))
        print("Авторизация успешна!")
        data = await _collect(client, query)
        await client.disconnect()

    except FloodWaitError as e:
        print(f"Telegram error: FloodWait {e.seconds}s")
        errors.append(f"Telegram flood wait: {e.seconds}s")
    except Exception as e:
        print(f"Telegram error: {e}")
        errors.append(str(e))

    return PersonResult(
        source=SOURCE_NAME,
        found=bool(data),
        data=data,
        errors=errors,
        timestamp=datetime.now(),
    )


async def _collect(client: TelegramClient, query: str) -> dict:
    result = {}

    try:
        search = await client(SearchRequest(q=query, limit=5))
        users = []
        for u in search.users:
            users.append({
                "id": u.id,
                "first_name": u.first_name or "",
                "last_name": u.last_name or "",
                "username": u.username or "",
                "phone": u.phone or "",
            })
        result["users"] = users
    except Exception as e:
        print(f"Telegram search error: {e}")
        result["users"] = []

    if query.startswith("@"):
        username = query.lstrip("@")
        try:
            entity = await client.get_entity(username)
            result["entity"] = {
                "id": entity.id,
                "title": getattr(entity, "title", None),
                "username": getattr(entity, "username", None),
                "participants_count": getattr(entity, "participants_count", None),
            }
            messages = []
            async for msg in client.iter_messages(entity, limit=5):
                messages.append({"id": msg.id, "text": msg.text, "date": str(msg.date)})
            result["recent_messages"] = messages
        except (UsernameInvalidError, UsernameNotOccupiedError):
            result["entity"] = None
        except Exception as e:
            print(f"Telegram entity error: {e}")
            result["entity_error"] = str(e)

    return result