#!/bin/bash
set -ex

HASH=$(git rev-parse HEAD)
GCLOUD_SDK=cloud-sdk:$HASH
GCLOUD_CONFIG=gcloud-config-$HASH
PROJECT=${PROJECT:?missing, usage: PROJECT=GCLOUD-PROJECT test.sh}

cleanup() {
  docker rm ${GCLOUD_CONFIG} || true
}
trap 'cleanup' 0
docker build -t ${GCLOUD_SDK} .
docker rm ${GCLOUD_CONFIG} || true
docker run --rm ${GCLOUD_SDK} gcloud components list | grep 'Not Installed' && false
docker run -ti --name ${GCLOUD_CONFIG} ${GCLOUD_SDK} gcloud auth login
docker run --rm --volumes-from ${GCLOUD_CONFIG} ${GCLOUD_SDK} gcutil --project ${PROJECT} listinstances
