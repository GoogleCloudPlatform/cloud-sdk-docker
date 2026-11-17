FROM us-docker.pkg.dev/gke-release/gcr.io/debian-base:trixie-v1.0.1-gke.0

ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH=/google-cloud-sdk/bin:$PATH

RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk

RUN ADDITIONAL_COMPONENTS="cloud-datastore-emulator cloud-firestore-emulator pubsub-emulator bigtable" && \
    if [ `uname -m` = 'x86_64' ]; then \
        ARCH="x86_64"; \
        ADDITIONAL_COMPONENTS="${ADDITIONAL_COMPONENTS} cloud-spanner-emulator"; \
    else \
        ARCH="arm"; \
    fi && \
    apt-get update && \
    apt-get dist-upgrade -qqy && \
    apt-get -y install --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        media-types \
        tzdata \
        openjdk-25-jre-headless && \
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    tar xzf google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    rm google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_emulator && \
    gcloud components install beta ${ADDITIONAL_COMPONENTS} && \
    GCLOUD_PYTHON="$(gcloud info --format='value(basic.python_location)')" && \
    echo "gcloud uses Python at $GCLOUD_PYTHON" && \
    test "$GCLOUD_PYTHON" = /google-cloud-sdk/platform/bundledpythonunix/bin/python3 && \
    ! command -v python3 && \
    gsutil version -l | grep -q "compiled crcmod: True" && \
    rm -rf /google-cloud-sdk/.install/.backup/ && \
    find /google-cloud-sdk/ -name "__pycache__" -type d  | xargs -n 1 rm -rf && \
    rm -rf /var/lib/apt/lists/* /tmp/*
