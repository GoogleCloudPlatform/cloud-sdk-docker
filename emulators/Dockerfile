# debian:buster-slim is used instead of alpine because the cloud bigtable emulator requires glibc.
FROM debian:buster-slim

ARG CLOUD_SDK_VERSION=356.0.0
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH /google-cloud-sdk/bin:$PATH

RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk

RUN mkdir -p /usr/share/man/man1/ && \
    apt-get update && \
    apt-get -y install \
        curl \
        python3 \
        python3-crcmod \
        bash \
        openjdk-11-jre-headless && \
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    rm google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image_emulator && \
    gcloud components remove anthoscli && \
    gcloud components install beta cloud-datastore-emulator cloud-firestore-emulator pubsub-emulator cloud-spanner-emulator bigtable && \
    rm /google-cloud-sdk/data/cli/gcloud.json && \
    rm -rf /google-cloud-sdk/.install/.backup/ && \
    find /google-cloud-sdk/ -name "__pycache__" -type d  | xargs -n 1 rm -rf

