# Hazelcast Open Binary Client Protocol

**Hazelcast Open Binary Client Protocol** definitions and code generator for multiple programming languages.

## Hazelcast Open Binary Client Protocol Definitions

The protocol is defined in `protocol-definitions/*.yaml` yaml files where each yaml file represents a service like Map, List, Set etc. 
Custom data types that are used in the protocol definitions are defined in `protocol-definitions/custom/Custom.yaml`.

## Service definition

A service is defined by a separate YAML file, containing all its method definitions.

```yaml
id: Service Id (0-255)
name: Service Name
methods:
  - id: METHOD-ID-1 (1-255)
    name: METHOD-NAME-1
    ...
  - id: METHOD-ID-2 (1-255)
    name: METHOD-NAME-2
    ...
```

A method(aka Remote method call) is defined by a request-response pair and an optional events section.

A basic method structure example:

```yaml
  - id: METHOD-ID-1 (1-255)
    name: METHOD-NAME-1
    since: 2.0
    doc: |
       Documentation of the method call
    request:
      retryable: false
      partitionIdentifier: None
      params:
        - name: parameter1
          type: String
          nullable: false
          since: 2.0
          doc: |
             Documentation of the parameter 1
        - name: parameter1
          type: Data
          nullable: false
          since: 2.0
          doc: |
             Documentation of the parameter 2
    response:
      params:
        - name: response parameter 1
          type: Data
          nullable: true
          since: 2.0
          doc: |
             the response parameter 1

    #Optional events section
    events: 
      - name: Event-1
        params:
          - name: event-param-1
            type: Data
            nullable: true
            since: 2.0
            doc: |
              Documentation of the event parameter 1
          - name: value
            type: Data
            nullable: true
            since: 2.0
            doc: |
              Documentation of the event parameter 2

```

Please refer to [schema](schema/protocol-schema.json) for details of a service definition.

## Code Generator

The new protocol generator generates the related language codecs into the configured folder. It does not depend on Hazelcast repo.

### Setup

You need to have python3 configured on your `PATH`. After cloning the repository, install the python library dependencies:

```bash
pip3 install -r requirements.txt
```

### Code Generation

You can generate codecs for a specific language by calling,

```bash

./generator.py [-r ROOT_DIRECTORY] [-l LANGUAGE] [-p PROTOCOL_DEFS_PATH] [-o OUTPUT_DIRECTORY] [-n NAMESPACE] [-b BINARY_OUTPUT_DIR] [-t TEST_OUTPUT_DIR] [--no-binary] [--no-id-check]

```

where 

* `ROOT_DIRECTORY` is the root folder for the generated codecs. If left empty, default value is set to `./output/[LANGUAGE]`.

* `LANGUAGE` is one of 
    * `java` : Java
    * `cpp` : C++
    * `cs` : C#
    * `py` : Python
    * `ts` : TypeScript
    * `go` : Go
     
`java` is the default value if no language is specified.

