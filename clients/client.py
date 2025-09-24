import urllib3
import requests
# import pandas as pd
import dill
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


class BaseModel_Meta(type):
    def __new__(cls,name: str, base: tuple[type], namespace: dict[str, any],**kwargs):
        super().__setattr__(cls,"__config__", kwargs)
        print(namespace)
        return super().__new__(cls,name,base,namespace)

    def __init__(cls,name: str, base: tuple,namespace: dict, **kwargs):
        # cls.propery = kwargs
        # print(cls.__name__)
        super().__init__(name,base,namespace)
    
    def __call__(cls,**kwargs):
        # print(cls.__name__)
        super().__setattr__("__notation__", kwargs)
        for i in kwargs:
            super().__setattr__(i, kwargs[i])
        return super().__call__()

class BaseModel(metaclass=BaseModel_Meta):
    def params(**kwargs):
        return kwargs
    pass

class PyDatabaseClient:
    def __init__(self):
        self.base_url = f"http://0.0.0.0:{5000}" # should be accquied from envirment variable
        self.token: Optional[str] = "notgiven"   # will be provide by sysllinkl
    
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
            print(table_.__dict__)
            #  create a funtion that will return a dict for the all of
            class_dict = {i:(base64.b64encode(pickle.dumps(class_data['__annotations__'][i])).decode("utf-8"),class_data[i] if class_data.get(i)  else {}) for i in class_data["__annotations__"]}
            print(class_dict)
            # print([i for i in class_dict["id"][1]])

            response = self._make_request(
                method.post,
                f"table/create/{self.token}",
                json={"pickled":class_dict,"name": table_.__name__}
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
        # class_dict = {
        #     i: (base64.b64encode(
        #         pickle.dumps(
        #             class_data['__annotations__'][i]
        #         )
        #     ).decode("utf-8")
        #     ,class_data[i] if class_data.get(i)  else {}) for i in class_data["__annotations__"]}
        
        payload={
            "name": data.__class__.__name__,
            "pickled": data.__notation__
        }
        print(data)

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

    def fetch(self,table_name:str,column: str = None):
        try: 
            payload = {
                "table_name": table_name,
                "conditions": column
            }
            response = self._make_request(
                method.post,
                f"table/fetch/{self.token}",
                json=payload
            )
            return response
        except Exception as e:
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

    client.create_table(book.__name__,book)
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

    # # sta2 = SQLExpr("id=7")
    # # onj = SQLExpr("name=aavart")
    # print(client.fetch("client_testtable"))

