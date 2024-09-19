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
    && curl -O https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz \
    && tar -xzf Python-3.11.9.tgz \
    && cd Python-3.11.9	\
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    # && python3 --version \	
    && python3.11 --version \
    && which python3.11 \
    && rm -rf Python-3.11.9 \
    && rm -rf Python-3.11.9.tgz

RUN apk --no-cache upgrade && apk --no-cache del \
	openssl-dev \
	zlib-dev \
	gcc \
	g++ \
	make \
    && apk cache clean 
RUN ARCH=`cat /tmp/arch` && apk --no-cache upgrade && apk --no-cache add \
        py3-crcmod \
        py3-openssl \
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
    gcloud --version
RUN git config --system credential.'https://source.developers.google.com'.helper gcloud.sh
VOLUME ["/root/.config"]

