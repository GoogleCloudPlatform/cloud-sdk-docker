cloud-sdk-docker-image
======================

Docker image with all the components of the Google Cloud SDK

## Usage

```
$ docker pull google/cloud-sdk
$ mkdir ~/.gcloud # to store you credentials
$ docker run -t -i -v ~/.gcloud:/.config/gcloud google/cloud-sdk /google-cloud-sdk/bin/gcloud auth login
Go to the following link in your browser: ...
Enter verification code: ...
Enter your Google Cloud project ID (or leave blank to not set): ...
$ docker run -t -i -v ~/.gcloud:/.config/gcloud google/cloud-sdk /google-cloud-sdk/bin/gcutil addinstance my-compute-instance --permit_root_ssh
```
