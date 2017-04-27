FROM alpine
RUN apk add --update curl python bash &&  rm -rf /var/cache/apk/*
ENV HOME /
#RUN curl https://sdk.cloud.google.com | bash

ARG CLOUD_SDK_VERSION=152.0.0
ARG SHA256SUM=8bfae5fe02005bd6613184d9331debe33beb6757d8fa8b1b2fd38b89a8b5659b

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz
RUN echo "${SHA256SUM}  google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" > google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz.sha256
RUN sha256sum -c google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz.sha256
RUN tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz 

ENV PATH /google-cloud-sdk/bin:$PATH
RUN gcloud config set core/disable_usage_reporting true
RUN gcloud config set component_manager/disable_update_check true
VOLUME ["/.config"]