* `PROTOCOL_DEFS_PATH` is the directory containing the `yaml` definitions of the protocol. If left empty, 
this value is defaulted to the `./protocol-definitions`. If the protocol definitions on the custom directory use
some custom types, a YAML file named `Custom.yaml` must be put inside the `PROTOCOL_DEFS_PATH/custom` directory. 
For the details of the custom type definition, see the [Custom Types](#custom-types) section.

* `OUTPUT_DIRECTORY` is the output directory for the generated codecs relative to the `ROOT_DIRECTORY`. If left empty,
this is inferred from the selected `LANGUAGE`. 
Default values are chosen according to the directories used by the Hazelcast clients.

* `NAMESPACE` is the namespace for the generated codecs. If left empty, default value is inferred from the selected `LANGUAGE`. 

* `BINARY_OUTPUT_DIR` is the output directory relative to the `ROOT_DIRECTORY` that is used for the binary files for the binary compatibility tests.
When left empty, default value is inferred from the selected `LANGUAGE`.

* `TEST_OUTPUT_DIR` is the output directory relative to the `ROOT_DIRECTORY` that is used for the test files for the binary compatibility tests.
Default value is inferred from the selected `LANGUAGE`.


* `--no-binary` flag restrains the generator from creating binary and test files for the binary compatibility tests.

* `--no-id-check` flag restrains the generator from checking sequentiality of service and method ids of protocol definitions.

If you want to generate the Java codecs into your development repo, and let's assume your local Hazelcast git repo is at 
`~/git/hazelcast/` then you can run the following command:

```bash
./generator.py -r ~/git/hazelcast/
```

This command generates the codecs at the `ROOT_DIRECTORY/OUTPUT_DIRECTORY` which is `~/git/hazelcast/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/`.
See that the `OUTPUT_DIRECTORY` is inferred from the language, namely `hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/` for `java`. 

If you want to specify an output directory relative to the root directory, you can run the following command:

```bash
./generator.py -r ~/git/hazelcast/ -o custom/out 
```

This command will generate the codecs at the `~/git/hazelcast/custom/out`.

### Schema Validation

The protocol definitions should validate against the [schema](schema/protocol-schema.json). You can configure your IDE to 
use this schema to validate and provide auto code completion.

The generator also uses this schema during the code generation for validation purposes. It stops and reports any schema violation to the console.

### Custom Types

If you are going to use a custom type,i.e., a complex type that is not defined in the [currently supported types](binary/__init__.py),  
as the type of your parameters in the protocol definitions, you need to define how to encode and decode this in the protocol level.

A custom type definition has the following structure:

```yaml
customTypes:
    - name: CustomType1
      since: 2.0
      returnWithFactory: true # optional
      params:
        - name: paramName1
          type: boolean
          nullable: false
          since: 2.0
        - name: paramName2
          type: String
          nullable: true
          since: 2.0
```

With this definition, the code generator generates a custom codec for your type and 
calls its encode/decode methods when encoding/decoding the parameters with this custom type. 
There are a few points to consider as described below. 

The codec for the custom type accesses the parameters defined in `params` using a 
predefined getter pattern in its encode method. These patterns are specific to each `LANGUAGE`.

For example, for the `java`, if the parameter is a `boolean` it is accessed as `customType1.isParamName1()`.
For other types `customType1.getParamName2()` pattern is used. So, make sure that your custom type satisfies 
this getter contract.

For the decode method of the custom type codec, there are two ways to generate
an instance of the custom type. Default way is constructing the object using a constructor
with parameters defined in the `params` in the order of their definition. For example, by default
the instance of `CustomType1` is created with the `new CustomType1(paramName1, paramName2)` expression.

If the custom type does not have a public constructor that takes the defined parameters in the order
of their definition, then you need to write a factory method to generate the object from these parameters.
To use a factory method as a way to create the custom type, you should set the `returnWithFactory` option to `true`.

Then, depending on the selected `LANGUAGE`, a custom factory method is called to create the object.

For example, for `java`, `CustomTypeFactory.createCustomType1(paramName1, paramName2)` method is called.
You need to add the `CustomType1 createCustomType1(boolean paramName1, String paramName2)` method to the `CustomTypeFactory` class on the Hazelcast side.

For the parameters of the custom type definition, an extra step is required for the enum types. 
Enums are represented as integers in the protocol level. So, you need to specify the type as `int` in the protocol
definition and add an `encodeInt` method to the `FixedSizeTypesCodec` for the enum type that performs the conversion
if the enums are not represented by integers in the language you try to generate codecs for. 
Also, you need to set `returnWithFactory` to `true` and add a factory method as described above if the conversion from 
enum type to int is required. In the factory method, you will receive an integer for the enum and be expected to 
convert it to your enum type and construct the object with it.

Custom type definitions are also validated against a [schema](/schema/custom-codec-schema.json). See the [Schema Validation](#schema-validation) 
section for details of the validation.

### Expanding the Client Protocol

Client protocol can be expanded by adding new
* services
* methods
* parameters to existing method requests, responses or events
* events to existing methods
* custom types
* parameters to existing custom types

While expanding the protocol, one needs to follow these simple guidelines:
* `since` field of the protocol definitions of the the newly added parameters, methods, events and custom types should 
be equal to the current protocol version. 
* New services should have the id of the 1 + the highest id of the existing services.
* New methods should come after the existing methods on the protocol definitions and have the id of the 1 + the id 
of the method that comes before it.
* New request, response or event parameters should come after the existing parameters on the protocol definitions 
and they should be in the increasing order of the protocol versions that is 2.1 parameters should follow 
2.0.1 parameters which should follow 2.0 parameters.
* New parameters to custom types should come after the existing parameters on the protocol definitions and they should
be in the increasing order of protocol versions as described above.
* Although not necessary, new events or custom types should come after the existing custom types or events on the 
protocol definitions.
 