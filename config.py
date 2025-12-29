import os
import logging
from pathlib import Path
from datetime import datetime

class Config:
    project_name="Pydatabase"
    version = "1.0.1"
    #=> app settings
    dev = True
    #=> Base configuration
    PROJECT_ROOT = Path(__file__).parent
    DATABASE_DIR = PROJECT_ROOT / "base"  # database should be under pybase control
    DATABASE_MAIN = DATABASE_DIR / "base.db"

    #=> Logging configuration 
    LOGGING_YML = "logging.yaml"
    LOGS_DIR = PROJECT_ROOT / "logs"
    LOG_APPLOG = 'logs/app.log'
    LOG_MODULELOG = 'logs/module_logs/'
    LOG_ERROR_LOG = 'logs/bugsanderror_log/'
    LOG_LEVEL =  logging.DEBUG if dev else logging.INFO 
    LOG_DATE_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s' 
    MAX_LOG_SIZE = 10 * 1024 * 1024     # Maximum log file size (in bytes) - 10MB
    LOG_BACKUP_COUNT = 30
    # Security settings
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # Network settings
    HOST = "0.0.0.0"  # Allow connections from any IP in the local network
    PORT = 5000
    
    # Database setting
    MAX_CONNECTIONS = 5
    BACKUP_INTERVAL_HOURS = 24

    @staticmethod
    def init():
        """Initialize required directories"""
        for directory in [Config.DATABASE_DIR, Config.LOGS_DIR]:
            directory.mkdir(exist_ok=True)
