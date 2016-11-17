#!/usr/bin/env bash

HAZELCAST_BRANCH="$1"
HAZELCAST_BRANCH="distributed_scheduled_exec"
rm $HAZELCAST_BRANCH.zip*

if([[ $HAZELCAST_BRANCH == v* ]])
then
   HAZELCAST_BRANCH=${HAZELCAST_BRANCH:1}
fi

rm -rf hazelcast-$HAZELCAST_BRANCH
rm -rf ../hazelcast/downloaded/