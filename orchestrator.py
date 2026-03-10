import asyncio
import aiohttp
from rich.console import Console
from rich.prompt import Prompt
from modules import vk, web_search, telegram
from utils.models import PersonResult
from datetime import datetime

console = Console()


async def safe_run(coro) -> PersonResult:
    try:
        return await coro
    except Exception as e:
        return PersonResult(
            source="unknown",
            found=False,
            data={},
            errors=[str(e)],
            timestamp=datetime.now(),
        )


async def pick_vk_user(query: str) -> dict | None:
    async with aiohttp.ClientSession() as session:
        users = await vk.search_users(session, query)

    if not users:
        console.print("[yellow]VK: пользователи не найдены[/yellow]")
        return None

    console.print("\n[bold cyan]Найдены пользователи VK:[/bold cyan]")
    for i, u in enumerate(users, 1):
        name = f"{u.get('first_name', '')} {u.get('last_name', '')}".strip()
        city = u.get("city", {}).get("title", "")
        uid = u.get("id", "")
        extra = f" — {city}" if city else ""
        console.print(f"  [bold]{i}.[/bold] {name}{extra}  [dim](id{uid})[/dim]")

    console.print(f"  [bold]0.[/bold] Пропустить VK")

    while True:
        choice = Prompt.ask("Выбери номер", default="1")
        if choice.isdigit() and 0 <= int(choice) <= len(users):
            break
        console.print("[red]Введи число из списка[/red]")

    idx = int(choice)
    if idx == 0:
        return None
    return users[idx - 1]


async def run(query: str) -> list[PersonResult]:
    results = []

    vk_user = await pick_vk_user(query)

    tasks = []

    if vk_user:
        tasks.append(safe_run(vk.fetch(vk_user)))

    tasks.append(safe_run(web_search.fetch(query)))
    tasks.append(safe_run(telegram.fetch(query)))

    gathered = await asyncio.gather(*tasks)
    results.extend(gathered)

    return results