# FROM marketplace.gcr.io/google/debian12:latest
FROM debian:trixie

ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk

RUN apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy \
        curl \
        python3-dev \
        python3-crcmod \
        apt-transport-https \
        lsb-release \
        openssh-client \
        git \
	gcc \
	python3-pip \
        gnupg

    # export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
RUN export CLOUD_SDK_REPO="cloud-sdk-trixie" && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg  | gpg --dearmor -o /etc/apt/keyrings/google-cloud-cli.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/google-cloud-cli.gpg] https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" > /etc/apt/sources.list.d/google-cloud-sdk.list 
RUN apt-get update && \
    apt-get install -y google-cloud-cli=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-app-engine-python=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-app-engine-python-extras=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-app-engine-java=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-app-engine-go=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-datastore-emulator=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-pubsub-emulator=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-bigtable-emulator=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-firestore-emulator=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-spanner-emulator=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-cbt=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-kpt=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-local-extract=${CLOUD_SDK_VERSION}-0 \
        google-cloud-cli-gke-gcloud-auth-plugin=${CLOUD_SDK_VERSION}-0 \
        kubectl
RUN gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_latest && \
    gcloud --version 
    kubectl version --client
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config", "/root/.kube"]
