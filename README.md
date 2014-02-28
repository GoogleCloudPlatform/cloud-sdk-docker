cloud-sdk-docker-image
======================

Source for [google/cloud-sdk](https://index.docker.io/u/google/cloud-sdk/): a [docker](https://docker.io) image with all the components and dependencies of the [Google Cloud SDK](https://developers.google.com/cloud/sdk/) installed.

## Usage

```
$ docker pull google/cloud-sdk
$ mkdir ~/.gcloud # to store your credentials
$ docker run -t -i -v ~/.gcloud:/.config/gcloud google/cloud-sdk /google-cloud-sdk/bin/gcloud auth login
Go to the following link in your browser: ...
Enter verification code: ...
Enter your Google Cloud project ID (or leave blank to not set): ...
$ docker run -t -i -v ~/.gcloud:/.config/gcloud google/cloud-sdk /google-cloud-sdk/bin/gcutil addinstance my-compute-instance --permit_root_ssh
```
