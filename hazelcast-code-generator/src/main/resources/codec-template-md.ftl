# Protocol Messages

## Compound Data Types Used In The Protocol Specification
Some common compound data structures used in the protocol message specification are defined in this section.

### Array
In the protocol specification, an array of a data type is frequently used. An array of a data type with n entries 
is encoded as shown below:

|Field|Type|Nullable|Description|
|-----|----|---------|----------|
|Length|int32|No|The length of the array.|
|Entry 1|provided data type|No|First entry of the array|
|Entry 2|provided data type|No|Second entry of the array|
|...|...|...|...|
|...|...|...|...|
|Entry n|provided data type|No|n'th entry of the array|

### Address Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Host|string|No|The name or the IP address of the server member|
|Port|int32|No|The port number used for this address|

### Cache Event Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Cache Event type|int32|No|The type of the event. Possible values and their meanings are:<br> CREATED(1):An event type indicating that the cache entry was created. <br>UPDATED(2): An event type indicating that the cache entry was updated, i.e. a previous mapping existed. <br>REMOVED(3): An event type indicating that the cache entry was removed. <br>EXPIRED(4): An event type indicating that the cache entry has expired.<br>EVICTED(5): An event type indicating that the cache entry has evicted. <br>INVALIDATED(6): An event type indicating that the cache entry has invalidated for near cache invalidation. <br>COMPLETED(7): An event type indicating that the cache operation has completed. <br>EXPIRATION_TIME_UPDATED(8): An event type indicating that the expiration time of cache record has been updated
|Name|string|No|Name of the cache|
|Key|byte-array|Yes|Key of the cache data|
|Value|byte-array|Yes|Value of the cache data|
|Old Value|byte-array|Yes|Old value of the cache data if exists|
|isOldValueAvailable|boolean|No|True if old value exist|

### Cache Simple Entry Listener Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Synchronous|boolean|No|If true, this cache entry listener implementation will be called in a synchronous manner.|
|OldValueRequired|boolean|No|If true, previously assigned values for the affected keys will be sent to this cache-entry-listener implementation.|
|EntryListenerFactory|string|Yes|Class name of a javax.cache.configuration.Factory for CacheEntryListener|
|EntryEventFilterFactory|string|Yes|Class name of a javax.cache.configuration.Factory for CacheEntryEventFilter|

### Distributed Object Info Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Service Name|string|No|Name of the service for the distributed object. <br>E.g. this is "hz:impl:cacheService" for Cache object|
|Name|string|No|Name of the object|

### Entry View Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Key|byte-array|No|Key of the entry|
|Value|byte-array|No|Value of the entry|
|Cost|int64|No|Cost of the entry|
|Creation Time|int64|No|Time when the entry is created|
|Expiration Time|int64|No|Time when the entry will expiry|
|Hits|int64|No|Number of hits|
|Last Access Time|int64|No|Time when entry is last accessed|
|Last Stored Time|int64|No|Time when entry is last stored|
|Last Update Time|int64|No|Time when entry is last updated|
|Version|int64|No|Version of the entry|
|Eviction Criteria Number|int64|No|The number of the eviction criteria applied|
|ttl|int64|No|Time to live for the entry|

### Eviction Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Size|int32|No|Size used by max size policy to determine whether eviction is required. The interpretation of the value depends on the configured Max Size Policy.|
|MaxSizePolicy|string|No|Maximum size policy. Valid values are: <br>"ENTRY_COUNT": Policy based on maximum number of entries stored per data structure<br>"USED_NATIVE_MEMORY_SIZE": used native memory in megabytes per data structure on each Hazelcast instance<br>"USED_NATIVE_MEMORY_PERCENTAGE": maximum used native memory percentage per data structure on each Hazelcast instance<br>"FREE_NATIVE_MEMORY_SIZE": minimum free native memory in megabytes per Hazelcast instance<br>"FREE_NATIVE_MEMORY_PERCENTAGE": minimum free native memory percentage per Hazelcast instance|
|EvictionPolicy|string|No|Eviction policy determines how eviction candidates are picked. Valid values are:<br>"LRU": Least Recently Used<br>"LFU": Least Frequently Used<br>"NONE": no eviction<br>"RANDOM": evict randomly|
|ComparatorClassName|string|Yes|Class name of the configured EvictionPolicyComparator implementation|
|Comparator|byte-array|Yes|Serialized instance of EvictionPolicyComparator implementation|

