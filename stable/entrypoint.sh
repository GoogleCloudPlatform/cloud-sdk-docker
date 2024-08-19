#!/bin/sh

set -e
# Run your preprocessing script

if [ ! -z "$APT_PACKAGES" ]; then
      packages=$(echo $APT_PACKAGES | tr " " "\n")
      apt-get update && apt-get install -qqy $packages
fi 

if [ ! -z "$COMPONENTS" ]; then
      components=$(echo $COMPONENTS | tr " " "\n")
      apt-get update && apt-get install -qqy \
                curl \
                lsb-release \
                gnupg 
      export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
      echo "deb https://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" > /etc/apt/sources.list.d/google-cloud-sdk.list
      curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
      
      echo $components
      apt-get update && apt-get install -qqy $components
fi

# Execute the main command
exec "$@"
