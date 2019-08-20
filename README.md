# Hazelcast Open Binary Client Protocol

**Hazelcast Open Binary Client Protocol** definitions and code generator for multiple programming languages.

## Hazelcast Open Binary Client Protocol Definitions

The protocol is defined in `protocol-definitions/*.yaml` yaml files where each yaml file represents a service like Map, List, Set etc.

## Service definition

A service is defined by a separate YAML file, containing all its method definitions.

```yaml
id: Service Id (1-255)
name: Service Name
methods:
  - id: METHOD-ID-1 (1-255)
    name: METHOD-NAME-1
    ...
  - id: METHOD-ID-2 (1-255)
    name: METHOD-NAME-2
    ...
```

A method(aka Remote method call) is defined by a request-response pair. If the method definition

A basic method structure example:

```yaml
  - id: METHOD-ID-1 (1-255)
    name: METHOD-NAME-1
    since: 2.0
    doc: |
       Documentation of the method call
    request:
      retryable: false
      acquiresResource: false
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

The new protocol generator, generates the related language codecs into the configured folder. It does not depend on hazelcast repo.

### Setup

You need to have python3 configured on your `PATH`. After cloning the repository, install the python library dependencies:

```bash
pip3 install -r requirements.txt
```

### Code Generation

You can generate codecs for your favorite language by calling,

```bash

./generator.py [-r ROOT_DIRECTORY] [-l LANGUAGE] [-p PROTOCOL_DEFS_PATH] [-o OUTPUT_DIRECTORY]

```

where 

* `ROOT_DIRECTORY` is the root folder. If left empty, default value is `./output/[LANGUAGE]`.
* `LANGUAGE` is one of 
    * `JAVA` : Java
    * `CPP` : C++
    * `CS` : C#
    * `PY` : Python
    * `TS` : Typescript
    * `GO` : Go
     
`JAVA` will be the default value if left empty.

* `PROTOCOL_DEFS_PATH` is the directory containing the `yaml` definitions of the protocol. If left empty, 
this value will be defaulted to the `./protocol-definitions`

* `OUTPUT_DIRECTORY` is the output directory for the generated codecs relative to the `ROOT_DIRECTORY`. If left empty,
this will be inferred from the selected `LANGUAGE`. 

If you want to generate java codecs into your development repo, and let's assume your local hazelcast git repo is at 
`~/git/hazelcast/` then you can call,

```bash
./generator.py -r ~/git/hazelcast/
```

to generate the codecs at the `ROOT_DIRECTORY/OUTPUT_DIRECTORY` which is `~/git/hazelcast/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/`.
See that the `OUTPUT_DIRECTORY` is inferred from the language, namely `hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/` for `JAVA`. 

If you want to specify an output directory relative to the root directory, you can call

```bash
./generator.py -r ~/git/hazelcast/ -o custom/out 
```

This command will generate the codecs at the `~/git/hazelcast/custom/out`.

### Schema Validation

The protocol definitions should validate against the [schema](schema/protocol-schema.json). You can configure your favorite IDE to 
use this schema to validate and provide autocompletion.

The generator also uses this schema during code generation. It will report any schema problem on the console.

 
