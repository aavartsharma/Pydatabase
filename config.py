import os
from pathlib import Path
from datetime import datetime

class Config:
    project_name="Pydatabase"
    version = "xxxxxxxxx"

    # Base configuration
    PROJECT_ROOT = Path(__file__).parent
    DATABASE_DIR = PROJECT_ROOT / "base"  # database should be under pybase control
    LOGS_DIR = PROJECT_ROOT / "logs"
    LOGGING_YML = "logging.yaml"
    
    # Security settings
    
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "your-encryption-key-change-this")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # Network settings
    HOST = "0.0.0.0"  # Allow connections from any IP in the local network
    PORT = 5000
    
    # Database settings
    MAX_CONNECTIONS = 5
    BACKUP_INTERVAL_HOURS = 24

    @staticmethod
    def init():
        """Initialize required directories"""
        for directory in [Config.DATABASE_DIR, Config.LOGS_DIR]:
            directory.mkdir(exist_ok=True)