### Hot Restart Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Enabled|boolean|No|Indicates whether hot restart is enabled|
|Fsync|boolean|No|When true, disk writes should be followed by an fsync() system call|

### Job Partition State Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Owner Address|Address|No|The address of the partition owner|
|State value|string|No|Value of the partition state. Possible values are:<br>"WAITING": Partition waits for being calculated. <br>"MAPPING": Partition is in mapping phase. <br>"REDUCING": Partition is in reducing phase (mapping may still not finished when this state is reached since there is a chunked based operation underlying). <br>"PROCESSED": Partition is fully processed <br>"CANCELLED": Partition calculation cancelled due to an internal exception

### Listener Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Listener type|uint8|no|Indicates the type of listener configuration. Possible values:<br>0 : Generic Listener<br>1 : Item Listener<br>2 : Entry Listener<br>3 : Quorum Listener<br>4 : Cache Partition Lost Listener<br>5 : Map Partition Lost Listener|
|Listener implementation|byte-array|Yes|A serialized instance of the actual listener implementation. Just one of "Listener implementation" and "Listener class name" should be not null.|
|Listener class name|string|Yes|The class name of a listener class, to be instantiated and used as a listener. Just one of "Listener implementation" and "Listener class name" should be not null.|
|Local|boolean|No|When true, the listener only receives events from the local member, otherwise cluster-wide events are delivered to the listener.|
|IncludeValue|boolean|No|When true, the value associated with the event must be included in the event.|

### Map Attribute Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Name|string|No|The name given to an attribute that is going to be extracted|
|Extractor|string|No|Full class name of the extractor e.g. {@code com.example.car.SpeedExtractor}|

### Map Index Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Attribute|string|No|Attribute to be indexed|
|Ordered|boolean|No|When true, indicates that the index will be ordered, otherwise unsorted|

### Map Store Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Enabled|boolean|No|True to enable this map-store, false to disable.|
|Write Coalescing|boolean|No|Setting this is meaningful if you are using write behind in MapStore. When write-coalescing is true, only the latest store operation on a key in the write-delay-seconds time-window will be reflected to MapStore.|
|Write Delay Seconds|int32|No|The number of seconds to delay the store writes.|
|Write Batch Size|int32|No|The number of operations to be included in each batch processing round.|
|Initial Load Mode|string|No|Sets the initial load mode. Valid values:<br>"LAZY": load is asynchronous.<br>"EAGER": load is blocked till all partitions are loaded.|
|Properties|Properties Data Type|No|Zero or more key-value pairs, which may be used to configure the map store implementation.|
|Class name|string|Yes|Name of MapStore implementation class.|
|Factory class name|string|Yes|Class name of a com.hazelcast.core.MapStoreFactory implementation to be instantiated and supply map store implementation.|
|MapStore implementation|byte-array|Yes|Serialized MapStore implementation instance.|
|MapStoreFactory implementation|byte-array|Yes|Serialized MapStoreFactory implementation instance.|

### Member Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Address|Address|No|Address of the member server|
|Uuid|string|No|Unique user id of the member server|
|isLiteMember|boolean|No|true if the server member is a liter server, false otherwise|
|attribute 1 name|string|No|Name of the attribute 1|
|attribute 1 value|string|No|Value of the attribute 1|
|attribute 2 name|string|No|Name of the attribute 2|
|attribute 2 value|string|No|Value of the attribute 2|
|...|...|...|...|
|...|...|...|...|
|attribute n name|string|No|Name of the attribute n|
|attribute n value|string|No|Value of the attribute n|

<br>n is the number of attributes for the server member.

