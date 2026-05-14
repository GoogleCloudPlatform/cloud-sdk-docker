ARG TARGETARCH=amd64
FROM debian:trixie-slim AS base-amd64
FROM python:3.15.0b1-slim-trixie AS base-arm64
FROM base-${TARGETARCH}
ARG TARGETARCH
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk
ARG INSTALL_COMPONENTS
RUN mkdir -p /usr/share/man/man1/
RUN apt-get update -qqy && apt-get -qqy upgrade && \
    apt-get install -qqy \
        curl \
        gcc \
        apt-transport-https \
        lsb-release \
        openssh-client \
        git \
        gnupg && \
    if [ "$TARGETARCH" = "arm64" ]; then \
        pip3 install --no-cache-dir crcmod; \
    fi && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb [signed-by=/etc/apt/keyrings/google-cloud-cli.gpg] https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" \
        > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg  | gpg --dearmor -o /etc/apt/keyrings/google-cloud-cli.gpg && \
    apt-get update && apt-get install -y google-cloud-cli=${CLOUD_SDK_VERSION}-0 $INSTALL_COMPONENTS && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_slim && \
    gcloud --version && \
    gsutil version -l && \
    bq version && \
    gcloud-crc32c /usr/bin/gcloud
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config"]
