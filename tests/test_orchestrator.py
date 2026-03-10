import pytest
from unittest.mock import AsyncMock, patch
from orchestrator import safe_run, run
from utils.models import PersonResult
from datetime import datetime


def _make_result(source: str, found: bool = True) -> PersonResult:
    return PersonResult(source=source, found=found, data={}, errors=[], timestamp=datetime.now())


@pytest.mark.asyncio
async def test_safe_run_returns_result_on_success():
    async def good():
        return _make_result("vk")

    result = await safe_run(good())
    assert result.source == "vk"
    assert result.found is True


@pytest.mark.asyncio
async def test_safe_run_catches_exception():
    async def bad():
        raise RuntimeError("упал")

    result = await safe_run(bad())
    assert result.found is False
    assert "упал" in result.errors[0]


@pytest.mark.asyncio
async def test_run_skips_vk_when_user_not_picked():
    with (
        patch("orchestrator.pick_vk_user", new=AsyncMock(return_value=None)),
        patch("orchestrator.web_search.fetch", new=AsyncMock(return_value=_make_result("web"))),
        patch("orchestrator.telegram.fetch", new=AsyncMock(return_value=_make_result("telegram"))),
    ):
        results = await run("Иван Петров")

    sources = [r.source for r in results]
    assert "vk" not in sources
    assert "web" in sources
    assert "telegram" in sources


@pytest.mark.asyncio
async def test_run_includes_vk_when_user_picked():
    mock_user = {"id": 1, "first_name": "Иван", "last_name": "Петров"}

    with (
        patch("orchestrator.pick_vk_user", new=AsyncMock(return_value=mock_user)),
        patch("orchestrator.vk.fetch", new=AsyncMock(return_value=_make_result("vk"))),
        patch("orchestrator.web_search.fetch", new=AsyncMock(return_value=_make_result("web"))),
        patch("orchestrator.telegram.fetch", new=AsyncMock(return_value=_make_result("telegram"))),
    ):
        results = await run("Иван Петров")

    sources = [r.source for r in results]
    assert "vk" in sources
    assert "web" in sources
    assert "telegram" in sources
