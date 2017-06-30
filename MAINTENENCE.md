# Releasing new versions

Update the `ENV CLOUD_SDK_VERSION` statement with the version number (e.g. `ENV CLOUD_SDK_VERSION 160.0.0`) in the 
following files:

* `Dockerfile`
* `debian_slim/Dockerfile`
* `alpine/Dockerfile`

Commit, and tag the release:

```bash
export VERSION=160.0.0
git add --all && git commit -m "Update SDK to $VERSION" --allow-empty && \
    git tag -a $VERSION -m "v${VERSION}" && \
    git push origin master --tags
```


## Updating a tagged version

**Caution:** Do not update version-tagged images on Docker Hub with breaking
changes. If a user is consuming `google/cloud-sdk:160.0.0-slim` image, then do
not change that image in a breaking way!

To recreate a version-tagged image in Docker Hub, delete the git tag locally
and remotely on GitHub:

```bash
git tag -d 159.0.0 && \
    git push origin :159.0.0
```

Then follow the steps in "Releasing new versions" to release the version
again.
