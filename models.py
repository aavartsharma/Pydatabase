from sqlmodel import SQLModel, Field
from typing import Optional

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