### Near Cache Config Data type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Name|string|No|Name of this near cache config|
|In memory format|string|No|in memory format of values in the near cache. Valid options are "BINARY", "OBJECT" and "NATIVE"|
|SerializeKeys|boolean|No|When false, keys will be maintained in OBJECT format in the near cache, otherwise they will be serialized to "BINARY"|
|InvalidateOnChange|boolean|No|When true, a Hazelcast instance with a Near Cache listens for cluster-wide changes on the entries of the backing data structure and invalidates its corresponding Near Cache entries. Changes done on the local Hazelcast instance always invalidate the Near Cache immediately.|
|TimeToLiveSeconds|int32|No|Maximum number of seconds for each entry to stay in the Near Cache.|
|MaxIdleSeconds|int32|No|Maximum number of seconds each entry can stay in the Near Cache while not touched.|
|CacheLocalEntries|boolean|No|True to also cache local entries, false otherwise|
|LocalUpdatePolicy|string|No|Defines how to reflect local updates to the Near Cache. Valid values are:<br>"INVALIDATE": A local put and local remove immediately invalidates the Near Cache.<br>"CACHE_ON_UPDATE": A local put immediately adds the new value to the Near Cache. A local remove works as in INVALIDATE mode.|
|PreloaderConfig|Near Cache Preloader Config|Yes|Configuration for near cache preloader.|

### Near Cache Preloader Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Enabled|boolean|No|Indicates whether near cache preloader is enabled|
|Directory|string|No|Directory in which near cache keys will be persisted for preloading|
|StoreInitialDelaySeconds|int32|No|Initial delay for the Near Cache key storage|
|StoreIntervalSeconds|int32|No|Interval for the Near Cache key storage (in seconds)|

### Predicate Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|ClassName|string|Yes|Name of Predicate class|
|Sql|string|Yes|SQL query to be used as predicate|
|Implementation|byte-array|Yes|A serialized Predicate instance|

### Properties Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Count|int32|No|Number of key-value pairs in this Properties instance|
|Key1|string|No|Key of first property|
|Value1|string|No|Value of first property|
|Key2|string|No|...|
|Value2|string|No|...|
|...|...|...|...|
|KeyN|string|No|...|
|ValueN|string|No|...|

<br>for Count key-value pairs.

### Query Cache Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|BatchSize|int32|No|After reaching this minimum size, buffered events are sent to QueryCache|
|BufferSize|int32|No|Maximum number of events which can be stored in a buffer of a partition|
|DelaySeconds|int32|No|Minimum number of delay seconds which an event waits in the buffer of node|
|IncludeValue|boolean|No|Flag to enable/disable value caching|
|Populate|boolean|No|Flag to enable/disable initial population of the QueryCache|
|Coalesce|boolean|No|Flag to enable/disable coalescing|
|InMemoryFormat|string|No|Memory format of values of entries in QueryCache. Valid values are:<br>BINARY<br>OBJECT|
|Name|string|No|Name of this QueryCache|
|PredicateConfig|Predicate Config|No|The predicate to filter events which wil be applied to the QueryCache|
|EvictionConfig|Eviction Config|No|Eviction configuration|
|ListenerConfigs|array of Listener Config|Yes|Array of entry listener configurations|
|IndexConfigs|array of Map Index Config|Yes|Array of map index configurations|

### Query Cache Event Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Sequence number|int64|No|The sequence number for the event|
|Key|byte-array|Yes|The key for the event|
|New Value|byte-array|Yes|The new value for the event|
|Event type|int32|No|The type of the event|
|Partition Id|int32|No|The partition id for the event key|

### Query Store Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Queue store config type|uint8|No|Type of queue store configuration. Valid types are:<br>0: queue store is configured with a queue store class name<br>1: queue store is configured with a factory class name<br>2: queue store is configured with a serialized queue store implementation<br>3: queue store is configured with a serialized queue store factory implementation|
|Queue store class name or factory class name (when queue store config type is 0 or 1)|string|No|Class name of a queue store or a queue store factory. Its interpretation depends on the queue store config type. This field only exists when config type is 0 or 1.|
|Serialized queue store instance or queue store factory instance (when queue store config type is 2 or 3)|byte-array|No|Serialized instance of a queue store or queue store factory implementation. Its interpretation depends on the queue store config type. This field only exists when config type is 2 or 3.|
|Properties|Properties Data Type|Yes|Configuration key-value pairs|
|Enabled|boolean|No|Whether queue store is enabled or not|

