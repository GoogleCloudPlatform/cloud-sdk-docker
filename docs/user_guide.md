# Using Google Cloud CLI Docker Images

This guide provides additional information on how to use, configure, and
troubleshoot the Google Cloud CLI Docker images.

## Authenticating with the Docker image

Authenticate with the Google Cloud CLI Docker image by running one of the
following commands:

*   Authenticate `gcloud` with your user credentials by running `gcloud auth
    login`:

    ```none
    docker run -ti --name gcloud-config gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud auth login
    ```

*   If you need to authenticate applications that use the Google Cloud APIs,
    pass the `--update-adc` option:

    ```none
    docker run -ti --name gcloud-config gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud auth login --update-adc
    ```

*   To set a default project that is selected each time you open the container,
    run the following command:

    ```none
    docker run -ti --name gcloud-config gcr.io/google.com/cloudsdktool/google-cloud-cli:stable /bin/bash -c 'gcloud auth login && gcloud config set project <your-project>'
    ```

    After you've authenticated successfully, credentials are preserved in the
    volume of the `gcloud-config` container.

    Note: `gcloud-config` container now has a volume containing your Google
    Cloud credentials. Don't use `gcloud-config` volume in other containers.

    To verify, list the compute instances using the credentials by running the
    container with `--volumes-from`:

    ```none
    docker run --rm --volumes-from gcloud-config gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud compute instances list --project <your-project>
    ```

*   If you want to authenticate using a service account, use the
    `auth/credential_file_override` property to set a path to a mounted service
    account. Then update the config to read the mounted service account using
    the `CLOUDSDK_CONFIG` environment variable.

    In the following example, the `mycloud` configuration has the
    `auth/credential_file_override` already set. The configuration points to a
    certificate file that is present within the container as a separate volume
    mount.

    ```none
    $ docker run -ti -e CLOUDSDK_CONFIG=/config/mygcloud \
                  -v `pwd`/mygcloud:/config/mygcloud \
                  -v `pwd`:/certs  gcr.io/google.com/cloudsdktool/google-cloud-cli:stable /bin/bash

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

## Installing additional components

You can install additional components in the Google Cloud CLI Docker image. The
approach to install additional components varies depending on the underlying
base image type.

### Debian-based images

By default, the stable images (`:stable` and `:VERSION-stable`) have no
components installed other than `bq` and `gsutil`. To install additional
components for the stable image, do one of the following:

*   **Building your own image based upon the `:stable` image Dockerfile**:
    Install packages that are not directly available through `apt-get` (e.g.,
    Docker engine).
*   **Installing additional packages or components at runtime**: Customize your
    image without hosting it.

#### Building your own image using the `:stable` image Dockerfile

To build your own image with additional components from `:stable`, you can clone
this repository and use the `docker build` command to build the `:stable` Docker
image from the Dockerfile with the `INSTALL_COMPONENTS` argument. For example,
to add `datastore-emulator` components:

```none
# clone the GitHub docker directory
$ git clone https://github.com/GoogleCloudPlatform/cloud-sdk-docker.git
$ docker build --build-arg CLOUD_SDK_VERSION=<release_version> \
   --build-arg INSTALL_COMPONENTS="google-cloud-cli-datastore-emulator=<release_version>-0" \
   -t my-cloud-sdk-docker:stable .
```

#### Installing additional packages or components at runtime

If you have pulled the `stable` Docker image, you can install the following
additional components during runtime:

*   `gcloud` components by using the `COMPONENTS` environment variable.
*   apt-packages by using the `APT_PACKAGES` environment variable.

For example, if you want to install the `cbt` and `kpt` components at runtime,
you can run the following command:

```none
docker run -e COMPONENTS='google-cloud-cli-cbt google-cloud-cli-kpt' \
gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud version
```

To install apt-packages `curl` and `gcc` while running the Docker image, execute
the following command:

```none
docker run -e APT_PACKAGES='curl gcc' \
gcr.io/google.com/cloudsdktool/google-cloud-cli:stable gcloud version
```

### Alpine-based images

To install additional components for Alpine-based images, create a Dockerfile
that uses the `google-cloud-cli` image as the base image.

For example, to add `kubectl` and `app-engine-java` components:

1.  Create the Dockerfile:

    ```dockerfile
    FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:alpine
    RUN apk --update add gcompat openjdk8-jre
    RUN gcloud components install app-engine-java kubectl
    ```

2.  Build the image:

    ```none
    docker build -t my-cloud-sdk-docker:alpine .
    ```

For Alpine based images, you must install dependencies of additional components
manually.

## Troubleshooting

### Failed to fetch <image-tag> error

If you get a `failed to fetch <image-tag>` error while trying to pull an image,
you are most likely trying to fetch an image tag that has been deprecated and
removed. Check the [Docker image options](#docker-image-options) for supported
tags.

### Vulnerabilities in the images

Images are scanned daily and common vulnerabilities and exposures (CVEs) are
mitigated before each new release. If your scanner detects unresolved
vulnerabilities, you can file a bug on the
[Google Cloud Issue Tracker](https://issuetracker.google.com/issues/new?component=187143)
with the vulnerability details.

### Tagless images in the repository

You may see tagless images in the Artifact Registry repository. These are
architecture-specific or attestation images created during the multi-arch build
process and are not intended for direct use. You can safely ignore them.
