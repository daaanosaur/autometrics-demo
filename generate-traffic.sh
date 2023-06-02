#!/bin/bash

# This script will fetch a URL using curl at a random interval between 100ms and 5s
while true; do
    # Generate a random sleep time between 100ms and 5s
    sleep_time=$(awk -v min=0.1 -v max=5 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')
    sleep "$sleep_time"

    # Fetch the URL using curl
    curl -s -o /dev/null "http://localhost:8080"  # Replace "https://example.com" with your desired URL
done