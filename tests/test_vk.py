import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from modules.vk import fetch, search_users
from utils.models import PersonResult


MOCK_USER = {
    "id": 1,
    "first_name": "Иван",
    "last_name": "Петров",
    "status": "тест",
    "bdate": "1.1.1990",
    "city": {"title": "Москва"},
    "country": {"title": "Россия"},
    "followers_count": 100,
    "site": "",
}


@pytest.mark.asyncio
async def test_fetch_success():
    with (
        patch("modules.vk.get_friends", new=AsyncMock(return_value=[{"first_name": "А", "last_name": "Б"}])),
        patch("modules.vk.get_groups", new=AsyncMock(return_value=[{"name": "Группа"}])),
        patch("modules.vk.get_wall", new=AsyncMock(return_value=[{"text": "Пост"}])),
        patch("aiohttp.ClientSession", MagicMock()),
    ):
        result = await fetch(MOCK_USER)

    assert isinstance(result, PersonResult)
    assert result.source == "vk"
    assert result.found is True
    assert result.data["profile"]["id"] == 1
    assert result.errors == []


@pytest.mark.asyncio
async def test_fetch_partial_failure():
    with (
        patch("modules.vk.get_friends", new=AsyncMock(side_effect=RuntimeError("закрыт"))),
        patch("modules.vk.get_groups", new=AsyncMock(return_value=[])),
        patch("modules.vk.get_wall", new=AsyncMock(return_value=[])),
        patch("aiohttp.ClientSession", MagicMock()),
    ):
        result = await fetch(MOCK_USER)

    assert result.found is True
    assert len(result.errors) > 0


@pytest.mark.asyncio
async def test_fetch_sets_timestamp():
    with (
        patch("modules.vk.get_friends", new=AsyncMock(return_value=[])),
        patch("modules.vk.get_groups", new=AsyncMock(return_value=[])),
        patch("modules.vk.get_wall", new=AsyncMock(return_value=[])),
        patch("aiohttp.ClientSession", MagicMock()),
    ):
        result = await fetch(MOCK_USER)

    assert result.timestamp is not None
