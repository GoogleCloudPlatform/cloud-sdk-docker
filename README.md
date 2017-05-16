
# Google Cloud SDK Docker


Baseline image for the [Google Cloud SDK](https://cloud.google.com/sdk/).

Imaage includes default command line tools:
*  gcloud:  Default set of gcloud commands
*  gsutil:  Cloud Storage Command Line Tool
*  bq: BigQuery Command Line Tool


## Dockerfile

To use the prebuilt **Alpine** based image, see

* [https://hub.docker.com/r/google/cloud-sdk/](https://hub.docker.com/r/google/cloud-sdk/)


```bash
docker run -ti google/cloud-sdk:latest
```

or via tagged version of the SDK:

```bash
docker run -ti google/cloud-sdk:153.0.0
```

>> **NOTE:** you may need to install the optional components:
```

For example, for python GAE support, you would need to extend the base image:

```dockerfile
FROM google/cloud-sdk
RUN gcloud components install app-engine-python
```

or for java
```
FROM google/cloud-sdk
RUN apk --update add openjdk7-jre
RUN gcloud components install app-engine-java
WORKDIR /apps
```

For a volume mount using credentials:
```
docker run -t -i --name gcloud-config google/cloud-sdk gcloud auth login
```
then
```
docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud compute instances list --project your_project
NAME        ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP      STATUS
instance-1  us-central1-a  n1-standard-1               10.240.0.2   8.34.219.29      RUNNING
```

#### Google Appengine base

The original image in this repository was based off of 

> FROM gcr.io/google_appengine/base

The full Dockerfile for that can be found [here](google_appengine_base/Dockerfile) for archival.