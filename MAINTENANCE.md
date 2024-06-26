# Releasing new versions

Update the `ARG CLOUD_SDK_VERSION` statement with the version number (e.g. `ARG CLOUD_SDK_VERSION 160.0.0`) in the 
following files:

* `Dockerfile`
* `debian_slim/Dockerfile`
* `alpine/Dockerfile`
* `debian_component_based/Dockerfile`
* `stable/Dockerfile`

Commit, and tag the release:

```bash
export VERSION=160.0.0
git add --all && git commit -m "Update SDK to $VERSION" --allow-empty && \
    git tag -a $VERSION -m "v${VERSION}" && \
    git push origin master --tags "${VERSION}"
```


## Updating a tagged version

**Caution:** Do not update version-tagged images on Docker Hub with breaking
changes. If a user is consuming `google/cloud-sdk:160.0.0-slim` image, then do
not change that image in a breaking way!

To recreate a version-tagged image in Docker Hub, delete the git tag locally
and remotely on GitHub:

```bash
export VERSION=160.0.0
git add --all && git commit -m "Re-release tag $VERSION" --allow-empty && \
    git tag -d $VERSION; \
    git tag -a $VERSION -m "v${VERSION}" && \
    git push origin ":${VERSION}" && \
    git push origin master --tags
```

Then follow the steps in "Releasing new versions" to release the version
again.
