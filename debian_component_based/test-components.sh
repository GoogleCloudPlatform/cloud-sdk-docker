#!/bin/bash
set -e

echo "Checking gsutil version"
gsutil version

echo "Checking local-extract version"
local-extract --version

echo "Checking gke-gcloud-auth-plugin version"
gke-gcloud-auth-plugin --version

echo "Checking bq version"
bq version

echo "Checking bundled-python version"
/google-cloud-sdk/platform/bundledpythonunix/bin/python --version

echo "Checking cbt version"
cbt version

echo "Checking crc checksum for gcloud"
gcloud-crc32c /google-cloud-sdk/bin/gcloud

echo "Checking kubectl version"
kubectl version --client

echo "Checking the emulators"
./test-dcb-emulators.sh
