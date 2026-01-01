import urllib3
import requests
import pickle
import base64
import inspect
import logging
from syslinkPy import Enum
from typing import Any, Dict, List, Optional
from pydantic import Field, BaseModel
from typing import Any
import json
import traceback
# make a class with ispect

# Disable SSL verification warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,  # Minimum level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s"
)

class method(Enum):
    get: str = "GET"
    put: str = "PUT"
    post: str = "POST"


class BaseModel_Meta(type):
    def __new__(cls,name: str, base: tuple[type], namespace: dict[str, Any],**kwargs):
        # super().__setattr__("__config__", kwargs)
        logging.info(f"name of the cls is {cls.__name__}")
        logging.info(f"name of the name is {name}")
        logging.info(f"bases is {base}")
        logging.info(f"namespace is {namespace}")
        logging.info(f"__new__ is called and here is kwargs value: {kwargs}")
        for i in namespace.get('__annotations__',{}):
            namespace[i] = Column(namespace['__qualname__'],i,namespace[i] if i in namespace else {})
        # logging.info(namespace)
        return super().__new__(cls,name,base,namespace)

    def __init__(cls,name: str, base: tuple,namespace: dict,**kwargs):
        logging.info("__init__ class was called and kwargs is ", kwargs)
        # cls.parmas = params
        # cls.propery = kwargs
        # logging.info(cls.__name__)
        super().__init__(name,base,namespace)
    
    def __call__(cls,**kwargs):
        logging.info(cls.__name__)
        # super().__setattr__("__notation__", kwargs)
        # for i in kwargs:
            # super().__setattr__(i, kwargs[i])
        obj = super().__call__()
        obj.__dict__ = kwargs
        logging.info(obj)
        return obj

class BaseModel(metaclass=BaseModel_Meta):
    @staticmethod
    def params(**kwargs) -> Any:
        return kwargs
    
    #=> use @func to automate the (self.tal,self.__add__.__name__,other)

class SQLExpr:
    def __init__(self, left, operator, right=None):
        self.left = left
        self.operator = operator
        self.right = right

    def __and__(self, other):
        return SQLExpr(self, self.__and__.__name__, other)

    def __or__(self, other):
        return SQLExpr(self,  self.__or__.__name__, other)

    def __invert__(self):
        return SQLExpr(self,  self.__invert__.__name__, self)

    def to_dict(self):
        """Convert the SQLExpression into a nested dictionary."""
        def serialize(obj):
            if isinstance(obj, Column):
                return {"table": obj.table_name, "column": obj.column_name}
            elif isinstance(obj, SQLExpr):
                return obj.to_dict()
            else:
                return obj

        return {
            "operator": self.operator,
            "left": serialize(self.left),
            "right": serialize(self.right) if self.right is not None else None
        }

    def __repr__(self):
        return f"SQLExpr({self.left=}, {self.operator=}, {self.right=})"


class Column:
    def __init__(self, table_name, column_name, field= {}):
        self.table_name = table_name
        self.column_name = column_name
        self.field = field

    def __gt__(self, other):
        return SQLExpr(self, self.__gt__.__name__, other)

    def __lt__(self, other):
        return SQLExpr(self,self.__lt__.__name__, other)

    def __eq__(self, other):
        return SQLExpr(self, self.__eq__.__name__, other)

    def __ge__(self, other):
        return SQLExpr(self, self.__ge__.__name__, other)

    def __le__(self, other):
        return SQLExpr(self, self.__le__.__name__, other)

    def __ne__(self, other):
        return SQLExpr(self, self.__le__.__name__, other)

    def __repr__(self):
        return f"Column({self.table_name}.{self.column_name})"
