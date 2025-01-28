#!/bin/bash

apt-get update && apt-get install -y lsof

# Start the server in the background
gcloud beta emulators $1 start --host-port=0.0.0.0:8085 --project=blah &

# Wait a few seconds for the server to start
sleep 10

# Check if the server is listening on the port
if lsof -i :8085 > /dev/null; then
  echo "Server started successfully (exiting with code 0)"
  kill -9 $(lsof -t -i :8085)
  exit 0
else
  echo "Server failed to start"
  exit 1
fi

