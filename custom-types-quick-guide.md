# Custom Types Quick Guide

_Abstract._ We will go over the steps required to extend an existing service with a new API. The
focus is on covering the details with respect to the client protocol and its related components. We
will not cover the underlying logic of the API itself. We use Java as the subject language for code
generation. The [README](README.md) covers the general framework, so please read that first.

## Adding a Service API

Let us take the `DynamicConfig.yaml` service as the baseline for an example. We will add a
fictitious method: `addUsefulConfig`.

_Note_. At the time of writing the highest `id` in `DynamicConfig.yaml` was `18` -- the `id` of the
last entry, hence the use of `19` for our example.

_Note._

```yaml
- id: 19
  name: addUsefulConfig
  since: 2.7
  doc: |
    Adds a useful configuration.
  request:
    retryable: false
    partitionIdentifier: -1
    params:
      - name: name
        type: String
        nullable: false
        since: 2.7
        doc: |
          The configuration name.
      - name: serviceAConfig
        type: ServiceAConfig
        nullable: false
        since: 2.7
        doc: |
          Configuration for Service A.
      - name: serviceBConfig
        type: ServiceBConfig
        nullable: false
        since: 2.7
        doc: |
          Configuration for Service B.
  response: {}
```

We have 3 fields in this new `addUsefulConfig` API:

- `name` which is a `String`. This is trivial so we won't touch on this again.
- `serviceAConfig` which is a `ServiceAConfig` -- a custom type we will create shortly.
- `serviceBConfig` which is a `ServiceBConfig` -- a custom type we will create shortly.

We have two custom types here: `ServiceAConfig` will model a Java configuration type that is defined
by standard language types, e.g. `int`, `String`, etc. By contrast, `ServiceBConfig` will be defined
by framework specific types that don't have a direct mapping in other target languages.

If we run `./generator.py` we will get some `dict` lookup errors because we've referenced some
custom types. In `Custom.yaml` we'll append the following:

```yaml
- name: ServiceAConfig
  since: 2.7
  params:
    - name: address
      type: String
      nullable: false
      since: 2.7
    - name: port
      type: int
      nullable: false
      since: 2.7
- name: ServiceBConfig
  since: 2.7
  params:
    - name: address
      type: String
      nullable: false
      since: 2.7
    - name: addressParser
      type: Data
      nullable: false
      since: 2.7
```

Open `schema/protocol-schema.json` and append to the array `definitions.param.properties.type.enum`
the string literals: `ServiceAConfig` and `ServiceBConfig`.

Now we need to define the corresponding domain types in Java that these custom types will map-to.
Let us consider the following existing `ServiceAConfig` and `ServiceBConfig` classes that already
exist and which cannot be modified for reasons of backwards compatibility.

```java
public final class ServiceAConfig {
    private final String address;
    private final int port;

    public ServiceAConfig(String address, int port) {
        this.address = address;
        this.port = port;
    }

    public String getAddress() {
        return address;
    }

    public int getPort() {
        return port;
    }
}

public final class ServiceBConfig {
    private final String address;
    private final AddressParser parser;

    public ServiceBConfig(String address, AddressParser parser) {
        this.address = address;
        this.parser = parser;
    }

    public String getAddress() {
        return address;
    }

    public AddressParser getParser() {
        return parser;
    }
}
```

`ServiceAConfig` has a simple mapping to its Java domain type; however, `ServiceBConfig` uses `Data`
as its type for `parser` and not `AddressParser`: this is to show an example where a configuration
carries something that is specific to the target language -- in this case an `AddressParser` which
cannot be represented in the client protocol, hence it being `Data`. You don't need to know anything
about `AddressParser` but that it implements `IdentifiableDataSerializable` and can therefore be
deserialized. For `ServiceBConfig` we must create an intermediate domain type, a so-called holder.

```java
public final class ServiceBConfigHolder {
    private final String address;
    private final Data addressParser;

    public ServiceBConfigHolder(String address, Data addressParser) {
        this.address = address;
        this.addressParser = addressParser;


    public String getAddress() {
        return address;
    }

    public Data getAddressParser() {
        return addressParser;
    }
}
```

The `ServiceBConfigHolder` is the same as `ServiceBConfig` Java class with the exception that we
have made `addressParser` now the opaque `Data` type.