class query():
    #=> you can make a baseclass for query which will automate the process of making query sturces
    #=> baseclass will give every instance of query a attribute which will contain a 
    #=> sturcre of query then function like where can just return a value and ti 
    #=> will be add to the attribute
    #=> you can use decoretors
    def __init__(self,**kwargs: Any):
        logging.info(f"this the query dict: {kwargs}")
        self.kwargs = kwargs
        logging.info("this is kwargs ", kwargs)
        breakpoint()
        # self.classes_list = list({item[0] for item in list(kwargs.values())[0] })
        # logging.info(self.classes)

    @staticmethod
    def select(*args) -> Any:  #=> return a instance of query
        breakpoint()
        # columns_list: list[Column] = [i.tal for i in args]
        return query(select = tuple(
            (i.table_name, i.column_name) if isinstance(i, Column) 
            else (i.__name__, None) 
            for i in args 
        ))
    @staticmethod
    def insert(*args):
        return query(insert=tuple((i.__name__,None) for i in args))

    def where(self, statement: SQLExpr) -> Any:
        # self.kwargs.where = 
        self.kwargs['where'] = statement.to_dict()
        breakpoint()
        return self

    def values(self, **kwargs):
        self.kwargs['values'] = kwargs
        return self
    # def a(self):
    #     d = 
    #     return kwargs

