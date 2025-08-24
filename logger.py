import os
import sys
import logging
from datetime import datetime
from typing import Optional, Dict, Any

# Configure logging

class Config:
    def __init__(self,**detail):
        for i in ("name",'version','detail'):
            if i not in detail:
                raise AttributeError(f"{i} is not specfiled")
        for i in detail:
            super().__setattr__(i,detail[i])
        self.detail = detail

class Utility:
    def __init__(self, **detail):
        self.config = Config(**detail)
        self.start_time = datetime.now()
        self.basename= lambda x: os.path.basename(x)
        # self.logger = sekf._setup_logger(name,version,detail)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/app.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )

        self.logger = logging.getLogger(self.basename(self.config.name))
        self.logger.info(f"Starting {self.basename(self.config.name)} v{self.config.version}")
    
    def _setup_logger(self, name: str, version: str, detail: str) -> logging.Logger:
        # Create logs directory if it doesn't exist
        log_dir = Path(Config.LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Create handlers
        current_date = datetime.utcnow().strftime('%Y-%m-%d')
        file_handler = logging.FileHandler(
            log_dir / f"{current_date}.log",
            encoding='utf-8'
        )
        console_handler = logging.StreamHandler()

        # Create formatters and add it to handlers
        log_format = logging.Formatter(
            f'[%(asctime)s UTC] [v{version}] [%(name)s] [%(levelname)s] - {detail} - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def debug():
        # add debug to the app.log
        pass
    
    def info():
        # add info to teh app.log
        pass
    
class APILogger:
    def __init__(self):
        self.logger = Utility(
            name="API",
            version=Config.version,
            detail="API Operations"
        ).logger

    def log_request(self, request_data: Dict[str, Any], client_id: str) -> None:
        """Log API request details"""
        log_entry = {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "client_id": client_id,
            "method": request_data.get("method"),
            "endpoint": request_data.get("endpoint"),
            "params": request_data.get("params"),
            "headers": request_data.get("headers")
        }
        self.logger.info(f"API Request: {json.dumps(log_entry)}")

    def log_response(self, response_data: Dict[str, Any], client_id: str) -> None:
        """Log API response details"""
        log_entry = {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "client_id": client_id,
            "status_code": response_data.get("status_code"),
            "response_time": response_data.get("response_time"),
            "endpoint": response_data.get("endpoint")
        }
        self.logger.info(f"API Response: {json.dumps(log_entry)}")

    def log_error(self, error_data: Dict[str, Any], client_id: str) -> None:
        """Log API errors"""
        log_entry = {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "client_id": client_id,
            "error_type": error_data.get("error_type"),
            "error_message": error_data.get("error_message"),
            "endpoint": error_data.get("endpoint"),
            "stack_trace": error_data.get("stack_trace")
        }
        self.logger.error(f"API Error: {json.dumps(log_entry)}")

    def log_security(self, security_data: Dict[str, Any], client_id: str) -> None:
        """Log security-related events"""
        log_entry = {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "client_id": client_id,
            "event_type": security_data.get("event_type"),
            "details": security_data.get("details"),
            "ip_address": security_data.get("ip_address")
        }
        self.logger.warning(f"Security Event: {json.dumps(log_entry)}")