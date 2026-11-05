#!/bin/sh

set -e
# Run your preprocessing script

if [ ! -z "$APT_PACKAGES" ]; then
      packages=$(echo $APT_PACKAGES | tr " " "\n")
      apt-get update && apt-get install -qqy $packages
fi

if [ ! -z "$COMPONENTS" ]; then
      version="${CLOUD_SDK_VERSION:-$(cat /usr/lib/google-cloud-sdk/VERSION 2>/dev/null || true)}"
      apt-get update && apt-get install -qqy --no-install-recommends ca-certificates
      echo "deb [signed-by=/etc/apt/keyrings/google-cloud-cli.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
          > /etc/apt/sources.list.d/google-cloud-sdk.list

      components="$COMPONENTS"
      if [ ! -z "$version" ]; then
            printf 'Package: google-cloud-cli*\nPin: version %s-0\nPin-Priority: 1001\n\nPackage: kubectl\nPin: version 1:%s-0\nPin-Priority: 1001\n' \
                "$version" "$version" > /etc/apt/preferences.d/google-cloud-cli
            components="google-cloud-cli=${version}-0 ${components}"
      fi

      echo $components
      apt-get update
      apt-get install -qqy --no-install-recommends $components
fi

# Execute the main command
exec "$@"
