#!/usr/bin/env bash

HAZELCAST_BRANCH="$1"
rm -rf hazelcast-$HAZELCAST_BRANCH
rm $HAZELCAST_BRANCH.zip*
rm -rf ../hazelcast/downloaded/