### Ringbuffer Store Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Ringbuffer store config type|uint8|No|Type of ringbuffer store configuration. Valid types are:<br>0: ringbuffer store is configured with a ringbuffer store's class name<br>1: ringbuffer store is configured with a factory class name<br>2: ringbuffer store is configured with a serialized ringbuffer store implementation<br>3: ringbuffer store is configured with a serialized ringbuffer store factory implementation|
|Ringbuffer store class name or factory class name (when config type is 0 or 1)|string|No|Class name of a ringbuffer store or a ringbuffer store factory. Its interpretation depends on the ringbuffer store config type. This field only exists when config type is 0 or 1.|
|Serialized ringbuffer store instance or ringbuffer store factory instance (when ringbuffer store config type is 2 or 3)|byte-array|No|Serialized instance of a ringbuffer store or ringbuffer store factory implementation. Its interpretation depends on the ringbuffer store config type. This field only exists when config type is 2 or 3.|
|Properties|Properties Data Type|Yes|Configuration key-value pairs|
|Enabled|boolean|No|Whether ringbuffer store is enabled or not|

### Timed Expiry Policy Factory Config Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Expiry policy type|string|No|Type of expiry policy. Valid values are:<br>CREATED: Expiry policy that defines the expiry duration of an entry based on when it was created.<br>MODIFIED: defines the expiry duration of an entry based on the last time it was updated.<br>ACCESSED: as above, but duration is based on the last time the entry was accessed.<br>Touched: an expiry policy that defines the expiry duration of an entry based on when it was last touched (created, accessed or updated).<br>ETERNAL: never expires entries|
|Duration amount|int64|No|Expiry duration as amount of configured time unit|
|Duration time unit|string|No|Duration unit of time. Valid values are NANOSECONDS, MICROSECONDS, MILLISECONDS, SECONDS, MINUTES, HOURS, DAYS|


### Transaction Id Data Type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Format Id|int32|No|The id of the transaction format|
|Global Transaction Id|byte-array|No|The global id for the transaction|
|Branch Qualifier|byte-array|No|The qualifier for the branch|

### Stack Trace Data type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Declaring Class|string|No|The name of the class|
|Method Name|string|No|The name of the method|
|File Name|string|Yes|The name of the java source file|
|Line Number|int32|No|The line number in the source code file|

### WAN Replication Ref Data type
| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Name|string|No|Name of an existing WAN replication config|
|MergePolicy|string|No|Name of a MapMergePolicy or CacheMergePolicy used to resolve conflicts that occur when target cluster already has the replicated entry key.|
|RepublishingEnabled|boolean|No|When true, WAN events are republished|
|Filters|array of string|Yes|Name of class implementing com.hazelcast.cache.wan.filter.CacheWanEventFilter or com.hazelcast.map.wan.filter.MapWanEventFilter for filtering WAN replication events|

## Error Message
Response Message Type Id: 109

| Field| Type| Nullable| Description|
|------|-----|---------|------------|
|Error Code|int32|No|The unique code identifying the error|
|Class Name|string|No|The class name which caused the error at the server side|
|Message|string|Yes|The brief description of the error|
|Stack Trace|array of stack-trace|No|The stack trace at the server side when the error occurred|
|Cause Error Code|int32|No|The error code for the actual cause of the error. If no cause exists, it is set to -1|
|Cause Class Name|string|Yes|The name of the class that actually cause the error|

The following error codes are defined in the system:

