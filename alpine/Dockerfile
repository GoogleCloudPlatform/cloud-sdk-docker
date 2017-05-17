FROM alpine:3.5
ARG CLOUD_SDK_VERSION=155.0.0
ARG SHA256SUM=4b64fba9d98b9e48cc7a37ed3b321e50f92e87f9c2b358d183f966dae05216a2
ENV PATH /google-cloud-sdk/bin:$PATH
RUN apk --no-cache add curl python && \
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    echo "${SHA256SUM}  google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" > google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz.sha256 && \
    sha256sum -c google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz.sha256 && \
    tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true
VOLUME ["/root/.config"]