With the boilerplate in-place we can now add the following to `java/__init__.py`'s
`_java_types_common` dictionary:

```python
    "ServiceAConfig": "com.hazelcast.config.ServiceAConfig",
    "ServiceBConfig": "com.hazelcast.config.ServiceBConfigHolder"
```

Note that the values are the coordinates of the configuration classes presented earlier.

Now, you should be able to run `./generator.py` successfully. Ignore binary compatibility error
warnings for now.

## Integrating Generated Codecs

The generator will create 3 assets:

- `output/java/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/DynamicConfigAddUsefulConfigCodec.java`
- `output/java/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/custom/ServiceAConfigCodec.java`
- `output/java/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/custom/ServiceBConfigCodec.java`

These need to be copied to the Hazelcast project under `com.hazelcast.client.impl.protocol.codec`
for the `DynamicConfigAddUsefulConfigCodec.java` and under
`com.hazelcast.client.impl.protocol.codec.custom` for `ServiceAConfigCodec.java` and resp.
`ServiceBConfigCodec.java`.

At this point you are pretty much done with `ServiceAConfig` as the generated code will
automatically map the protocol type to your domain type. However, for `ServiceBConfig` you need to
deserialize `addressParser` `Data` field into an actual `AddressParser` and then manually
instantiate your `ServiceBConfig` type.

For many examples of how this is done I recommend looking at
`ClientDynamicClusterConfig#addWanReplicationConfig` which shows mapping of the domain types to
their respective holder types on the way out to the server; and `AddWanReplicationConfigTask` which
shows the mapping of holder types to their respective configuration types. This example covers most
scenarios you would encounter.

## Binary Compatibility Tests

The generator produces binary compatibility tests. Currently this step will be broken if you have
followed the steps. To fix the errors add the following to `binary/__init__.py`'s
`CustomConfigTypes` list:

```python
    "ServiceAConfig",
    "ServiceBConfig"
```

Now also add the following to `binary/util.py`'s `reference_objects_dict`:

```python
    'ServiceAConfig': 'aServiceAConfig',
    'ServiceBConfig': 'aServiceBConfig',
```

These are the names to which the generated tests will refer to an instance of the respective type.

You will need to copy the artifacts of the API version you just added to, in our case 2.7 to the
Hazelcast project under the paths listed.

- `output/java/hazelcast/src/test/resources/2.7.protocol.compatibility.binary`
- `output/java/hazelcast/src/test/resources/2.7.protocol.compatibility.null.binary`
- `output/java/hazelcast/src/test/java/com/hazelcast/client/protocol/compatibility/ClientCompatibilityNullTest_2_7.java`
- `output/java/hazelcast/src/test/java/com/hazelcast/client/protocol/compatibility/ClientCompatibilityTest_2_7.java`
- `output/java/hazelcast/src/test/java/com/hazelcast/client/protocol/compatibility/MemberCompatibilityNullTest_2_7.java`
- `output/java/hazelcast/src/test/java/com/hazelcast/client/protocol/compatibility/MemberCompatibilityTest_2_7.java`

If you open the test files up in your IDE you will see some reference errors for `aServiceAConfig`
and `aServiceBConfig`. For example, if you were to open `ClientCompatibilityTest_2_7.java`. You must
add these to `com.hazelcast.client.protocol.compatibility.ReferenceObjects` in the Hazelcast
project. If you need a `String` when creating instances of `ServiceAConfig` or `ServiceBConfig` you
should use `aString` and likewise for other basic types. You should follow this naming strategy when
adding your new instances. For example, in `ReferenceObjects.java`:

```java
    // ...
    public static final ServiceAConfig aServiceAConfig = new ServiceAConfig(aString, anInt);
    public static final ServiceBConfigHolder aServiceBConfig = new ServiceBConfigHolder(aString, aData);
```

Note `aString`, `anInt` and `aData` were already defined. With this change you should be able to run
all the new compatibility tests. But they will fail. The final step is to make sure that the domain
types that you map-to from your protocol definition, i.e. `ServiceAConfig.java` and
`ServiceBConfigHolder.java` define an appropriate `equals` and `hashCode`. With these changes the
tests will pass.