| Error Name| Error Code| Description|
|-----------|-----------|------------|
|ARRAY_INDEX_OUT_OF_BOUNDS|1|Thrown to indicate that an array has been accessed with an illegal index. The index is either negative or greater than or equal to the size of the array.|
|ARRAY_STORE|2| Thrown to indicate that an attempt has been made to store the wrong type of object into an array of objects. For example, the following code generates an ArrayStoreException:<br>Object x[] = new String[3];<br>x[0] = new Integer(0);|
|AUTHENTICATION|3|The authentication failed.|
|CACHE|4|Thrown to indicate an exception has occurred in the Cache|
|CACHE_LOADER|5|An exception to indicate a problem has occurred executing a CacheLoader|
|CACHE_NOT_EXISTS|6|This exception class is thrown while creating com.hazelcast.cache.impl.CacheRecordStore instances but the cache config does not exist on the node to create the instance on. This can happen in either of two cases:<br>the cache's config is not yet distributed to the node, or <br>the cache has been already destroyed.<br> For the first option, the caller can decide to just retry the operation a couple of times since distribution is executed in a asynchronous way.|
|CACHE_WRITER|7|An exception to indicate a problem has occurred executing a CacheWriter|
|CALLER_NOT_MEMBER|8|A Retryable Hazelcast Exception that indicates that an operation was sent by a machine which isn't member in the cluster when the operation is executed.|
|CANCELLATION|9|Exception indicating that the result of a value-producing task, such as a FutureTask, cannot be retrieved because the task was cancelled.|
|CLASS_CAST|10|The class conversion (cast) failed.|
|CLASS_NOT_FOUND|11|The class does not exists in the loaded jars at the server member.|
|CONCURRENT_MODIFICATION|12|You are trying to modify a resource concurrently which is not allowed.|
|CONFIG_MISMATCH|13|Thrown when 2 nodes want to join, but their configuration doesn't match.|
|CONFIGURATION|14|Thrown when something is wrong with the server or client configuration.|
|DISTRIBUTED_OBJECT_DESTROYED|15|The distributed object that you are trying to access is destroyed and does not exist.|
|DUPLICATE_INSTANCE_NAME|16|An instance with the same name already exists in the system.|
|EOF|17|End of file is reached (May be for a file or a socket)|
|ENTRY_PROCESSOR|18|An exception to indicate a problem occurred attempting to execute an EntryProcessor against an entry|
|EXECUTION|19|Thrown when attempting to retrieve the result of a task that aborted by throwing an exception.|
|HAZELCAST|20|General internal error of Hazelcast.|
|HAZELCAST_INSTANCE_NOT_ACTIVE|21|The Hazelcast server instance is not active, the server is possibly initialising.|
|HAZELCAST_OVERLOAD|22|Thrown when the system won't handle more load due to an overload. This exception is thrown when backpressure is enabled.|
|HAZELCAST_SERIALIZATION|23|Error during serialization/de-serialization of data.|
|IO|24|An IO error occurred.|
|ILLEGAL_ARGUMENT|25|Thrown to indicate that a method has been passed an illegal or inappropriate argument|
|ILLEGAL_ACCESS_EXCEPTION|26|An IllegalAccessException is thrown when an application tries to reflectively create an instance (other than an array), set or get a field, or invoke a method, but the currently executing method does not have access to the definition of the specified class, field, method or constructor|
|ILLEGAL_ACCESS_ERROR|27|Thrown if an application attempts to access or modify a field, or to call a method that it does not have access to|
|ILLEGAL_MONITOR_STATE|28|When an operation on a distributed object is being attempted by a thread which did not initially own the lock on the object.|
|ILLEGAL_STATE|29|Signals that a method has been invoked at an illegal or inappropriate time|
|ILLEGAL_THREAD_STATE|30|Thrown to indicate that a thread is not in an appropriate state for the requested operation.|
|INDEX_OUT_OF_BOUNDS|31|Thrown to indicate that an index of some sort (such as to a list) is out of range.|
|INTERRUPTED|32|Thrown when a thread is waiting, sleeping, or otherwise occupied, and the thread is interrupted, either before or during the activity|
|INVALID_ADDRESS|33|Thrown when given address is not valid.|
|INVALID_CONFIGURATION|34|An InvalidConfigurationException is thrown when there is an Invalid Configuration. Invalid Configuration can be a wrong Xml Config or logical config errors that are found at real time.|
|MEMBER_LEFT|35|Thrown when a member left during an invocation or execution.|
|NEGATIVE_ARRAY_SIZE|36|The provided size of the array can not be negative but a negative number is provided.|
|NO_SUCH_ELEMENT|37|The requested element does not exist in the distributed object.|
|NOT_SERIALIZABLE|38|The object could not be serialized|
|NULL_POINTER|39|The server faced a null pointer exception during the operation.|
|OPERATION_TIMEOUT|40|An unchecked version of java.util.concurrent.TimeoutException. <p>Some of the Hazelcast operations may throw an *OperationTimeoutException*. Hazelcast uses OperationTimeoutException to pass TimeoutException up through interfaces that don't have TimeoutException in their signatures.</p>|
|PARTITION_MIGRATING|41|Thrown when an operation is executed on a partition, but that partition is currently being moved around.|
|QUERY|42|Error during query.|
|QUERY_RESULT_SIZE_EXCEEDED|43|Thrown when a query exceeds a configurable result size limit.|
|QUORUM|44|An exception thrown when the cluster size is below the defined threshold.|
|REACHED_MAX_SIZE|45|Exception thrown when a write-behind MapStore rejects to accept a new element.|
|REJECTED_EXECUTION|46|Exception thrown by an Executor when a task cannot be accepted for execution.|
|REMOTE_MAP_REDUCE|47|This is used for failed remote operations. This can happen if the get result operation fails to retrieve values for some reason.|
|RESPONSE_ALREADY_SENT|48|There is some kind of system error causing a response to be send multiple times for some operation.|
|RETRYABLE_HAZELCAST|49|The operation request can be retried.|
|RETRYABLE_IO|50|Indicates that an operation can be retried. E.g. if map.get is send to a partition that is currently migrating, a subclass of this exception is thrown, so the caller can deal with it (e.g. sending the request to the new partition owner).|
|RUNTIME|51|Exceptions that can be thrown during the normal operation of the Java Virtual Machine|
|SECURITY|52|There is a security violation|
|SOCKET|53|There is an error in the underlying TCP protocol|
|STALE_SEQUENCE|54|Thrown when accessing an item in the Ringbuffer using a sequence that is smaller than the current head sequence. This means that the and old item is read, but it isn't available anymore in the ringbuffer.|
|TARGET_DISCONNECTED|55|Indicates that an operation is about to be sent to a non existing machine.|
|TARGET_NOT_MEMBER|56|Indicates operation is sent to a machine that isn't member of the cluster.|
|TIMEOUT|57|Exception thrown when a blocking operation times out|
|TOPIC_OVERLOAD|58|Thrown when a publisher wants to write to a topic, but there is not sufficient storage to deal with the event. This exception is only thrown in combination with the reliable topic.|
|TOPOLOGY_CHANGED|59|Thrown when a topology change happens during the execution of a map reduce job and the com.hazelcast.mapreduce.TopologyChangedStrategy is set to com.hazelcast.mapreduce.TopologyChangedStrategy.CANCEL_RUNNING_OPERATION.|
|TRANSACTION|60|Thrown when something goes wrong while dealing with transactions and transactional data-structures.|
|TRANSACTION_NOT_ACTIVE|61|Thrown when an a transactional operation is executed without an active transaction.|
|TRANSACTION_TIMED_OUT|62|Thrown when a transaction has timed out.|
|URI_SYNTAX|63|Thrown to indicate that a string could not be parsed as a URI reference|
|UTF_DATA_FORMAT|64|Signals that a malformed string in modified UTF-8 format has been read in a data input stream or by any class that implements the data input interface|
|UNSUPPORTED_OPERATION|65|The message type id for the operation request is not a recognised id.|
|WRONG_TARGET|66|An operation is executed on the wrong machine.|
|XA|67|An error occurred during an XA operation.|
|ACCESS_CONTROL|68|Indicates that a requested access to a system resource is denied.|
|LOGIN|69|Basic login exception.|
|UNSUPPORTED_CALLBACK|70|Signals that a CallbackHandler does not recognize a particular Callback.|
|NO_DATA_MEMBER|71|Thrown when there is no data member in the cluster to assign partitions.|
|REPLICATED_MAP_CANT_BE_CREATED|72|Thrown when com.hazelcast.core.HazelcastInstance.getReplicatedMap(String) is invoked on a lite member.|
|MAX_MESSAGE_SIZE_EXCEEDED|73|Thrown when client message size exceeds Integer.MAX_VALUE.|
|WAN_REPLICATION_QUEUE_FULL|74|Thrown when the wan replication queues are full.|
|ASSERTION_ERROR|75|Thrown to indicate that an assertion has failed.|
|OUT_OF_MEMORY_ERROR|76|Thrown when the Java Virtual Machine cannot allocate an object because it is out of memory, and no more memory could be made available by the garbage collector.|
|STACK_OVERFLOW_ERROR|77|Thrown when a stack overflow occurs because an application recurses too deeply.|
|NATIVE_OUT_OF_MEMORY_ERROR|78|Thrown when Hazelcast cannot allocate required native memory.|

