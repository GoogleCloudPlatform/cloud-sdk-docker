FROM docker:27.3.1 as static-docker-source

FROM alpine:3.20
ARG CLOUD_SDK_VERSION
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION
ENV PATH /google-cloud-sdk/bin:$PATH
COPY --from=static-docker-source /usr/local/bin/docker /usr/local/bin/docker
COPY --from=static-docker-source /usr/local/libexec/docker/cli-plugins/docker-buildx /usr/local/libexec/docker/cli-plugins/docker-buildx
RUN addgroup -g 1000 -S cloudsdk && \
    adduser -u 1000 -S cloudsdk -G cloudsdk
RUN if [ `uname -m` = 'x86_64' ]; then echo -n "x86_64" > /tmp/arch; else echo -n "arm" > /tmp/arch; fi;
# install python 3.11
RUN apk --no-cache upgrade && apk --no-cache add \
        curl \
        openssl-dev \
        zlib-dev \
        gcc \
        g++ \
        make \
        sqlite-dev \ 
        readline-dev \
	libffi-dev \
    && curl -O https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz \
    && tar -xzf Python-3.11.9.tgz \
    && cd Python-3.11.9 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    # && python3 --version \    
    && python3.11 --version \
    && ln -sf /usr/local/bin/python3.11 /usr/bin/python3 \
    && rm -rf Python-3.11.9 \
    && rm -rf Python-3.11.9.tgz 
RUN python3 --version && \
    python3 -m ensurepip --upgrade && \
    python3 -m pip install crcmod && \
    # apk add --no-cache musl-dev rust cargo && \
    python3 -m pip install pyOpenSSL && \
    python3 -m pip install cryptography
RUN export CLOUDSDK_PYTHON=/usr/local/bin/python3.11
RUN ARCH=`cat /tmp/arch` && apk --no-cache upgrade && apk --no-cache add \
        bash \
        libc6-compat \
        openssh-client \
        git \
    && curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    tar xzf google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    rm google-cloud-cli-${CLOUD_SDK_VERSION}-linux-${ARCH}.tar.gz && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment docker_image_alpine && \
    gcloud --version && \
    python3 --version 
    #python3.12 --version 	
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config"]

