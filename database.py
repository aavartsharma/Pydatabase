import sqlite3  # for database
import logging   # logging libary
from config import Config    # config.py
# from pathlib import Path  
from datetime import datetime   # for datetime
from security import SecurityManager   # security.py
from typing import Any, Dict, List, Optional, Union   # for type annotation

logger = logging.getLogger(__name__)

class PyDatabase:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.security = SecurityManager()
        self.db_path = Config.DATABASE_DIR / f"{db_name}.db" 
        self.conn = self._initialize_database()
        
    def _initialize_database(self) -> sqlite3.Connection:
        """Initialize SQLite database with encryption"""
        # Create database directory if it doesn't exist
        Config.DATABASE_DIR.mkdir(exist_ok=True)
        
        # Create new database connection
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        
        # Initialize query logging table and for now this should be changed
        # there should be table crearte ion on intalixing
        conn.execute("""   
            CREATE TABLE IF NOT EXISTS query_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                timestamp TEXT,
                user TEXT,
                status TEXT
            )
        """)
        
        return conn
    
    def _log_query(self, query: str, user: str, status: str = "success") -> None:
        """Log SQL query execution"""
        try:
            self.conn.execute(
                "INSERT INTO query_log (query, timestamp, user, status) VALUES (?, ?, ?, ?)",
                (query, datetime.now().isoformat(), user, status)
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log query: {e}")
    
    def execute_query(self, query: str, params: Optional[tuple] = None,user: str = "system") -> Dict[str, Any]:
        """Execute a SQL query with security checks"""
        # List of dangerous SQL operations to block
        dangerous_operations: list[str] = [
            "DROP", "TRUNCATE", "DELETE FROM", "ALTER", 
            "MODIFY", "RENAME", "VACUUM", "ATTACH"
        ]
        
        # Check for dangerous operations
        query_upper: str = query.upper()
        for operation in dangerous_operations:  # this should be changed a file can do this but should have key and for the table
            if operation in query_upper:
                self._log_query(query, user, "blocked")
                raise ValueError(f"Operation not allowed: {operation}")
        
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Handle different query types
            if query_upper.startswith("SELECT"):
                columns = [description[0] for description in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                self._log_query(query, user)
                return {
                    "type": "select",
                    "columns": columns,
                    "rows": results,
                    "row_count": len(results)
                }
            else:
                self.conn.commit()
                self._log_query(query, user)
                return {
                    "type": "update",
                    "rows_affected": cursor.rowcount
                }
                
        except Exception as e:
            self._log_query(query, user, f"error: {str(e)}")
            raise
    
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
        
        return self.execute_query(query, user=user)
    
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