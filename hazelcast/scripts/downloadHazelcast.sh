#!/usr/bin/env bash

HAZELCAST_REPO="$1"
HAZELCAST_BRANCH="$2"

wget -q https://github.com/$HAZELCAST_REPO/hazelcast/archive/$HAZELCAST_BRANCH.zip
unzip -oq $HAZELCAST_BRANCH.zip

if([[ $HAZELCAST_BRANCH == v* ]])
then
   HAZELCAST_BRANCH=${HAZELCAST_BRANCH:1}
fi

cp -R ./hazelcast-$HAZELCAST_BRANCH/hazelcast/src/main ../hazelcast/downloaded/
