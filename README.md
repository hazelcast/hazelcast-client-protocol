# hazelcast-client-protocol

This project generates code of client protocol accross languages.

## Templates that codes are generated from

    hazelcast/src/main/java/com/hazelcast/client/impl/protocol/template/

## How to add a new message

    /**
     * ALL MESSAGES MUST HAVE JAVADOC
     *
     * @param name          name of the map
     * @param id            id
     * @param localOnly     if true fires events that originated from this node only, otherwise fires all events
     * @return A unique string which is used as a key to remove the listener.
     */
    @Request(id = 69, retryable = false, response = ResponseMessageConst.STRING,
            event = {EventMessageConst.EVENT_MEMBER, EventMessageConst.EVENT_IMAPBATCHINVALIDATION})
    @Since("1.4")
    Object exampleAddListener(String name, int regId, @Since("1.5") boolean localOnly);


- javadoc

A detailed javadoc is important since we are generating a protocol documentation from these javadocs.


- id

Messages have unique id's within its corresponding template class. They are given incrementally.
A new message is always added to at the end of the template class. Its id is one more of the message above it.  

- retryable

If message will do a read-only or idempotent task on the server we mark it as retryable = true, otherwise false.

- response

Type of the response of this message from server.  An existing type can be chosen from / or a new one can be added.
Following two classes contains response types and definitions. 

    /hazelcast/src/main/java/com/hazelcast/client/impl/protocol/constants/ResponseMessageConst.java
    /hazelcast/src/main/java/com/hazelcast/client/impl/protocol/template/ResponseTemplate.java

Note that return value of `exampleAddListener` is Object. This type is not used when generating protocol. 


- event

This field is optional. And it is list of event types. 
If message is a listener registration, and sends events, event types is described here. 

An existing type can be chosen from / or a new one can be added.
Following two classes contains event types and definitions. 

    /hazelcast/src/main/java/com/hazelcast/client/impl/protocol/constants/EventMessageConst.java
    /hazelcast/src/main/java/com/hazelcast/client/impl/protocol/template/EventResponseTemplate.java

- Since tag on message 

A message itself or its parameters can have since tag. If tag is omitted from message it means @Since("1.0")

Version should be given accordingly to the version of protocol. Protocol version can be found in master pom.xml

Example : <version>1.6.0-13</version>

This means that next release of protocol will be 1.6. Since tag should be as follows `@Since("1.6")`

- Since tag on parameters

New parameters can be added to a message. It is always added at the end of parameter list.

Old parameters can not be deleted or their types can not be modified. 

When adding a new parameter, if version we add new parameter is same as message introdued @Since tag can be omitted.
If parameter is added in a new version, then @Since tag should be added in front of parameter type. 

- name of the message

Name of the message codec is given via function name . It is `exampleAddListener` in this example.

## Output directory of generated classes

    hazelcast-client-protocol/hazelcast/target/generated-sources/annotations

## To generate java classes and hazelcast-client-protocol.jar 

    mvn clean compile

Code generation needs to download an existing hazelcast and compile against it. Following properties from master
`pom.xml` are used to find a hazelcast branch. 

    <hazelcast.git.repo>hazelcast</hazelcast.git.repo>
    <hazelcast.git.branch>master</hazelcast.git.branch>

If you want to generate code against a specific branch of yours, replace them accordingly as follows:

    <hazelcast.git.repo>YOUR_GIT_USER_NAME</hazelcast.git.repo>
    <hazelcast.git.branch>YOUR_BRANCH</hazelcast.git.branch>
    
This is especially useful when you modify (add field to) an existing message. In that case, this repo can not be 
compiled against hazelcast/master, because generated codecs has a field missing in some methods.  To solve this,
you need to put your development branch here, so that we can verify generated codecs and development branches are consistent.     

After giving correct branch, `mvn clean install` can be used to install jar locally. To test your branch locally,
you can change the version in master pom.xml of hazelcast project.

        <client.protocol.version>1.6.0-12</client.protocol.version>
 
For your hazelcast development branch to be ready(pass the tests in pr builder), first new version of 
hazelcast-client-protocol needs to be released. Contact clients team to request a new release. 
After hazelcast-client-protocol released. 

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
