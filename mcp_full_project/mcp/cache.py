import asyncio, time
from typing import Any, Optional

class InMemoryCache:
    def __init__(self):
        self._store = {}
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        async with self._lock:
            exp = time.time() + ttl if ttl else None
            self._store[key] = (value, exp)

    async def get(self, key: str):
        async with self._lock:
            row = self._store.get(key)
            if not row:
                return None
            value, exp = row
            if exp and time.time() > exp:
                del self._store[key]
                return None
            return value

    async def delete(self, key: str):
        async with self._lock:
            if key in self._store:
                del self._store[key]

global_cache = InMemoryCache()
