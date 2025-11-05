import logger
import pickle
import base64
import keyword
import sqlite3 
import traceback
import sqlmodel
from config import Config    # config.py
from syslinkPy import Enum    # this is not any official libary in python
from datetime import datetime  
from security import SecurityManager   # security.py
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql import operators
from pydantic import BaseModel, create_model
from models import init, clinet_object_hashmap #=> models.py
from sqlalchemy import inspect, Select,text,Table, MetaData
from sqlalchemy.exc import InvalidRequestError
from typing import Any, Dict, List, Optional, Union, TypeVar   # for type annotation
from sqlmodel import Field as field, Session, SQLModel, create_engine, select, update

#(__name__,Config.version,"Idon'tknow",Config.project_name)
logging = logger.Utility(name=__file__,version=Config.version,detail="idnotknow").logger

class status(Enum):
    success:str
    failed:str


# class Hero(SQLModel, table=True):
#     id: int | None = field(default=None, primary_key=True)
#     name: str
    
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
        self.tables = lambda: {
                cls.__tablename__: cls
                for cls in SQLModel.__subclasses__()
                if hasattr(cls, "__tablename__")
            }

    def _initialize_database(self):
        Config.init()
        init.init(self.engine)
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


    def table_schema(self, table_name: str):
        return self.inspector.get_columns(table_name)

    # def create_class(self,table_name: str):
    #     # sturecture = self.fetch(table_name,Select(clinet_object_hashmap).where(name==table_name))
    #     print(SQLModel.metadata.tables)
    #     print(SQLModel.metadata)
    #     class_table = SQLModel.metadata.tables[table_name]
    #     print(class_table)
    #     print(type(class_table))
    #     return class_table

    def create_class(self,table_name: str, class_data: dict):
        # logging.info(f"creae")
        logging.info(f"the value data at create_table: {class_data}")
        class_dict: dict = {
            i: (  
                pickle.loads(base64.b64decode(class_data[i][0].encode("utf-8"))),
                field(**class_data[i][1])
            )
            for i in class_data
        }

        logging.info(f"the last class_dict value : {class_dict}")
        try:
            # Before each test
            # SQLModel.metadata.clear()
            breakpoint()
            classname: type = create_model(
                table_name,
                __base__=SQLModel,
                __tablename__=table_name,
                __cls_kwargs__={"table":True},
                **class_dict
            )
            SQLModel.metadata.create_all(self.engine,tables=[classname.__table__])
            return classname
        except InvalidRequestError as e:
            logging.error(f"{table_name} table is already created!!!")
            return None
            pass
        except Exception as e:
            # logging.error(f"create_model has problem {")
            traceback.print_exc()
            raise e

    def insert(self, client_name: str,table_name:str, class_dict: dict, class_args: dict) -> status:
        with Session(self.engine) as session:
            logging.info(f"insert function is called - {class_args}")
            # class_init = self.create_class(table_name,class_args)
            # session.add(class_init(**class_dict))
            breakpoint()
            models = tables()
            session.add(models[table_name](**class_dict))
            # SQLModel.__subclasses__()[table_name]()
            session.commit()
        return status.success

    # class fetchData(SQLModel,)
    def fetch(self, client_token:str, statement: dict, class_list: list[str]) -> List[Dict[str,any]]:
        with Session(self.engine) as session:
            logging.info(f"statement - {statement}")
            #select(models.)
            # Build fields dynamically from columns
            # fields: dict = {}
            # for col in user_table.columns:
            #     if col.primary_key:
            #         fields[col.name] = (Optional[int], None)
            #     else:
            #         fields[col.name] = (col.type.python_type, ...)  # required field

            # # Dynamically create SQLModel subclass
            # DynamicUser = type("User", (SQLModel,), {"__annotations__": {k: v[0] for k, v in fields.items()},
            #                             **{k: Field(default=v[1]) for k, v in fields.items()},
            #                             "__table__": user_table})
            breakpoint()
            classes = {i:create_class(i,class_list[i]) for i in class_list}
            n = [(n:=sqlmodel.__dict__[i])(*statement[i]) if not n else n.__dict__(i)(statement[i]) for i in statement]
            result = session.exec(k).all() 
            logging.info(f"session.exec - {k}")
            logging.info(f"session.exec.all() - {result}")
            return result 
    
    def update(self,table_name, condition, updates):
        statment = update(table_class).where(condition).values(**updates)
        session.exec(statement)
        session.commit()

    def create_table(self ,clinet_name:str ,table_name:str ,class_data:dict):  # maek a system later
        classname = self.create_class(table_name,class_data)
        SQLModel.metadata.create_all(self.engine,tables=[classname.__table__])
        # del classname

    def delete(self, table_class, condition):
        with Session(self.engine) as session:
            statement = delete(table_class).where(condition)
            session.exec(statement)
            session.commit()

    def alter_table(self):
        with self.engine.connect() as conn:
            conn.execute(text("ALTER TABLE user ADD COLUMN email VARCHAR"))
            conn.commit()

    def delete_all(self):
        with Session(self.engine) as session:
            statement = delete(table_class)
            session.exec(statement)
            session.commit()

    def drop_table(self,table_class):
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
    
    print(f"output: ", type(test.name))

    #================ querys =================#
        # select(test)
        # select(test).where(User.name == "name")
        # select(test.name, test.id)
        # select(test).order_by(user.aga.desc())
        # select(test).limit(5)
        # select(test).offset(5)
        # 

    # SQLModel.metadata.create_all(db.engine)
    with Session(db.engine) as session:
        rows = [test(id=1,name="aavar"), test(id=2,name="asf")]
        # [session.add(i) for i in rows]
        # session.add_all(rows)
        # session.commit()
        # session.refresh()
        statement = select(test).where(test.name == 'sdf')
        breakpoint()
        print(f"select is {statement.__dict__} ans where is {statement.where(test.name).__dict__}")
        print(f"select is type - {type(statement)} and where type - {type(statement.where(test.name=='ava'))}")

    # db.insert("sfsfsf", rows)
    # db.insert("agsag", )
    # db.create_table("gun", 
    #     id=(Optional[int],field(default=None,primary_key=True)),
    #     name=(str,field()),
    #     classs=(str,field())
    # )
    # print(db.insert("notgiven", test(name="ada lovelace")))
    
    pass