Please note that there may be error messages with an error code which is not listed in this table. The client can handle this situation differently based on the particular implementation (e.g. throw an unknown error code exception).
<#list model?keys as key>
<#assign map=model?values[key_index]?values/>
<#if map?has_content>

<br><hr><br>
<#if key == "com.hazelcast.client.impl.protocol.template.ClientMessageTemplate">
## General Protocol Operations
<#else>
## ${util.getDistributedObjectName(key)}
</#if>

<#list map as cm>
<br>
### ${util.getDistributedObjectName(key)}.${cm.name?cap_first}
${util.getOperationDescription(cm.comment)}
<#if cm.retryable == 1 >This message is idempotent.</#if><br>
**Available since ${cm.messageSince}**

#### Request Message
**Type Id**      : ${cm.id}<br>
**Partition Id** : ${resolvePartitionIdentifier(cm.partitionIdentifier)}

    <#if cm.requestParams?has_content>

| Name| Type| Nullable| Description|Available since|
|-----|-----|---------|------------|-----|
        <#list cm.requestParams as param>
|${param.name}| ${convertTypeToDocumentType(param.type)}| <#if param.nullable >Yes<#else>No</#if><#if param.containsNullable> / Contains Nullable</#if>|${util.getDescription(param.name, cm.comment)}|${param.sinceVersion}|
        </#list>
    <#else>
