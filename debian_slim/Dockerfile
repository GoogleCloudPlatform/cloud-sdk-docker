FROM debian:trixie-slim
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk
ARG INSTALL_COMPONENTS
RUN apt-get update -qqy && apt-get dist-upgrade -qqy && apt-get install -qqy --no-install-recommends \
        ca-certificates \
        curl \
        media-types \
        apt-transport-https \
        lsb-release \
        openssh-client \
        git \
        gnupg && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb [signed-by=/etc/apt/keyrings/google-cloud-cli.gpg] https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" \
        > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg  | gpg --dearmor -o /etc/apt/keyrings/google-cloud-cli.gpg && \
    apt-get update && apt-get install -y --no-install-recommends google-cloud-cli=${CLOUD_SDK_VERSION}-0 $INSTALL_COMPONENTS && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_slim && \
    gcloud info && \
    GCLOUD_PYTHON="$(gcloud info --format='value(basic.python_location)')" && \
    echo "gcloud uses Python at $GCLOUD_PYTHON" && \
    test "$GCLOUD_PYTHON" = /usr/lib/google-cloud-sdk/platform/bundledpythonunix/bin/python3 && \
    ! command -v python3 && \
    gsutil version -l | grep -q "compiled crcmod: True" && \
    bq version && \
    gcloud-crc32c /usr/bin/gcloud && \
    rm -rf /var/lib/apt/lists/*
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config"]
