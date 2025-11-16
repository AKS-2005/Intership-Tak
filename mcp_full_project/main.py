from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from typing import Optional
import asyncio
from mcp import fetchers, cache, schemas, errors


app = FastAPI(title="MCP - Market Data Collector & Processor")

@app.get("/health", response_model=schemas.Health)
async def health():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/ticker/{symbol}", response_model=schemas.TickerData)
async def get_ticker(symbol: str, source: Optional[str] = Query(None, description="ccxt | cmc"), use_cache: bool = True):
    try:
        key = f"ticker:{symbol}:{source or 'best'}"
        if use_cache:
            cached = await cache.global_cache.get(key)
            if cached:
                return cached
        if source == "ccxt":
            data = await fetchers.fetch_from_ccxt(symbol)
        elif source == "cmc":
            data = await fetchers.fetch_from_cmc(symbol)
        else:
            # try CCXT then CMC, fallback to simulated
            try:
                data = await fetchers.fetch_from_ccxt(symbol)
            except Exception:
                data = await fetchers.fetch_from_cmc(symbol)
        if use_cache:
            await cache.global_cache.set(key, data, ttl=5)
        return data
    except Exception as exc:
        raise errors.ApiException(status_code=502, detail=str(exc))

@app.get("/history/{symbol}")
async def get_history(symbol: str, start: Optional[int] = None, end: Optional[int] = None, limit: int = 100):
    try:
        history = await fetchers.fetch_historical(symbol, start=start, end=end, limit=limit)
        return {"symbol": symbol, "count": len(history), "data": history}
    except Exception as exc:
        raise errors.ApiException(status_code=502, detail=str(exc))

@app.websocket("/ws/subscribe/{symbol}")
async def ws_subscribe(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        for tick in fetchers.simulated_tick_stream(symbol):
            await websocket.send_json(tick)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        return
    except Exception:
        await websocket.close(code=1011)

@app.exception_handler(errors.ApiException)
async def api_exception_handler(request, exc: errors.ApiException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
