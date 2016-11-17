#!/usr/bin/env bash

HAZELCAST_REPO="$1"
HAZELCAST_BRANCH="$2"

wget -q https://github.com/$HAZELCAST_REPO/hazelcast/archive/$HAZELCAST_BRANCH.zip
HAZELCAST_BRANCH="distributed_scheduled_exec"
unzip -oq $HAZELCAST_BRANCH.zip

if([[ $HAZELCAST_BRANCH == v* ]])
then
   HAZELCAST_BRANCH=${HAZELCAST_BRANCH:1}
fi

cp -R ./hazelcast-feature-$HAZELCAST_BRANCH/hazelcast/src/main ../hazelcast/downloaded/
