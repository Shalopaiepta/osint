import aiohttp
from datetime import datetime
from config import VK_TOKEN, VK_API_BASE, VK_API_VERSION
from utils.models import PersonResult
from utils.rate_limiter import rate_limited

SOURCE_NAME = "vk"

SEARCH_FIELDS = "photo_200,city,country,bdate,education,contacts,site,status,followers_count"


async def _vk_request(session: aiohttp.ClientSession, method: str, params: dict) -> dict:
    params = {**params, "access_token": VK_TOKEN, "v": VK_API_VERSION}
    async with session.get(f"{VK_API_BASE}/{method}", params=params) as resp:
        resp.raise_for_status()
        data = await resp.json()
        if "error" in data:
            raise RuntimeError(f"VK API error {data['error']['error_code']}: {data['error']['error_msg']}")
        return data["response"]


@rate_limited(delay=0.4)
async def search_users(session: aiohttp.ClientSession, query: str) -> list[dict]:
    data = await _vk_request(session, "users.search", {
        "q": query,
        "count": 10,
        "fields": SEARCH_FIELDS,
    })
    return data.get("items", [])


@rate_limited(delay=0.4)
async def get_friends(session: aiohttp.ClientSession, user_id: int) -> list[dict]:
    try:
        data = await _vk_request(session, "friends.get", {
            "user_id": user_id,
            "fields": "first_name,last_name",
            "count": 50,
        })
        return data.get("items", [])
    except RuntimeError:
        return []


@rate_limited(delay=0.4)
async def get_groups(session: aiohttp.ClientSession, user_id: int) -> list[dict]:
    try:
        data = await _vk_request(session, "groups.get", {
            "user_id": user_id,
            "extended": 1,
            "count": 30,
        })
        return data.get("items", [])
    except RuntimeError:
        return []


@rate_limited(delay=0.4)
async def get_wall(session: aiohttp.ClientSession, user_id: int) -> list[dict]:
    try:
        data = await _vk_request(session, "wall.get", {
            "owner_id": user_id,
            "count": 10,
            "filter": "owner",
        })
        return data.get("items", [])
    except RuntimeError:
        return []


async def fetch(user: dict) -> PersonResult:
    errors = []
    user_id = user["id"]

    try:
        async with aiohttp.ClientSession() as session:
            friends, groups, wall = (
                await get_friends(session, user_id),
                await get_groups(session, user_id),
                await get_wall(session, user_id),
            )
    except Exception as e:
        errors.append(str(e))
        friends, groups, wall = [], [], []

    return PersonResult(
        source=SOURCE_NAME,
        found=True,
        data={
            "profile": user,
            "friends": friends,
            "groups": groups,
            "wall": wall,
        },
        errors=errors,
        timestamp=datetime.now(),
    )
