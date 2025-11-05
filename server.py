"""provide a fast a api to my syslink modules to queay data in pydatabase"""
import logger
import pickle
import base64
import sqlite3
import traceback
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
# T = TypeVar("T")

class SQLQueryRequest(BaseModel):
    clint_name: str
    table_name: str
    columns: type
    query: Optional[str] = None
    params: Optional[List[Any]] = None

# class SQLQueryCreateTable(BaseModel):
#     client_name: str
#     pickled: str

# class SQLQuery(BaseModel):
#     table_name: str
#     conditions: Optional[str] = None

# class CreateTableRequest[T](BaseModel):
#     table_name: str
#     columns: List[Dict[str,str]]

# class fetchRequest(BaseModel):
#     table_name: str 



# @app.post("/login")
# async def login(request: LoginRequest):
#     """Login endpoint with security logging"""
#     try:
#         # Log login attempt
#         api_logger.log_security({
#             "event_type": "LOGIN_ATTEMPT",
#             "details": f"Login attempt for user: {request.username}",
#             "ip_address": request.client.host
#         }, request.username)

#         token = SecurityManager.create_token(request.username)

#         # Log successful login
#         api_logger.log_security({
#             "event_type": "LOGIN_SUCCESS",
#             "details": f"Successful login for user: {request.username}",
#             "ip_address": request.client.host
#         }, request.username)

#         return {"token": token}

#     except Exception as e:
#         # Log login failure
#         api_logger.log_security({
#             "event_type": "LOGIN_FAILURE",
#             "details": f"Failed login for user: {request.username}. Error: {str(e)}",
#             "ip_address": request.client.host
#         }, request.username)

#         raise HTTPException(status_code=401, detail="Authentication failed")

class PickledData(BaseModel):
    table_name: str
    pickled: dict

@app.post("/table/create/{client_token}")
async def create_table(client_token:str ,pickled: PickledData):  #   current_user: Dict[str, Any] = Depends(SecurityManager.verify_token)
    """Create a new table"""
    try:
        # db.
        # logging.info(request.query)
        logging.info(f"client_token is {client_token}")
        logging.info(pickled.pickled)
        
        result = db.create_table(
            client_token,
            pickled.table_name,
            pickled.pickled
        )
        # db.insert(client_token, pickled.table_name)
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

class insertData(BaseModel):
    table_name: str
    pickled: dict
    columns: dict

@app.post("/table/insert/{client_token}")
async def insert_data(client_token: str,request: insertData):
    try:
        logging.info(f"insert_data have got input: {request.pickled}")
        result = db.insert(client_token,request.table_name, request.pickled, request.columns)
        logging.info(f"insert data success: {result}")
        return result
    except Exception as e:
        logging.error(f"Error in insert endpoint - {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=333,detail=str(e))

class fetchData(BaseModel):
    query: dict    #=> query dict that contain strucetur of query
    pickled: dict  #=> dict of class type casted to string 

@app.post("/table/fetch/{client_token}")
async def fetch(client_token: str, query: fetchData):
    """fetch data from database"""
    try:
        logging.info(query)
        result =  db.fetch(
            client_token,
            query.query,
            query.pickled
        )
        logging.info(f"result of the query is {result}")
        return result
    except Exception as e:
        logging.error(f"Eror while fetching: {e}")
        raise e

@app.post("/table/update/{client_token}")
async def update(client_token:str):
    """asdfdsfsdfsd"""
    pass

@app.post("/table/schema/{client_token}")
async def get_table_schema(client_token: str,_: Dict[str, Any] = Depends(SecurityManager.verify_token)):
    """Get schema information for a table"""
    try:
        return {"schema": db.table_schema(user_name,table_name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/table/delete/{client_token}")
async def delete(client_token: str, request: SQLQueryRequest):
    """delete table row in database"""
    try: 
        logging.info(f"Delete endpoint variables: {locals()}")
        return db.delete(client_token,request.table_name,request.conditions)
    except Exception as e:
        logging.error(f"Error occurted delete endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/table/drop/{client_token}")
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
    return {'status':"pass"} #=> test

