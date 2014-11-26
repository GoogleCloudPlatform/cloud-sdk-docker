#!/bin/bash
set -ex

HASH=$(git rev-parse HEAD)
GCLOUD_SDK=cloud-sdk:$HASH
GCLOUD_CONFIG=gcloud-config-$HASH
PROJECT=${PROJECT:?missing, usage: PROJECT=GCLOUD-PROJECT test.sh}

docker build -t ${GCLOUD_SDK} .
docker rm ${GCLOUD_CONFIG} || true
docker run ${GCLOUD_SDK} gcloud components list | grep preview | grep Installed
docker run -ti --name ${GCLOUD_CONFIG} ${GCLOUD_SDK} gcloud auth login
docker run --rm --volumes-from ${GCLOUD_CONFIG} ${GCLOUD_SDK} gcutil listinstances

