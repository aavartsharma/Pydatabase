from sqlmodel import SQLModel, Field
from typing import Optional
import sys
import inspect 

class User(SQLModel,table=True):
    id: int = Field(primary_key=True)
    name: str
    age: int

class query_log(SQLModel,table=True):
    Sno: Optional[int] = Field(default=None,primary_key=True)
    Query: str
    Timestamp: str
    Client: str
    Status: str
    

class client(SQLModel,table=True):
    Id: str = Field(primary_key=True)
    Name: str
    Token: str
    Joined: str
    Active: str
    Owned_Tables: str
    File_Location: str

class table_owner(SQLModel,table=True):
    Table_Id: str = Field(primary_key=True)
    Table_Name: str
    Owner_Id: str
    Owner_name: str

class client_log(SQLModel,table=True):
    Id: str = Field(primary_key=True)
    Client_Id: str
    Client_Name: str
    Logged_In_At: str
    Logged_In_At: str

class clinet_object_hashmap(SQLModel,table=True):
    Sno: Optional[int] = Field(default=None, primary_key=True)
    Client_Id: str
    class_name: str

class init():
    # print(classes)
    
    @classmethod
    def init(clse,engine):
        current_module = sys.modules[__name__]
        # classes = inspect.getmembers(current_module, inspect.isclass)
        classes = [
            cls.__table__ for name, cls in inspect.getmembers(current_module, inspect.isclass)
            if cls.__module__ == __name__ and not (cls is init)  # belongs to this module
        ]
        
        # print(classes)
        SQLModel.metadata.create_all(engine,tables=classes)
