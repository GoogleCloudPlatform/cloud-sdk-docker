#!/bin/bash

echo "Checking gsutil version" 
gsutil -v

echo "Checking kpt version"
kpt version

echo "Checking local-extract version"
local-extract --version

echo "Checking gke-gcloud-auth-plugin version"
gke-gcloud-auth-plugin --version

echo "Checking bq version"
bq version

echo "Checking bundled-python version"
/usr/lib/google-cloud-sdk/platform/bundledpythonunix/bin/python --version

echo "Checking cbt version"
cbt version

echo "Checking crc checksum for gcloud"
gcloud-crc32c /usr/bin/gcloud

echo "Checking kubectl version"
kubectl version

echo "Checking the emulators"
./test-all-emulators.sh
