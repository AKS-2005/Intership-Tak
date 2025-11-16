import asyncio
import types
from mcp import fetchers

def test_fetch_from_ccxt_simulated():
    
    data = asyncio.get_event_loop().run_until_complete(fetchers.fetch_from_ccxt("BTC/USDT"))
    assert isinstance(data, dict)
    assert data["symbol"] == "BTC/USDT"
    assert "last" in data and isinstance(data["last"], float)

def test_fetch_historical_length():
    hist = asyncio.get_event_loop().run_until_complete(fetchers.fetch_historical("BTC/USDT", limit=10))
    assert isinstance(hist, list)
    assert len(hist) == 10
    assert "open" in hist[0] and "close" in hist[0]
