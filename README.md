The Google Cloud CLI Docker image lets you pull a specific version of gcloud CLI as a Docker image from [Artifact Registry](https://cloud.google.com/artifact-registry) and quickly execute Google Cloud CLI commands in an isolated, correctly configured container. 

You can refer to the image's [documentation page](https://cloud.google.com/sdk/docs/downloads-docker) for complete details.

# Google Cloud CLI Docker

The Google Cloud CLI Docker image is the gcloud CLI installed on top of a Debian or Alpine image. The Google Cloud CLI Docker Images enable the usage of gcloud as well as its bundled components without having to manually install gcloud in your local machine.

## What's new / Important updates

***April 07, 2024***

> [!IMPORTANT]  
> <p> To enhance security, Google Cloud CLI Docker images (<code>:latest</code>,
> <code>:alpine</code>, <code>:slim</code>, <code>:emulators</code>,
> <code>:debian_component_based</code>) will undergo a gradual
> reduction of non-essential, non-Google dependencies. Specifically, starting with
> the gcloud version 519.0.0 (scheduled for release on April 22,
> 2025), the <code>docker-buildx</code> dependency will be removed from the
> <code>:alpine</code> and <code>:debian_component_based</code> images.</p>
>
> <p>If your workflows rely on <code>docker-buildx</code>
> within these image types, you will need to pin your workflow to
> gcloud version 518.0.0 or earlier. For continued use of
> <code>docker-buildx</code> with the latest gcloud versions,
> build and host your own Docker image using a custom Dockerfile.
> Here are some examples:
> <a href="https://cloud.devsite.corp.google.com/sdk/docs/dockerfile_example">Dockerfile Examples</a>.</p>
> </aside>


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

