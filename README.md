The Google Cloud CLI Docker image lets you pull a specific version of gcloud CLI as a Docker image from [Artifact Registry](https://cloud.google.com/artifact-registry) and quickly execute Google Cloud CLI commands in an isolated, correctly configured container. 

You can refer to the image's [documentation page](https://cloud.google.com/sdk/docs/downloads-docker) for complete details.

# Google Cloud CLI Docker

The Google Cloud CLI Docker image is the gcloud CLI installed on top of a Debian or Alpine image. The Google Cloud CLI Docker Images enable the usage of gcloud as well as its bundled components without having to manually install gcloud in your local machine.

## Docker image options

There are six Google Cloud Docker images. We recommend that you install
the following stable image:

* `:stable`, `:VERSION-stable`: Default, Smallest (Debian-based) image with a
standard gcloud installation.

If you want to use an Alpine-based image, you can install the following
image:

* `:alpine`, `:VERSION-alpine`: Smaller (Alpine-based) image with no additional
components installed. This image supports linux/arm.

If you want images with additional packages or gcloud components pre-installed,
you can install one of the following options:

* `:emulators`, `:VERSION-emulators`: Smaller (Debian-based) image with emulator
components pre-installed.
* `:latest`, `:VERSION`: Large (Debian-based) image with additional components
pre-installed.
* `:slim`, `:VERSION-slim`: Smaller (Debian-based) image with no components
pre-installed.
* `:debian_component_based`, `:VERSION-debian_component_based`: Large (Debian-based)
image with additional components pre-installed. As opposed to `:latest` which
used deb packages, this image uses the component manager to install components.
This image supports linux/arm.

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

1. Verify the installation by running:

  ```none
  docker run --rm gcr.io/google.com/cloudsdktool/google-cloud-cli:489.0.0-stable gcloud version
  ```

  If you have used the floating `:stable` tag (which always point to the latest
  release), verify the installation by running the following command:

  ```none
  docker run --rm gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud version
  ```

