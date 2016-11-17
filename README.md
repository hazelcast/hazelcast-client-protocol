# hazelcast-client-protocol

This project generates code of client protocol accross languages.

## Output directory of generated classes

    hazelcast-client-protocol/hazelcast/target/generated-sources/annotations

## To generate java classes and hazelcast-client-protocol.jar

    mvn clean compile

We have code generation for some other languages as well. 

## To generate for other languages
 
    mvn clean compile -Dhazelcast.generator.[LANGUAGE]=TRUE 

Supported options for [LANGUAGE] are 

1. cpp (C++) 
2. cs  (C#) 
3. py (python)
4. md (documentation of protocol)
5. node (Node.js)

To generate for another custom languages, an ftl file with 
`codec-template-[LANGUAGE].ftl` needs to be added to  
hazelcast-client-protocol/hazelcast-code-generator/src/main/resources
  
For ftl see,  
http://freemarker.incubator.apache.org/

After putting the ftl file, following command can be run to generate sources

    mvn clean compile -Dhazelcast.generator.[LANGUAGE]=TRUE
    
## How To Generate Java Compatibility Tests
Use the following command to generate the compatibility tests
    `mvn clean compile -DskipTests -Dprotocol.compatibility.generate.tests=true`
This will generate the compatibility tests inside the ./hazelcast/target/generated-sources/annotations/com/hazelcast/client/protocol/compatibility folder.
Please note that the compilation will fail but the tests will be generated. You can copy the tests from here to hazelcast repository.
