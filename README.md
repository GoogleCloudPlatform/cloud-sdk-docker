cloud-sdk-docker
================

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

    #
    # To use Google Container Environment (GCE)
    #

    # Save credentials in gcloud-config volume
    $ docker run -t -i --name gcloud-config google/cloud-sdk gcloud container clusters get-credentials <cluster-name>
    
    # Re-use the credentials from gcloud-config volumes & run kubectl commands:
    $ docker run -t -i --name gcloud-config google/cloud-sdk kubectl cluster-info

    #
    # To use Google Container Registry (GCR) with docker from host
    #
    
    # Get an auth token
    $ docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud auth print-access-token
    # Login to docker
    $ docker login -e not@val.id -u _token -p <token> https://gcr.io

    # Use docker as usual...
    $ docker pull gcr.io/<project>/<repo>
    
If you are using this image from *within* [Google Compute Engine](https://cloud.google.com/compute/). If you enable a Service Account with the necessary scopes, there is no need to auth or use a config volume:

    # Get the cloud sdk image:
    $ docker pull google/cloud-sdk

    # Just start using the sdk commands:
    $ docker run --rm -ti google/cloud-sdk gcloud info
    $ docker run --rm -ti google/cloud-sdk gcloud components list
    $ docker run --rm -ti google/cloud-sdk gcutil listinstances
    $ docker run --rm -ti google/cloud-sdk gsutil ls
