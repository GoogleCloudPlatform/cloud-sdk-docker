
# Google Cloud SDK Docker


This is Docker image for the [Google Cloud SDK](https://cloud.google.com/sdk/).

Image is debian-based and includes default command line tools and all [components](https://cloud.google.com/sdk/downloads#apt-get) for the SDK.
*  gcloud:  Default set of gcloud commands
*  gsutil:  Cloud Storage Command Line Tool
*  bq: BigQuery Command Line Tool

## Supported tags and respective Dockerfile links

* ```google/cloud-sdk:latest```, ```google/cloud-sdk:VERSION```: (large image with additional components pre-installed, Debian-based)
* ```google/cloud-sdk:slim```,  ```google/cloud-sdk:VERSION-slim```: (smaller image with no components pre-installed, Debian-based)
* ```google/cloud-sdk:alpine```,  ```google/cloud-sdk:VERSION-alpine```: (smaller image with no components pre-installed, Alpine-based)

## Usage

To use this image, pull from [Docker Hub](https://hub.docker.com/r/google/cloud-sdk/), run the following command:


```
docker pull google/cloud-sdk:latest
```

verify the install
```bash
docker run -ti  google/cloud-sdk:latest gcloud version
Google Cloud SDK 159.0.0
```

or specify a version number:

```bash
docker run -ti google/cloud-sdk:155.0.0 gcloud version
```

Then authenticate by running:

```
docker run -ti --name gcloud-config google/cloud-sdk gcloud auth login
```

Once authentication succeeds, credentials are preserved in the volume of _gcloud-config_ container. 
To list compute instances using these credentials, use the configured volume:
```
docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud compute instances list --project your_project
NAME        ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP      STATUS
instance-1  us-central1-a  n1-standard-1               10.240.0.2   8.34.219.29      RUNNING
```

> :warning: **Warning**:  the volume gcloud-config now has your credentials/JSON key file embedded in it; carefully control access to it.

### Installing additional components

By default, all gcloud components are installed on the default image:  [https://cloud.google.com/sdk/downloads#apt-get](https://cloud.google.com/sdk/downloads#apt-get)

The google/cloud-sdk:slim and google/cloud-sdk:alpine images do not contain additional components pre-installed. 
You can extend these images by following the instructions below:


*Debian*

```
cd debian_slim/
docker build --build-arg CLOUD_SDK_VERSION=159.0.0 --build-arg INSTALL_COMPONENTS="google-cloud-sdk-datastore-emulator" -t my-cloud-sdk-docker:slim .
```

*Alpine*

To install additional components for those images, you need to extend the default.  For example, to generate an image that includes kubectl and app-engine-java:

```Dockerfile
FROM google/cloud-sdk:alpine
RUN apk --update add openjdk7-jre
RUN gcloud components install app-engine-java kubectl
```
then with that Dockerfile

```
docker build  -t my-cloud-sdk-docker:alpine .
```

### Google App Engine base

The original image in this repository was based off of 

> FROM gcr.io/google_appengine/base

The full Dockerfile for that can be found [here](google_appengine_base/Dockerfile) for archival as well as in image tag google/cloud-sdk-docker:legacy