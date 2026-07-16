#!/bin/bash

EMULATOR_NAME="$1"
echo "=== Testing emulator: ${EMULATOR_NAME} ==="

# Start the server in the background
gcloud beta emulators ${EMULATOR_NAME} start --host-port=0.0.0.0:8085 --project=blah &
EMULATOR_PID=$!

# Poll for up to 30 seconds for the port to open
for i in {1..30}; do
  if (echo > /dev/tcp/127.0.0.1/8085) 2>/dev/null; then
    echo "Server for ${EMULATOR_NAME} started successfully (exiting with code 0)"
    kill $EMULATOR_PID 2>/dev/null || kill -9 $EMULATOR_PID 2>/dev/null
    sleep 2
    exit 0
  fi
  sleep 1
done

echo "Server for ${EMULATOR_NAME} failed to start within 30 seconds"
kill $EMULATOR_PID 2>/dev/null || kill -9 $EMULATOR_PID 2>/dev/null
sleep 2
exit 1
