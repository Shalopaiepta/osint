import pytest
from unittest.mock import patch, MagicMock
from modules.web_search import fetch
from utils.models import PersonResult


MOCK_RESULTS = [
    {"title": "Иван Петров", "href": "https://example.com", "body": "описание"},
    {"title": "Петров Иван", "href": "https://vk.com/ivan", "body": ""},
]


@pytest.mark.asyncio
async def test_fetch_returns_results():
    with patch("modules.web_search._search_sync", return_value=MOCK_RESULTS):
        result = await fetch("Иван Петров")

    assert isinstance(result, PersonResult)
    assert result.source == "web"
    assert result.found is True
    assert len(result.data["results"]) == 2
    assert result.errors == []


@pytest.mark.asyncio
async def test_fetch_empty_results():
    with patch("modules.web_search._search_sync", return_value=[]):
        result = await fetch("zzz_nonexistent_xyz")

    assert result.found is False
    assert result.data["results"] == []


@pytest.mark.asyncio
async def test_fetch_exception_is_captured():
    with patch("modules.web_search._search_sync", side_effect=Exception("сеть недоступна")):
        result = await fetch("Иван Петров")

    assert result.found is False
    assert "сеть недоступна" in result.errors[0]


@pytest.mark.asyncio
async def test_fetch_stores_query():
    with patch("modules.web_search._search_sync", return_value=MOCK_RESULTS):
        result = await fetch("Иван Петров Москва")

    assert result.data["query"] == "Иван Петров Москва"
