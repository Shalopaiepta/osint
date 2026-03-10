from telethon import TelegramClient
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")

async def main():
    print(f"Используем api_id={api_id}, api_hash={api_hash[:6]}...")
    client = TelegramClient("test_session", api_id, api_hash)
    await client.start(phone=lambda: input("Введи номер телефона: "))
    print("Авторизация успешна!")
    me = await client.get_me()
    print(f"Вошёл как: {me.first_name} {me.last_name or ''} (@{me.username or 'нет'})")
    await client.disconnect()

asyncio.run(main())