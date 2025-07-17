import sqlite3  # for database
import logger
import keyword
from config import Config    # config.py
from syslinkPy import Enum
from datetime import datetime   # for datetime
from security import SecurityManager   # security.py
from typing import Any, Dict, List, Optional, Union   # for type annotation

logging = logger.Utility(name=__file__,version=Config.version,detail="idnotknow").logger #(__name__,Config.version,"Idon'tknow",Config.project_name)
# print(__file__)

class status(Enum):
    success:str
    failed:str

class Column:
    def __init__(self,name:str ,typeof:str, isprimekey: bool = False , AUTOINCREMENT = False):
        if(not isprimekey and AUTOINCREMENT):
            raise ValueError("autoincrement is only allowed for primarykey")
        self.name = name
        self.typeof = typeof.capitalize()
        self.isprimekey = isprimekey
        self.AUTOINCREMENT = AUTOINCREMENT
    
    def querystr(self) -> str:
        return f'{self.name} {self.typeof} {"PRIMARY KEY" if self.isprimekey else ""} {"AUTOINCREMENT" if self.AUTOINCREMENT else ""}'

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
        self.db_path = Config.DATABASE_DIR / "base.db" 
        self.conn, self.cursor = self._initialize_database()
        # self.cursor = self.conn.cursor()

        #-------- lambda function --------#

        self._delete = lambda tablename: _execute_query(f"DELETE FROM {tablename}")
        self._drop_table = lambda tablename: _execute_query(f"DROP TABLE {tablename}")
        self._drop_all = lambda: _execute_query("""SELECT 'DROP TABLE IF EXISTS "' || name || '";' FROM sqlite_master WHERE type='table' AND nam;w :e NOT LIKE 'sqlite_%';""")


    # def delete_table(self,tablename:str):
    #     _execute_query(f"DELETE FROM {tablename}")

    # def drop_table(self,tablename:str):
    #     _execute_query(f"DROP TABLE {tablename}")

    # def drop_all(self):
    #     self.conn.cursor().execute("""SELECT 'DROP TABLE IF EXISTS "' || name || '";' FROM sqlite_master WHERE type='table' AND nam;w :e NOT LIKE 'sqlite_%';""")

    def _initialize_database(self) -> sqlite3.Connection:
        """Initialize SQLite database with encryption"""
        # Create database directory if it doesn't exist
        # Config.DATABASE_DIR.mkdir(exist_ok=True)
        Config.init()
        
        # Create new database connection
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        self._execute_query("""   
            CREATE TABLE IF NOT EXISTS query_log (
                Sno INTEGER PRIMARY KEY AUTOINCREMENT,
                Query TEXT,
                Timestamp TEXT,
                Client TEXT,
                Status TEXT
            )
        """,conn=conn,cursor=cursor)
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS client (
                Id TEXT PRIMARY KEY,
                Name TEXT,
                Token TEXT,
                Joined TEXT,
                Active TEXT,
                Owned_Tables TEXT,
                File_Location TEXT
            )
        """,conn=conn,cursor=cursor) 

        self._execute_query("""
            CREATE TABLE IF NOT EXISTS table_owner (
                Table_Id TEXT PRIMARY KEY,
                Table_Name TEXT,
                Owner_Id TEXT,
                Owner_name TEXT
            ) 
        """,conn=conn,cursor=cursor)

        self._execute_query("""
            CREATE TABLE IF NOT EXISTS client_log (
                Log_Id TEXT PRIMARY KEY,
                Client_Id TEXT,
                Client_Name TEXT,
                logged_In_At TEXT,
                logged_Out_At TEXT
            )
        """,conn=conn,cursor=cursor)
        return conn , cursor
    
    def _execute_query(self,query: str, params: tuple | None = None,conn=None,cursor=None) -> Dict: # here is no sql injection security
        try:
            if not conn:
                conn = self.conn
            if not cursor:
                cursor = self.cursor
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            columns = lambda descrp: [description[0] for description in descrp] if descrp else None
            results = [dict(zip(columns(cursor.description), row)) for row in cursor.fetchall()]
            return {
                "columns": columns(cursor.description),
                "rows": results,
                "row_count": len(results),
                "rows_affected": cursor.rowcount
            }
        except Exception as e:
            # self._log_query(query,"admin",status.failed)
            logging.error(f"Error excuting {query},{params}: {e}")
            raise e
    
    def _log_query(self, query: str, user: str, status: str = status.success) -> None:
        """Log SQL query execution"""
        try:
            # print(_insert_query)
            self._insert_query("aavart",table_name="query_log",Query=query,Timestamp=datetime.now().isoformat(" "),Client=user,Status = status)

        except Exception as e:
           logging.error(f"Failed to log query: {e}")
           raise e
    
    def _insert_query(self,table_name: str, **column) -> status:
        """asdfasdfasdfasdfsafsadf"""
        try:
            query= f"""INSERT INTO {table_name} ({",".join([i for i in column])}) VALUES ({",".join(["?" for i in range(len(column))])})"""
            params= tuple(column[i] for i in column)
            self._execute_query(query,params)
            return status.success
        except Exception as e:
            logging.error(f"Failed to log Query: {e}")
            raise e
            return status.failed

    def _create_table(self, table_name: str, *columns: List[Column]):
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(tuple(i.querystr() for i in columns))}
        )
        """

        try:
            result = self._execute_query(query)
            return result

        except Exception as e:
            logging.info(locals())
            logging.error(f"Error occured: {e}")
            raise e

    def _table_schema(self,table_name:str):
        rows = self._execute_query(f"PRAGMA table_info({table_name});")
        return rows
        # return [
        #     {
        #         "name": row[1],
        #         "type": row[2],
        #         "notnull": bool(row[3]),
        #         "pk": bool(row[5]),
        #     }
        #     for row in rows
        # ]

    def _fetch_data(self,table_name: str):
        result = self._execute_query(f"SELECT * from {table_name}")
        return result
    # def _insert_query(self,table_name: str, **column) -> status:
    #     """dsfsadfasfasdfasfdsaf"""
    #     try:
    #         self.conn.execute(
    #             f"""INSERT INTO {table_name} ({",".join([i for i in column])}) VALUES ({",".join(["?" for i in range(len(column))])})""",
    #             tuple(column[i] for i in column)
    #         )
    #         self.conn.commit()
    #         return status.success
    #     except Exception as e:
    #         logging.error(f"Failed to log Query: {e}")
    #         raise e
    #         return status.failed


    # def _execute_query(self, user: str,query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
    #     """Execute a SQL query with security checks"""
    #     _execute_query(self.conn,query,params)
    

    def table_schema(self,user, table_name: str) -> List[Dict[str, str]]:
        """Get schema information for a table"""
        logging.info(f"User query - user:{user}, queryed: {table_schema.__name__}")
        return self._table_schema(table_name)

    def insert(self,user,table_name: str, **column) -> status:
        try:
            for i in column:
                if keyword.iskeyword(i):
                    raise ValueError(f"arg can't be a keyword , {i}")
            self._insert_query(table_name,**column)

        except sqlite3.OperationalError as e:
            logging.warning(f"Schema of {table_name} is {self._table_schema(table_name)}")
        except Exception as e:
            logging.error(f"Failed to log Query: {e}")
            raise e
            return status.failed
    
    def create_table(self,user: str, table_name: str, *columns: List[Column]) -> Dict[str, Any]:
        """Create a new table with specified columns"""
        # Validate table name (prevent SQL injection)
        if table_name.isalnum():
            logging.warning("Table name must  not be alphanumeric")
            raise ValueError("Table name must not  alphanumeric")
        for i in columns:
            if keyword.iskeyword(i.name):
                raise ValueError(f"arg can't be a keyword , {i.name}")
        result = self._create_table(table_name,*columns)
        result["status"] = status.success
        return result
    
    def delete():
        pass
    
    def delete_all():
        pass

    def drop_table():
        pass

    def drop_all():
        pass

    def verify_token(self, client_token: str) -> bool:
        query = f"""select * from client where Id='{client_token}'"""
        _execute_query("system",)
        pass

                                 
if (__name__ == "__main__"):  # for test componett of this file
    db= PyDatabase()
    print(db.create_table("aavart","test_table2", Column("Sno", "INTEGER", True,True),Column("name", "TEXT"), Column("classes", "INTEGER")))
    # db.in
    # print(db.insert("test_table2",name="aavart sharma",classes=3))
    print(db._fetch_data("aavart","test_table2"))
    print(db.table_schema("aavart","test_table2"))
