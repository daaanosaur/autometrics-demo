# Autometrics :heart: FastAPI

An example fastapi app that makes use of autometrics.

## Setup

### Running the app

Create and activate a virtual env

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```sh
pip install -r requirements.txt
```

Run the app

```sh
uvicorn app:app --reload --port=8080
```

Optionally generate traffic for all the api routes

```sh
chmod +x generate-traffic.sh
./generate-traffic.sh
```

### Setting up local Prometheus

> Skip this if you already have Prometheus set up locally

#### With `am`

You can use the `am` CLI to quickly spin up Prometheus and the Autometrics Explorer dashboard:

```sh
# Install the Autometrics cli
brew install autometrics-dev/tap/am
# Start scraping localhost:8080
am start :8080
```

You can also run the CLI via docker:

```sh
docker run \
  --network host
  -e LISTEN_ADDRESS=0.0.0.0:6789 \
  -p 6789:6789 \
  -p 9090:9090 \
  autometrics/am start :8080
```

### Install and Configure the Autometrics VSCode Extension

Update the VSCode Extension settings to use the url to your local Prometheus server. Since we're using `am` to run prometheus, we need to update the settings:

```json
{
  "autometrics.prometheusUrl": "http://localhost:9090/prometheus"
}
```

### Generating Data

There is a script in the root of the repo that can be executed to generate data inside Prometheus. See: `generate-traffic.sh`

You can copy-paste the script into a shell, or execute it directly from the repo.
