# Google Cloud SDK Docker

This is Docker image for the [Google Cloud SDK](https://cloud.google.com/sdk/).

The `:latest` tag of this image is Debian-based and includes default command
line tools of Google Cloud SDK (`gcloud`, `gsutil`, `bq`) as well as all
[additional components](https://cloud.google.com/sdk/downloads#apt-get).

## Supported tags

* `google/cloud-sdk:latest`, `google/cloud-sdk:VERSION`: (large image with
  additional components pre-installed, Debian-based)
* `google/cloud-sdk:slim`,  `google/cloud-sdk:VERSION-slim`: (smaller image with
  no components pre-installed, Debian-based)
* `google/cloud-sdk:alpine`,  `google/cloud-sdk:VERSION-alpine`: (smallest image
  with no additional components installed, Alpine-based)

&rarr; Check out [Docker Hub](https://hub.docker.com/r/google/cloud-sdk/tags/) for available tags.

[![Docker Pulls](https://img.shields.io/docker/pulls/google/cloud-sdk.svg)]()
[![Docker Build Status](https://img.shields.io/docker/build/google/cloud-sdk.svg)]()
[![Docker Automated buil](https://img.shields.io/docker/automated/google/cloud-sdk.svg)]()

## Usage

To use this image, pull from [Docker Hub](https://hub.docker.com/r/google/cloud-sdk/), run the following command:


```
docker pull google/cloud-sdk:latest
```

Verify the install

```bash
docker run -ti  google/cloud-sdk:latest gcloud version
Google Cloud SDK 159.0.0
```

or use a particular version number:

```bash
docker run -ti google/cloud-sdk:160.0.0 gcloud version
```

Then, authenticate by running:

```
docker run -ti --name gcloud-config google/cloud-sdk gcloud auth login
```

Once you authenticate successfully, credentials are preserved in the volume of
the `gcloud-config` container.

To list compute instances using these credentials, run the container with
`--volumes-from`:

```
docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud compute instances list --project your_project
NAME        ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP      STATUS
instance-1  us-central1-a  n1-standard-1               10.240.0.2   8.34.219.29      RUNNING
```

> :warning: **Warning:** The `gcloud-config` container now has a volume
> containing your Google Cloud credentials. Do not use `gcloud-config` volume in
> other containers.

### Installing additional components

By default, [all gcloud components
are](https://cloud.google.com/sdk/downloads#apt-get) installed on the default
images (`google/cloud-sdk:latest` and `google/cloud-sdk:VERSION`).

The `google/cloud-sdk:slim` and `google/cloud-sdk:alpine` images do not contain
additional components pre-installed. You can extend these images by following
the instructions below:

#### Debian-based images

```
cd debian_slim/
docker build --build-arg CLOUD_SDK_VERSION=159.0.0 \
    --build-arg INSTALL_COMPONENTS="google-cloud-sdk-datastore-emulator" \
    -t my-cloud-sdk-docker:slim .
```

#### Alpine-based images

To install additional components for Alpine-based images, create a Dockerfile
that uses the gcloud image as the base image. For example, to add `kubectl` and
`app-engine-java` components:

```Dockerfile
FROM google/cloud-sdk:alpine
RUN apk --update add openjdk7-jre
RUN gcloud components install app-engine-java kubectl
```

and run:

```
docker build  -t my-cloud-sdk-docker:alpine .
```

Note that in this case, you have to install dependencies of additional
components manually.

### Installing different version of gcloud sdk:
```
docker build -t my-cloud-sdk-docker:alpine --build-arg CLOUD_SDK_VERSION=<release_number> .
```

### Legacy image (Google App Engine based)

The original image in this repository was based off of 

> FROM gcr.io/google_appengine/base

The full Dockerfile for that can be found
[here](google_appengine_base/Dockerfile) for archival as well as in image tag
`google/cloud-sdk-docker:legacy`
