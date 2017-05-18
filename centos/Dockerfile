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
    yum install -y google-cloud-sdk which gcc python-devel python-setuptools && \
    easy_install -U pip && \
    pip install -U crcmod && \
    yum remove gcc python-devel python-setuptools && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true
VOLUME ["/root/.config"]