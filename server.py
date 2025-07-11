"""provide a fast a api to my syslink modules to queay data in pydatabase"""
import sqlite3
import logger
from config import Config
from database import PyDatabase
from security import SecurityManager
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Depends, Request, Body
# ... (previous imports and setup) ...

logging = logger.Utility(name=__file__,version=Config.version,detail="idnotknow").logger

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

# @app.post("/login") 

@app.post("/table/create/{client_token}")
async def create_table(client_token:str ,request: CreateTableRequest, current_user: Dict[str, Any] = Depends(SecurityManager.verify_token)):
    """Create a new table"""
    try:
        # db.
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

@app.post("/table/insert/{client_token}")
async def insert_data(client_token: str,request: CreateTableRequest):
    """sdfasfsflsfjslfjslfjlfjalfjlfjaslfjaslfjafljafl"""
    try:
        result= db.insert()
    except Exception as e:
        raise HTTPException(status_code=333,detail=str(e))

@app.post("/table/update/{client_token}")
async def update(client_token:str):
    """asdfdsfsdfsd"""
    pass

@app.get("/table/schema/{client_token}")
async def get_table_schema(client_token: str,_: Dict[str, Any] = Depends(SecurityManager.verify_token)):
    """Get schema information for a table"""
    try:
        return {"schema": db.get_table_schema(table_name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/programs/{name}")
async def client_login(name: str,token: str):
    # if name and token matched in database table
    db.execute_query("select * from users")
    pass

@app.get("/signup")
async def client_signup(user: str, password):
    pass 

@app.get("/test")
async def test():
    return {'status':"pass"}

