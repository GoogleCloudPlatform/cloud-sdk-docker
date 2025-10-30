FROM alpine:3.20
ARG CLOUD_SDK_VERSION
ARG USE_GCLOUD_HEAD=false
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH /google-cloud-sdk/bin:$PATH
RUN addgroup -g 1000 -S cloudsdk && \
    adduser -u 1000 -S cloudsdk -G cloudsdk
RUN if [ `uname -m` = 'x86_64' ]; then echo -n "x86_64" > /tmp/arch; else echo -n "arm" > /tmp/arch; fi;
RUN ARCH=`cat /tmp/arch` && apk --no-cache upgrade && apk --no-cache add \
        curl \
        python3 \
        py3-crcmod \
        py3-openssl \
        bash \
        libc6-compat \
        openssh-client \
        git \
        gnupg \
    && if [ "$USE_GCLOUD_HEAD" = "true" ]; then \
        echo "Installing gcloud from HEAD artifacts..." && \
        tar xzf cloud-sdk-release/google-cloud-sdk.tar.gz && \
        rm -rf cloud-sdk-release; \
    else \
        echo "Installing gcloud version ${CLOUD_SDK_VERSION} from public URL..." && \
        curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
        tar xzf google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
        rm google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz; \
    fi && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_alpine && \
    if [ "$USE_GCLOUD_HEAD" = "true" ]; then \
        /google-cloud-sdk/bin/gcloud components install TESTING -q; \
    fi && \
    gcloud --version && \
    gsutil version -l && \
    bq version && \
    gcloud-crc32c /google-cloud-sdk/bin/gcloud
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config"]
