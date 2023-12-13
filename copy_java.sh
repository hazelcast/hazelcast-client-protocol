# the output path is the generated "output" folder by this repo. do not add / at the end
OUTPUT_PATH=$1
# path of hazelcast folder that have pom.xml (hazelcast-root). do not add / at the end
HZ_PATH=$2

cp -r $OUTPUT_PATH/java/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/* $HZ_PATH/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/
cp -r $OUTPUT_PATH/java/hazelcast/src/test/java/com/hazelcast/client/protocol/compatibility/* $HZ_PATH/hazelcast/src/test/java/com/hazelcast/client/protocol/compatibility/
cp -r $OUTPUT_PATH/java/hazelcast/src/test/resources/* $HZ_PATH/hazelcast/src/test/resources/