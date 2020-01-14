FROM docker:17.12.0-ce as static-docker-source

FROM debian:buster
ARG CLOUD_SDK_VERSION=276.0.0
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH /google-cloud-sdk/bin:$PATH
COPY --from=static-docker-source /usr/local/bin/docker /usr/local/bin/docker
RUN apt-get -qqy update && apt-get install -qqy \
        curl \
        gcc \
        python-dev \
        python-pip \
        apt-transport-https \
        lsb-release \
        openssh-client \
        git \
        make \
        gnupg && \
    pip install -U crcmod
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    rm google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz
RUN /google-cloud-sdk/install.sh --bash-completion=false --path-update=true --usage-reporting=false \
	--additional-components app-engine-java app-engine-python alpha beta \
	pubsub-emulator cloud-datastore-emulator app-engine-go bigtable cbt datalab \
	app-engine-python-extras kubectl
VOLUME ["/root/.config", "/root/.kube"]
