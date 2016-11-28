#!/usr/bin/env bash

HAZELCAST_REPO="$1"
HAZELCAST_BRANCH="$2"
DOWNLOADED_HAZELCAST_BRANCH=${2##*/}    # finds downloaded-file-name by extracting string after rightmost slash.(e.g. extracted name from `fix/3.8/abc` will be `abc`)
COPY_HAZELCAST_BRANCH=${2//\//-}    # finds unzipped directory name by replacing `/` with `-` (e.g. `fix/3.8/abc` will become `fix-3.8-abc`)

wget -q https://github.com/$HAZELCAST_REPO/hazelcast/archive/$HAZELCAST_BRANCH.zip
unzip -oq $DOWNLOADED_HAZELCAST_BRANCH.zip

if([[ $DOWNLOADED_HAZELCAST_BRANCH == v* ]])
then
   DOWNLOADED_HAZELCAST_BRANCH=${DOWNLOADED_HAZELCAST_BRANCH:1}
fi

cp -R ./hazelcast-${COPY_HAZELCAST_BRANCH}/hazelcast/src/main ../hazelcast/downloaded/
