cloud-sdk-docker-image
======================

Sources for [`google/cloud-sdk`](https://index.docker.io/u/google/cloud-sdk/) docker image.

## Description

A [Docker](https://docker.io) image bundling all the components and dependencies of the [Google Cloud SDK](https://developers.google.com/cloud/sdk/):

- App Engine SDK for Go
- App Engine SDK for Java
- App Engine SDK for Python and PHP
- Big Query Command Line Tool 
- Cloud DNS Admin Command Line Interface
- Cloud SQL Admin Command Line Interface
- Cloud Storage Command Line Tool 
- Compute Engine Command Line Tool

## Usage

    # get the cloud sdk image
    $ docker pull google/cloud-sdk
    # auth & save the credentials in gcloud-config volumes
    $ docker run -t -i -name gcloud-config google/cloud-sdk gcloud auth login
    Go to the following link in your browser: ...
    Enter verification code: ...
    Enter your Google Cloud project ID (or leave blank to not set): ...
    # re-use the credentials from gcloud-config volumes & run sdk commands
    $ docker run -t -i --volumes-from gcloud-config google/cloud-sdk gcutil listinstances
