"""provide a fast a api to my syslink modules to queay data in pydatabase"""
import logger
import sqlite3
import traceback
from config import Config
from security import SecurityManager
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from database import Column, PyDatabase, SQLExpr, Field
from fastapi import FastAPI, HTTPException, Depends, Request, Body
# ... (previous imports and setup) ...

logging = logger.Utility(name=__file__,version=Config.version,detail="idnotknow").logger

app = FastAPI()
db = PyDatabase()

class SQLQueryRequest(BaseModel):
    query: str
    params: Optional[List[Any]] = None

class SQLQuery(BaseModel):
    table_name: str
    conditions: Optional[str] = None

class CreateTableRequest(BaseModel):
    table_name: str
    columns: List[Dict[str,str]]

class fetchRequest(BaseModel):
    table_name: str


# @app.post("/query")
# async def execute_query(request: SQLQueryRequest,current_user: Dict[str, Any] = Depends(SecurityManager.verify_token)):
#     """Execute a SQL query"""
#     try:
#         result = db.execute_query(
#             request.query,
#             tuple(request.params) if request.params else None,
#             user=current_user.get("sub", "anonymous")
#         )
#         return result
#     except sqlite3.Error as e:
#         raise HTTPException(status_code=400, detail=f"SQL error: {str(e)}")
#     except ValueError as e:
#         raise HTTPException(status_code=403, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/login") 

@app.post("/table/fetch/{client_token}")
async def fetch(client_token: str, query: SQLQuery):
    """fetch data from database"""
    try:
        logging.info(query)
        result =  db.fetch(
            client_token,
            query.table_name,
            SQLExpr(query.conditions) if query.conditions else None
        )
        logging.info(f"result of the query is {result}")
        return result
    except Exception as e:
        logging.error(f"Eror while fetching: {e}")
        raise e

@app.post("/table/create/{client_token}")
async def create_table(client_token:str ,request: CreateTableRequest):  #   current_user: Dict[str, Any] = Depends(SecurityManager.verify_token)
    """Create a new table"""
    try:
        # db.
        logging.info(request.columns)
        logging.info(f"client_token is {client_token}")
        columns = [Column(**i) for i in request.columns]
        print(columns[0].__dict__)
        result = db.create_table(
            "testuser",
            request.table_name,
            *columns
        )
        logging.info(f"result of create_table is {result}")
        return result
    except ValueError as e:
        logging.error(f"Error : {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error : {str(e)}")
        raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/table/insert/{client_token}")
async def insert_data(client_token: str,request: CreateTableRequest):
    """sdfasfsflsfjslfjslfjlfjalfjlfjaslfjaslfjafljafl"""
    try:
        result= db.insert(client_token, request.table_name, **request.columns[0])
        return result
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
        return {"schema": db.table_schema(user_name,table_name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/table/delete/{client_token}")
async def delete(client_token: str, table_name: str, condition):
    """delete table row in database"""
    try: 
        return db.delete(user_name,table_name,condition)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/table/drop/{client_token}")
async def drop(client_token: str, table_name: str | None = None):
    """drop itn eh table"""
    try: 
        return db.drop_table(table_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/table/options")
async def options():
    """sfdsfsf"""
    return {"options": "under dev "}

@app.get("/test")
async def test():
    return {'status':"pass"}

