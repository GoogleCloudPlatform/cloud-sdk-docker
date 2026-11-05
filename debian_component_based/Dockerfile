FROM debian:trixie-slim
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH=/google-cloud-sdk/bin:$PATH
RUN groupadd -r -g 1000 cloudsdk && \
    useradd -r -u 1000 -m -s /bin/bash -g cloudsdk cloudsdk
RUN apt-get update -qqy && apt-get dist-upgrade -qqy && apt-get install -qqy --no-install-recommends \
        ca-certificates \
        curl \
        media-types \
        lsb-release \
        openssh-client \
        git \
        openjdk-25-jre-headless && \
    rm -rf /var/lib/apt/lists/*
RUN if [ `uname -m` = 'x86_64' ]; then ARCH="x86_64"; else ARCH="arm"; fi && \
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    tar xzf google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    rm google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz
# nomos is not available on ARM right now.
RUN ADDITIONAL_COMPONENTS="app-engine-java app-engine-python alpha beta pubsub-emulator cloud-datastore-emulator app-engine-go bigtable cbt app-engine-python-extras kubectl gke-gcloud-auth-plugin local-extract anthos-auth" && \
    if [ `uname -m` = 'x86_64' ]; then ADDITIONAL_COMPONENTS="${ADDITIONAL_COMPONENTS} nomos"; fi && \
    /google-cloud-sdk/install.sh --bash-completion=false --path-update=true --usage-reporting=false \
	--additional-components ${ADDITIONAL_COMPONENTS} && \
	GCLOUD_PYTHON="$(gcloud info --format='value(basic.python_location)')" && \
	echo "gcloud uses Python at $GCLOUD_PYTHON" && \
	test "$GCLOUD_PYTHON" = /google-cloud-sdk/platform/bundledpythonunix/bin/python3 && \
	! command -v python3 && \
	gsutil version -l | grep -q "compiled crcmod: True" && \
	rm -rf /google-cloud-sdk/.install/.backup
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config", "/root/.kube"]
RUN gcloud config set metrics/environment docker_image_debian_component_based
