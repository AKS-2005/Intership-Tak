
# MCP – Market Data Collector & Processor 

This project provides a complete scaffold for an MCP-style market-data backend service.
It integrates real crypto-market data sources (like CCXT and CoinMarketCap) while also supporting fully simulated data for testing or offline use.

The architecture is modular, production-ready, and easy to extend.

## What This Project Does

This MCP server acts as a unified market-data layer. It collects, processes, and serves crypto price information through a clean API interface.

It includes:

## FastAPI backend with multiple endpoints

* `/health`
  Basic service-status endpoint.

* `/ticker/{symbol}`
  Returns the latest market price for a given symbol.
  Uses real data when possible, and falls back to simulated data if APIs are unavailable.

* `/history/{symbol}`
  Returns example OHLCV historical data (demo implementation).

* `/ws/subscribe/{symbol}`
  WebSocket endpoint for streaming live tick updates (simulated).


## Key System Components

## **1. Fetchers**

Fetch modules are built with a dual-mode design:

* **Online mode:**
  Uses CCXT and HTTP-based APIs to fetch live data.

* **Offline / test mode:**
  Automatically switches to simulated deterministic data so tests never depend on real networks.

## **2. In-memory async cache**

A lightweight caching layer improves performance and reduces API load.
It can easily be upgraded to Redis for production use.

## **3. Retry utilities**

Reusable functions ensure that temporary API failures are retried safely.

## **4. Custom exception layer**

Provides standardized errors throughout the service, making debugging easier.

## **5. Offline-friendly test suite**

All tests are designed to pass even without internet access.
They work by mocking fetchers or relying on built-in simulated data.

## **6. Dockerfile included**

The server can be containerized and deployed consistently across environments.

---

## **Setup Instructions**

## **1. Create virtual environment & install dependencies**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## **2. Configure project settings**

In development, configuration can be customized through environment variables or a local configuration file such as:

```
mcp/config.py
```

(This file is excluded from version control so every user can configure it independently.)

## **3. Run the server**

```bash
uvicorn main:app --reload
```

## **4. Run the test suite**

```bash
pytest -q
```

---

## **Production-Ready Extensions**

This scaffold is intentionally flexible. To convert it into a production-grade system, you may add:

### 🔹 Redis caching

Replace the in-memory cache with `aioredis` for distributed caching.

### 🔹 Real exchange WebSocket clients

Use CCXT Pro or native exchange SDKs for live tick data.

### 🔹 Rate-limiting & observability

Add request throttling and Prometheus metrics for monitoring.

### 🔹 CI/CD pipelines

Use GitHub Actions for automated linting, testing, and deployment.



