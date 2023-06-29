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
uvicorn fastapi-example:app --reload --port=8080
```

Optionally generate traffic for all the api routes

```sh
chmod +x generate-traffic.sh
./generate-traffic.sh
```

### Setting up local Prometheus

> Skip this if you already have Prometheus set up locally

#### With `am`

```sh
# Install the Autometrics cli
brew install autometrics-dev/tap/am
# Start scraping localhost:8080
am start :8080
```

#### With Quickmetrics

There is a docker-compose setup in the [Quickmetrics repo](https://github.com/autometrics-dev/quickmetrics), which can spin up Prometheus (and other components) for you.

#### Without Quickmetrics

Follow instructions in autometrics-dev. I used Docker:

```sh
docker pull prom/prometheus
# I'm using port 8063 for prometheus because 9090 is already taken on my machine
docker run \
    -p 8063:9090 \
    -v /absolute/path/to/this/project/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```

where the `prometheus.yml` file is similar to the one in this repo:

```yaml
scrape_configs:
  - job_name: python-autometrics-example-fastapi
    metrics_path: /metrics
    static_configs:
      - targets: ["localhost:8080"]
    # For a real deployment, you would want the scrape interval to be
    # longer but for testing, you want the data to show up quickly
    scrape_interval: 200ms
```

### Install and Configure Autometrics VSCode Extension

...

Update the VSCode Extension settings to use the url to your local Prometheus server. Since I'm not using the default port (`9090`), I need to update the settings:

```json
{
  "autometrics.prometheusUrl": "http://localhost:8063"
}
```

### Generating Data

There is a script in the root of the repo that can be executed to generate data inside Prometheus. See: `generate-traffic.sh`

You can copy-paste the script into a shell, or execute it directly from the repo.
