FROM debian:jessie
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y --no-install-recommends wget unzip python php5-mysql php5-cli op\
enjdk-7-jre-headless
RUN wget https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.zip
RUN unzip google-cloud-sdk.zip
RUN google-cloud-sdk/install.sh --usage-reporting=true --path-update=true --bash-comple\
tion=true --rc-path=/.bashrc --disable-installation-options
RUN yes | /google-cloud-sdk/bin/gcloud components update pkg-go pkg-python pkg-java
CMD /bin/bash
