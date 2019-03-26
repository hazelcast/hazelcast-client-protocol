#!/usr/bin/env bash

mkdir tempDownloaded
cd tempDownloaded

HAZELCAST_REPO="$1"
HAZELCAST_BRANCH="$2"
# finds downloaded-file-name by extracting string after rightmost slash.(e.g. extracted name from `fix/3.8/abc` will be `abc`)
DOWNLOADED_HAZELCAST_BRANCH=${2##*/}
# finds unzipped directory name by replacing `/` with `-` (e.g. `fix/3.8/abc` will become `fix-3.8-abc`)
COPY_HAZELCAST_BRANCH=${2//\//-}

wget -q https://github.com/${HAZELCAST_REPO}/hazelcast/archive/${HAZELCAST_BRANCH}.zip
unzip -oq ${DOWNLOADED_HAZELCAST_BRANCH}.zip

if ([[ ${DOWNLOADED_HAZELCAST_BRANCH} == v* ]]); then
   DOWNLOADED_HAZELCAST_BRANCH=${DOWNLOADED_HAZELCAST_BRANCH:1}
fi

echo "HAZELCAST_REPO: $HAZELCAST_REPO" > download.info
echo "HAZELCAST_BRANCH: $HAZELCAST_BRANCH" >> download.info
echo "DOWNLOADED_HAZELCAST_BRANCH: $DOWNLOADED_HAZELCAST_BRANCH" >> download.info
echo "COPY_HAZELCAST_BRANCH: $DOWNLOADED_HAZELCAST_BRANCH" >> download.info

cp -R ./hazelcast-${COPY_HAZELCAST_BRANCH}/hazelcast/src/main ../../hazelcast/downloaded/
