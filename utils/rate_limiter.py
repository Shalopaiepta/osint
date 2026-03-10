import asyncio
import functools


def rate_limited(delay: float = 0.4):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            await asyncio.sleep(delay)
            return result
        return wrapper
    return decorator


async def retry(coro_func, retries: int = 3, delay: float = 2.0, *args, **kwargs):
    last_exc = None
    for attempt in range(retries):
        try:
            return await coro_func(*args, **kwargs)
        except Exception as e:
            last_exc = e
            if attempt < retries - 1:
                await asyncio.sleep(delay * (attempt + 1))
    raise last_exc
