import uvicorn
from config import Config

if __name__ == "__main__":
    uvicorn.run("server:app",host=Config.HOST,port=Config.PORT,reload=True,log_config=Config.LOGGING_YML)

    