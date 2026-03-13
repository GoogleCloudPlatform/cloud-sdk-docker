# debian12 is used instead of alpine because the cloud bigtable emulator requires glibc.
FROM marketplace.gcr.io/google/debian12:latest

ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH /google-cloud-sdk/bin:$PATH

RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk

RUN echo -n "cloud-datastore-emulator cloud-firestore-emulator pubsub-emulator bigtable" > /tmp/additional_components
RUN if [ `uname -m` = 'x86_64' ]; then echo -n " cloud-spanner-emulator" >> /tmp/additional_components; fi;
RUN cat /tmp/additional_components
RUN if [ `uname -m` = 'x86_64' ]; then echo -n "x86_64" > /tmp/arch; else echo -n "arm" > /tmp/arch; fi;

RUN ARCH=`cat /tmp/arch` && \
    mkdir -p /usr/share/man/man1/ && \
    # Add sid first
    echo 'deb http://deb.debian.org/debian/ sid main' >> /etc/apt/sources.list && \
    apt-get update && \
    # Upgrade everything based on the new sources list
    apt-get -qqy upgrade && \
    # Install all required packages, including openjdk from sid
    apt-get -y install \
        curl \
        python3 \
        python3-crcmod \
        bash \
        openjdk-21-jre-headless && \
    # The -t sid might not even be strictly necessary anymore for openjdk
    # as sid is now the highest priority, but it doesn't hurt.
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    tar xzf google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    rm google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_emulator && \
    gcloud components install beta `cat /tmp/additional_components` && \
    rm -rf /google-cloud-sdk/.install/.backup/ && \
    find /google-cloud-sdk/ -name "__pycache__" -type d  | xargs -n 1 rm -rf && \
    rm -rf /var/lib/apt/lists tmp/*
