from fastapi import FastAPI, Response
import uvicorn
import random
from autometrics import autometrics
from autometrics.objectives import Objective, ObjectiveLatency, ObjectivePercentile

from prometheus_client import generate_latest

app = FastAPI()


# Set up a metrics endpoint for Prometheus to scrape
# `generate_latest` returns the latest metrics data in the Prometheus text format
@app.get("/metrics")
def metrics():
    return Response(generate_latest())


API_SLO_HIGH_SUCCESS = Objective(
    "My API SLO for High Success Rate (90%)",
    success_rate=ObjectivePercentile.P90,
)


@app.get("/")
@autometrics(objective=API_SLO_HIGH_SUCCESS)
def read_root():
    # Generate a random number between 1 and 10
    error_chance = random.randint(1, 10)

    # If the random number is 1, raise an error
    if error_chance == 1:
        raise Exception("Random error occurred!")
    do_something()
    return {"Hello": "World"}


@autometrics(objective=API_SLO_HIGH_SUCCESS)
@app.get("/async-test")
async def async_test_route():
    message = await my_async_function()
    return {"Hello": message}


@autometrics
def do_something():
    print("I did something")


RANDOM_SLO_HIGH_SUCCESS = Objective(
    "My Random SLO for High Success Rate (99%)",
    success_rate=ObjectivePercentile.P99,
)


@autometrics(objective=RANDOM_SLO_HIGH_SUCCESS)
async def my_async_function():
    print("I did something async")
    return "Hello, async world!"


@autometrics
def my_new_function_with_args(arg1, arg2):
    print("I did something with args")
    return f"Hello, {arg1} and {arg2}!"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
