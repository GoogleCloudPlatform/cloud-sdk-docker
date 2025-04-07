FROM marketplace.gcr.io/google/debian12:latest AS bootstrap

RUN apt-get update && \
    apt-get install --no-install-recommends -y --allow-change-held-packages \
        gnupg curl ca-certificates apt-utils && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo 'deb [trusted=yes] http://packages.cloud.google.com/apt apt-transport-artifact-registry-stable main' | tee -a /etc/apt/sources.list.d/artifact-registry.list

RUN apt-get update && apt-get install apt-transport-artifact-registry

FROM docker:28.0.4 as static-docker-source

FROM marketplace.gcr.io/google/debian12:latest
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
COPY --from=static-docker-source /usr/local/bin/docker /usr/local/bin/docker
COPY --from=static-docker-source /usr/local/libexec/docker/cli-plugins/docker-buildx /usr/local/libexec/docker/cli-plugins/docker-buildx
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk
# ca-certificates is required for https
RUN apt-get update && \
    apt-get install --no-install-recommends -y --allow-change-held-packages \
        ca-certificates

# Copy only the ar+https
COPY --from=bootstrap "/usr/lib/apt/methods/ar+https" "/usr/lib/apt/methods/ar+https"
# Copy the apache notice type license for OSPO
COPY --from=bootstrap "/usr/share/doc/apt-transport-artifact-registry" "/usr/share/doc/apt-transport-artifact-registry"

# Remove all other apt sources, silence errors if file doesn't exist
RUN rm -f /etc/apt/sources.list.d/* /etc/apt/sources.list

# If GOOGLE_APPLICATION_CREDENTIALS is passed in docker build command use it, if not leave it unset to support GCE Metadata in CI builds
ARG GOOGLE_APPLICATION_CREDENTIALS

# Use a secret mount to access your long lived credentials, without the risk of leaking them in any of the docker layers
# Make sure the distribution is correct; in this case, it is trying to access Debian Bookworm repository
RUN --mount=type=secret,id=credentials \
    echo 'deb [trusted=yes] ar+https://us-apt.pkg.dev/remote/artifact-foundry-prod/debian-3p-remote-bookworm bookworm main' | \
    tee -a  /etc/apt/sources.list.d/artifact-registry.list && \
    apt-get update
# RUN echo 'deb ar+https://us-apt.pkg.dev/remote/artifact-foundry-prod/debian-3p-remote-bookworm bookworm main' | \
#    tee -a  /etc/apt/sources.list.d/artifact-registry.list
RUN --mount=type=secret,id=credentials \ 
    apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy \
        curl \
        python3-dev \
        python3-crcmod \
	python3-pip \
        apt-transport-https \
        lsb-release \
        openssh-client \
        git \
        make \
	gcc \
        gnupg && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb [trusted=yes] https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    # --mount=type=secret,id=credentials \
    apt-get update && \
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
        kubectl && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_latest && \
    gcloud --version && \
    docker --version && kubectl version --client
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config", "/root/.kube"]
