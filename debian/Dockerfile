FROM debian:jessie
RUN apt-get update && apt-get install -qqy curl python2.7 gcc python-dev python-setuptools apt-transport-https lsb-release  && \
    easy_install -U pip && \
    pip install -U crcmod && \
    export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && apt-get install -y google-cloud-sdk && \
    apt-get -y remove gcc python-dev python-setuptools && \
    rm -rf /var/lib/apt/lists/* && \    
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true
VOLUME ["/root/.config"]