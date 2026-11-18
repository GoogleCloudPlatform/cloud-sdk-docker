#!/bin/bash

set -euo pipefail

gcloud components install gcloud-go --quiet

export CLOUDSDK_USE_GOCLOUD=1 GOCLOUD_PARSER=python GOCLOUD_RUNNER=python

gocloud_check="$(gcloud meta test --check-from-gocloud 2>&1)" || {
  echo "${gocloud_check}"
  exit 1
}
if [[ "${gocloud_check}" != *"CLOUDSDK_FROM_GOCLOUD: 1"* ]]; then
  echo "gcloud did not run through gocloud: ${gocloud_check}"
  exit 1
fi

gcloud config list
gcloud version
gcloud meta check-import grpc
