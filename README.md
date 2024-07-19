# Google Cloud CLI Docker

The Google Cloud CLI Docker Images (comprising the `:stable`, `:latest`, `:slim`, `:alpine`, `:emulators`, and `:debian_component_based` images located within this repository) are a set of images enabling the usage of the Google Cloud CLI as well as its bundled components.

The `:stable` tag is Debian-based and includes default command
line tools of Google Cloud CLI (`gcloud`, `gsutil`, `bq`). [Additional components](https://cloud.google.com/sdk/docs/install#deb) can also be installed using the INSTALL_COMPONENTS build argument.

## Repositories
The Google Cloud CLI Docker Image is hosted on [Container Registry](https://gcr.io/google.com/cloudsdktool/google-cloud-cli).

The full repository name for Container Registry is `gcr.io/google.com/cloudsdktool/google-cloud-cli`.

## Supported tags

* `:stable`, `:VERSION-stable`: (default image with the basic version of gcloud without any pre-installed components, Debian-based)
* `:latest`, `:VERSION`: (large image with
  additional components pre-installed, Debian-based)
* `:slim`,  `:VERSION-slim`: (smaller image with
  no components pre-installed, Debian-based)
* `:alpine`,  `:VERSION-alpine`: (smallest image
  with no additional components installed, Alpine-based)
* `:debian_component_based`, `:VERSION-debian_component_based`: (Similar to
  :latest but component installer based)
* `:emulators`, `:VERSION`: (as small as possible with all the emulators)

&rarr; Check out [Container Registry](https://gcr.io/google.com/cloudsdktool/google-cloud-cli) for available tags.

## Usage

To use this image, pull from [Container Registry](https://gcr.io/google.com/cloudsdktool/google-cloud-cli) and then run the following command:

```
docker pull gcr.io/google.com/cloudsdktool/google-cloud-cli:stable
```

Verify the install

```bash
docker run gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud version
Google Cloud CLI 485.0.0
```

or use a particular version number (485.0.0 or greater for `:stable`):

```bash
docker run gcr.io/google.com/cloudsdktool/google-cloud-cli:stable-485.0.0 gcloud version
```

You can authenticate `gcloud` with your user credentials by running [`gcloud auth login`](https://cloud.google.com/sdk/gcloud/reference/auth/login):

```
docker run -ti --name gcloud-config gcr.io/google.com/cloudsdktool/google-cloud-cli gcloud auth login
```

If you need to authenticate any program that uses the Google Cloud APIs, you need to pass the `--update-adc` option:

```
docker run -ti --name gcloud-config gcr.io/google.com/cloudsdktool/google-cloud-cli gcloud auth login --update-adc
```

If you want to use a specific project for future uses, you can set this inside the `gcloud-config` container:

```
docker run -ti --name gcloud-config gcr.io/google.com/cloudsdktool/google-cloud-cli /bin/bash -c 'gcloud auth login && gcloud config set project your-project'
```

Once you authenticate successfully, credentials are preserved in the volume of
the `gcloud-config` container.

To list compute instances using these credentials, run the container with
`--volumes-from`:

```
docker run --rm --volumes-from gcloud-config gcr.io/google.com/cloudsdktool/google-cloud-cli gcloud compute instances list --project your_project
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
                 -v `pwd`:/certs  gcr.io/google.com/cloudsdktool/google-cloud-cli:alpine /bin/bash

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
You can set any Cloud SDK property via an ENV,
[please read](https://cloud.google.com/sdk/docs/properties#setting_properties_using_environment_variables) and [here.](https://cloud.google.com/sdk/gcloud/reference/config)

### Components Installed in Each Tag

|                    Component                         | :latest | :alpine | :slim | :debian_component_based | :emulators |
|:----------------------------------------------------:|:-------:|:-------:|:-----:|:-----------------------:|:----------:|
| App Engine Go Extensions                             |    x    |         |       |            x            |            |
| Appctl                                               |         |         |       |            x            |            |
| Artifact Registry Go Module Package Helper           |         |         |       |                         |            |
| BigQuery Command Line Tool                           |    x    |    x    |   x   |            x            |     x      |
| Bundled Python 3.9                                   |    x    |    x    |   x   |            x            |     x      |
| Cloud Bigtable Command Line Tool                     |    x    |         |       |            x            |            |
| Cloud Bigtable Emulator                              |    x    |         |       |            x            |     x      |
| Cloud Datastore Emulator                             |    x    |         |       |            x            |     x      |
| Cloud Firestore Emulator                             |    x    |         |       |                         |     x      |
| Cloud Pub/Sub Emulator                               |    x    |         |       |            x            |     x      |
| Cloud Run Proxy                                      |         |         |       |                         |            |
| Cloud SQL Proxy                                      |         |         |       |                         |            |
| Cloud Spanner Emulator                               |    x    |         |       |                         |     x      |
| Cloud Spanner Migration Tool                         |         |         |       |                         |            |
| Cloud Storage Command Line Tool                      |    x    |    x    |   x   |            x            |     x      |
| Google Cloud CLI Core Libraries                      |    x    |    x    |   x   |            x            |     x      |
| Google Cloud CRC32C Hash Tool                        |    x    |    x    |   x   |            x            |     x      |
| Google Container Registry's Docker credential helper |         |         |       |                         |            |
| Kustomize                                            |         |         |       |            x            |            |
| Log Streaming                                        |         |         |       |                         |            |
| Minikube                                             |         |         |       |            x            |            |
| Nomos CLI                                            |         |         |       |            x            |            |
| On-Demand Scanning API extraction helper             |    x    |         |       |            x            |            |
| Skaffold                                             |         |         |       |            x            |            |
| Terraform Tools                                      |         |         |       |                         |            |
| anthos-auth                                          |         |         |       |            x            |            |
| config-connector                                     |         |         |       |                         |            |
| gcloud Alpha Commands                                |    x    |         |   x   |            x            |            |
| gcloud Beta Commands                                 |    x    |         |   x   |            x            |     x      |
| gcloud app Java Extensions                           |    x    |         |       |            x            |            |
| gcloud app Python Extensions                         |    x    |         |       |            x            |            |
| gcloud app Python Extensions (Extra Libraries)       |    x    |         |       |            x            |            |
| gke-gcloud-auth-plugin                               |    x    |         |       |            x            |            |
| kpt                                                  |    x    |         |       |            x            |            |
| kubectl                                              |    x    |         |       |            x            |            |
| kubectl-oidc                                         |         |         |       |                         |            |
| pkg                                                  |         |         |       |                         |            |


### Installing additional components

#### Debian-based images

```
cd stable/
docker build --build-arg CLOUD_SDK_VERSION=485.0.0 \
    --build-arg INSTALL_COMPONENTS="google-cloud-cli-datastore-emulator=485.0.0-0" \
    -t my-cloud-sdk-docker:stable .
```

```
cd debian_slim/
docker build --build-arg CLOUD_SDK_VERSION=485.0.0 \
    --build-arg INSTALL_COMPONENTS="google-cloud-cli-datastore-emulator=485.0.0-0" \
    -t my-cloud-sdk-docker:slim .
```

#### Alpine-based images

To install additional components for Alpine-based images, create a Dockerfile
that uses the `cloud-sdk` image as the base image. For example, to add `kubectl` and
`app-engine-java` components:

```Dockerfile
FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:alpine
RUN apk --update add gcompat openjdk8-jre
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

## Support

The Google Cloud CLI Team works to ensure that the images within this repository provide fully functional installs of the Google Cloud CLI. This work includes addressing any bugs or issues that prevent the execution of the `gcloud` command line tool or components installed by default on each image. The team also works to ensure that third party packages necessary for the function of the Google Cloud CLI are using stable release versions, and that base OS images are updated to recent, stable releases in a timely manner. 

For workflows separate from or unrelated to the execution of the Cloud CLI that require additional or different dependencies, the Cloud CLI team recommends creating your own image layer on top of the Cloud CLI Docker Image where you can remove and install dependencies as needed. The Cloud CLI Team will not address issues related to workflows or tools unrelated to the execution of the Google Cloud CLI. Similarly, the team will deny requests for additional packages or tooling unrelated to the intended functioning of the Google Cloud CLI. 

### Identifying Vulnerabilities

If you or your organization have detected vulnerabilities within any of the Cloud CLI Docker Images, please [file a bug.](https://issuetracker.google.com/issues/new?component=187143) Your bug must contain the type of each vulnerability and the **exact location within the image where each is present**. Vulnerabilities within base OS images will not be addressed beyond ensuring the Cloud CLI Docker images are using recent, stable releases of Debian or Alpine Linux.

### Pinning version

Images tagged `:latest`, `:alpine`, `:slim` and `:debian_component_based` use
the most recent version of Google Cloud SDK, which may change its behaviour in
the future. List of components installed by default in each image can also
change between versions. To avoid such changes breaking the tool you are using,
it is not recommended to use these tags in any production tools directly.
Instead use a particular version as listed in [Supported tags](#supported-tags)
and update it periodically.
