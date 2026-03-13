# debian12 is used instead of alpine because the cloud bigtable emulator requires glibc.
ARG FINAL_STAGE=prod
FROM marketplace.gcr.io/google/debian12:latest AS prod

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
    apt-get update && \
    apt-get -qqy upgrade && \
    apt-get -y install \
        curl \
        python3 \
        python3-crcmod \
        bash && \
    echo 'deb http://deb.debian.org/debian/ trixie main' >> /etc/apt/sources.list && \
    apt-get update && apt-get -qqy upgrade && \
    apt-get -y -t trixie install openjdk-21-jre-headless && \
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    tar xzf google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    rm google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_emulator && \
    gcloud components install beta `cat /tmp/additional_components` && \
    rm -rf /google-cloud-sdk/.install/.backup/ && \
    find /google-cloud-sdk/ -name "__pycache__" -type d  | xargs -n 1 rm -rf && \
    rm -rf /var/lib/apt/lists

FROM prod AS test
ARG INSTALL_COMPONENTS_TEST=false
COPY release/ /tmp/cloud-sdk-release
RUN if [ "$INSTALL_COMPONENTS_TEST" = "true" ]; then \
        ARCH=`cat /tmp/arch` && \
        cp "/tmp/cloud-sdk-release/linux_${ARCH}_components-2.json" "/tmp/cloud-sdk-release/components-2.json" && \
        cp "/tmp/cloud-sdk-release/linux_${ARCH}_components-vHEAD.json" "/tmp/cloud-sdk-release/components-vHEAD.json" && \
        export CLOUDSDK_COMPONENT_MANAGER_SNAPSHOT_URL="file:///tmp/cloud-sdk-release/components-2.json,file:///tmp/cloud-sdk-release/components-2-TESTING.json" && \
        /google-cloud-sdk/install.sh --bash-completion=false --path-update=true --usage-reporting=false && \
        gcloud components update && \
        gcloud components install TESTING; \
    fi

FROM ${FINAL_STAGE}
