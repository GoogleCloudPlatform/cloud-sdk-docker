
# Google Cloud SDK Docker


The [Cloud SDK](https://cloud.google.com/sdk/) is the command-line interface to the Google Cloud Platform.  It is a flexible utility which uses GCPs own Cloud APIs to perform many different tasks such as deploying code on AppEngine, to creating Compute Engine VMs to checking IAM permissions and so on.  It is the command line interface to pretty much every Google Cloud Platform API and service.   

This article describes some more ways customers can use it by demonstrating several use cases involving containerizing the Cloud SDK.   The following shows Dockerfiles targeted towards various operating systems and some sample usecases (Its nothing new, just a sample set to document the baseline dockerfiles.

* [Dockerfile](#dockerfile)
    - [Ubuntu](#ubuntu)
    - [CentOS](#centos)
    - [Alpine](#alpine)
* [Usecases](#usecases)
    - [Containerize local development environment](#containerize-local-development-environment)
    - [Run gcloud cli without installing SDK locally](#run-gcloud-cli-without-installing-sdk-locally)
    - [Run emulators in containers](#run-emulators-in-containers)
    - [Automate simple DevOps tasklets](#automate-simple-devdps-tasklets)       

## Dockerfile

To use any of the images below, enter the folder for the OS in question and run

```bash
docker build -t cloud-sdk .
```

If you want to use a prebuilt **Alpine** based image, see

* [https://hub.docker.com/r/google/cloud-sdk/](https://hub.docker.com/r/google/cloud-sdk/)

specifically

```bash
docker run -ti google/cloud-sdk:latest
```

or via tagged version of the SDK:

```bash
docker run -ti google/cloud-sdk:153.0.0
docker run -ti google/cloud-sdk:152.0.0
docker run -ti google/cloud-sdk:151.0.1
```

>> **NOTE:** with any of these images, you can also install the optional components and add that to your baseline container
```
$ docker run -ti google/cloud-sdk:latest gcloud components list

Your current Cloud SDK version is: 153.0.0
The latest available version is: 153.0.0

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                  Components                                                 │
├───────────────┬──────────────────────────────────────────────────────┬──────────────────────────┬───────────┤
│     Status    │                         Name                         │            ID            │    Size   │
├───────────────┼──────────────────────────────────────────────────────┼──────────────────────────┼───────────┤
│ Not Installed │ App Engine Go Extensions                             │ app-engine-go            │  47.9 MiB │
│ Not Installed │ Bigtable Command Line Tool                           │ cbt                      │   3.9 MiB │
│ Not Installed │ Cloud Datalab Command Line Tool                      │ datalab                  │   < 1 MiB │
│ Not Installed │ Cloud Datastore Emulator                             │ cloud-datastore-emulator │  15.4 MiB │
│ Not Installed │ Cloud Datastore Emulator (Legacy)                    │ gcd-emulator             │  38.1 MiB │
│ Not Installed │ Cloud Pub/Sub Emulator                               │ pubsub-emulator          │  21.0 MiB │
│ Not Installed │ Emulator Reverse Proxy                               │ emulator-reverse-proxy   │  14.5 MiB │
│ Not Installed │ Google Container Registry's Docker credential helper │ docker-credential-gcr    │   3.4 MiB │
│ Not Installed │ gcloud Alpha Commands                                │ alpha                    │   < 1 MiB │
│ Not Installed │ gcloud Beta Commands                                 │ beta                     │   < 1 MiB │
│ Not Installed │ gcloud app Java Extensions                           │ app-engine-java          │ 128.6 MiB │
│ Not Installed │ gcloud app Python Extensions                         │ app-engine-python        │   6.1 MiB │
│ Not Installed │ kubectl                                              │ kubectl                  │  14.9 MiB │
│ Installed     │ BigQuery Command Line Tool                           │ bq                       │   < 1 MiB │
│ Installed     │ Cloud SDK Core Libraries                             │ core                     │   5.9 MiB │
│ Installed     │ Cloud Storage Command Line Tool                      │ gsutil                   │   2.9 MiB │
│ Installed     │ Default set of gcloud commands                       │ gcloud                   │           │
└───────────────┴──────────────────────────────────────────────────────┴──────────────────────────┴───────────┘
```

For example, for python GAE support, you would need to extend the base image:

```dockerfile
FROM google/cloud-sdk
RUN gcloud components install app-engine-python
```

Then build and run that:
```
docker build -t cloud-sdk-docker-gae .
docker run -t cloud-sdk-docker-gae
```


### Upgrading SDK versions

Alpine has the SDK version and its sha256 hash embedded into the Dockerfile.  The alpine image triggers a build rule in
DockerHub to automatically create :latest and :_sdkversion_ images 

* [https://hub.docker.com/r/google/cloud-sdk/tags/](https://hub.docker.com/r/google/cloud-sdk/tags/)

To build your own versioned image, first create a tag for that release

edit [alpine/Dockerfile](alpine/Dockerfile) and specify the version and sha256 hash.  You can find the hash on the cloud SDK install page
here:  

* [https://cloud.google.com/sdk/downloads#versioned](https://cloud.google.com/sdk/downloads#versioned)

```bash
ARG CLOUD_SDK_VERSION=153.0.0
ARG SHA256SUM=ade29e765f7847bf6081affb6eada69b45138d4abb443b1484e891312990e958
```

then simply push
```bash
export TAG_VER=153.0.0
git add -A
git commit -m "Updating version $TAG_VER"
git push
git tag $TAG_VER
git push --tags
```

A github [pre-commit](hooks/pre-commit) hook is also provided which will build the alpine image with the SDK provided.  It requires docker on your build
machine so if you have that installed, just copy this file into 
```
cp hooks/pre-commit .git/hooks/pre-commit
```
Then on git commit, the script will build the image specified and then compare its output to the value of '$TAG_VER'.  If the build does not succeed and gcloud 
is not initialized with that version, the commit will fail.


### Ubuntu

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y curl python2.7 apt-transport-https lsb-release
RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

ENV HOME /
RUN  apt-get update && apt-get install -y google-cloud-sdk

RUN gcloud config set core/disable_usage_reporting true
RUN gcloud config set component_manager/disable_update_check true
VOLUME ["/.config"]
```

### CentOS

```dockerfile
FROM centos

RUN  echo $'[google-cloud-sdk]\n\
name=Google Cloud SDK\n\
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el7-x86_64\n\
enabled=1\n\
gpgcheck=1\n\
repo_gpgcheck=1\n\
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg\n\
       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg'\
        >> /etc/yum.repos.d/google-cloud-sdk.repo 

ENV HOME /
RUN yum install -y google-cloud-sdk which 

RUN gcloud config set core/disable_usage_reporting true
RUN gcloud config set component_manager/disable_update_check true
VOLUME ["/.config"]
```

### Alpine

```dockerfile
FROM alpine
RUN apk --no-cache add curl python bash
ENV HOME /
#RUN curl https://sdk.cloud.google.com | bash

ARG CLOUD_SDK_VERSION=154.0.1
ARG SHA256SUM=b38a272872adcd79e93a87aa1867d4fd36567b40898559a57c1679e048529dea

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz
RUN echo "${SHA256SUM}  google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" > google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz.sha256
RUN sha256sum -c google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz.sha256
RUN tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz 

ENV PATH /google-cloud-sdk/bin:$PATH
RUN gcloud config set core/disable_usage_reporting true
RUN gcloud config set component_manager/disable_update_check true
VOLUME ["/.config"]
```

The SHA256 checksum is listed on the SDK [documentation page](https://cloud.google.com/sdk/downloads#versioned).

> Note: you can pass in the ARG value of the sdk version and checksum as overrides:

```bash
docker build --build-arg CLOUD_SDK_VERSION=151.0.1 --build-arg SHA256SUM=26b84898bc7834664f02b713fd73c7787e62827d2d486f58314cdf1f6f6c56bb -t alpine_151 --no-cache .
```

#### Google Appengine base

The original base image in this repository was based off of 

> FROM gcr.io/google_appengine/base

The full Dockerfile for this base can be found [here](google_appengine_base/Dockerfile) for archival.

---

## Usecases

### Containerize local development environment

You're an App Engine developer and you want to keep your workstation in  as much of a consistent state as possible.  That means you would rather not install the Cloud SDK or run dev_appserver.py directly from your laptop.   What you would rather do is spin up any components for your local development without having Cloud SDK installed on the laptop.   

What you'd like to do is run Cloud SDK and dev_appserver.py in a container.
To do that, you need to run dev_appserver.py from the Cloud SDK docker image but map your deployable sources to that container.

You will also need to run an image that extends the base cloud-sdk docker image and adds appengine support:
```dockerfile
FROM google/cloud-sdk
RUN apk --update add python
RUN gcloud components install app-engine-python
```

Then build:
```
docker build -t cloud-sdk-gae-python .
```

For example with python, I'm mapping my current source directory to the container (under /apps) and instructing it to run the dev_appserver.py

```
docker run -p 8080:8080 -p 8000:8000 -v path_to_your_app.yaml:/apps cloud-sdk-gae-python dev_appserver.py --host=0.0.0.0 --admin_host=0.0.0.0 /apps/app.yaml
INFO     2016-10-28 19:39:31,206 devappserver2.py:769] Skipping SDK update check.
WARNING  2016-10-28 19:39:31,269 simple_search_stub.py:1146] Could not read search indexes from /tmp/appengine.None.root/search_indexes
INFO     2016-10-28 19:39:31,272 api_server.py:205] Starting API server at: http://localhost:44119
INFO     2016-10-28 19:39:31,276 dispatcher.py:197] Starting module "default" running at: http://0.0.0.0:8080
```

You can also configure your container image if you’d like to use Maven
You can also do this with maven but you will need to install the dependencies into the extended image itself as shown in the following Dockerfile that sets up your execution environment for maven:

```dockerfile
FROM google/cloud-sdk
RUN apk --update add openjdk7-jre maven
RUN gcloud components install app-engine-java
WORKDIR /apps
```

Build your containerized runtime environment:

```
docker build -t cloud-sdk-gae-java .
```

Then just launch with your app:

```
docker run -p 8080:8080 -v path_to_your_pom.xml:/apps cloud-sdk-gae-java mvn appengine:run
```

(Note: you'll need to specify the host/port for the dev_appserver in the pom.xml <configuration/> section for the appengine-maven-plugin)

### Run gcloud cli without installing SDK locally

Don't want to install, update and maintain a local SDK install?  Install the SDK requires python installed locally.  If you containerize the SDK, all you need to run is docker.  If you pull the published google/cloudsdk:latest image, you are guaranteed to have the latest release of the SDK.  Note that once you pull an image down, it will remain cached in your local repository until you delete the local image and pull again.   Alternatively, if you want to remain on a given version, you can always specify the docker image to pull.  Note: we support only the last two releases of the SDK from 'latest'.

For example, first initialize the volume to use by authorizing it with your credentials:

```
docker run -t -i --name gcloud-config google/cloud-sdk gcloud auth login
```

Then reuse that volume but now use any gcloud command:

```
docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud compute instances list --project your_project
NAME        ZONE           MACHINE_TYPE   PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP      STATUS
instance-1  us-central1-a  n1-standard-1               10.240.0.2   8.34.219.29      RUNNING
```

You can also use this technique to initialize a volume with a service account.  This is useful if you want to have several service accounts handy as volumes where each service account is scoped with a different IAM Role.

To setup a service account credential in a volume, first download the JSON certificate file and map a volume to the Cloud SDK container:   

In the following example, my service account certificate file is stored on my local system 
at $HOME/certs/serviceAccountFile.json

```
docker run -t -v $HOME/certs:/data -i --name gcloud-config cloudsdk_ubuntu  gcloud auth activate-service-account --key-file /data/serviceAccountFile.json
Activated service account credentials for: [svc-2-429@mineral-minutia-820.iam.gserviceaccount.com]
```

> :warning: **WARNING:** the volume _gcloud-config_ now has your credentials/JSON key file embedded in it; carefully control access to it!

Then run a new container but specify the volume.  You'll see that the configured credentials already exist

```
docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud config list
Your active configuration is: [default]
[component_manager]
disable_update_check = true
[core]
account = your_service_account@your_project.iam.gserviceaccount.com
disable_usage_reporting = False
project = your_project
```

Now run some gcloud command on behalf of that service account.

```
docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud compute instances list
NAME                              ZONE           MACHINE_TYPE               PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP      STATUS
gae-default-20161011t124615-9sc2  us-central1-c  custom (1 vCPU, 1.00 GiB)               10.240.0.2   104.198.247.152  RUNNING
```

You can continue to do this with other restricted service accounts in volumes.  This will allow you to easily control which service accounts and its capabilities you use by having it already defined in a redistributable the container image (vs. using gcloud's --configuration= parameter in each command).

If you wanted to run a specific version of the SDK using your current credential set, you can directly map your active volume:

```
docker run --rm -it -v $HOME/.config/:/.config/ googl/cloud-sdk:151.0.0 gcloud config list
```

### Run emulators in containers

Running emulators in a container provides an easy, predictable configuration for an emulator.  You can always reuse a given configuration without needing to initialize the SDK with credentials.  For example, the following starts up the pubsub emulator from a baseline SDK:


As before, first extend the default sdk image and install the emulators:

Dockerfile
```dockerfile
FROM google/cloud-sdk
RUN apk --update add openjdk7-jre
RUN gcloud components install beta pubsub-emulator
```

Then create the baseline image to use for emulators:

```
docker build -t cloud-sdk-emulator .
```

```
docker run --rm -ti -p 8283:8283 cloud-sdk-emulator gcloud beta emulators pubsub start --host-port 0.0.0.0:8283
Executing: /google-cloud-sdk/platform/pubsub-emulator/bin/cloud-pubsub-emulator --host=0.0.0.0 --port=8283
[pubsub] This is the Google Pub/Sub fake.
[pubsub] Oct 25, 2016 4:29:31 AM com.google.cloud.pubsub.testing.v1.Main main
[pubsub] INFO: Server started, listening on 8283
```               

You can even extend and link some code you run in an container to connect with this emulator.  In this mode, you run your emulator in one container, acquire the container's internal address, then separately run your application in another container but link to the emulator via docker networking.  There are several ways to do this securely too with docker custom networks.   


```
docker run -tid --name pubsubemulator cloud-sdk-emulator gcloud beta emulators pubsub start --host-port 0.0.0.0:8283
```

We need to pass in the internal IP address for the emulator into your application container.  The following command returns the internal IP address which we will use later.

```
docker inspect -f "{{ .NetworkSettings.IPAddress }}" pubsubemulator
```

Now run your application container with credentials but link it back to your emulator by passing in an environment variable for the emulators internal IP address

```
docker run -ti -e PUBSUB_EMULATOR_HOST=`docker inspect -f "{{ .NetworkSettings.IPAddress }}" pubsubemulator`:8283 -e GOOGLE_APPLICATION_CREDENTIALS=/certs/your_service_account.json -v ~/certs/:/certs/ myapp
```

Note: you need to pass in GOOGLE_APPLICATION_CREDENTIALS because the PubSub client library tries to acquire an access token before contacting the emulator.

### Automate simple DevOps tasklets 

Suppose you want to run different automated tasks with service account with restricted access.  First create a service account and initialize a volume as shown in the "Reuse service account credential" use case.  Once you’ve done that, you can invoke any script that uses gcloud-cli.  We described some of the scripting you can do with gcloud in a previous blog post here.

As a concrete example, suppose you have a script which lists out the service accounts and their keys:

$ svc.sh 
```bash
#!/bin/bash
for project in  $(gcloud projects list --format="value(projectId)")
do
  echo "ProjectId:  $project"
  for robot in $(gcloud beta iam service-accounts list --project $project --format="value(email)")
   do
     echo "    -> Robot $robot"
     for key in $(gcloud beta iam service-accounts keys list --iam-account $robot --project $project --format="value(name.basename())")
        do
          echo "        $key" 
     done
   done
done
```

If you want to run that script using credentials initialized and attached to a volume in a container, simply run the gcloud-sdk container, reference the volume with credentials and map your script to the running container. In this example, I initialized gcloud-config with a given service account and then mapped svc.sh script from my local workstation to the gcloud-sdk image.  The entrypoint for the image is the script itself

```bash
docker run --rm -ti -v path_to_your_script:/scripts/ --volumes-from gcloud-config google/cloud-sdk /scripts/svc.sh
ProjectId:  your_project
    -> Robot 1071284184436-dvq7199h093skqu4885eoj03p56dcob2@developer.gserviceaccount.com
        71551c1b80f347a9cb3d00bb0410d93b9a66ff7f
        b578f5dbf55cbe9024dcc550e949f49d850ac7c1
    -> Robot mineral-minutia-820@appspot.gserviceaccount.com
        26bd660b2c44a4c9fd9aee494a06b0a75188ccd6
        36d46346555e185c2b089c74d79b23cf4182b6da
    -> Robot 1071284184436-compute@developer.gserviceaccount.com
        75c134bb04330ad66f9aa3bbb964031896e8ad44
        2f50a25d6107a9ff7bd8074e5e48622b1287b6dc
    -> Robot svc-2-429@mineral-minutia-820.iam.gserviceaccount.com
        2705030cb6d96e324fcb60be572f5e0da8fd183f
        e4536f3eed76703b7f626b2f88741be29a77f71a
```

For more info on scripting gcloud see [previous blog post](https://cloudplatform.googleblog.com/2016/06/filtering-and-formatting-fun-with.html) on this topic.

Hopefully, these basic use cases have given you some ideas on how to containerize the Cloud SDK and extend the image and customize in ways to suit your need. 
