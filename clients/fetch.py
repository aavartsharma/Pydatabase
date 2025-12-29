from client import query 
from client import PyDatabaseClient 
from client import BaseModel

db = PyDatabaseClient()
class person(BaseModel):
    id: int = BaseModel.params(primary_key = True)
    name: str
    cake: str
print(db.fetch(query.select(person).where(person.cake == 'sdf')))
