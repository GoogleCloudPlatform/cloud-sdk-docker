FROM centos:centos7
RUN  echo $'[google-cloud-sdk]\n\
name=Google Cloud SDK\n\
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el7-x86_64\n\
enabled=1\n\
gpgcheck=1\n\
repo_gpgcheck=1\n\
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg\n\
       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg'\
        >> /etc/yum.repos.d/google-cloud-sdk.repo && \
    yum install -y which gcc python-devel python-setuptools openssh-clients \
      google-cloud-sdk \
      google-cloud-sdk-app-engine-python \
      google-cloud-sdk-app-engine-java \
      google-cloud-sdk-app-engine-go \
      google-cloud-sdk-datalab \
      google-cloud-sdk-datastore-emulator \
      google-cloud-sdk-pubsub-emulator \
      kubectl && \
    easy_install -U pip && \
    pip install -U crcmod Pillow && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image
VOLUME ["/root/.config"]