# Migrating to the `:stable` image

If you are using the `:latest`, `:alpine`, `:emulators`, `:slim` or
`:debian_component_based` Docker images, we recommend that you migrate to the
Debian-based `:stable` image for a smaller image size and more timely security
updates. To transition to using the `:stable` image you can
[extend the `:stable` Docker image](#extending-the-stable-docker-image) to match
the image you have been using.

In some cases (e.g., installing older incompatible dependencies like Python 2 or
older JDKs), extending the `:stable` image is not always feasible. In which case
you may have to build your own Dockerfile.

## Extending the `:stable` Docker image

You can use the `:stable` Docker image as a base image and install additional
components and apt packages to extend it to match the other Debian-based Docker
images (e.g., `:latest`, `:emulators`, and `:slim`). To extend the `:stable`
Docker image, you can do one of the following:

*   [Extending the `:stable` base image by customizing at runtime](#extending-the-stable-base-image-by-customizing-at-runtime)
*   [Extending the `:stable` base image by building your own Dockerfile](#extending-the-stable-base-image-by-building-your-own-dockerfile)

### Extending the `:stable` base image by customizing at runtime

You can extend the `:stable` Docker image to use as a replacement for the
`:latest`, `:emulators` or `:slim` image by customizing it at runtime.

#### Customize to the `:latest` Image

Run the following `docker run` command to make the `:stable` image match the
`:latest` image at runtime:

```none
docker run -e APT_PACKAGES='curl lsb-release openssh-client git gnupg' \
-e COMPONENTS='google-cloud-cli-datastore-emulator google-cloud-cli-pubsub-emulator google-cloud-cli-bigtable-emulator google-cloud-cli-firestore-emulator google-cloud-cli-spanner-emulator google-cloud-cli-cbt google-cloud-cli-local-extract google-cloud-cli-gke-gcloud-auth-plugin kubectl' \
gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud version
```

#### Customize to the `:emulators` Image

You can run the following command to make the `:stable` image match the
`:emulators` image at runtime:

```none
docker run -e APT_PACKAGES='curl' \
-e COMPONENTS='google-cloud-cli-datastore-emulator google-cloud-cli-pubsub-emulator google-cloud-cli-bigtable-emulator google-cloud-cli-firestore-emulator google-cloud-cli-spanner-emulator' \
gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud version
```

#### Customize to the `:slim` Image

You can make the `:stable` image match the `:slim` image at runtime by running
the following `docker run` command:

```none
docker run -e APT_PACKAGES='curl lsb-release openssh-client git gnupg' \
gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud version
```

#### Extending the `:stable` image with build configuration

You can use your own custom
[build configuration](https://cloud.google.com/build/docs/build-config-file-schema)
file(s) to customize the `:stable` Docker image to install additional packages
or components. For example, if you want to customize your `:stable` Docker image
to install `python3-google-auth` and `python3-requests` packages and install the
`pubsub emulator` component, you can use the following build config file.

```yaml
steps:
  - id: 'extend-stable'
    name: gcr.io/google.com/cloudsdktool/google-cloud-cli:500.0.0-stable
    args:
      - gcloud
      - version
    env:
      - 'APT_PACKAGES=python3-google-auth python3-requests'
      - 'COMPONENTS=google-cloud-cli-pubsub-emulator'
```

### Extending the `:stable` base image by building your own Dockerfile

You can customize the `:stable` Docker image by creating your own Dockerfile
with the `:stable` image as the base image and then build the Docker image with
the `docker build` command.

#### Build your own `:latest` Image

To convert the `:stable` image into the `:latest` image, do the following:

1.  Create your own Dockerfile from `:stable` by installing the required
    components and packages:

    ```dockerfile
    FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:stable

    RUN apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy --no-install-recommends \
          curl \
          ca-certificates \
          openssh-client \
          git \
          gnupg && \
       export CLOUD_SDK_VERSION=$(gcloud version | grep "Google Cloud SDK" | grep -oE '[^ ]+$') && \
       echo "deb [signed-by=/etc/apt/keyrings/google-cloud-cli.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
       apt-get update && \
       apt-get install -y --no-install-recommends google-cloud-cli-datastore-emulator=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-pubsub-emulator=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-bigtable-emulator=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-firestore-emulator=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-spanner-emulator=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-cbt=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-local-extract=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-gke-gcloud-auth-plugin=${CLOUD_SDK_VERSION}-0 \
          kubectl
    ```

2.  Build the Dockerfile to get your own `:latest` Docker image:

    ```none
    docker build -t my-cloud-sdk-docker:latest .
    ```

#### Build your own `:emulators` Image

To convert the `:stable` image into the `:emulators` image, do the following:

1.  Create the Dockerfile with required components and packages as:

    ```dockerfile
    FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:stable

    RUN apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy --no-install-recommends \
          curl \
          ca-certificates && \
       export CLOUD_SDK_VERSION=$(gcloud version | grep "Google Cloud SDK" | grep -oE '[^ ]+$') && \
       echo "deb [signed-by=/etc/apt/keyrings/google-cloud-cli.gpg] https://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
       apt-get update && \
       apt-get install -y --no-install-recommends google-cloud-cli-datastore-emulator=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-pubsub-emulator=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-bigtable-emulator=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-firestore-emulator=${CLOUD_SDK_VERSION}-0 \
          google-cloud-cli-spanner-emulator=${CLOUD_SDK_VERSION}-0
    ```

2.  Build the Dockerfile by running the command:

    ```none
    docker build -t my-cloud-sdk-docker:emulators .
    ```

#### Build your own `:slim` Image

To convert the `:stable` image into the `:slim` image, do the following:

1.  Create a Dockerfile using `:stable` as base image:

    ```dockerfile
    FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:stable

    RUN apt-get update -qqy && apt-get -qqy upgrade && apt-get install -qqy --no-install-recommends \
          curl \
          lsb-release \
          openssh-client \
          git \
          gnupg
    ```

2.  Build the Dockerfile by running the following command:

    ```none
    docker build -t my-cloud-sdk-docker:slim .
    ```
