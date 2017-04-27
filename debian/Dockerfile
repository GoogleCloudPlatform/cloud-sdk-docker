FROM debian

RUN apt-get update && apt-get install -y curl python2.7 apt-transport-https lsb-release
RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
ENV HOME /
RUN  apt-get update && apt-get install -y google-cloud-sdk

RUN gcloud config set core/disable_usage_reporting true
RUN gcloud config set component_manager/disable_update_check true
VOLUME ["/.config"]