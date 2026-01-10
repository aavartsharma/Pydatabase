from client import PyDatabaseClient, query, BaseModel

db = PyDatabaseClient()
print(db.get_schema("person2"))
