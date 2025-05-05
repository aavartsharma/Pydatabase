from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def frist_example():
    return {"thisthis": "fastApi"}

