import logger
import uvicorn
from config import Config

logging = logger.Utility(name=__file__,version=Config.version,detail="idnotknow").logger

if __name__ == "__main__":
    try:
        logging.info("Starting the Server...")
        uvicorn.run("server:app",host=Config.HOST,port=Config.PORT,reload=True,log_config=Config.LOGGING_YML)
    except Exception as e:
        logging.error(f"Failed to run server: {e}")
        raise e

    