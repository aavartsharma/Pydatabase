import urllib3
import requests
# import pandas as pd
#import dill
import pickle
import base64
import inspect
from syslinkPy import Enum
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from pydantic import Field, BaseModel
import json
import traceback
# make a class with ispect

# Disable SSL verification warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class method(Enum):
    get: str = "GET"
    put: str = "PUT"
    post: str = "POST"

class column():
    def __init__(self,table_name,colum,feild):
        self.tal = (table_name,colum)
        self.feild = feild 
    #=> use @func to automate the (self.tal,self.__add__.__name__,other)
    def __and__(self, other):
        return (self.tal,self.__add__.__name__,other) 
    def __or__(self, other):
        return (self.tal,self.__add__.__name__,other)     
    def __invert__(self):
        return (self.tal,self.__invert__.__name__,)
    def __gt__(self,other):
        return (self.tal,self.__gt__.__name__,other) 
    def __lt__(self,other):
        return (self.tal, self.__lt__.__name__,other)
    def __eq__(self,other):
        return (self.tal, self.__eq__.__name__,other) 

class BaseModel_Meta(type):
    def __new__(cls,name: str, base: tuple[type], namespace: dict[str, any],**kwargs):
        # super().__setattr__("__config__", kwargs)
        print(f"name of the cls is {cls.__name__}")
        print(f"name of the name is {name}")
        print(f"bases is {base}")
        print(f"namespace is {namespace}")
        print(f"__new__ is called and here is kwargs value: {kwargs}")
        for i in namespace.get('__annotations__',{}):
            namespace[i] = column(namespace['__qualname__'],i,namespace[i] if i in namespace else {})
        # print(namespace)
        return super().__new__(cls,name,base,namespace)

    def __init__(cls,name: str, base: tuple,namespace: dict,**kwargs):
        print("__init__ class was called and kwargs is ", kwargs)
        # cls.parmas = params
        # cls.propery = kwargs
        # print(cls.__name__)
        super().__init__(name,base,namespace)
    
    def __call__(cls,**kwargs):
        print(cls.__name__)
        # super().__setattr__("__notation__", kwargs)
        # for i in kwargs:
            # super().__setattr__(i, kwargs[i])
        obj = super().__call__()
        obj.__dict__ = kwargs
        print(obj)
        return obj

class BaseModel(metaclass=BaseModel_Meta):
    @staticmethod
    def params(**kwargs):
        return kwargs
    
class query():
    def __init__(self,**kwargs: dict[column]):
        print(f"this the query dict: {kwargs}")
        self.kwargs = kwargs

    @staticmethod
    def select(*args):  #=> return a instance of query
        return query(select = [i.tal for i in args])

    def where(self, statement: column):
        # self.kwargs.where = 
        self.kwargs['where'] = statement
        return self

class PyDatabaseClient:
    def __init__(self):
        self.base_url = f"http://0.0.0.0:{5000}" # should be accquied from envirment variable
        self.token: Optional[str] = "notgiven"   # will be provide by sysllinkl
        self.make_dict = lambda class_data: {
            i:(
                base64.b64encode(pickle.dumps(class_data['__annotations__'][i])).decode("utf-8"),
                class_data[i] if class_data.get(i)  else {}
            ) 
            for i in class_data["__annotations__"]
        }
    
    @classmethod
    def define_obj():
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
        print(json)
        response = requests.request(
            method,
            f"{self.base_url}/{endpoint}",
            json=json,
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    
    def create_table(self, table_: type):
        """clint_name: str
    table_name: str
    query: Optional[str] = None
    params: Optional[List[Any]] = None"""
        try:
            # listc = [json.dumps({j:pickle.dumps(book.__dict__[j]) if isinstance(book.__dict__[j],type) else j: book.__dict__[j] for j in book.__dict__ if isinstance(i.__dict__[j],dict)}) for i in columns]
            # print(listc)
            # payload = {
            #     "name": "test_dummy2",
            #     "table_name": table_name,
            #     "query": None,
            #     "columns": listc
            # }
            # print(payload)
            # cls1 = base64.b64encode(dill.dumps(columns[0])).decode("utf-8")
            # print(cls1)
            class_data = table_.__dict__
            print(f"class data is {class_data}")
            #  create a funtion that will return a dict for the all of
            # class_dict = {i:(base64.b64encode(pickle.dumps(class_data['__annotations__'][i])).decode("utf-8"),class_data[i] if class_data.get(i)  else {}) for i in class_data["__annotations__"]}
            class_dict = self.make_dict(class_data) # make_dict is defined in __init__
            print(f"dict send response: {class_dict}")
            # print([i for i in class_dict["id"][1]])

            response = self._make_request(
                method.post,
                f"table/create/{self.token}",
                json={
                    "table_name": table_.__name__,
                    "pickled":class_dict
                }
            )
            return response
        except Exception as e:
            print(e)
            print("Error details: ")
            traceback.print_exc()
            # raise e
            return str(e)
            # print(str(e.http_error_msg))
    
    def insert(self,data: type) -> str:
        """Insert a document into a collection"""
        if (not isinstance(data, BaseModel)):
            raise ValueError("bazinga")

        class_dicta = type(data).__dict__
        print(f"class_dicta value is {class_dicta}")
        class_dict: dict = self.make_dict(class_data=class_dicta)
        print(f"class dict value is {class_dict}")
        payload={
            "table_name": data.__class__.__name__,
            "pickled": data.__dict__,
            "columns": class_dict
        }
        print(f"the payload value is {payload}")

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

    def fetch(self,statement: query):
        try:
            response = self._make_request(
                method.post,
                f"table/fetch/{self.token}",
                json=statement.__dict__
            )
            return response
        except Exception as e:
            print(type(statement))
            print(e)
            return e
    
    def delete(self,table_name: str, columns: str = None) -> int:
        """Delete documents from a collection"""
        payload = {
            "table_name": table_name,
            "conditions": columns
        }
        print("colums: ", columns)
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

    # print('hello world')
    client = PyDatabaseClient()
    def f(**k):
        return k
    class book():
        id: Optional[int] = f(default=None,primary_key=True)
        name: str
        version: str

    print({i:book.__dict__[i] for i in book.__dict__ if isinstance(book.__dict__[i],dict)})

    # print(client.delete("client_testtable"))
    # print(Column.__dict__)
    # print(PyDatabaseClient.__dict__)
    # print(client.create_table("client_testtable",Column("name", "TEXT","False")))
    # print(client.test())
    # a = Column("sno","INTEGER" , True, True)
    # print(a.__dict__)
    # print(client.insert("client_testtable",name="harry"))
    # id = Field("id")
    # classes = Field("class")
    # name = Field("name")
    # query = (name == "aavart")

    # # sta2 = kQLExpr("id=7")
    # # onj = QLExpr("name=aavart")
    # print(client.fetch("client_testtable"))

