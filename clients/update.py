from client import query
from client import PyDatabaseClient
from client import BaseModel
import random

db  = PyDatabaseClient()

class person2(BaseModel):
    id: int = BaseModel.params(primary_key = True) 
    name:str 
    password: int

# print(db.insert(person2(name='aavart', password = 33)))
print(db.update(query.update(person2).where(person2.id == 1).values(password=43)))



