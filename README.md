cloud-sdk-docker
================


**  >>>> NOTE <<<< **
> The base soruce image for the Cloud SDK Container will be rebased to Alpine Linux on or after 5/15/17.
> For more information, please see:
* [https://github.com/GoogleCloudPlatform/cloud-sdk-docker/issues/58](https://github.com/GoogleCloudPlatform/cloud-sdk-docker/issues/58)
---

[`google/cloud-sdk`](https://index.docker.io/u/google/cloud-sdk/) is a [Docker](https://docker.io) image bundling all the components and dependencies of the [Google Cloud SDK](https://cloud.google.com/sdk/) including alpha and beta components.

## Usage

Follow these instructions if you are running docker *outside* of Google Compute Engine:

    # Get the cloud sdk image:
    $ docker pull google/cloud-sdk

    # Auth & save the credentials in gcloud-config volumes:
    $ docker run -t -i --name gcloud-config google/cloud-sdk gcloud init

    # If you would like to use service account instead please look here:
    $ docker run -t -i --name gcloud-config google/cloud-sdk gcloud auth activate-service-account <your-service-account-email> --key-file /tmp/your-key.p12 --project <your-project-id>

    # Re-use the credentials from gcloud-config volumes & run sdk commands:
    $ docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud info
    $ docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud components list
    $ docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcutil listinstances
    $ docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gsutil ls

If you are using this image from *within* [Google Compute Engine](https://cloud.google.com/compute/). If you enable a Service Account with the necessary scopes, there is no need to auth or use a config volume:

    # Get the cloud sdk image:
    $ docker pull google/cloud-sdk

    # Just start using the sdk commands:
    $ docker run --rm -ti google/cloud-sdk gcloud info
    $ docker run --rm -ti google/cloud-sdk gcloud components list
    $ docker run --rm -ti google/cloud-sdk gcutil listinstances
    $ docker run --rm -ti google/cloud-sdk gsutil ls
