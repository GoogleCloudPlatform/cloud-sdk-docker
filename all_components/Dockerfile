ARG FINAL_STAGE=prod
FROM marketplace.gcr.io/google/debian12:latest AS prod
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH /google-cloud-sdk/bin:$PATH
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk
RUN echo 'deb http://deb.debian.org/debian/ sid main' >> /etc/apt/sources.list && \
    apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy \
        curl \
        gcc \
        python3-dev \
        python3-pip \
        python3-crcmod \
        apt-transport-https \
        lsb-release \
        openssh-client \
        git \
        make \
        gnupg && \
    apt-get -y -t sid install openjdk-21-jre-headless
RUN if [ `uname -m` = 'x86_64' ]; then echo -n "x86_64" > /tmp/arch; else echo -n "arm" > /tmp/arch; fi; \
    ARCH=`cat /tmp/arch` && \
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
    echo -n "anthoscli app-engine-java app-engine-python alpha beta pubsub-emulator cloud-datastore-emulator app-engine-go bigtable cbt app-engine-python-extras kubectl gke-gcloud-auth-plugin kustomize minikube skaffold kpt local-extract cloud-sql-proxy docker-credential-gcr package-go-module cloud-firestore-emulator cloud-run-proxy log-streaming managed-flink-client terraform-tools config-connector enterprise-certificate-proxy istioctl kubectl-oidc pkg" > /tmp/additional_components && \
    if [ `uname -m` = 'x86_64' ]; then echo -n " nomos anthos-auth cloud-spanner-emulator spanner-migration-tool" >> /tmp/additional_components; fi && \
    /google-cloud-sdk/install.sh --bash-completion=false --path-update=true --usage-reporting=false --additional-components `cat /tmp/additional_components` && \
    rm -rf /google-cloud-sdk/.install/.backup
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config", "/root/.kube"]

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
