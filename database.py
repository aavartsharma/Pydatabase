import sqlite3  # for database
import logging   # logging libary
from config import Config    # config.py
# from pathlib import Path  
from syslinkPy import Enum
from datetime import datetime   # for datetime
from security import SecurityManager   # security.py
from typing import Any, Dict, List, Optional, Union   # for type annotation

logger = logging.getLogger(__name__)

class PyDatabase:

    class status(Enum):
        success:str
        failed:str

    def __init__(self):
        self.security = SecurityManager()
        self.db_path = Config.DATABASE_DIR / "base.db" 
        self.conn = self._initialize_database()

        self._execute_query_admin("""   
            CREATE TABLE IF NOT EXISTS query_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                timestamp TEXT,
                user TEXT,
                status TEXT
            )
        """)

        self._execute_query_admin("""
            CREATE TABLE IF NOT EXiSTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                token TEXT
            )
        """)

        self._execute_query_admin("""
            CREATE TABLE IF NOT EXISTS users_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_login TIME
            )
        """)
        
    def _initialize_database(self) -> sqlite3.Connection:
        """Initialize SQLite database with encryption"""
        # Create database directory if it doesn't exist
        Config.DATABASE_DIR.mkdir(exist_ok=True)
        
        # Create new database connection
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        
        # Initialize query logging table and for now this should be changed
        # there should be table crearte ion on intalixing
        
        return conn
    
    def _log_query(self, query: str, user: str, status: str = status.success) -> None:
        """Log SQL query execution"""
        try:
            self.conn.execute(
                "INSERT INTO query_log (query, timestamp, user, status) VALUES (?, ?, ?, ?)",
                (query, datetime.now().isoformat(), user, status)
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log query: {e}")
    
    def execute_query(self, user: str,query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        """Execute a SQL query with security checks"""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            columns = [description[0] for description in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            self._log_query(query, user)
            return {
                "columns": columns,
                "rows": results,
                "row_count": len(results),
                "rows_affected": cursor.rowcount
            }
                
        except Exception as e:
            self._log_query(query, user, self.status.failed)
            raise
    
    def _execute_query_admin(self,query: str, parmas: tuple | None = None) -> Dict:
        try: 
            self.conn.cursor().execute(query)
            self.conn.commit()
            self._log_query(query,"admin",self.status.success)
        except Exception as e:
            self._log_query(query,"admin",self.status.failed)
            raise e
    
    def drop_table(self,tablename:str):
        self.conn.cursor().execute(f"DROP TABLE {tablename}")
        self.conn.commit()
        pass

    def clear_table(self,tablename:str):
        self.conn.cursor().execute(f"DELETE FROM {tablename}")
        self.conn.commit()
        pass

    def clear_all(self):
        self.conn.cursor().execute("""SELECT 'DROP TABLE IF EXISTS "' || name || '";'
FROM sqlite_master
WHERE type='table' AND name NOT LIKE 'sqlite_%';""")
        self.conn.commit()
        pass

    def create_table(self, table_name: str, columns: Dict[str, str], user: str = "system") -> Dict[str, Any]:
        """Create a new table with specified columns"""
        # Validate table name (prevent SQL injection)
        if not table_name.isalnum():
            raise ValueError("Table name must be alphanumeric")
        
        # Build CREATE TABLE query
        column_defs = []
        for col_name, col_type in columns.items():
            if not col_name.isalnum():
                raise ValueError(f"Invalid column name: {col_name}")
            if col_type.upper() not in {"TEXT", "INTEGER", "REAL", "BLOB", "NULL"}:
                raise ValueError(f"Invalid column type: {col_type}")
            column_defs.append(f"{col_name} {col_type}")
            
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            {', '.join(column_defs)}
        )
        """
        
        return self.execute_query(user,query)
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, str]]:
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