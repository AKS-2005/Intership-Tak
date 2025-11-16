import asyncio, random, time, os
from typing import Dict, Any, List
from .utils import retry

SIMULATED_BASE = 100.0


try:
    import httpx
except Exception:
    httpx = None

try:
    import ccxt.async_support as ccxt
except Exception:
    ccxt = None

try:
    from . import config
except Exception:
    config = None

# Helper
def _live_ok(use: str = None):
    if config and getattr(config, "FORCE_SIMULATED", False):
        return False
    if use == "cmc":
        return httpx is not None and config and getattr(config, "CMC_API_KEY", None)
    if use == "ccxt":
        return ccxt is not None
    return (httpx is not None and config and getattr(config, "CMC_API_KEY", None)) or (ccxt is not None)


async def _fetch_ccxt_real(symbol: str) -> Dict[str, Any]:
    if not ccxt:
        raise RuntimeError("ccxt not available")
    exchange = ccxt.binance()
    try:
        ticker = await exchange.fetch_ticker(symbol)
        await exchange.close()
        return {
            "symbol": symbol,
            "bid": ticker.get("bid"),
            "ask": ticker.get("ask"),
            "last": ticker.get("last"),
            "volume": ticker.get("baseVolume") or ticker.get('quoteVolume'),
            "source": "ccxt",
            "raw": ticker
        }
    except Exception:
        await exchange.close()
        raise

# 
CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
async def _fetch_cmc_real(symbol: str) -> Dict[str, Any]:
    if not httpx:
        raise RuntimeError("httpx not available")
    if not config or not getattr(config, "CMC_API_KEY", None):
        raise RuntimeError("CMC API key not configured")
    params = {"symbol": symbol.replace("/", "")}
    headers = {"X-CMC_PRO_API_KEY": getattr(config, "CMC_API_KEY")}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(CMC_URL, params=params, headers=headers)
        r.raise_for_status()
        data = r.json()
    
    symbol_key = params["symbol"]
    quote = data.get("data", {}).get(symbol_key, {}).get("quote", {}).get("USD", {})
    price = quote.get("price")
    if price is None:
        raise RuntimeError("Unexpected CMC response structure")
    return {
        "symbol": symbol,
        "bid": price * 0.999,
        "ask": price * 1.001,
        "last": price,
        "volume": quote.get("volume_24h"),
        "source": "cmc",
        "raw": quote
    }


@retry(attempts=2, delay=0.2)
async def fetch_from_ccxt(symbol: str) -> Dict[str, Any]:
    if _live_ok("ccxt"):
        try:
            return await _fetch_ccxt_real(symbol)
        except Exception:
            pass
    
    await asyncio.sleep(0.01)
    price = SIMULATED_BASE + random.random() * 10
    return {"symbol": symbol, "bid": round(price - 0.1,6), "ask": round(price + 0.1,6), "last": round(price,6), "volume": round(random.random()*1000,6), "source": "simulated"}

@retry(attempts=2, delay=0.2)
async def fetch_from_cmc(symbol: str) -> Dict[str, Any]:
    if _live_ok("cmc"):
        try:
            return await _fetch_cmc_real(symbol)
        except Exception:
            pass
    
    await asyncio.sleep(0.01)
    price = SIMULATED_BASE + random.random() * 12
    return {"symbol": symbol, "bid": round(price - 0.2,6), "ask": round(price + 0.2,6), "last": round(price,6), "volume": round(random.random()*2000,6), "source": "simulated"}

# Historical OHLCV 
async def fetch_historical(symbol: str, start: int = None, end: int = None, limit: int = 100) -> List[Dict[str,Any]]:
    now = int(time.time())
    step = 60
    candles = []
    for i in range(limit):
        t = now - i*step
        price = SIMULATED_BASE + (i % 10) + (random.random()-0.5)*2
        candles.append({"t": t, "open": price-0.3, "high": price+0.5, "low": price-0.6, "close": price, "volume": round(random.random()*1000,3)})
    return list(reversed(candles))

# Simple sync 
def simulated_tick_stream(symbol: str):
    base = SIMULATED_BASE
    while True:
        base += (random.random() - 0.5) * 0.5
        tick = {"symbol": symbol, "last": round(base,6), "bid": round(base-0.1,6), "ask": round(base+0.1,6), "ts": int(time.time())}
        yield tick
