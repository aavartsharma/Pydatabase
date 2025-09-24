import logger
import pickle
import base64
import keyword
import sqlite3 
from models import init, clinet_object_hashmap
from config import Config    # config.py
from syslinkPy import Enum    # this is not any official libary in python
from datetime import datetime  
from pydantic import BaseModel, create_model
from security import SecurityManager   # security.py
from sqlalchemy.schema import CreateTable
from sqlalchemy import inspect, Select,text
from typing import Any, Dict, List, Optional, Union, TypeVar   # for type annotation
from sqlmodel import Field as field, Session, SQLModel, create_engine, select, update

logging = logger.Utility(name=__file__,version=Config.version,detail="idnotknow").logger #(__name__,Config.version,"Idon'tknow",Config.project_name)
# print(__file__)
T = TypeVar("T")
class status(Enum):
    success:str
    failed:str


# class Hero(SQLModel, table=True):
#     id: int | None = field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: int | None = None
    
class StaticMethodMeta(type):
    def __new__(cls, name, bases, dct) -> type:
        new_dct = {}
        for key, value in dct.items():
            if callable(value) and not key.startswith('__'):
                value = staticmethod(value)
            new_dct[key] = value
        return super().__new__(cls,name, bases, new_dct)


class PyDatabase():
    def __init__(self):
        self.security = SecurityManager()
        self.engine = create_engine(f"sqlite:///{Config.DATABASE_MAIN}",echo=True)
        self.inspector = inspect(self.engine)
        self._initialize_database()

    def _initialize_database(self):
        Config.init()
        init.init(self.engine)
        # class query_log(SQLModel, table=True):
        #     Sno: Opitonal[int] = field(primary_key=True)
        #     Query: str
        #     Time_Stamp: str
        #     Client: str
        #     Status: str

        # class client(SQLModel, table=True):
        #     Id: str = field(primary_key=True)
        #     Name: str
        #     Token: str
        #     Joined: str
        #     Active: str
        #     Owned_tables: str
        #     File_location: str

        # class table_owner(SQLModel, table=True):
        #     Table_Id: str = field(primary_key=True)
        #     Table_Name: str
        #     Owner_Id: str
        #     Owner_Name: str

        # class client_log(SQLModel, table=True):
        #     Id: str = field(primary_key=True)
        #     Client_Id : str
        #     Client_Name: str
        #     Logged_In_At: str
        #     Logged_Out_At: str

        # class clinet_object_hashmap(SQLModel,table=True):
        #     Sno: Optional[int] = field(default=None, primary_key=True)
        #     Client_Id: str
        #     class_name: str
            

        # query_log
        # client
        # table_owner
        # client_log

        # SQLModel.metadata.create_all(self.engine)
        
        return None
    
    def _log_query(self, query: str, user: str, status: str = status.success) -> None:
        """Log SQL query execution"""
        try:
            # print(_insert_query)
            self._insert_query("aavart",table_name="query_log",Query=query,Timestamp=datetime.now().isoformat(" "),Client=user,Status = status)

        except Exception as e:
           logging.error(f"Failed to log query: {e}")
           raise e

    def fetch(self, table_name: str, statement: Select) -> List[Dict[str,any]]:
        with Session(engine) as session:
            persons = session.exec(statement).all()
            return persons

    def table_schema(self, table_name: str):
        return self.inspector.get_columns(table_name)

    def create_class(self,table_name: str,*args: list[Dict]):
        self.fetch(table_name,Select(clinet_object_hashmap).where(name==table_name))
        
        pass

    def insert(self, client_name: str, rows: type) -> status:
        with Session(self.engine) as session:
            logging.info(f"insert function is called - {rows}")
            session.add(rows)
            session.commit()
        return status.success
    
    def update(self,table_name, condition, updates):
        statment = update(table_class).where(condition).values(**updates)
        session.exec(statement)
        session.commit()

    def create_table(self,clinet_name,table_name, class_data):  # maek a system later
        # test1 = create_model(
        #     "test1",
        #     __base__=SQLModel,
        #     __tablename__='test1',
        #     __cls_kwargs__={"table": True},
        #     id=(Optional[int], field(default=None, primary_key=True)),
        #     name=(str, field()),
        #     dmg=(int, field())
        # )
        # classname:type
        class_dict: dict = {
            i: (  pickle.loads(  base64.b64decode(class_data[i][0].encode("utf-8"))  ),field(**class_data[i][1])  )
            for i in class_data
        }

        logging.info(f"the value data at create_table: {class_data}")
        logging.info(f"the last class_dict value : {class_dict}")
        
        classname = create_model(
            table_name,
            __base__=SQLModel,
            __tablename__=table_name,
            __cls_kwargs__={"table":True},
            **class_dict
        )
        classname.__table__.create(self.engine)
        # SQLModel.metadata.create_all(self.engine)
        del classname
        

    def delete(self, table_class, condition):
        with Session(self.engine) as session:
            statement = delete(table_class).where(condition)
            session.exec(statement)
            session.commit()
        pass

    def alter_table(self):
        with self.engine.connect() as conn:
            conn.execute(text("ALTER TABLE user ADD COLUMN email VARCHAR"))
            conn.commit()

    def delete_all(self):
        with Session(self.engine) as session:
            statement = delete(table_class)
            session.exec(statement)
            session.commit()

    def drop_table(self,table_class: T):
        table_class.__table__.drop(self.engine)

    def drop_table_all(self):
        SQLModel.metadata.drop_all(self.engine)

    def verify_token(self):
        pass

# -------------------- TEST AREA -------------------- #                               
if (__name__ == "__main__"):  # for test componett of this file
    db= PyDatabase()

    class test(SQLModel, table=True):
        id: Optional[int] = field(primary_key=True)
        name: str

    # SQLModel.metadata.create_all(db.engine)
    # rows = [test(id=1,name="aavar"), test(id=2,name="asf")]
    # db.insert("sfsfsf", rows)
    # db.insert("agsag", )
    # db.create_table("gun", 
    #     id=(Optional[int],field(default=None,primary_key=True)),
    #     name=(str,field()),
    #     classs=(str,field())
    # )
    # print(db.insert("notgiven", test(name="ada lovelace")))
    
    pass


