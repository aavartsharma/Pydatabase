from client import PyDatabaseClient
from client import query
from client import BaseModel

db = PyDatabaseClient()

class person2(BaseModel):
    id: int = BaseModel.params(primary_key = True)
    name: str
    password: int
if (__name__ == "__main__"):
    print(db.delete(query.delete(person2).where(person2.name == 'aavart')))
