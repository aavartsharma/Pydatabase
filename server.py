import sqlite3
from fastapi import FastAPI, HTTPException, Depends, Request, Body
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from security import SecurityManager
from database import PyDatabase
# ... (previous imports and setup) ...

app = FastAPI()
db = PyDatabase()

class SQLQueryRequest(BaseModel):
    query: str
    params: Optional[List[Any]] = None

class CreateTableRequest(BaseModel):
    table_name: str
    columns: Dict[str, str]

@app.post("/query")
async def execute_query(request: SQLQueryRequest,current_user: Dict[str, Any] = Depends(SecurityManager.verify_token)):
    """Execute a SQL query"""
    try:
        result = db.execute_query(
            request.query,
            tuple(request.params) if request.params else None,
            user=current_user.get("sub", "anonymous")
        )
        return result
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"SQL error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/table")
async def create_table(request: CreateTableRequest, current_user: Dict[str, Any] = Depends(SecurityManager.verify_token)):
    """Create a new table"""
    try:
        result = db.create_table(
            request.table_name,
            request.columns,
            user=current_user.get("sub", "anonymous")
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"/table/{table_name}/schema")
async def get_table_schema(table_name: str,_: Dict[str, Any] = Depends(SecurityManager.verify_token)):
    """Get schema information for a table"""
    try:
        return {"schema": db.get_table_schema(table_name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))