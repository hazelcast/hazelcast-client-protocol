PYTHON=/c/Python37/python.exe
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROTOCOL_DIR="$( dirname $SCRIPT_DIR )"

pushd $PROTOCOL_DIR

# generate codecs
$PYTHON ./generator.py -l cs --no-binary

# note: codec files contain the client-side methods, along with the
# server-side methods enclosed in '#if SERVER_CODEC' blocks. files are
# copied to the client project, which uses them raw, and linked into
# the testing projects, which defines SERVER_CODEC.

# wipe existing codecs in the C# repository
rm -rf ../src/Hazelcast.Net/Protocol/Codecs/*.cs
rm -rf ../src/Hazelcast.Net/Protocol/CustomCodecs/*.cs

# copy generated codecs to the C# repository
cp output/cs/src/Hazelcast.Net/Protocol/Codecs/*.cs ../src/Hazelcast.Net/Protocol/Codecs/
cp output/cs/src/Hazelcast.Net/Protocol/CustomCodecs/*.cs ../src/Hazelcast.Net/Protocol/CustomCodecs/

# NOTE
# for now, we don't have server-side custom codecs, so no src/Hazelcast.Net.Testing/Protocol/CustomCodecs/
# should we have them, we'd need to make sure that the server-side non-custom codecs *do* use them

# clear generated codecs that we'd rather ignore for now
find ../src -name Atomic*ApplyCodec.cs | xargs -d '\n' rm
find ../src -name Atomic*AlterCodec.cs | xargs -d '\n' rm
find ../src -name CPSession*Codec.cs | xargs -d '\n' rm
find ../src -name CPSubsystem*Codec.cs | xargs -d '\n' rm
find ../src -name CPMember*Codec.cs | xargs -d '\n' rm
find ../src -name Fenced*Codec.cs | xargs -d '\n' rm
find ../src -name CountDownLatch*Codec.cs | xargs -d '\n' rm
find ../src -name Semaphore*Codec.cs | xargs -d '\n' rm
find ../src -name MultiMapPutAllCodec.cs | xargs -d '\n' rm
find ../src -name ClientRemoveMigrationListenerCodec.cs | xargs -d '\n' rm

popd