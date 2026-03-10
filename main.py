import asyncio
import sys
from rich.console import Console
from rich.prompt import Prompt
from config import validate_config
from orchestrator import run
from output.renderer import render_results

console = Console()


async def main():
    console.print("[bold white]OSINT Tool[/bold white] — локальный сбор публичной информации\n")

    try:
        validate_config()
    except EnvironmentError as e:
        console.print(f"[bold red]Ошибка конфигурации:[/bold red] {e}")
        console.print("Создай файл [bold].env[/bold] по образцу [bold].env.example[/bold]")
        sys.exit(1)

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = Prompt.ask("[bold]Введи имя или username[/bold]")

    if not query.strip():
        console.print("[red]Запрос не может быть пустым[/red]")
        sys.exit(1)

    console.print(f"\n[dim]Поиск: {query}[/dim]\n")

    results = await run(query.strip())
    render_results(results)


if __name__ == "__main__":
    asyncio.run(main())