Header only request message, no message body exist.
    </#if>

#### Response Message
**Type Id** : ${cm.hexadecimalResponseId}

${util.getReturnDescription(cm.comment)}

    <#if cm.responseParams?has_content>

| Name| Type| Nullable|Available since|
|-------|------------|----------|-----|
        <#list cm.responseParams as param>
|${param.name}| ${convertTypeToDocumentType(param.type)}| <#if param.nullable >Yes<#else>No</#if><#if param.containsNullable> / Contains Nullable</#if>|${param.sinceVersion}|
        </#list>
    <#else>
Header only response message, no message body exist.
    </#if>

    <#if cm.events?has_content>

<#list cm.events as event >

#### Event Message
**Type Id** : ${event.hexadecimalTypeId}

    <#if event.eventParams?has_content>

| Name| Type| Nullable| Description|Available since|
|-------|------------|----------|------------|-----|
        <#list event.eventParams as param>
|${param.name}| ${convertTypeToDocumentType(param.type)}| <#if param.nullable >Yes<#else>No</#if>|${param.description}|${param.sinceVersion}|
        </#list>
    <#else>

Header only event message, no message body exist.
    </#if>

</#list>

    </#if>

</#list>

</#if>
</#list>
#Glossary
| Terminology| Definition|
|-----------|------------|
|client|Any Hazelcast native client implementation|
|server/member|A Hazelcast cluster member|
|protocol||Hazelcast client-server communication protocol|
|serialization|Hazelcast internal implementation of serialization used to encode an object into a byte array and decode a byte array into an object|
|protocol-version||The version of the protocol starting at 1|
|fragmentation|Splitting a large message into pieces for transmission|
|Reassembly|Combining the message parts (fragments) to form the actual large message on reception|
|Cluster|A virtual environment formed by Hazelcast members communicating with each other|

