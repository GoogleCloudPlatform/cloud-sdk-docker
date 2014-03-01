cloud-sdk-docker-image
======================

Source for [google/cloud-sdk](https://index.docker.io/u/google/cloud-sdk/): a [docker](https://docker.io) image with all the components and dependencies of the [Google Cloud SDK](https://developers.google.com/cloud/sdk/) installed.

## Usage

```
# get the cloud sdk image
$ docker pull google/cloud-sdk
# auth & save the credentials in gcloud-config volumes
$ docker run -t -i -name gcloud-config google/cloud-sdk gcloud auth login
Go to the following link in your browser: ...
Enter verification code: ...
Enter your Google Cloud project ID (or leave blank to not set): ...
# re-use the credentials from gcloud-config volumes & run sdk command
$ docker run -t -i --volumes-from gcloud-config google/cloud-sdk gcutil listinstances
```
