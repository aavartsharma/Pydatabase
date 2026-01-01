from client import PyDatabaseClient
from client import BaseModel
from client import query

db = PyDatabaseClient()

class person(BaseModel):
    id: int = BaseModel.params(primary_key = True)
    name: str 
    cake: str

print(db.insert(person(name='shinomiya',cake='new')))
breakpoint()
