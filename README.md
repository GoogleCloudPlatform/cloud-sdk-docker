The Google Cloud CLI Docker image lets you pull a specific version of gcloud CLI as a Docker image from [Artifact Registry](https://cloud.google.com/artifact-registry) and quickly execute Google Cloud CLI commands in an isolated, correctly configured container. 

You can refer to the image's [documentation page](https://cloud.google.com/sdk/docs/downloads-docker) for complete details.

# Google Cloud CLI Docker

The Google Cloud CLI Docker image is the gcloud CLI installed on top of a Debian or Alpine image. The Google Cloud CLI Docker Images enable the usage of gcloud as well as its bundled components without having to manually install gcloud in your local machine.

## What's new / Important updates

***Jun 04, 2025***

**`docker` and `make` package removed from the gcloud docker images**

> [!WARNING]  
> We are removing the `docker` and `make` dependencies from all
Google Cloud CLI Docker images to mitigate customers' exposure to vulnerabilities
found in this component and its dependencies according to the [following
timeline](#update_timeline). If your workflows rely on the `docker` or the `make` packages, you will need to
pin to the respective `Pin-To` gcloud version or earlier.
Alternatively, you could build your own docker image and include the
`docker` or the `make` packages using a custom Dockerfile. Here are some examples:
[Dockerfile Examples](https://cloud.google.com/sdk/docs/dockerfile_example).
For any questions or
concerns about the change, reach out to the
[gcloud support team](https://issuetracker.google.com/issues/new?component=187143).
We have previously removed the `docker-buildx` package from the
gcloud CLI docker images. For more information about already
removed packages, see the [announcements on GitHub](https://github.com/GoogleCloudPlatform/cloud-sdk-docker/discussions/categories/announcements?discussions_q=is%3Aopen+category%3AAnnouncements+label%3A3pPackageRemoval).

***May 28, 2025***

**Support for gcloud firestore and datastore emulators with Java 17 or earlier is ending on June 24, 2025**

> [!WARNING]  
> The firestore & datastore emulators will require
Java 21 or later starting with the gcloud release 528.0.0
(June 24, 2025). After this change, the firestore
and datastore emulators will fail to start in environments with Java
versions prior to 21. To fix this, users of the `:latest`, `:emulators` and
`:debian_component_based` images can use their own Dockerfile to upgrade to
Java 21 or later to continue using the latest firestore and
datastore emulators
([examples](https://cloud.google.com/sdk/docs/dockerfile_example#build-your-own-gcloud-docker-image-for-java21)).
Alternatively the users can pin-to gcloud version `527.0.0` or
earlier where the prior java versions were supported. For any questions or
concerns about the change, reach out to the
[gcloud support team](https://issuetracker.google.com/issues/new?component=187143).


### Update Timeline

|  <img width=105/> Date  | Package | Removed in gcloud version | `Pin-to` gcloud version to continue using the package | Package removed from images |
|:----------:|:----------:|:-------------------------------------------:|:--------------------:|:----------:|
| Jul 01, 2025 | `docker` | 529.0.0 | 528.0.0 | `:alpine` and `:debian_component_based` |
| Jul 22, 2025 | `docker` | 531.0.0 | 530.0.0 | `:slim` and `:latest` |
| Aug 05, 2025 | `make` | 533.0.0 | 532.0.0 | `:latest` and `:debian_component_based` |


## Docker image options

There are six Google Cloud CLI Docker images, and all will install the
`gcloud`, `gsutil` and `bq` command-line tools. We recommend that you install
the `:stable` image for a minimal environment. You can also
use the stable image as the base image for your own deployments which gives you
the flexibility of installing only the components and packages that you need in
your image:

* `:stable`, `:VERSION-stable`: Provides a gcloud installation
with `gsutil` and `bq` components. The image is built upon the latest
[Google-Provided](/software-supply-chain-security/docs/base-images#google-provided_base_images)
Debian 12 base image. This image supports both `linux/amd` and `linux/arm`
platforms. To install specific gcloud versions, use
the `:VERSION-stable` tag.

If you want to use an Alpine-based image, you can install the following
image:

* `:alpine`, `:VERSION-alpine`: Similar to stable but built upon the latest
[Alpine 3.20](https://github.com/alpinelinux/docker-alpine/tree/v3.20)
base image. This image supports both `linux/amd` and `linux/arm` platforms. To
install specific gcloud versions, use the `:VERSION-alpine` tag.

If you want images with additional
[components](#components_installed_in_each_tag) or packages pre-installed,
you can install one of the following options:

* `:emulators`, `:VERSION-emulators`: Similar to stable, with the
addition of all the emulator components. The image is build upon the latest
[Google-Provided](/software-supply-chain-security/docs/base-images#google-provided_base_images)
Debian 12 base image and uses component manager to install the components. This
image supports both `linux/amd` and `linux/arm` platforms. To install specific
gcloud versions, use the `:VERSION-emulators`
tag.

* `:latest`, `:VERSION`: Similar to stable, with additional components
(List of components installed in the image are listed
[below](#components_installed_in_each_tag)) pre-installed. The image is build
upon the latest
[Google-Provided](/software-supply-chain-security/docs/base-images#google-provided_base_images)
Debian 12 base image and uses deb packages to install the components. To install
specific gcloud versions, use the `:VERSION`
tag.

* `:slim`, `:VERSION-slim`: Similar to stable but includes the additional
third party packages like `curl`, `python3-crcmod`, `apt-transport-https`,
`lsb-release`, `openssh-client`, `git`, `make`, and `gnupg`. This image is
built upon the latest
[Google-Provided](/software-supply-chain-security/docs/base-images#google-provided_base_images)
Debian 12 base image. This image supports both `linux/amd` and `linux/arm`
platforms. To install specific gcloud versions, use
the `:VERSION-slim` tag.

* `:debian_component_based`, `:VERSION-debian_component_based`: Similar to
stable, with additional components
(List of components installed in the image are listed
[below](#components_installed_in_each_tag)) pre-installed. The image is build
upon the latest
[Google-Provided](/software-supply-chain-security/docs/base-images#google-provided_base_images)
Debian 12 base image and uses component manager to install the components. This
image supports both `linux/amd` and `linux/arm` platforms. To install specific
gcloud versions, use the `:VERSION-debian_component_based` tag.

## Installing a Docker image

The Docker image is hosted on
[Artifact Registry](https://console.cloud.google.com/artifacts/docker/google.com:cloudsdktool/us/gcr.io/google-cloud-cli)
with the following repository name:
`gcr.io/google.com/cloudsdktool/google-cloud-cli`. The images are also available
using the `us.gcr.io`, `eu.gcr.io`, and `asia.gcr.io` repositories.

1. To use the image of the stable Google Cloud CLI release,
  `gcr.io/google.com/cloudsdktool/google-cloud-cli:stable`,
  pull it from [Artifact Registry](https://console.cloud.google.com/artifacts/docker/google.com:cloudsdktool/us/gcr.io/google-cloud-cli)
  by running the following command:

  ```none
  docker pull gcr.io/google.com/cloudsdktool/google-cloud-cli:489.0.0-stable
  ```

2. Verify the installation by running:

  ```none
  docker run --rm gcr.io/google.com/cloudsdktool/google-cloud-cli:489.0.0-stable gcloud version
  ```

  If you have used the floating `:stable` tag (which always point to the latest
  release), verify the installation by running the following command:

  ```none
  docker run --rm gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud version
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

