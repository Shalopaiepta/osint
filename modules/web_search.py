import asyncio
from datetime import datetime
from duckduckgo_search import DDGS
from config import DDGS_MAX_RESULTS
from utils.models import PersonResult

SOURCE_NAME = "web"


async def fetch(query: str) -> PersonResult:
    errors = []
    results = []

    try:
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, _search_sync, query)
    except Exception as e:
        errors.append(str(e))

    return PersonResult(
        source=SOURCE_NAME,
        found=bool(results),
        data={"query": query, "results": results},
        errors=errors,
        timestamp=datetime.now(),
    )


def _search_sync(query: str) -> list[dict]:
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=DDGS_MAX_RESULTS))
