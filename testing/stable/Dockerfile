FROM marketplace.gcr.io/google/debian12:latest as build_image

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
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-cloud-cli=${CLOUD_SDK_VERSION}-0 $INSTALL_COMPONENTS &&\
    rm -rf /root/.cache/pip/ && \
    find / -name '*.pyc' -delete && \
    find / -name '*__pycache__*' -delete
FROM marketplace.gcr.io/google/debian12:latest as runtime_image
COPY --from=build_image /usr/lib/google-cloud-sdk /usr/lib/google-cloud-sdk

ENV PATH=$PATH:/usr/lib/google-cloud-sdk/bin
# Create a non-root user
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk
RUN if [ `uname -m` = 'x86_64' ]; then echo -n "x86_64" > /tmp/arch; else echo -n "arm" > /tmp/arch && \
    apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy \
        python3-dev \
        python3-crcmod; fi;
RUN gcloud --version && \
    gsutil version && \
    bq version && \
    gcloud-crc32c /usr/bin/gcloud && \
    gcloud config set core/disable_usage_reporting false && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_stable && \
    rm -rf /root/.cache/pip/ && \
    find / -name '*.pyc' -delete && \
    find / -name '*__pycache__*' -exec rm -r {} \+
VOLUME ["/root/.config"]

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Set the entrypoint to the preprocessing script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
