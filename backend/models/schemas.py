from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    question: str
    
class QueryResponse(BaseModel):
    sql_query: str
    response: str
    total_cost: float
    total_tokens: int
    cached: bool = False

class HealthResponse(BaseModel):
    status: str
    database_connected: bool
    
class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None