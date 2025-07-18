from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import QueryRequest, QueryResponse, HealthResponse, ErrorResponse
from ..services.sql_assistant import SQLAssistantService
from ..core.database import db_manager

router = APIRouter()

def get_sql_assistant():
    return SQLAssistantService()

@router.post("/query", response_model=QueryResponse)
async def query_database(
    request: QueryRequest,
    assistant: SQLAssistantService = Depends(get_sql_assistant)
):
    try:
        sql_query, response, cost, tokens, cached = assistant.ask_question(request.question)
        
        return QueryResponse(
            sql_query=sql_query,
            response=response,
            total_cost=cost,
            total_tokens=tokens,
            cached=cached
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    db_connected = db_manager.test_connection()
    return HealthResponse(
        status="healthy" if db_connected else "unhealthy",
        database_connected=db_connected
    )