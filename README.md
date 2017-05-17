
# Google Cloud SDK Docker


This is Docker image for the [Google Cloud SDK](https://cloud.google.com/sdk/).

Image includes default command line tools:
*  gcloud:  Default set of gcloud commands
*  gsutil:  Cloud Storage Command Line Tool
*  bq: BigQuery Command Line Tool

## Supported tags and respective Dockerfile links

- [155.0.0, latest] (Dockerfile)

## Usage

To use the prebuilt **Alpine** based image, pull and run from

```
docker pull google/cloud-sdk:latest
```

```bash
docker run -ti  google/cloud-sdk:latest gcloud version
Google Cloud SDK 155.0.0
bq 2.0.24
core 2017.05.10
gcloud 
gsutil 4.26
```

or via tagged version of the SDK:

```bash
docker run -ti google/cloud-sdk:153.0.0 gcloud version
```

### Installing additional components

If you need to run additional gcloud components, you need to extend the base image:

For example, for appengine-python:
```dockerfile
FROM google/cloud-sdk
RUN gcloud components install app-engine-python
```

or for app-engine-java
```
FROM google/cloud-sdk
RUN apk --update add openjdk7-jre
RUN gcloud components install app-engine-java
WORKDIR /apps
```

### Volume mounts

For a volume mount using credentials:
```
docker run -t -i --name gcloud-config google/cloud-sdk gcloud auth login
```
then
```
docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud compute instances list --project your_project
NAME        ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP      STATUS
instance-1  us-central1-a  n1-standard-1               10.240.0.2   8.34.219.29      RUNNING
```

### Google Appengine base

The original image in this repository was based off of 

> FROM gcr.io/google_appengine/base

The full Dockerfile for that can be found [here](google_appengine_base/Dockerfile) for archival.