ARG FINAL_STAGE=prod
FROM alpine:3.20 AS prod
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH /google-cloud-sdk/bin:$PATH
RUN addgroup -g 1000 -S cloudsdk && \
    adduser -u 1000 -S cloudsdk -G cloudsdk
RUN if [ `uname -m` = 'x86_64' ]; then echo -n "x86_64" > /tmp/arch; else echo -n "arm" > /tmp/arch; fi; \
    ARCH=`cat /tmp/arch` && apk --no-cache upgrade && apk --no-cache add \
        curl \
        python3 \
        py3-crcmod \
        py3-openssl \
        bash \
        libc6-compat \
        openssh-client \
        git \
        gnupg \
    && \
    if [ -z "$CLOUD_SDK_VERSION" ]; then \
        SDK_URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-${ARCH}.tar.gz"; \
        SDK_TAR="google-cloud-cli-linux-${ARCH}.tar.gz"; \
    else \
        SDK_URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz"; \
        SDK_TAR="google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz"; \
    fi && \
    curl -O "${SDK_URL}" && \
    tar xzf "${SDK_TAR}" && \
    rm "${SDK_TAR}" && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_alpine && \
    gcloud --version && \
    gsutil version -l && \
    bq version && \
    gcloud-crc32c /google-cloud-sdk/bin/gcloud
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config"]

FROM prod AS test
ARG INSTALL_COMPONENTS_TEST=false
COPY release/ /tmp/cloud-sdk-release
RUN if [ "$INSTALL_COMPONENTS_TEST" = "true" ]; then \
        ARCH=`cat /tmp/arch` && \
        cp "/tmp/cloud-sdk-release/linux_${ARCH}_components-2.json" "/tmp/cloud-sdk-release/components-2.json" && \
        cp "/tmp/cloud-sdk-release/linux_${ARCH}_components-vHEAD.json" "/tmp/cloud-sdk-release/components-vHEAD.json" && \
        export CLOUDSDK_COMPONENT_MANAGER_SNAPSHOT_URL="file:///tmp/cloud-sdk-release/components-2.json,file:///tmp/cloud-sdk-release/components-2-TESTING.json" && \
        gcloud components update && \
        gcloud components install TESTING; \
    fi

FROM ${FINAL_STAGE}
