from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class Health(BaseModel):
    status: str
    version: Optional[str] = None

class TickerData(BaseModel):
    symbol: str
    bid: float
    ask: float
    last: float
    volume: Optional[float] = None
    source: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None
