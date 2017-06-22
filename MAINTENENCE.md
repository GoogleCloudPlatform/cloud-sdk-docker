


To publish a new release, update the README with the version to deploy under "Supported tags and respective Dockerfile links".

Then edit the following files and update the SDK version:

* Dockerfile
* debian_slim/Dockerfile
* alpine/Dockerfile

then

finally,
```bash
export TAG_VER=159.0.0
git add -A
git commit -m "Update SDK to $TAG_VER"

git push

git tag -a $TAG_VER -m "Push $TAG_VER"
git push origin $TAG_VER

```

To recreate a tagged version in github and dockerhub, first delete the local and remote tags:

```
git tag -d 159.0.0

git push origin :159.0.0
```

After that, you can tag and re-push your current version.  This will trigger a rebuild in dockerhub

A github [pre-commit](hooks/pre-commit) hook is also provided which will build the default image with the SDK provided. 

It requires docker on your build machine so if you have that installed, just copy this file into 
```
cp hooks/pre-commit .git/hooks/pre-commit
```
Then on git commit, the script will build the image specified and then compare its output to the value of '$TAG_VER'.  

If the build does not succeed or gcloud is not initialized with that version, the commit will fail.

You can also pass in the ARG value of the sdk version and checksum as overrides for aplpine/Dockerfile:

```bash
docker build --build-arg CLOUD_SDK_VERSION=151.0.1 -t alpine_151 --no-cache .
```

---

Archived versions of the SDK can be found under in GCS bucket: 
```
gsutil ls gs://cloud-sdk-release
```
* [https://storage.cloud.google.com/cloud-sdk-release](https://storage.cloud.google.com/cloud-sdk-release)


The Alpine image contains the SHA256 checksum for that version as listed on the SDK [documentation page](https://cloud.google.com/sdk/downloads#versioned).
