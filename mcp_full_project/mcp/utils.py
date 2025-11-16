import asyncio, functools
from typing import Callable, Any

def retry(attempts: int = 3, delay: float = 0.5):
    def deco(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exc = None
            for i in range(attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    await asyncio.sleep(delay)
            raise last_exc
        return wrapper
    return deco
