import logger
import socket
import uvicorn
from config import Config

logging = logger.Utility(name=__file__,version=Config.version,detail="idnotknow").logger

def get_local_ip():
    # Use UDP socket to get your LAN IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external IP, doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


if __name__ == "__main__":
    try:
        logging.info("Starting the Server...")
        logging.info(f"Local ip of meachine is {get_local_ip()}")
        uvicorn.run("server:app",host=Config.HOST,port=Config.PORT,reload=True,log_config=Config.LOGGING_YML)
    except Exception as e:
        logging.error(f"Failed to run server: {e}")
        raise e

    