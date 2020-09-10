PYTHON=/c/Python37/python.exe
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROTOCOL_DIR="$( dirname $SCRIPT_DIR )"

pushd $PROTOCOL_DIR

$PYTHON ./generator.py -l cs --no-binary

rm -rf ../src/Hazelcast.Net/Protocol/Codecs/*.cs
rm -rf ../src/Hazelcast.Net/Protocol/CustomCodecs/*.cs
cp output/cs/src/Hazelcast.Net/Protocol/Codecs/*.cs ../src/Hazelcast.Net/Protocol/Codecs/
cp output/cs/src/Hazelcast.Net/Protocol/CustomCodecs/*.cs ../src/Hazelcast.Net/Protocol/CustomCodecs/

rm -rf ../src/Hazelcast.Net.Testing/Protocol/Codecs/*.cs
cp output/cs/src/Hazelcast.Net/Protocol/Codecs/*.cs ../src/Hazelcast.Net.Testing/Protocol/Codecs/
#rm -rf ../src/Hazelcast.Net.Testing/Protocol/CustomCodecs/*.cs
#cp output/cs/src/Hazelcast.Net/Protocol/CustomCodecs/*.cs ../src/Hazelcast.Net.Testing/Protocol/CustomCodecs/

# NOTE
# for now, we don't have server-side custom codecs, so no src/Hazelcast.Net.Testing/Protocol/CustomCodecs/
# should we have them, we'd need to make sure that the server-side non-custom codecs *do* use them

# TEMP
find ../src -name CP*Codec.cs | xargs -d '\n' rm
find ../src -name Atomic*Codec.cs | xargs -d '\n' rm
find ../src -name Fenced*Codec.cs | xargs -d '\n' rm
find ../src -name CountDownLatch*Codec.cs | xargs -d '\n' rm
find ../src -name Semaphore*Codec.cs | xargs -d '\n' rm
#find ../src -name EndpointQualifierCodec.cs | xargs -d '\n' rm
find ../src -name MultiMapPutAllCodec.cs | xargs -d '\n' rm

popd