#!/bin/bash

EMULATOR_NAME="$1"
echo "=== Testing emulator: ${EMULATOR_NAME} ==="

# Start the server in its own process group so child processes (Java/Go/C++
# emulator servers spawned by the gcloud wrapper) can be terminated cleanly
# without holding port 8085 open for subsequent emulator tests.
setsid gcloud beta emulators ${EMULATOR_NAME} start --host-port=0.0.0.0:8085 --project=blah &
EMULATOR_PID=$!

cleanup() {
  kill -- -"$EMULATOR_PID" 2>/dev/null || true
  for j in {1..10}; do
    if ! (echo > /dev/tcp/127.0.0.1/8085) 2>/dev/null; then
      break
    fi
    sleep 1
  done
  kill -9 -- -"$EMULATOR_PID" 2>/dev/null || true
  wait "$EMULATOR_PID" 2>/dev/null || true
}

# Poll for up to 30 seconds for the port to open
for i in {1..30}; do
  if (echo > /dev/tcp/127.0.0.1/8085) 2>/dev/null; then
    echo "Server for ${EMULATOR_NAME} started successfully (exiting with code 0)"
    cleanup
    exit 0
  fi
  sleep 1
done

echo "Server for ${EMULATOR_NAME} failed to start within 30 seconds"
cleanup
exit 1
