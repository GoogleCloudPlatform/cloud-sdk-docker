FROM docker:26.1.3 as static-docker-source

FROM marketplace.gcr.io/google/debian12:latest as build_image
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
COPY --from=static-docker-source /usr/local/bin/docker /usr/local/bin/docker
COPY --from=static-docker-source /usr/local/libexec/docker/cli-plugins/docker-buildx /usr/local/libexec/docker/cli-plugins/docker-buildx
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
        make \
        gnupg && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y google-cloud-cli=${CLOUD_SDK_VERSION}-0 &&\
    gcloud --version && \
    docker --version && rm -rf /root/.cache/pip/ && \
    find / -name '*.pyc' -delete && \
    find / -name '*__pycache__*' -delete
RUN apt-get install -qqy \
        gcc \
        python3-pip
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config"]

FROM marketplace.gcr.io/google/debian12:latest as runtime_image
COPY --from=build_image /usr/lib/google-cloud-sdk /usr/lib/google-cloud-sdk
COPY --from=build_image /root/.config /root/.config

ENV PATH=$PATH:/usr/lib/google-cloud-sdk/bin

