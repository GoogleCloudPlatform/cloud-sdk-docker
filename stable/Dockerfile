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
FROM debian:trixie-slim AS runtime_image
COPY --from=build_image /usr/lib/google-cloud-sdk /usr/lib/google-cloud-sdk

ENV PATH=$PATH:/usr/lib/google-cloud-sdk/bin
# Create a non-root user
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk
RUN if [ `uname -m` = 'x86_64' ]; then echo -n "x86_64" > /tmp/arch; else echo -n "arm" > /tmp/arch && \
    apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy \
        python3-dev \
        python3-crcmod; fi;
RUN gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_stable && \
    gcloud info && \
    (if [ `uname -m` != 'x86_64' ]; then python3 --version; fi) && \
    gsutil version -l && \
    bq version && \
    gcloud-crc32c /usr/lib/google-cloud-sdk/bin/gcloud && \
    rm -rf /root/.cache/pip/ && \
    find /usr/lib/google-cloud-sdk -name '*.pyc' -delete && \
    find /usr/lib/google-cloud-sdk -name '*__pycache__*' -exec rm -r {} \+
VOLUME ["/root/.config"]

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Set the entrypoint to the preprocessing script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