class PyDatabaseClient:
    def __init__(self):
        self.base_url = f"http://0.0.0.0:{5000}" # should be accquied from envirment variable
        self.token: Optional[str] = "notgiven"   # will be provide by sysllinkl
        self.make_dict = lambda class_data: {
            i:(
                base64.b64encode(pickle.dumps(class_data['__annotations__'][i])).decode("utf-8"),
                class_data[i].field if class_data.get(i)  else {}
            ) 
            for i in class_data["__annotations__"]
        }
    
    @classmethod
    def define_obj(cls) -> None:
        pass

    def login(self, token: str) -> bool:
        """Login to the database server"""
        try:
            response = requests.post(
                f"{self.base_url}/login",
                json={"token": token},
                verify=False
            )
            if response.status_code == 200:
                self.token = response.json()["token"]
                return True
            return False
        except requests.RequestException:
            return False
    
    def _make_request(self, method: str, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Make an authenticated request to the server"""
        # if not self.token:
        #     raise ValueError("Not authenticated. Call login() first")
        headers={
            "accept": 'application/json',
            "Content-Type": "application/json"
        }
        logging.info(f'json that is being send : {json}')
        response = requests.request(
            method,
            f"{self.base_url}/{endpoint}",
            json=json,
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    
    def create_table(self, table_: type) -> str:
        """clint_name: str
            table_name: str
            query: Optional[str] = None
            params: Optional[List[Any]] = None"""
        try:
            # listc = [json.dumps({j:pickle.dumps(book.__dict__[j]) if isinstance(book.__dict__[j],type) else j: book.__dict__[j] for j in book.__dict__ if isinstance(i.__dict__[j],dict)}) for i in columns]
            # logging.info(listc)
            # payload = {
            #     "name": "test_dummy2",
            #     "table_name": table_name,
            #     "query": None,
            #     "columns": listc
            # }
            # logging.info(payload)
            # cls1 = base64.b64encode(dill.dumps(columns[0])).decode("utf-8")
            # logging.info(cls1)
            class_data = table_.__dict__
            logging.info(f"class data is {class_data}")
            #  create a funtion that will return a dict for the all of
            # class_dict = {i:(base64.b64encode(pickle.dumps(class_data['__annotations__'][i])).decode("utf-8"),class_data[i] if class_data.get(i)  else {}) for i in class_data["__annotations__"]}
            class_dict: dict[str, Any] = self.make_dict(class_data) # make_dict is defined in __init__
            logging.info(f"dict send response: {class_dict}")
            # logging.info([i for i in class_dict["id"][1]])

            response: str = str(self._make_request(
                method.post,
                f"table/create/{self.token}",
                json={
                    "table_name": table_.__name__,
                    "pickled":class_dict
                }
            ))
            return response
        except Exception as e:
            logging.error(f"Error - {e}", exc_info=True)
            # if(Config.dev):
            #     breakpoint()
            # traceback.logging.info_exc()
            # raise e
            return str(e)
            # logging.info(str(e.http_error_msg))
    
    def insert(self,data: type) -> str:
        """Insert a document into a collection"""
        if (not isinstance(data, BaseModel)):
            raise ValueError("bazinga")
        breakpoint()
        insert_query = query.insert(type(data)).values(**data.__dict__)
        breakpoint()
        # class_dicta = type(data).__dict__
        # logging.info(f"class_dicta value is {class_dicta}")
        # class_dict: dict = self.make_dict(class_data=class_dicta)
        # logging.info(f"class dict value is {class_dict}")
        # payload={
        #     "table_name": data.__class__.__name__,
        #     "pickled": data.__dict__,
        #     "columns": class_dict
        # }

        payload = {
            "query": self.change(insert_query)
        }
        logging.info(f"the payload value is {payload}")
        return self._make_request(
            method.post, 
            f"table/insert/{self.token}",
            json=payload
        )
    
    def update(self, collection: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """Update documents in a collection"""
        response = self._make_request(
            "POST",
            f"{collection}/update",
            {"query": query, "update": update_data}
        )
        return response["updated_count"]

    @staticmethod
    def change(raw_object):
        breakpoint()
        if isinstance(raw_object,dict):
            # for i in raw_object:
            #     raw_object[i] =  change(raw_object[i])
            new_tuple = {i:PyDatabaseClient.change(raw_object[i]) for i in raw_object}
            return new_tuple
        elif isinstance(raw_object,list) or isinstance(raw_object,tuple):
            # new_tuple = 
            # for i in range(len(raw_object)):
            #     raw_object[i]= change(raw_object[i])
            new_tuple = tuple(PyDatabaseClient.change(i) for i in raw_object)
            return new_tuple
        elif hasattr(raw_object,'__dict__'):
            breakpoint()   #=> this line is problem somehow __dict__ of person class is being stuce here
            return PyDatabaseClient.change(raw_object.__dict__)['kwargs']
        else: # is a normal
            return raw_object

    def fetch(self,statement: query):
        try:
            breakpoint()
            payload = {
                "query": self.change(statement)
            }
            response = self._make_request(
                method.post,
                f"table/fetch/{self.token}",
                json=payload
            )
            return response
        except Exception as e:
            logging.error(f"error occured: {e}")
            return e
    
    def delete(self,table_name: str, columns: str = None) -> int:
        """Delete documents from a collection"""
        payload = {
            "table_name": table_name,
            "conditions": columns
        }
        logging.info("colums: ", columns)
        response = self._make_request(
            method.post,
            f"table/delete/{self.token}",
            json=payload
        )
        return response

    def Drop_table(self,table_name:str):
        pass

    def alter_table(self,table_name: str, **data):
        pass

    def get_schema(self, table_name: str):
        payload = {}
        response = self._make_request(
            method.post,
            f"table/schema/{self.token}",
        )
        pass

    def test(self):
        return self._make_request(method.get, "test")

if(__name__ == "__main__"):

    # logging.info('hello world')
    client = PyDatabaseClient()
    def f(**k):
        return k
    class book():
        id: Optional[int] = f(default=None,primary_key=True)
        name: str
        version: str

    logging.info({i:book.__dict__[i] for i in book.__dict__ if isinstance(book.__dict__[i],dict)})

    # logging.info(client.delete("client_testtable"))
    # logging.info(Column.__dict__)
    # logging.info(PyDatabaseClient.__dict__)
    # logging.info(client.create_table("client_testtable",Column("name", "TEXT","False")))
    # logging.info(client.test())
    # a = Column("sno","INTEGER" , True, True)
    # logging.info(a.__dict__)
    # logging.info(client.insert("client_testtable",name="harry"))
    # id = Field("id")
    # classes = Field("class")
    # name = Field("name")
    # query = (name == "aavart")

    # # sta2 = kQLSQLExpr("id=7")
    # # onj = QLSQLExpr("name=aavart")
    # logging.info(client.fetch("client_testtable"))

