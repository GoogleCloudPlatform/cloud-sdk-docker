#!/bin/bash
export VERSION=291.0.0 && \
  git add --all && git commit -m "Update SDK to $VERSION" --allow-empty && \
  git tag --force  -a $VERSION -m "v${VERSION}" && \
  git push --force origin master --tags "${VERSION}"