<#function convertTypeToDocumentType javaType>
    <#switch javaType?trim>
        <#case "int">
            <#return "int32">
        <#case "integer">
            <#return "int32">
        <#case "short">
            <#return "int16">
        <#case "boolean">
            <#return "boolean">
        <#case "byte">
            <#return "uint8">
        <#case "long">
            <#return "int64">
        <#case "char">
            <#return "int8">
        <#case util.DATA_FULL_NAME>
            <#return "byte-array">
        <#case "java.lang.String">
            <#return "string">
        <#case "boolean">
            <#return "boolean">
        <#case "java.util.List<" + util.DATA_FULL_NAME + ">">
            <#return "array of byte-array">
        <#case "java.util.List<" + util.DATA_FULL_NAME + ">">
            <#return "array of byte-array">
        <#case "java.util.List<com.hazelcast.core.Member>">
            <#return "array of Member">
        <#case "java.util.List<com.hazelcast.client.impl.client.DistributedObjectInfo>">
            <#return "array of Distributed Object Info">
        <#case "java.util.List<java.util.Map.Entry<com.hazelcast.nio.Address,java.util.List<java.lang.Integer>>>">
            <#return "array of Address-Partition Id List pair">
        <#case "java.util.Collection<" + util.DATA_FULL_NAME + ">">
            <#return "array of byte-array">
        <#case "java.util.Map<" + util.DATA_FULL_NAME + "," + util.DATA_FULL_NAME + ">">
            <#return "array of key-value byte array pair">
        <#case "java.util.List<java.util.Map.Entry<"+ util.DATA_FULL_NAME + "," + util.DATA_FULL_NAME + ">>">
            <#return "array of key-value byte array pair">
        <#case "java.util.List<java.util.Map.Entry<"+ util.DATA_FULL_NAME + "," + util.DATA_FULL_NAME + ">>">
            <#return "array of key-value byte array pair">
        <#case "com.hazelcast.map.impl.SimpleEntryView<" + util.DATA_FULL_NAME +"," + util.DATA_FULL_NAME +">">
            <#return "array of Entry View">
        <#case "com.hazelcast.nio.Address">
            <#return "Address">
        <#case "com.hazelcast.core.Member">
            <#return "Member">
        <#case "javax.transaction.xa.Xid">
            <#return "Transaction Id">
        <#case "com.hazelcast.map.impl.querycache.event.QueryCacheEventData">
            <#return "Query Cache Event Data">
        <#case "java.util.List<com.hazelcast.mapreduce.JobPartitionState>">
            <#return "array of Job Partition State">
        <#case "java.util.List<com.hazelcast.cache.impl.CacheEventData>">
            <#return "array of Cache Event Data">
        <#case "java.util.List<com.hazelcast.map.impl.querycache.event.QueryCacheEventData>">
            <#return "array of Query Cache Event Data">
        <#case "java.util.List<java.lang.String>">
            <#return "array of string">
        <#case "java.util.List<java.lang.Long>">
            <#return "array of longs">
        <#default>
            <#return "Unknown Data Type " + javaType>
    </#switch>
</#function>


<#function resolvePartitionIdentifier partitionIdentifier>
    <#switch partitionIdentifier?trim>
        <#case "random">
            <#return "a random partition id from 0 to PARTITION_COUNT(PARTITION_COUNT exclusive)">
        <#case "-1">
            <#return "-1">
        <#case "partitionId">
            <#return "the value passed in partitionId field">
        <#default>
            <#return "Murmur hash of " + partitionIdentifier + " % partition count">
    </#switch>
</#function>
