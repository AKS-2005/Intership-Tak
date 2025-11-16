from fastapi.testclient import TestClient
from main import app
import asyncio
from mcp import cache, fetchers

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_ticker_and_cache(monkeypatch):
    
    async def fake_fetch(symbol):
        return {"symbol": symbol, "bid": 1.0, "ask": 2.0, "last": 1.5, "volume": 10.0, "source": "fake"}
    monkeypatch.setattr(fetchers, "fetch_from_ccxt", fake_fetch)
    
    asyncio.get_event_loop().run_until_complete(cache.global_cache.delete("ticker:BTC/USDT:best"))
    r = client.get("/ticker/BTC/USDT")
    assert r.status_code == 200
    js = r.json()
    assert js["symbol"] == "BTC/USDT"
    
    r2 = client.get("/ticker/BTC/USDT")
    assert r2.status_code == 200

def test_history_endpoint():
    r = client.get("/history/BTC/USDT?limit=5")
    assert r.status_code == 200
    js = r.json()
    assert js["count"] == 5
