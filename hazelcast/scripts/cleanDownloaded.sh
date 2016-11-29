#!/usr/bin/env bash

HAZELCAST_BRANCH="${1//\//-}"   # finds directory name by replacing `/` with `-` (e.g. `fix/3.8/abc` will become `fix-3.8-abc`)
rm $HAZELCAST_BRANCH.zip*

if([[ $HAZELCAST_BRANCH == v* ]])
then
   HAZELCAST_BRANCH=${HAZELCAST_BRANCH:1}
fi

rm -rf hazelcast-$HAZELCAST_BRANCH
rm -rf ../hazelcast/downloaded/