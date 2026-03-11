import asyncio
import aiohttp
import ssl
from datetime import datetime
from config import SERPAPI_KEY
from utils.models import PersonResult

SOURCE_NAME = "web"

SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


async def fetch(query: str) -> PersonResult:
    errors = []
    results = []

    try:
        results = await _search(query)
    except Exception as e:
        errors.append(str(e))

    return PersonResult(
        source=SOURCE_NAME,
        found=bool(results),
        data={"query": query, "results": results},
        errors=errors,
        timestamp=datetime.now(),
    )


async def _search(query: str) -> list[dict]:
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 10,
        "hl": "ru",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get("https://serpapi.com/search", params=params, ssl=SSL_CONTEXT) as resp:
            resp.raise_for_status()
            data = await resp.json()
            results = []
            for r in data.get("organic_results", []):
                results.append({
                    "title": r.get("title", ""),
                    "href": r.get("link", ""),
                    "body": r.get("snippet", ""),
                })
            return results