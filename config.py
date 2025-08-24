import os
from pathlib import Path
from datetime import datetime

class Config:
    project_name="Pydatabase"
    version = "1.0.1"

    # Base configuration
    PROJECT_ROOT = Path(__file__).parent
    DATABASE_DIR = PROJECT_ROOT / "base"  # database should be under pybase control
    DATABASE_MAIN = DATABASE_DIR / "base.db"
    LOGS_DIR = PROJECT_ROOT / "logs"
    LOGGING_YML = "logging.yaml"
    LOG_LEVEL = "INFO"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    MAX_LOG_SIZE = 10 * 1024 * 1024     # Maximum log file size (in bytes) - 10MB
    LOG_BACKUP_COUNT = 30
    
    # Security settings
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