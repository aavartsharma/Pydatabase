import logger
import sqlite3  # for database
import keyword
from config import Config    # config.py
from syslinkPy import Enum    # this is not any official libary in python
from datetime import datetime  
from pydantic import BaseModel # for datetime
from security import SecurityManager   # security.py
from sqlmodel import Field as field, Session, SQLModel, create_engine, select
from sqlalchemy.schema import CreateTable
from sqlalchemy import inspect, Select,text
from typing import Any, Dict, List, Optional, Union, TypeVar   # for type annotation

logging = logger.Utility(name=__file__,version=Config.version,detail="idnotknow").logger #(__name__,Config.version,"Idon'tknow",Config.project_name)
# print(__file__)
T = TypeVar("T")
class status(Enum):
    success:str
    failed:str


class Hero(SQLModel, table=True):
    id: int | None = field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
    
class StaticMethodMeta(type):
    def __new__(cls, name, bases, dct) -> type:
        new_dct = {}
        for key, value in dct.items():
            if callable(value) and not key.startswith('__'):
                value = staticmethod(value)
            new_dct[key] = value
        return super().__new__(cls,name, bases, new_dct)


class Pydatabase():
    def __init__(self):
        self.security = SecurityManager()
        self.engine = create_engine(f"sqlite:///{Config.DATABASE_MAIN}",echo=True)
        self.inspector = inspect(self.engine)

    def _initialize_database(self):
        Config.init()
        class query_log(SQLModel, table=True):
            Sno: Opitonal[int] = field(primary_key=True)
            Query: str
            Time_Stamp: str
            Client: str
            Status: str

        class client(SQLModel, table=True):
            Id: str = field(primary_key=True)
            Name: str
            Token: str
            Joined: str
            Active: str
            Owned_tables: str
            File_location: str

        class table_owner(SQLModel, table=True):
            Table_Id: str = field(primary_key=True)
            Table_Name: str
            Owner_Id: str
            Owner_Name: str

        class client_log(SQLModel, table=True):
            Id: str = field(primary_key=True)
            Client_Id : str
            Client_Name: str
            Logged_In_At: str
            Logged_Out_At: str

        # query_log
        # client
        # table_owner
        # client_log

        SQLModel.metadata.create_all(self.engine)
        
        return None
    
    def _log_query(self, query: str, user: str, status: str = status.success) -> None:
        """Log SQL query execution"""
        try:
            # print(_insert_query)
            self._insert_query("aavart",table_name="query_log",Query=query,Timestamp=datetime.now().isoformat(" "),Client=user,Status = status)

        except Exception as e:
           logging.error(f"Failed to log query: {e}")
           raise e

    def fetch(self, table_name: str, statement: Select , ) -> List[Dict[str,any]]:
        with Session(engine) as session:
            persons = session.exec(statement).all()
            return persons

    def table_schema(self, table_name: str):
        return self.inspector.get_columns(table_name)

    def insert(self, cliebt_name: str, rows: List[T]) -> status:
        with Session(self.engine) as session:
            for i in rows:
                session.add(i)
            session.commit()
            pass

    def create_table(self, table_class):  # maek a system later
        with Session(self.engine) as session:
            pass

    def delete(self, ):
        with Session(self.engine) as session:
            statement = delete().where(Person.age < 20)
            session.exec(statement)
            session.commit()
        pass

    def alter_table(self):
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE user ADD COLUMN email VARCHAR"))
            conn.commit()

    def delete_all(self):
        pass

    def drop_table(self):
        pass

    def drop_table_all(self):
        pass

    def verify_token(self):
        pass
    pass

# -------------------- TEST AREA -------------------- #                               
if (__name__ == "__main__"):  # for test componett of this file
    db= Pydatabase()

    class test(SQLModel, table=True):
        id: Optional[int] = field(primary_key=True)
        name: str

    SQLModel.metadata.create_all(db.engine)
    rows = [test(id=1,name="aavar"), test(id=2,name="asf")]
    db.insert("sfsfsf", rows)
    # db.insert("agsag", )
    pass


