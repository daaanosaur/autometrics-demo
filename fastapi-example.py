from fastapi import FastAPI
import uvicorn
from autometrics import autometrics

app = FastAPI()

@app.get("/")
@autometrics
def read_root():
    do_something()
    return {"Hello": "World"}

@autometrics
def do_something():
    print("I did something")

if __name__ == "__main__":    
    uvicorn.run(app, host="localhost", port=8080)