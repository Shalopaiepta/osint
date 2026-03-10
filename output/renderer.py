from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from utils.models import PersonResult

console = Console()


def render_results(results: list[PersonResult]):
    for result in results:
        if result.source == "vk":
            _render_vk(result)
        elif result.source == "web":
            _render_web(result)
        elif result.source == "telegram":
            _render_telegram(result)

        if result.errors:
            for err in result.errors:
                console.print(f"  [red]⚠ Ошибка:[/red] {err}")


def _render_vk(result: PersonResult):
    console.rule("[bold blue]VK")

    if not result.found:
        console.print("[yellow]Профиль не найден[/yellow]")
        return

    profile = result.data.get("profile", {})
    name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
    uid = profile.get("id", "")
    status = profile.get("status", "")
    bdate = profile.get("bdate", "")
    city = profile.get("city", {}).get("title", "")
    country = profile.get("country", {}).get("title", "")
    followers = profile.get("followers_count", "")
    site = profile.get("site", "")

    info = Table.grid(padding=(0, 2))
    info.add_column(style="bold cyan")
    info.add_column()
    info.add_row("Имя:", name)
    info.add_row("ID:", str(uid))
    info.add_row("Ссылка:", f"https://vk.com/id{uid}")
    if bdate:
        info.add_row("Дата рождения:", bdate)
    if city or country:
        info.add_row("Город/Страна:", f"{city}, {country}".strip(", "))
    if followers:
        info.add_row("Подписчики:", str(followers))
    if status:
        info.add_row("Статус:", status)
    if site:
        info.add_row("Сайт:", site)

    console.print(Panel(info, title="Профиль"))

    friends = result.data.get("friends", [])
    if friends:
        console.print(f"\n[bold]Друзья[/bold] (первые {len(friends)}):")
        for f in friends:
            console.print(f"  • {f.get('first_name', '')} {f.get('last_name', '')}")

    groups = result.data.get("groups", [])
    if groups:
        console.print(f"\n[bold]Группы[/bold] (первые {len(groups)}):")
        for g in groups:
            console.print(f"  • {g.get('name', '')}")

    wall = result.data.get("wall", [])
    if wall:
        console.print(f"\n[bold]Последние посты[/bold] (первые {len(wall)}):")
        for post in wall:
            text = (post.get("text", "") or "")[:120]
            if text:
                console.print(f"  └ {text}")


def _render_web(result: PersonResult):
    console.rule("[bold green]Веб-поиск")

    if not result.found:
        console.print("[yellow]Ничего не найдено[/yellow]")
        return

    query = result.data.get("query", "")
    console.print(f"Запрос: [italic]{query}[/italic]\n")

    for i, r in enumerate(result.data.get("results", []), 1):
        title = r.get("title", "")
        url = r.get("href", "")
        body = (r.get("body", "") or "")[:100]
        console.print(f"[bold]{i}.[/bold] {title}")
        console.print(f"   [dim]{url}[/dim]")
        if body:
            console.print(f"   {body}")
        console.print()


def _render_telegram(result: PersonResult):
    console.rule("[bold magenta]Telegram")

    if not result.found:
        console.print("[yellow]Ничего не найдено[/yellow]")
        return

    users = result.data.get("users", [])
    if users:
        console.print(f"[bold]Найденные пользователи[/bold] ({len(users)}):")
        for u in users:
            line = f"  • {u.get('first_name', '')} {u.get('last_name', '')}".strip()
            if u.get("username"):
                line += f" (@{u['username']})"
            if u.get("phone"):
                line += f" — {u['phone']}"
            console.print(line)

    entity = result.data.get("entity")
    if entity:
        console.print(f"\n[bold]Канал/группа:[/bold]")
        console.print(f"  Название: {entity.get('title', '')}")
        if entity.get("username"):
            console.print(f"  Username: @{entity['username']}")
        if entity.get("participants_count"):
            console.print(f"  Участников: {entity['participants_count']}")

    messages = result.data.get("recent_messages", [])
    if messages:
        console.print(f"\n[bold]Последние сообщения:[/bold]")
        for m in messages:
            text = (m.get("text") or "")[:120]
            if text:
                console.print(f"  └ {text}")
