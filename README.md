
# Google Cloud SDK Docker


The [Cloud SDK](https://cloud.google.com/sdk/) is the command-line interface to the Google Cloud Platform.  It is a flexible utility which uses GCPs own Cloud APIs to perform many different tasks such as deploying code on AppEngine, to creating Compute Engine VMs to checking IAM permissions and so on.  It is the command line interface to pretty much every Google Cloud Platform API and service.   

This article describes some more ways customers can use it by demonstrating several use cases involving containerizing the Cloud SDK.   The following shows Dockerfiles targeted towards various operating systems and some sample usecases (Its nothing new, just a sample set to document the baseline dockerfiles.

* [Dockerfile](#dockerfile)
    - [Ubuntu](#ubuntu)
    - [CentOS](#centos)
    - [Alpine](#alpine)
    - [Alpine Package](#alpine-package)
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

If you want to use a prebuilt image, see

* [https://hub.docker.com/r/google/cloud-sdk/](https://hub.docker.com/r/google/cloud-sdk/)

specifically

```bash
docker run -ti google/cloud-sdk:latest
```

or via tagged version of the SDK:

```
docker run -ti google/cloud-sdk:152.0.0
docker run -ti google/cloud-sdk:151.0.1
```

>> NOTE, with any of these images, you can also install the optional components too:
* google-cloud-sdk-app-engine-python
* google-cloud-sdk-app-engine-java 
* google-cloud-sdk-datalab 
* google-cloud-sdk-datastore-emulator 
* google-cloud-sdk-pubsub-emulator  
* google-cloud-sdk-bigtable-emulator kubectl


### Upgrading SDK versions

Alpine has the SDK version and its sha256 hash embedded into the Dockerfile.  The alpine image triggers a build rule in
DockerHub to automatically create :latest and :_sdk_release_ images 

To build a new release, first create a tag for that release

edit [alpine/Dockerfile](alpine/Dockerfile) and specify the version and sha256 hash.  You can find the hash on the cloud SDK install page
here:  

* [https://cloud.google.com/sdk/downloads#versioned](https://cloud.google.com/sdk/downloads#versioned)

```bash
ARG CLOUD_SDK_VERSION=151.0.1
ARG SHA256SUM=26b84898bc7834664f02b713fd73c7787e62827d2d486f58314cdf1f6f6c56bb
```

then simply push
```bash
export TAG_VER=152.0.0
git add -A
git commit -m 'Updating version $TAG_VER'
git push
git tag $TAG_VER
git push --tags
```

A github [pre-commit](hooks/pre-commit) hook is also provided which will build the alpine image with the SDK provided.  Just copy this file into 
```
cp hooks/pre-commit .git/hooks/pre-commit
```

The following images shows the dockerhub integration done with GitHub that autobuilds the images.
* [DockerHub Tags](images/tags.png)
* [DockerHub Build Rules](images/build_rules.png)
* [gitHub Integrations](images/github_integration.png)

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
RUN apk add --update curl python bash &&  rm -rf /var/cache/apk/*
ENV HOME /
#RUN curl https://sdk.cloud.google.com | bash

ARG CLOUD_SDK_VERSION=151.0.1
ARG SHA256SUM=26b84898bc7834664f02b713fd73c7787e62827d2d486f58314cdf1f6f6c56bb

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

#### Alpine Package

The following describes building and running the Cloud SDK as an Alpine package.  In other words, its a package you can use Alpine's installer to 
setup instead of sourcing from a base image and then installing Cloud SDK as docker commands.

For more information see:

* [https://wiki.alpinelinux.org/wiki/Creating_an_Alpine_package](https://wiki.alpinelinux.org/wiki/Creating_an_Alpine_package)
* [https://pkgs.alpinelinux.org/packages](https://pkgs.alpinelinux.org/packages)


At the time of writing (3/16), the package is not in the official alpine community repository. 

> _Note:_  the package below is pinned to SDK 147.0.0.   You can either update gcloud post-install or regenerate a new package.

*APKBUILD*

```bash
pkgname=google-cloud-sdk
pkgver=147.0.0
pkgrel=0
pkgdesc="Google Cloud SDK"
url="https://cloud.google.com/sdk"
arch="x86_64"
license="GPL"
depends="python libc6-compat"
makedepends="$depends"
install=""
source="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-$pkgver-linux-x86_64.tar.gz"
builddir="$srcdir/$pkgname"

package() {
        mkdir -p "$pkgdir"/ || return 1
        mkdir -p "$pkgdir"/usr/bin || return 1
        cp -R "$builddir" "$pkgdir"/ || return 1
        ln -s /google-cloud-sdk/bin/gcloud "$pkgdir"/usr/bin/gcloud || return 1
}

sha1sums="16292eee83078233dd6e3ca83760314b1f95168b  google-cloud-sdk-147.0.0-linux-x86_64.tar.gz"
md5sums="eed7bc81905ce18cf821d844430d7750  google-cloud-sdk-147.0.0-linux-x86_64.tar.gz"
sha256sums="d517d9971daeaa4e3d13e34a112f684320da96ce5082e20ad745035ca16375ce  google-cloud-sdk-147.0.0-linux-x86_64.tar.gz"
sha512sums="7e9077e8aa9c91b011fea9329f43a465be63d95718183d0ec72b67a4eaacbd21693fb4c2dfd1f7526167a1fe6dcaa43f6b8afc62ab1aae60a71ae240c8972f9a  google-cloud-sdk-147.0.0-linux-x86_64.tar.gz"
```

#### Google Appengine base

The original base image in this repository was based off of 

> FROM gcr.io/google_appengine/base

The full Dockerfile for this base can be found [here](google_appengine_base/Dockerfile) for archival.


## Usecases

### Containerize local development environment

You're an App Engine developer and you want to keep your workstation in  as much of a consistent state as possible.  That means you would rather not install the Cloud SDK or run dev_appserver.py directly from your laptop.   What you would rather do is spin up any components for your local development without having Cloud SDK installed on the laptop.   

What you'd like to do is run Cloud SDK and dev_appserver.py in a container.
To do that, you need to run dev_appserver.py from the Cloud SDK docker image but map your deployable sources to that container.   

For example with python, I'm mapping my current source directory to the container (under /apps) and instructing it to run the dev_appserver.py

```
docker run -p 8080:8080 -p 8000:8000 -v path_to_your_app.yaml:/apps google/cloud-sdk dev_appserver.py --host=0.0.0.0 --admin_host=0.0.0.0 /apps/app.yaml
INFO     2016-10-28 19:39:31,206 devappserver2.py:769] Skipping SDK update check.
WARNING  2016-10-28 19:39:31,269 simple_search_stub.py:1146] Could not read search indexes from /tmp/appengine.None.root/search_indexes
INFO     2016-10-28 19:39:31,272 api_server.py:205] Starting API server at: http://localhost:44119
INFO     2016-10-28 19:39:31,276 dispatcher.py:197] Starting module "default" running at: http://0.0.0.0:8080
```

You can also configure your container image if you’d like to use Maven
You can also do this with maven but you will need to install the dependencies into the extended image itself as shown in the following Dockerfile that sets up your execution environment for maven:

```
FROM google/cloud-sdk
RUN apt-get install -y maven default-jdk
WORKDIR /apps
```

Build your containerized runtime environment:

```
docker build -t cloudsdk-java .
```

Then just launch with your app:

```
docker run -p 8080:8080 -v path_to_your_pom.xml:/apps cloudsdk-java mvn appengine:run
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

> Warning:  the volume gcloud-config now has your credentials/JSON key file embedded in it; carefully control access to it!

Then run a new container but specify the volume.  You'll see that the configured credentials already exist

```
docker run --rm -ti --volumes-from gcloud-config google/cloud-sdk gcloud config list
Your active configuration is: [default]
[component_manager]
disable_update_check = true
[core]
account = your_service_account@yoru_project.iam.gserviceaccount.com
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

### Run emulators in containers

Running emulators in a container provides an easy, predictable configuration for an emulator.  You can always reuse a given configuration without needing to initialize the SDK with credentials.  For example, the following starts up the pubsub emulator from a baseline SDK:

```
docker run --rm -ti -p 8283:8283 google/cloud-sdk gcloud beta emulators pubsub start --host-port 0.0.0.0:8283
Executing: /google-cloud-sdk/platform/pubsub-emulator/bin/cloud-pubsub-emulator --host=0.0.0.0 --port=8283
[pubsub] This is the Google Pub/Sub fake.
[pubsub] Oct 25, 2016 4:29:31 AM com.google.cloud.pubsub.testing.v1.Main main
[pubsub] INFO: Server started, listening on 8283
```               

You can even extend and link some code you run in an container to connect with this emulator.  In this mode, you run your emulator in one container, acquire the container's internal address, then separately run your application in another container but link to the emulator via docker networking.  There are several ways to do this securely too with docker custom networks.   

First run the emulator:

```
docker run -tid --name pubsubemulator google/cloud-sdk gcloud beta emulators pubsub start --host-port 0.0.0.0:8283
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

```
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
