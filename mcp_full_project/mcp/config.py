
import os

# CCXT 
CCXT_API_KEY = os.getenv("CCXT_API_KEY", None)
CCXT_API_SECRET = os.getenv("CCXT_API_SECRET", None)

# CoinMarketCap PRO API key
CMC_API_KEY = os.getenv("CMC_API_KEY", None)

# Toggle 
FORCE_SIMULATED = os.getenv("FORCE_SIMULATED", "false").lower() in ("1","true","yes")
