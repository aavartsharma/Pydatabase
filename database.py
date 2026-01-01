import logger
import pickle
import base64
import traceback
import sqlmodel

from config import Config                        #=> config.py
from syslinkPy import Enum                       #=> this is not any official libary in python
from security import SecurityManager             #=> security.py
from models import init, clinet_object_hashmap   #=> models.py

from datetime import datetime  
from pydantic import BaseModel, create_model

from sqlalchemy import inspect, select,text,Table, MetaData
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.schema import CreateTable

from sqlmodel import (
    Field as field, 
    Session, 
    SQLModel, 
    create_engine, 
    select as Select, 
    insert,
    update
)

from collections.abc import Iterable
from typing import (    #=> for type annotation
    Any, 
    Dict, 
    List, 
    Optional, 
    Union, 
    TypeVar
)


#(__name__,Config.version,"Idon'tknow",Config.project_name)
logging = logger.Utility(name=__file__,version=Config.version,detail="idnotknow").logger

class status(Enum):
    success:str
    failed:str
   
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
        self.metadata = SQLModel.metadata
        self.tables = lambda: {
            cls.__tablename__: cls
            for cls in SQLModel.__subclasses__()
            if hasattr(cls, "__tablename__")
        }

    def _initialize_database(self):
        Config.init()
        init.init(self.engine)
        #+> SQLModel.metadata.create_all(self.engine)
    
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
            return self.tables()[table_name] 
            pass
        except Exception as e:
            # logging.error(f"create_model has problem {")
            traceback.print_exc()
            raise e

    def insert(self, client_name: str,statement: dict) -> str:
        with Session(self.engine) as session:
            logging.info(f"statement - {statement}")
            query_created = self.query.create_q(statement,self.metadata,self.engine)
            breakpoint()
            result = session.exec(query_created) 
            logging.info(f"session.exec - {query_created}")
            logging.info(f"session.exec.all() - {result}")

            #session.add(class_init(**class_dict))
            #session.commit()
            #logging.info(f"insert function is called - {class_args}")
            # class_init = self.create_class(table_name,class_args)
            # session.add(class_init(**class_dict))
            #breakpoint()
            # why the hell this code is doing here
            #models = self.tables()
            #session.add(models[table_name](**class_dict))
            # SQLModel.__subclasses__()[table_name]()
            #session.commit()
        return status.success

    # class fetchData(SQLModel,)
    def fetch(self, client_token: str, statement: dict) -> List[Dict[str,Any]]:
        with Session(self.engine) as session:
            logging.info(f"statement - {statement}")
            query_created = self.query.create_q(statement,self.metadata,self.engine)
            result = session.exec(query_created).all() 
            logging.info(f"session.exec - {query_created}")
            logging.info(f"session.exec.all() - {result}")
            return result 
    
    def update(self,client_token: str, statement: str) -> List[Dict[str,Any]]:
        with Session(self.engine) as session:
            logging.info(f'statement = {statement}')
            query_created = self.query.create_q(statement,self.metadata,self.engine)
            result = session.exec(query_created).all()
            logging.info(f"session.exec - {query_created}")
            logging.info(f"session.exec.all() - {result}")
            session.commit()
            return result
        statment = update(table_name).where(condition).values(**updates)
        session.exec(statement)

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

    class query():
        """managing query relate operations"""
        @staticmethod
        def create_table_class(class_name: str, metadata, engine):
            """create Table class for a table in database by it's name,metadata and engine"""
            return Table(class_name,metadata, autoload_with= engine)

        @staticmethod
        def create_expr(expr_dict: dict, metadata, engine):
            """convert dict --> SQLModel/sqlalchemy expression """
            core_function = lambda x: PyDatabase.query.create_expr(x, metadata,engine)
            if(all(i in expr_dict for i in ['left', 'operator','right']) if isinstance(expr_dict, Iterable) else False):
                #=> if the dict is sql expression
                breakpoint()
                return getattr(core_function(expr_dict['left']),expr_dict['operator'])(core_function(expr_dict['right']))
            elif (all(i in expr_dict for i in ['table', 'column']) if isinstance(expr_dict,Iterable) else False):
                #=> if the dict is table 
                breakpoint()
                # return getattr(getattr(core_function(expr_dict['table']),'columns'),expr_dict['column'])
                return getattr(getattr(PyDatabase.query.create_table_class(expr_dict['table'],metadata,engine),'columns'),expr_dict['column'])
            else:
                return expr_dict 

        @staticmethod
        def create_q(query_dict: dict, metadata, engine):
            """converts whole query_dict to a SQLModel/sqlalchemy query"""
            sql_query = None 
            for i in query_dict:
                if(sql_query == None):  #=> if it is a global function like select
                    breakpoint()
                    sql_query = globals()[i]  
                else:
                    sql_query = getattr(sql_query,i)   
                match query_dict[i]:
                    #=> query_dict[i] is the arguments of a function 
                    #=> x is temp variable for query_dict[i]
                    case x if isinstance(x, (list, tuple)):  #=> for most case x will be select function
                        table_objects = [] 
                        for j in x:
                            breakpoint()
                            name, col = j
                            if(col):
                                table_objects.append(PyDatabase.query.create_table_class(name,metadata,engine).columns[col]) 
                            else:
                                table_objects.append(PyDatabase.query.create_table_class(name,metadata,engine))
                        sql_query = sql_query(*table_objects)

                    case x if isinstance(x, dict):
                        sql_query = sql_query(PyDatabase.query.create_expr(x, metadata, engine)) 

                    case x if isinstance(x, (int,str)):
                        sql_query = sql_query(x) 
                    case _:
                        logging.error(f"{_} has inappropriate datatype")

            return sql_query 
        

    def create_table(self ,clinet_name:str ,table_name:str ,class_data:dict):  # make a system later
        classname = self.create_class(table_name,class_data)
        logging.info(f"classname.__table__ is {classname.__table__}")
        SQLModel.metadata.create_all(self.engine,tables=[classname.__table__])
        # del classname 

#-_-_-_-_-_-_-_-_-_-_ End Of PyDatabase _-_-_-_-_-_-_-_-_-_#







# --------------------------------------------------- #
# --------------------------------------------------- #
# -------------------- TEST AREA -------------------- #                               
# --------------------------------------------------- #
# --------------------------------------------------- #
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
        # db.fetch('sdfd',stamet)
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


