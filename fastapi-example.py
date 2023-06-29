from fastapi import FastAPI, Response
import uvicorn
import asyncio
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


# Define Objectives for the api routes

API_SLO_HIGH_SUCCESS = Objective(
    "Animal API Route SLO for High Success Rate (99%)",
    success_rate=ObjectivePercentile.P99,
)

API_QUICK_RESPONSES = Objective(
    "Animal API SLO for Low Latency (100ms)",
    success_rate=ObjectiveLatency.Ms100,
)

ANIMALS = ["snail", "rabbit", "panda"]


@app.get("/")
@autometrics(objective=API_SLO_HIGH_SUCCESS)
def animals():
    return {"animals": list_animals_helper()}


@app.get("/snail")
@autometrics(objective=API_QUICK_RESPONSES)
async def snail():
    # Snails are slow. They have sometimes have high latency
    await random_delay()
    return {"suggestion": "Let's take it easy"}


@app.get("/rabbit")
@autometrics(objective=API_QUICK_RESPONSES)
def rabbit():
    # Rabbits are fast. They have very low latency
    return {"suggestion": "Let's drink coffee and go for a jog"}


@app.get("/panda")
@autometrics(objective=API_SLO_HIGH_SUCCESS)
def panda():
    # Pandas are clumsy. They randomly error 10% of the time
    randomly_error()
    return {"suggestion": "Let's eat bamboo"}


@autometrics
def list_animals_helper():
    """Return all animals"""
    return ANIMALS


@autometrics
def randomly_error():
    """Randomly raise an error with a 10% chance"""
    # Generate a random number between 1 and 10
    error_chance = random.randint(1, 10)

    # If the random number is 1, raise an error
    if error_chance == 1:
        raise Exception("Random error occurred!")


@autometrics
async def random_delay():
    """Generate a random latency between 0 and 110ms"""
    delay = random.randint(0, 11) * 0.01
    await asyncio.sleep(delay)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
