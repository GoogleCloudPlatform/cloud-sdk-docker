cloud-sdk-docker
================

[`google/cloud-sdk`](https://index.docker.io/u/google/cloud-sdk/) is a [Docker](https://docker.io) image bundling all the components and dependencies
of the [Google Cloud SDK](https://cloud.google.com/sdk/):

- [App Engine SDK for Go](https://cloud.google.com/appengine/docs/go/)
- [App Engine SDK for Java](https://cloud.google.com/appengine/docs/java/)
- [App Engine SDK for Python](https://cloud.google.com/appengine/docs/python/) and [PHP](https://cloud.google.com/appengine/docs/php/)
- [Big Query Command Line Tool ](https://cloud.google.com/bigquery/bq-command-line-tool)
- [Cloud DNS Admin Command Line Interface](https://cloud.google.com/dns/migrating-bind-zone-command-line)
- [Cloud SQL Admin Command Line Interface](https://cloud.google.com/sql/docs/admin-api/)
- [Cloud Storage Command Line Tool](https://cloud.google.com/storage/docs/gsutil)
- [Compute Engine Command Line Tool](https://cloud.google.com/compute/docs/gcloud-compute/)

## Usage

Follow these instructions if you are running docker *outside* of Google
Compute Engine:

    # get the cloud sdk image
    $ docker pull google/cloud-sdk

    # auth & save the credentials in gcloud-config volumes
    $ docker run -t -i --name gcloud-config google/cloud-sdk gcloud auth login
    Go to the following link in your browser: ...
    Enter verification code: ...
    You are now logged in as [...]
    Your current project is [None]. You can change this setting by running:
       $ gcloud config set project <project>
    gcloud config set project ...

    # If you would like to use service account instead please look here:
    docker run --volume /.config/gcloud/ \
      --tty \
      --interactive \
      --name gcloud-config \
      busybox true
    docker run --tty \
      --interactive \
      --rm \
      --volumes-from gcloud-config \
      --volume $(pwd)/<your-private-key>.p12:/tmp/your-key.p12 \
      google/cloud-sdk \
      gcloud auth activate-service-account <your-service-account-email> --key-file /tmp/your-key.p12 --project <your-project-id>

    # re-use the credentials from gcloud-config volumes & run sdk commands
    $ docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcutil listinstances
    $ docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gsutil ls
    $ docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud components list
    $ docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud version

If you are using this image from *within* [Google Compute Engine](https://cloud.google.com/compute/). If you enable a Service Account with the necessary scopes, there is no need to auth or use a config volume:

    # get the cloud sdk image
    $ docker pull google/cloud-sdk

    # just start using the sdk commands
    $ docker run --rm -ti google/cloud-sdk gcutil listinstances
    $ docker run --rm -ti google/cloud-sdk gsutil ls
    $ docker run --rm -ti google/cloud-sdk gcloud components list
    $ docker run --rm -ti google/cloud-sdk gcloud version
