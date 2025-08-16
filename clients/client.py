import urllib3
import requests
# import pandas as pd
from syslinkPy import Enum
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

# Disable SSL verification warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class method(Enum):
    get: str = "GET"
    put: str = "PUT"
    post: str = "POST"

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
    
    def create_table(self,table_name: str, *columns: List[Column]):
        try:
            listc = [i.__dict__ for i in columns]
            print(listc)
            payload = {
                "table_name": table_name,
                "columns": listc
            }

            response = self._make_request(
                method.post,
                f"table/create/{self.token}",
                json=payload
            )
            return response
        except Exception as e:
            print(e)
            return str(e)
            # print(str(e.http_error_msg))
    
    def insert(self,table_name: str,**data : Dict[str, str]) -> str:
        """Insert a document into a collection"""
        payload={
            "table_name": table_name,
            "columns": [data]
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
    class book():
        id: Optional[int] = Field(default=None,primary_key=True)
    print(client.delete("client_testtable"))
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

