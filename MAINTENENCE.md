

The Alpine image contains the SHA256 checksum for that version as listed on the SDK [documentation page](https://cloud.google.com/sdk/downloads#versioned).

```bash
export TAG_VER=153.0.0
git add -A
git commit -m "Updating version $TAG_VER"
git push
git tag $TAG_VER
git push --tags
```

A github [pre-commit](hooks/pre-commit) hook is also provided which will build the alpine image with the SDK provided. 

It requires docker on your build machine so if you have that installed, just copy this file into 
```
cp hooks/pre-commit .git/hooks/pre-commit
```
Then on git commit, the script will build the image specified and then compare its output to the value of '$TAG_VER'.  

If the build does not succeed or gcloud is not initialized with that version, the commit will fail.

You can also pass in the ARG value of the sdk version and checksum as overrides:

```bash
docker build --build-arg CLOUD_SDK_VERSION=151.0.1 --build-arg SHA256SUM=26b84898bc7834664f02b713fd73c7787e62827d2d486f58314cdf1f6f6c56bb -t alpine_151 --no-cache .
```

---

Archived versions of the SDK can be found under in GCS bucket: 
```
gsutil ls gs://cloud-sdk-release
```
* [https://storage.cloud.google.com/cloud-sdk-release](https://storage.cloud.google.com/cloud-sdk-release)



