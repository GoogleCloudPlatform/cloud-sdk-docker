FROM debian:jessie
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y --no-install-recommends wget unzip python php5-mysql php5-cli php5-cgi openjdk-7-jre-headless openssh-client
RUN wget https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.zip
RUN unzip google-cloud-sdk.zip
RUN google-cloud-sdk/install.sh --usage-reporting=true --path-update=true --bash-completion=true --rc-path=/.bashrc --disable-installation-options
RUN yes | google-cloud-sdk/bin/gcloud components update pkg-go pkg-python pkg-java
RUN mkdir /.ssh
ENV PATH /google-cloud-sdk/bin:$PATH
VOLUME ["/.config"]
CMD bash
