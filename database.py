import sqlite3  # for database
import logger
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
        self.conn = self._initialize_database()

        self._execute_query_admin("""   
            CREATE TABLE IF NOT EXISTS query_log (
                Sno INTEGER PRIMARY KEY AUTOINCREMENT,
                Query TEXT,
                Timestamp TEXT,
                Client TEXT,
                Status TEXT
            )
        """)

        self._execute_query_admin("""
            CREATE TABLE IF NOT EXISTS client (
                Id TEXT PRIMARY KEY,
                Name TEXT,
                Token TEXT,
                Joined TEXT,
                Active TEXT,
                Owned_Tables TEXT,
                File_Location TEXT
            )
        """) 

        self._execute_query_admin("""
            CREATE TABLE IF NOT EXISTS table_owner (
                Table_Id TEXT PRIMARY KEY,
                Table_Name TEXT,
                Owner_Id TEXT,
                Owner_name TEXT
            ) 
        """)

        self._execute_query_admin("""
            CREATE TABLE IF NOT EXISTS client_log (
                Log_Id TEXT PRIMARY KEY,
                Client_Id TEXT,
                Client_Name TEXT,
                logged_In_At TEXT,
                logged_Out_At TEXT
            )
        """)
        self.conn.commit()

    def _initialize_database(self) -> sqlite3.Connection:
        """Initialize SQLite database with encryption"""
        # Create database directory if it doesn't exist
        Config.DATABASE_DIR.mkdir(exist_ok=True)
        
        # Create new database connection
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        # print("row factory : ",conn.row_factory)
        # Initialize query logging table and for now this should be changed
        # there should be table crearte ion on intalixing
        
        return conn

    
    def _log_query(self, query: str, user: str, status: str = status.success) -> None:
        """Log SQL query execution"""
        try:
            # print(_insert_query)
            self._insert_query("query_log",Query=query,Timestamp=datetime.now().isoformat(" "),Client=user,Status = status)

        except Exception as e:
           logging.error(f"Failed to log query: {e}")
           raise e
    
    def _insert_query(self,table_name: str, **column) -> status:
        try:
            self.conn.execute(
                f"""INSERT INTO {table_name} ({",".join([i for i in column])}) VALUES ({",".join(["?" for i in range(len(column))])})""",
                tuple(column[i] for i in column)
            )
            self.conn.commit()
            return status.success
        except Exception as e:
            logging.error(f"Failed to log Query: {e}")
            raise e
            return status.failed


    def _execute_query(self, user: str,query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        """Execute a SQL query with security checks"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            logging.info(cursor.description)
            columns = lambda descrp: [description[0] for description in descrp] if descrp else None
            results = [dict(zip(columns(cursor.description), row)) for row in cursor.fetchall()]
            self._log_query(query, user)
            return {
                "columns": columns(cursor.description),
                "rows": results,
                "row_count": len(results),
                "rows_affected": cursor.rowcount
            }
                
        except Exception as e:
            self._log_query(query, user, status.failed)
            raise e
    
    def _execute_query_admin(self,query: str, parmas: tuple | None = None) -> Dict: # here is no sql injection security
        try: 
            self.conn.cursor().execute(query)
            self.conn.commit()
            # logging.info(f"Query is {query}")
            self._log_query(query,"admin",status.success)
        except Exception as e:
            self._log_query(query,"admin",status.failed)
            raise e
    

    def table_schema(self, table_name: str) -> List[Dict[str, str]]:
        """Get schema information for a table"""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        return [
            {
                "name": row[1],
                "type": row[2],
                "notnull": bool(row[3]),
                "pk": bool(row[5])
            }
            for row in cursor.fetchall()
        ]

    def insert_query(self,table_name: str, **column) -> status:
        try:
            self._insert_query(table_name,**column)

        except sqlite3.OperationalError as e:
            loggin.warning(f"Schema of {table_name} is {self._table_schema(table_name)}")
        except Exception as e:
            logging.error(f"Failed to log Query: {e}")
            raise e
            return status.failed
    

    def create_table(self, table_name: str, user: str = "system", *columns: List[Column]) -> Dict[str, Any]:
        """Create a new table with specified columns"""
        # Validate table name (prevent SQL injection)
        if table_name.isalnum():
            logging.warning("Table name must  not be alphanumeric")
            raise ValueError("Table name must not  alphanumeric")
            
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(tuple(i.querystr() for i in columns))}
        )
        """

        try:
            logging.info(query)
            result = self._execute_query(user, query)
            logging.info(result)
            return result

        except Exception as e:
            logging.info(locals())
            logging.error(f"Error occured: {e}")
            raise e

    def verify_token(self, client_token: str) -> bool:
        query = f"""select * from client where Id='{client_token}'"""
        _execute_query("system",)
        pass

    def delete_table(self,tablename:str):
        self.conn.cursor().execute(f"DELETE FROM {tablename}")
        self.conn.commit()
        pass

    def drop_table(self,tablename:str):
        self.conn.cursor().execute(f"DROP TABLE {tablename}")
        self.conn.commit()
        pass

    def drop_all(self):
        self.conn.cursor().execute("""SELECT 'DROP TABLE IF EXISTS "' || name || '";'
FROM sqlite_master
WHERE type='table' AND nam;w
                                   :e NOT LIKE 'sqlite_%';""")
        self.conn.commit()
        pass
                                 
if (__name__ == "__main__"):  # for test componett of this file
    db= PyDatabase()
    db.create_table("test_table","Psudouser", Column("Sno", "INTEGER", True,True),Column("name", "TEXT"), Column("class", "INTEGER"))
    # db.in
