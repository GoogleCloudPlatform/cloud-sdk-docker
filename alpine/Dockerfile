ARG FINAL_STAGE=prod
FROM alpine:3.23 AS prod
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH=/google-cloud-sdk/bin:$PATH
RUN addgroup -g 1000 -S cloudsdk && \
    adduser -u 1000 -S cloudsdk -G cloudsdk
# The image ships the musl bundled Python (bundled-python3-alpine component,
# installed to platform/bundledpythonunixmusl) instead of a system Python.
# A system python3 is only installed temporarily to bootstrap
# `gcloud components install` and is removed in the same layer.
RUN if [ `uname -m` = 'x86_64' ]; then echo -n "x86_64" > /tmp/arch; else echo -n "arm" > /tmp/arch; fi; \
    ARCH=`cat /tmp/arch` && apk --no-cache upgrade && apk --no-cache add \
        curl \
        bash \
        libc6-compat \
        openssh-client \
        git \
        gnupg \
    && \
    apk --no-cache add --virtual .bootstrap-python python3 && \
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
    rm -rf /google-cloud-sdk/platform/bundledpythonunix && \
    PYTHONDONTWRITEBYTECODE=1 CLOUDSDK_PYTHON=python3 gcloud components install bundled-python3-alpine --quiet --no-compile-python && \
    apk del .bootstrap-python && \
    ! command -v python3 && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_alpine && \
    gcloud info && \
    /google-cloud-sdk/platform/bundledpythonunixmusl/bin/python3 --version && \
    gsutil version -l && \
    bq version && \
    gcloud-crc32c /google-cloud-sdk/bin/gcloud
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
RUN gcloud auth configure-docker --quiet --include-artifact-registry
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
