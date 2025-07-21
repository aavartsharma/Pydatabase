import urllib3
import requests
import pandas as pd
from syslinkPy import Enum
from typing import Any, Dict, List, Optional

# Disable SSL verification warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class method(Enum):
    get: str = "GET"
    put: str = "PUT"
    post: str = "POST"

class Column:
    def __init__(self,name:str ,typeof:str, isprimekey: bool = str(False) , AUTOINCREMENT = str(False)):
        if(not isprimekey and AUTOINCREMENT):
            raise ValueError("autoincrement is only allowed for primarykey")
        self.name = name
        self.typeof = typeof
        self.isprimekey = isprimekey
        self.AUTOINCREMENT = AUTOINCREMENT
    
    def querystr(self) -> str:
        return f'{self.name} {self.typeof} {"PRIMARY KEY" if self.isprimekey else ""} {"AUTOINCREMENT" if self.AUTOINCREMENT else ""}'

class PyDatabaseClient:
    def __init__(self):
        self.base_url = f"http://0.0.0.0:{5000}" # should be accquied from envirment variable
        self.token: Optional[str] = "notgiven"   # will be provide by sysllinkl
        
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
        response = requests.request(
            method,
            f"{self.base_url}/{endpoint}",
            json=json,
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    
    def insert(self, collection: str, document: Dict[str, Any]) -> str:
        response = self._make_request("POST", collection, document)
        return response["_id"]
    
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

    # def fetch(self,table_name:str,)

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

    
    def delete(self, collection: str, query: Dict[str, Any]) -> int:
        """Delete documents from a collection"""
        response = self._make_request("POST", f"{collection}/delete", query)
        return response["deleted_count"]

    def Drop_table(self,table_name:str):
        pass

    def alter_table(self,table_name: str, **data):
        pass

    def get_schema(self, table_name: str):
        pass

    def test(self):
        return self._make_request(method.get, "test")

if(__name__ == "__main__"):

    # print('hello world')
    client = PyDatabaseClient()
    # print(client.create_table("client_testtable",Column("name", "TEXT","False")))
    # print(client.test())
    # a = Column("sno","INTEGER" , True, True)
    # print(a.__dict__)
    print(client.insert("client_testtable",name="aavart"))

