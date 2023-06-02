from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import uvicorn
import random
from autometrics import (
    autometrics,
    get_autometrics_admin_html,
)
from prometheus_client import generate_latest

app = FastAPI()


# Set up a metrics endpoint for Prometheus to scrape
# `generate_latest` returns the latest metrics data in the Prometheus text format
@app.get("/metrics")
def metrics():
    return Response(generate_latest())


@app.get("/")
@autometrics
def read_root():
    # Generate a random number between 1 and 10
    error_chance = random.randint(1, 10)

    # If the random number is 1, raise an error
    if error_chance == 1:
        raise Exception("Random error occurred!")
    do_something()
    return {"Hello": "World"}


@app.get("/async-test")
@autometrics
async def async_test_route():
    message = await my_async_function()
    return {"Hello": message}


# HACK - add the admin panel UI manually
@autometrics
@app.get("/autometrics/admin", response_class=HTMLResponse)
def autometrics_admin():
    return get_autometrics_admin_html(prom_url="http://localhost:8063")
    # return get_autometrics_admin_html(
    #     cdn_root="http://localhost:8063", prom_url="http://localhost:8063"
    # )


@autometrics
def do_something():
    print("I did something")


@autometrics
async def my_async_function():
    print("I did something async")
    return "Hello, async world!"


@autometrics
def my_new_function_with_args(arg1, arg2):
    print("I did something with args")
    return f"Hello, {arg1} and {arg2}!"


if __name__ == "__main__":
    # run_admin_server()  # FIXME - server dies
    uvicorn.run(app, host="localhost", port=8080)
