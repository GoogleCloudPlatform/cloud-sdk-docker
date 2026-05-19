ARG TARGETARCH=amd64
FROM debian:trixie-slim AS base-amd64
FROM python:3.14.4-slim-trixie AS base-arm64

FROM debian:trixie-slim AS build_image

ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ARG INSTALL_COMPONENTS

RUN apt-get update -qqy && apt-get -qqy upgrade && \
    apt-get install -qqy \
        curl \
        ca-certificates \
        lsb-release \
        gnupg && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb [signed-by=/etc/apt/keyrings/google-cloud-cli.gpg] https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" \
        > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg  | gpg --dearmor -o /etc/apt/keyrings/google-cloud-cli.gpg && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-cloud-cli=${CLOUD_SDK_VERSION}-0 $INSTALL_COMPONENTS &&\
    rm -rf /root/.cache/pip/ && \
    find /usr/lib/google-cloud-sdk -name '*.pyc' -delete && \
    find /usr/lib/google-cloud-sdk -name '*__pycache__*' -delete
FROM base-amd64 AS prep-amd64
COPY --from=build_image /usr/lib/google-cloud-sdk /usr/lib/google-cloud-sdk
RUN echo -n "x86_64" > /tmp/arch

FROM base-arm64 AS prep-arm64
COPY --from=build_image /usr/lib/google-cloud-sdk /usr/lib/google-cloud-sdk
RUN apt-get update -qqy && apt-get install -qqy gcc && \
    echo -n "arm" > /tmp/arch && \
    pip3 install --no-cache-dir crcmod && \
    apt-get remove -y gcc && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

ARG TARGETARCH
FROM prep-${TARGETARCH}
ENV PATH=$PATH:/usr/lib/google-cloud-sdk/bin
# Create a non-root user
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk
RUN if [ "$TARGETARCH" = "amd64" ]; then \
        export CLOUDSDK_PYTHON=/usr/lib/google-cloud-sdk/platform/bundledpythonunix/bin/python3; \
    fi && \
    gcloud --version && \
    gsutil version -l && \
    bq version && \
    gcloud-crc32c /usr/lib/google-cloud-sdk/bin/gcloud && \
    gcloud config set core/disable_usage_reporting false && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_stable && \
    rm -rf /root/.cache/pip/ && \
    find /usr/lib/google-cloud-sdk -name '*.pyc' -delete && \
    find /usr/lib/google-cloud-sdk -name '*__pycache__*' -exec rm -rf {} \+
VOLUME ["/root/.config"]

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Set the entrypoint to the preprocessing script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
