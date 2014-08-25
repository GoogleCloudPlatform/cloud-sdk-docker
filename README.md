cloud-sdk-docker
================

## Description

[`google/cloud-sdk`](https://index.docker.io/u/google/cloud-sdk/) is a [Docker](https://docker.io) image bundling all components and dependencies
of the [Google Cloud SDK](https://developers.google.com/cloud/sdk/):

- App Engine SDK for Go
- App Engine SDK for Java
- App Engine SDK for Python and PHP
- Big Query Command Line Tool 
- Cloud DNS Admin Command Line Interface
- Cloud SQL Admin Command Line Interface
- Cloud Storage Command Line Tool 
- Compute Engine Command Line Tool

## Usage

Follow these instructions if you are running docker *outside* of Google
Compute Engine:

    # get the cloud sdk image
    $ docker pull google/cloud-sdk

    # auth & save the credentials in gcloud-config volumes
    $ docker run -t -i --name gcloud-config google/cloud-sdk gcloud auth login
    Go to the following link in your browser: ...
    Enter verification code: ...
    You are now logged in as [...]
    Your current project is [None]. You can change this setting by running:
       $ gcloud config set project <project>
    gcloud config set project ...

    # re-use the credentials from gcloud-config volumes & run sdk commands
    $ docker run -t -i --volumes-from gcloud-config google/cloud-sdk gcutil listinstances
    $ docker run -t -i --volumes-from gcloud-config google/cloud-sdk gsutil ls
    $ docker run -t -i --volumes-from gcloud-config google/cloud-sdk gcloud components list
    $ docker run -t -i --volumes-from gcloud-config google/cloud-sdk gcloud version

If you are using this image from *within* Google Compute Engine with an enabled
Service Account and your instance was created with the necessary scopes, there
is no need to auth or use a config volume:

    # get the cloud sdk image
    $ docker pull google/cloud-sdk

    # just start using the sdk commands
    $ docker run -t -i google/cloud-sdk gcutil listinstances
    $ docker run -t -i google/cloud-sdk gsutil ls
    $ docker run -t -i google/cloud-sdk gcloud components list
    $ docker run -t -i google/cloud-sdk gcloud version
