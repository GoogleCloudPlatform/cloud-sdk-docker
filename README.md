The Google Cloud CLI Docker image lets you pull a specific version of gcloud CLI as a Docker image from [Artifact Registry](https://cloud.google.com/artifact-registry) and quickly execute Google Cloud CLI commands in an isolated, correctly configured container. 

You can refer to the image's [documentation page](https://cloud.google.com/sdk/docs/downloads-docker) for complete details.

# Google Cloud CLI Docker

The Google Cloud CLI Docker image is the gcloud CLI installed on top of a Debian or Alpine image. The Google Cloud CLI Docker Images enable the usage of gcloud as well as its bundled components without having to manually install gcloud in your local machine.

## What's new / Important updates

***April 23, 2025***

> [!WARNING]  
> <p> To enhance security, we will be removing the
> <code>docker-buildx</code> dependency from the gcloud Docker images (<code>:latest</code>,
> <code>:alpine</code>, <code>:slim</code>, <code>:emulators</code>,
> <code>:debian_component_based</code>). Starting with
> the gcloud version 519.0.0,
> the <code>docker-buildx</code> dependency has been removed from the
> <code>:alpine</code> and <code>:debian_component_based</code> images.</p>
>
> <p>If your workflows rely on <code>docker-buildx</code>
> within these image types, you will need to pin your workflow to
> gcloud version 518.0.0 or earlier. For continued use of
> <code>docker-buildx</code> with the latest gcloud versions,
> build and host your own Docker image using a custom Dockerfile.
> Here are some examples:
> <a href="https://cloud.google.com/sdk/docs/dockerfile_example">Dockerfile Examples</a>.</p>
> </aside>


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

