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
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/{self.basename(__file__)}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )

        self.logger = logging.getLogger(self.basename(self.config.name))
        self.logger.info(f"Starting {self.basename(self.config.name)} v{self.config.version}")
    
    def debug():
        # add debug to the app.log
        pass
    
    def info():
        # add info to teh app.log
        pass
    
