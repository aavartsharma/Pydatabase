from client import PyDatabaseClient, query, BaseModel
from delete import person2 

db = PyDatabaseClient()

print(db.delete_all(query.delete(person2)))
