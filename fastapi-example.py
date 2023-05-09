from fastapi import FastAPI, Response
import uvicorn
from autometrics import autometrics
from prometheus_client import generate_latest

app = FastAPI()


# Set up a metrics endpoint for Prometheus to scrape
# `generate_lates` returns the latest metrics data in the Prometheus text format
@app.get("/metrics")
def metrics():
    return Response(generate_latest())


@app.get("/")
@autometrics
def read_root():
    do_something()
    return {"Hello": "World"}


@app.get("/async-test")
@autometrics
async def async_test_route():
    message = await my_async_function()
    return {"Hello": message}


@autometrics
def do_something():
    print("I did something")


@autometrics
async def my_async_function():
    print("I did something async")
    return "Hello, async world!"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
