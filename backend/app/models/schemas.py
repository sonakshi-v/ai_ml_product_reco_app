from pydantic import BaseModel
from typing import List, Optional, Dict, Any
class ChatRequest(BaseModel): message: str; top_k: int = 5
class Product(BaseModel):
    uniq_id: str; title: str
    brand: Optional[str] = None; description: Optional[str] = None
    price: Optional[float] = None; categories: Optional[List[str]] = None
    image: Optional[str] = None; score: Optional[float] = None
    extra: Optional[Dict[str, Any]] = None
class ChatResponse(BaseModel): query: str; recommendations: List[Product]