The Google Cloud CLI Docker image lets you pull a specific version of gcloud CLI
as a Docker image from
[Artifact Registry](https://cloud.google.com/artifact-registry) and quickly
execute Google Cloud CLI commands in an isolated, correctly configured
container.

You can refer to the image's
[documentation page](https://cloud.google.com/sdk/docs/downloads-docker) for
complete details.

# Google Cloud CLI Docker

The Google Cloud CLI Docker image is the gcloud CLI installed on top of a Debian
or Alpine image. The Google Cloud CLI Docker Images enable the usage of gcloud
as well as its bundled components without having to manually install gcloud in
your local machine.

## Docker image options

There are six Google Cloud CLI Docker images, and all will install the `gcloud`
and `bq` command-line tools. These images are built with
`--no-install-recommends` to keep them minimal. Users should not rely on
recommended or transient dependencies (such as `make`) being present. If your
workflow requires additional tools, you should install them explicitly.

We recommend that you install the `:stable` image for a minimal environment. You
can also use the stable image as the base image for your own deployments which
gives you the flexibility of installing only the components and packages that
you need in your image:

*   `:stable`, `:VERSION-stable`: Provides a gcloud installation with `bq`
    components. The image is built upon the latest Debian (`trixie-slim`) base
    image. This image supports both `linux/amd` and `linux/arm` platforms. To
    install specific gcloud versions, use the `:VERSION-stable` tag.

If you want to use an Alpine-based image, you can install the following image:

*   `:alpine`, `:VERSION-alpine`: Similar to stable but built upon the latest
    [Alpine 3.23](https://github.com/alpinelinux/docker-alpine/tree/v3.23) base
    image. This image supports both `linux/amd` and `linux/arm` platforms. To
    install specific gcloud versions, use the `:VERSION-alpine` tag.

If you want images with additional components or packages pre-installed, you can
install one of the following options:

*   `:emulators`, `:VERSION-emulators`: Similar to stable, with the addition of
    all the emulator components. The image is built upon the latest Debian
    (`trixie-slim`) base image and uses component manager to install the
    components. This image supports both `linux/amd` and `linux/arm` platforms.
    To install specific gcloud versions, use the `:VERSION-emulators` tag.

*   `:latest`, `:VERSION`: Similar to stable, with additional components
    pre-installed. The image is built upon the latest Debian (`trixie-slim`)
    base image and uses deb packages to install the components. This image
    supports both `linux/amd` and `linux/arm` platforms. To install specific
    gcloud versions, use the `:VERSION` tag.

*   `:slim`, `:VERSION-slim`: Similar to stable but includes additional packages
    like `curl`, `gcc`, `python3-dev`, `python3-pip`, `apt-transport-https`,
    `lsb-release`, `openssh-client`, `git`, and `gnupg`. This image is built
    upon the latest Debian (`trixie-slim`) base image. This image supports both
    `linux/amd` and `linux/arm` platforms. To install specific gcloud versions,
    use the `:VERSION-slim` tag.

*   `:debian_component_based`, `:VERSION-debian_component_based`: Similar to
    stable, with additional components pre-installed. The image is built upon
    the latest Debian (`trixie-slim`) base image and uses component manager to
    install the components. This image supports both `linux/amd` and `linux/arm`
    platforms. To install specific gcloud versions, use the
    `:VERSION-debian_component_based` tag.

## Installing a Docker image

The Docker image is hosted on
[Artifact Registry](https://console.cloud.google.com/artifacts/docker/google.com:cloudsdktool/us/gcr.io/google-cloud-cli)
with the following repository name:
`gcr.io/google.com/cloudsdktool/google-cloud-cli`. The images are also available
using the `us.gcr.io`, `eu.gcr.io`, and `asia.gcr.io` repositories.

1.  To use the image of the stable Google Cloud CLI release,
    `gcr.io/google.com/cloudsdktool/google-cloud-cli:stable`, pull it from
    [Artifact Registry](https://console.cloud.google.com/artifacts/docker/google.com:cloudsdktool/us/gcr.io/google-cloud-cli)
    by running the following command:

    ```none
    docker pull gcr.io/google.com/cloudsdktool/google-cloud-cli:573.0.0-stable
    ```

2.  Verify the installation by running:

    ```none
    docker run --rm gcr.io/google.com/cloudsdktool/google-cloud-cli:573.0.0-stable gcloud version
    ```

    If you have used the floating `:stable` tag (which always point to the
    latest release), verify the installation by running the following command:

    ```none
    docker run --rm gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud version
    ```

For detailed instructions on authenticating, installing additional components,
troubleshooting, and migrating to the `:stable` image, see the
[User Guide](docs/user_guide.md) and [Migration Guide](docs/migration_guide.md).

## Cloud CLI Release Tracking

You can also follow the Cloud CLI Release schedule here:

-   [https://groups.google.com/g/google-cloud-sdk-announce](https://groups.google.com/g/google-cloud-sdk-announce)
