from client import PyDatabaseClient
from client import BaseModel

db = PyDatabaseClient()

class person(BaseModel):
    id: int = BaseModel.params(primary_key = True)
    name: str 
    cake: str

db.insert(person(name='aavart',cake='sdf'))
