# Google Cloud SDK Docker

This is Docker image for the [Google Cloud SDK](https://cloud.google.com/sdk/).

The `:latest` tag of this image is Debian-based and includes default command
line tools of Google Cloud SDK (`gcloud`, `gsutil`, `bq`) as well as all
[additional components](https://cloud.google.com/sdk/downloads#apt-get).

## Repositories
The Google Cloud SDK Docker Image is hosted on both [Container Registry](https://gcr.io/google.com/cloudsdktool/cloud-sdk) and [Docker Hub](https://hub.docker.com/r/google/cloud-sdk/).

The full repository name for Container Registry is `gcr.io/google.com/cloudsdktool/cloud-sdk`.

The full repository name for Docker Hub is `google/cloud-sdk`.

## Supported tags

* `:latest`, `:VERSION`: (large image with
  additional components pre-installed, Debian-based)
* `:slim`,  `:VERSION-slim`: (smaller image with
  no components pre-installed, Debian-based)
* `:alpine`,  `:VERSION-alpine`: (smallest image
  with no additional components installed, Alpine-based)
* `:debian_component_based`, `:VERSION`: (Similar to
  :latest but component installer based)

&rarr; Check out [Container Registry](https://gcr.io/google.com/cloudsdktool/cloud-sdk) for available tags.

[![Docker Pulls](https://img.shields.io/docker/pulls/google/cloud-sdk.svg)]()
[![Docker Build Status](https://img.shields.io/docker/build/google/cloud-sdk.svg)]()
[![Docker Automated buil](https://img.shields.io/docker/automated/google/cloud-sdk.svg)]()

## Usage

To use this image, pull from [Container Registry](https://gcr.io/google.com/cloudsdktool/cloud-sdk) and then run the following command:

```
docker pull gcr.io/google.com/cloudsdktool/cloud-sdk:latest
```

(Note: To pull from Docker Hub, replace all instances of `gcr.io/google.com/cloudsdktool/cloud-sdk` with `google/cloud-sdk`.)



Verify the install

```bash
docker run gcr.io/google.com/cloudsdktool/cloud-sdk:latest gcloud version
Google Cloud SDK 159.0.0
```

or use a particular version number:

```bash
docker run gcr.io/google.com/cloudsdktool/cloud-sdk:260.0.0 gcloud version
```

You can authenticate `gcloud` with your user credentials by running [`gcloud auth login`](https://cloud.google.com/sdk/gcloud/reference/auth/login):

```
docker run -ti --name gcloud-config gcr.io/google.com/cloudsdktool/cloud-sdk gcloud auth login
```

If you need to authenticate any program that uses the Google Cloud APIs, you need to pass the `--update-adc` option:

```
docker run -ti --name gcloud-config gcr.io/google.com/cloudsdktool/cloud-sdk gcloud auth login --update-adc
```

Once you authenticate successfully, credentials are preserved in the volume of
the `gcloud-config` container.

To list compute instances using these credentials, run the container with
`--volumes-from`:

```
docker run --rm --volumes-from gcloud-config gcr.io/google.com/cloudsdktool/cloud-sdk gcloud compute instances list --project your_project
NAME        ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP      STATUS
instance-1  us-central1-a  n1-standard-1               10.240.0.2   8.34.219.29      RUNNING
```

> :warning: **Warning:** The `gcloud-config` container now has a volume
> containing your Google Cloud credentials. Do not use `gcloud-config` volume in
> other containers.


Alternatively, you can use `auth/credential_file_override` property to set a path to a mounted service account
and then the config to read that using `CLOUDSDK_CONFIG` environment variable.

for example, `mycloud` configuration below has the `auth/credential_file_override` already set and points towards a certificate file
that will be present within the container as a separate volume mount.

> See [issue#152](https://github.com/GoogleCloudPlatform/cloud-sdk-docker/issues/152#event-1933393673)

```
$ docker run -ti -e CLOUDSDK_CONFIG=/config/mygcloud \
                 -v `pwd`/mygcloud:/config/mygcloud \
                 -v `pwd`:/certs  gcr.io/google.com/cloudsdktool/cloud-sdk:alpine /bin/bash

bash-4.4# gcloud config list
[auth]
credential_file_override = /certs/svc_account.json

bash-4.4# head -10  /certs/svc_account.json
{
  "type": "service_account",
  "project_id": "project_id1",
....

bash-4.4# gcloud projects list
PROJECT_ID           NAME         PROJECT_NUMBER
project_id1          GCPAppID     1071284184432

```
### Components Installed in Each Tag

|                    Component                         | :latest | :alpine | :slim | :debian_component_based |
|:----------------------------------------------------:|:-------:|:-------:|:-----:|:-----------------------:|
| App Engine Go Extensions                             |    x    |         |       |            x            |
| Appctl                                               |         |         |       |                         |
| BigQuery Command Line Tool                           |    x    |    x    |   x   |            x            |
| Cloud Bigtable Command Line Tool                     |    x    |         |       |            x            |
| Cloud Bigtable Emulator                              |    x    |         |       |            x            |
| Cloud Datalab Command Line Tool                      |    x    |         |       |            x            |
| Cloud Datastore Emulator                             |    x    |         |       |            x            |
| Cloud Firestore Emulator                             |    x    |         |       |                         |
| Cloud Pub/Sub Emulator                               |    x    |         |       |            x            |
| Cloud SDK Core Libraries                             |    x    |    x    |   x   |            x            |
| Cloud SQL Proxy                                      |         |         |       |                         |
| Cloud Spanner Emulator                               |    x    |         |       |                         |
| Cloud Storage Command Line Tool                      |    x    |    x    |   x   |            x            |
| Emulator Reverse Proxy                               |         |         |       |                         |
| Google Cloud Build Local Builder                     |         |         |       |                         |
| Google Container Registry's Docker credential helper |         |         |       |                         |
| Kind                                                 |         |         |       |                         |
| Kustomize                                            |         |         |       |                         |
| Minikube                                             |         |         |       |                         |
| Nomos CLI                                            |         |         |       |                         |
| Skaffold                                             |         |         |       |                         |
| anthos-auth                                          |         |         |       |                         |
| gcloud Alpha Commands                                |    x    |         |   x   |            x            |
| gcloud Beta Commands                                 |    x    |         |   x   |            x            |
| gcloud app Java Extensions                           |    x    |         |       |            x            |
| gcloud app Python Extensions                         |    x    |         |       |            x            |
| gcloud app Python Extensions (Extra Libraries)       |    x    |         |       |            x            |
| kpt                                                  |    x    |         |       |                         |
| kubectl                                              |    x    |         |   x   |            x            |


### Installing additional components

#### Debian-based images

```
cd debian_slim/
docker build --build-arg CLOUD_SDK_VERSION=159.0.0 \
    --build-arg INSTALL_COMPONENTS="google-cloud-sdk-datastore-emulator" \
    -t my-cloud-sdk-docker:slim .
```

#### Alpine-based images

To install additional components for Alpine-based images, create a Dockerfile
that uses the `cloud-sdk` image as the base image. For example, to add `kubectl` and
`app-engine-java` components:

```Dockerfile
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:alpine
RUN apk --update add openjdk7-jre
RUN gcloud components install app-engine-java kubectl
```

and run:

```
docker build -t my-cloud-sdk-docker:alpine .
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

### Cloud SDK Release Tracking

You can also follow the Cloud SDK Release schedule here
- [https://groups.google.com/forum/#!forum/google-cloud-sdk-announce](https://groups.google.com/forum/#!forum/google-cloud-sdk-announce)
