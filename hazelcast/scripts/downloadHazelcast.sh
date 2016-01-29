#!/usr/bin/env bash

HAZELCAST_BRANCH="$1"
wget -q https://github.com/hazelcast/hazelcast/archive/$HAZELCAST_BRANCH.zip
unzip -oq $HAZELCAST_BRANCH.zip
cp -R ./hazelcast-$HAZELCAST_BRANCH/hazelcast/src/main ../hazelcast/downloaded/
