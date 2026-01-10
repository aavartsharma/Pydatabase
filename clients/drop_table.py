from client import PyDatabaseClient, query
from delete import person2

db = PyDatabaseClient()
print(db.drop_table("person"))
