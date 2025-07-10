import sys
import logging
from datetime import datetime
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class Config:
    def __init__(self,utility,version,created,project,**detail):
        self.app_name = utility
        self.version = version
        self.created_at = created
        self.author = project
        self.detail = detail

class Utility:
    
    def __init__(self, config: Config,**moreinfo):
        self.config = config
        self.moreinfo = moreinfo
        self.start_time = datetime.now()
        logger.info(f"Starting {self.config.app_name} v{self.config.version}")
    
    def debug():
        # add debug to the app.log
        pass
    
    def info():
        # add info to teh app.log
        pass
    
