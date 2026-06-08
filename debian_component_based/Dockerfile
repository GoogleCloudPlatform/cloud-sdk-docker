ARG TARGETARCH=amd64
FROM debian:trixie-slim AS base-amd64
ENV CLOUDSDK_PYTHON=/google-cloud-sdk/platform/bundledpythonunix/bin/python3

FROM debian:trixie-slim AS base-arm64
RUN apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy \
        python3 \
        python3-crcmod && \
    rm -rf /var/lib/apt/lists/*

FROM debian:trixie-slim AS build_image
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH=/google-cloud-sdk/bin:$PATH
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk
RUN apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy \
        curl \
        gcc \
        python3-dev \
        python3-pip \
        python3-crcmod \
        apt-transport-https \
        lsb-release \
        openssh-client \
        git \
        gnupg \
        openjdk-21-jre-headless
RUN if [ `uname -m` = 'x86_64' ]; then echo -n "x86_64" > /tmp/arch; else echo -n "arm" > /tmp/arch; fi;
RUN ARCH=`cat /tmp/arch` && curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    tar xzf google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    rm google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz
RUN echo -n "app-engine-java app-engine-python alpha beta pubsub-emulator cloud-datastore-emulator app-engine-go bigtable cbt app-engine-python-extras kubectl gke-gcloud-auth-plugin kustomize minikube skaffold kpt local-extract" > /tmp/additional_components
# These components are not available on ARM right now.
RUN if [ `uname -m` = 'x86_64' ]; then echo -n " nomos anthos-auth" >> /tmp/additional_components; fi;
RUN /google-cloud-sdk/install.sh --bash-completion=false --path-update=true --usage-reporting=false \
	--additional-components `cat /tmp/additional_components` && rm -rf /google-cloud-sdk/.install/.backup

ARG TARGETARCH
FROM base-${TARGETARCH} AS runtime_image
ARG TARGETARCH
COPY --from=build_image /google-cloud-sdk /google-cloud-sdk
RUN if [ "$TARGETARCH" = "amd64" ]; then \
        ln -sf /google-cloud-sdk/platform/bundledpythonunix/bin/python3 /usr/bin/python3; \
    fi && \
    ln -sf /usr/bin/python3 /usr/bin/python
ENV PATH=/google-cloud-sdk/bin:$PATH
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk

RUN apt-get update -qqy && apt-get install -qqy \
        curl \
        apt-transport-https \
        lsb-release \
        openssh-client \
        git \
        gnupg \
        openjdk-21-jre-headless && \
    rm -rf /var/lib/apt/lists/*

RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config", "/root/.kube"]
RUN gcloud config set metrics/environment docker_image_debian_component_based

