cs_reserved_words = {
    "abstract", "add", "as", "ascending", "async", "await", "base", "bool", "break", "by", "byte",
    "case", "catch", "char", "checked", "class", "const", "continue", "decimal", "default", "delegate",
    "descending", "do", "double", "dynamic", "else", "enum", "equals", "explicit", "extern", "false",
    "finally", "fixed", "float", "for", "foreach", "from", "get", "global", "goto", "group", "if",
    "implicit", "in", "int", "interface", "internal", "into", "is", "join", "let", "lock", "long",
    "namespace", "new", "null", "object", "on", "operator", "orderby", "out", "override", "params",
    "partial", "private", "protected", "public", "readonly", "ref", "remove", "return", "sbyte",
    "sealed", "select", "set", "short", "sizeof", "stackalloc", "static", "string", "struct", "switch",
    "this", "throw", "true", "try", "typeof", "uint", "ulong", "unchecked", "unsafe", "ushort",
    "using", "value", "var", "virtual", "void", "volatile", "where", "while", "yield"
}

cs_ignore_service_list = {

    # entire services - correspond to an entire yaml file in protocol definitions
    "MC", "Jet", "ExecutorService", "Cache", "XATransaction", "ContinuousQuery",
    "DurableExecutor", "CardinalityEstimator", "ScheduledExecutor",
    "CPSubsystem",
    "SqlSummary", "JobAndSqlSummary",
    # service.methods - correspond to method entries in yaml files in protocol definitions
    "Map.replaceAll", "Sql.mappingDdl",
    "AtomicLong.apply", "AtomicRef.apply",
    "Atomic*.apply", "Atomic*.alter", "MultiMap.putAll", "Client.removeMigrationListener", "SQL*_reserved*",
    "Client.tpcAuthentication",
    "Map.putAllWithMetadata", "client.addMigrationListener",
    "CPMap.putIfAbsent", "ReplicatedMap.endEntryViewIteration",
    # custom codecs - for dynamic config - temp disabling
    "AwsConfig", "AzureConfig", "GcpConfig", "EurekaConfig", "KubernetesConfig",
    "WanSyncConfig", "WanCustomPublisherConfig", "WanBatchPublisherConfig",
    "DiscoveryConfig", "DiscoveryStrategyConfig", "CacheConfigHolder", "QueueStoreConfigHolder",
    "WanConsumerConfigHolder", "WanBatchPublisherConfigHolder", "WanCustomPublisherConfigHolder",
    "DynamicConfig.AddQueueConfig", "DynamicConfig.AddWanReplicationConfig","TimedExpiryPolicyFactoryConfigCodec",
}

def cs_types(key, d):
    try:
        cs_type = d[key]
        cs_type = d[key]
    except KeyError:
        try:
            cs_type = _cs_types_common[key]
        except KeyError:
            cs_type = None
    if cs_type is None:
        raise NotImplementedError("Missing type mapping for '" + key + "'")
    elif cs_type == "NA":
        raise NotImplementedError("Missing (N/A) type mapping for '" + key + "'")
    return cs_type

# looks for a type in encode types, then in common types
def cs_types_encode(key):
    return cs_types(key, _cs_types_encode)

# looks for a type in decode types, then in common types
def cs_types_decode(key):
    return cs_types(key, _cs_types_decode)

def cs_custom_codec_param_name(codec, param):
    try:
        return _cs_codec_params[codec + "." + param]
    except KeyError:
        return param

def cs_sizeof(key):
    cs_type = cs_types_decode(key)
    if cs_type == "Guid":
        cs_type = "CodecGuid"
    cs_type = cs_type[0].capitalize() + cs_type[1:]
    return "BytesExtensions.SizeOf" + cs_type

def cs_escape_keyword(value):
    if value not in cs_reserved_words:
        return value
    return "@" + value

# we want to get rid of 'IsSomething' as it's not idiomatic .NET
# but, in some places, it would be breaking - so... tweaking here
def cs_param_prefix(codec_name, param_type, param_name):
    if param_type != 'boolean':
        return ""
    if codec_name in [
        'DataPersistenceConfig',
        'DiskTierConfig',
        'HotRestartConfig',
        'NearCachePreloaderConfig',
        'TieredStoreConfig',
        'EventJournalConfig',
        'MerkleTreeConfig',
        'WanReplicationRef',
        'CacheSimpleEntryListenerConfig',
        'VectorSearchOptions'
    ]:
        return ""
    return "Is"

# map custom codec parameters
_cs_codec_params = {
    # get rid of Config/Options suffix for properties
    "IndexConfig.bTreeIndexConfig": "BTreeIndex",
    "IndexConfig.bitmapIndexOptions": "BitmapIndex", # yes, 'Options' in Java too
    "BTreeIndexConfig.memoryTierConfig": "MemoryTier",
    "BTreeIndexConfig.diskTierConfig": "DiskTier",
    "TieredStoreConfig.memoryTierConfig": "MemoryTier",
    "TieredStoreConfig.diskTierConfig": "DiskTier",

    # get rid of isWhatever = Whatever
    "DataPersistenceConfig.enabled": "Enabled",
    "DataPersistenceConfig.fsync": "Fsync",
}

# map common types (for encoding and decoding)
_cs_types_common = {

    # core types
    "boolean": "bool",
    "int": "int",
    "long": "long",
    "byte": "byte",
    "Integer": "int",
    "Long": "long",
    "float": "float",
    "UUID": "Guid",
    "longArray": "long[]",
    "byteArray": "byte[]",
    "String": "string",
    "Data": "IData",
    "Map_String_String": "IDictionary<string, string>",

    # misc. models
    "Address": "Hazelcast.Networking.NetworkAddress",
    "ErrorHolder": "Hazelcast.Protocol.Models.ErrorHolder",
    "StackTraceElement": "Hazelcast.Exceptions.StackTraceElement",
    "SimpleEntryView": "Hazelcast.Models.MapEntryStats<IData, IData>",
    "RaftGroupId": "Hazelcast.CP.CPGroupId",
    "DistributedObjectInfo": "Hazelcast.Models.DistributedObjectInfo",
    "EndpointQualifier": "Hazelcast.Models.EndpointQualifier",
    "HazelcastJsonValue": "Hazelcast.Core.HazelcastJsonValue",
    "Map_EndpointQualifier_Address": "Dictionary<Hazelcast.Models.EndpointQualifier, Hazelcast.Networking.NetworkAddress>",
    "RaftGroupInfo":"Hazelcast.CP.CPGroupInfo",
    "List_RaftGroupInfo": "ICollection<Hazelcast.CP.CPGroupInfo>",
    "SqlPage": "Hazelcast.Sql.SqlPage",
    "SqlQueryId": "Hazelcast.Sql.SqlQueryId",
    "SqlError": "Hazelcast.Sql.SqlError",
    "SqlColumnMetadata": "Hazelcast.Sql.SqlColumnMetadata",
    "Capacity": "Hazelcast.Models.Capacity",
    "CacheEventData": "NA",
    "ClientBwListEntry": "NA",
    "MigrationState": "NA",
    "ReplicatedMapEntryViewHolder": "NA",
    "ResourceDefinition": "NA",
    "List_ResourceDefinition": "NA",

    # compact
    "Schema":"Hazelcast.Serialization.Compact.Schema",
    "List_Schema":"IEnumerable<Hazelcast.Serialization.Compact.Schema>",
    "FieldDescriptor":"Hazelcast.Serialization.Compact.SchemaField",

    # all config holders below to Hazelcast.Protocol.Models
    "RingbufferStoreConfigHolder": "Hazelcast.Protocol.Models.RingbufferStoreConfigHolder",
    "EvictionConfigHolder": "Hazelcast.Protocol.Models.EvictionConfigHolder",
    "WanConsumerConfigHolder": "Hazelcast.Protocol.Models.WanConsumerConfigHolder",
    "QueueStoreConfigHolder": "Hazelcast.Protocol.Models.QueueStoreConfigHolder",
    "MapStoreConfigHolder" : "Hazelcast.Protocol.Models.MapStoreConfigHolder",
    "NearCacheConfigHolder": "Hazelcast.Protocol.Models.NearCacheConfigHolder",
    "PredicateConfigHolder": "Hazelcast.Protocol.Models.PredicateConfigHolder",
    "QueryCacheConfigHolder": "Hazelcast.Protocol.Models.QueryCacheConfigHolder",
    "CacheConfigHolder": "Hazelcast.Protocol.Models.CacheConfigHolder",
    "ListenerConfigHolder": "Hazelcast.Protocol.Models.ListenerConfigHolder",
    "WanCustomPublisherConfigHolder": "Hazelcast.Protocol.Models.WanCustomPublisherConfigHolder",
    "WanBatchPublisherConfigHolder": "Hazelcast.Protocol.Models.WanBatchPublisherConfigHolder",
    "AnchorDataListHolder": "Hazelcast.Protocol.Models.AnchorDataListHolder",
    "PagingPredicateHolder": "Hazelcast.Protocol.Models.PagingPredicateHolder",

    # all configs/options belong to Hazelcast.Models
    "TimedExpiryPolicyFactoryConfig": "Hazelcast.Models.TimedExpiryPolicyFactoryOptions",
    "IndexConfig": "Hazelcast.Models.IndexOptions",
    "BitmapIndexOptions": "Hazelcast.Models.BitmapIndexOptions", # yes, 'Options' in Java too
    "MemoryTierConfig": "Hazelcast.Models.MemoryTierOptions",
    "DiskTierConfig": "Hazelcast.Models.DiskTierOptions",
    "BTreeIndexConfig": "Hazelcast.Models.BTreeIndexOptions",
    "EventJournalConfig": "Hazelcast.Models.EventJournalOptions",
    "HotRestartConfig": "Hazelcast.Models.HotRestartOptions",
    "MerkleTreeConfig": "Hazelcast.Models.MerkleTreeOptions",
    "DataPersistenceConfig": "Hazelcast.Models.DataPersistenceOptions",
    "TieredStoreConfig": "Hazelcast.Models.TieredStoreOptions",
    "AttributeConfig": "Hazelcast.Models.AttributeOptions",
    "ListenerConfig": "Hazelcast.Models.ListenerOptions",
    "CacheSimpleEntryListenerConfig": "Hazelcast.Models.CacheSimpleEntryListenerOptions",
    "DurationConfig": "Hazelcast.Models.DurationOptions",
    "MergePolicyConfig": "Hazelcast.Models.MergePolicyOptions",
    "PartitioningAttributeConfig": "Hazelcast.Models.PartitioningAttributeOptions",
    "DiscoveryStrategyConfig": "Hazelcast.Models.DiscoveryStrategyOptions",
    "DiscoveryConfig": "Hazelcast.Models.DiscoveryOptions",
    "WanSyncConfig": "Hazelcast.Models.WanSyncOptions",
    "AwsConfig": "Hazelcast.Models.AwsOptions",
    "GcpConfig": "Hazelcast.Models.GcpOptions",
    "AzureConfig": "Hazelcast.Models.AzureOptions",
    "KubernetesConfig": "Hazelcast.Models.KubernetesOptions",
    "EurekaConfig": "Hazelcast.Models.EurekaOptions",
    "WanReplicationRef": "Hazelcast.Models.WanReplicationRef",
    "Version":"Hazelcast.Models.ClusterVersion",

    # except NearCache
    "NearCacheConfig": "Hazelcast.NearCaching.NearCacheOptions",
    "NearCachePreloaderConfig": "Hazelcast.NearCaching.NearCachePreloaderOptions",

    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "MCEvent": "NA",

    "MemberInfo": "Hazelcast.Models.MemberInfo",
    "MemberVersion": "Hazelcast.Models.MemberVersion",

    "VectorDocument": "Hazelcast.Models.VectorDocument<IData>",
    "VectorSearchResult": "Hazelcast.Models.VectorSearchResultEntry<IData,IData>",
    "VectorPair": "Hazelcast.Protocol.Models.VectorPairHolder",
    "VectorSearchOptions": "Hazelcast.Models.VectorSearchOptions"


}

# map types for encoding
_cs_types_encode = {

    # encode as interface
    "CPMember": "Hazelcast.CP.CPMember",

    # encode as collections
    "List_Long": "ICollection<long>",
    "List_Integer": "ICollection<int>",
    "List_UUID": "ICollection<Guid>",
    "List_List_UUID":"ICollection<ICollection<Guid>>",
    "List_String": "ICollection<string>",
    "List_Xid": "NA",
    "List_Data": "ICollection<IData>",
    "List_List_Data": "ICollection<ICollection<IData>>",
    "ListCN_Data": "ICollection<IData>",
    "List_ListCN_Data": "ICollection<ICollection<IData>>",
    "List_MemberInfo": "ICollection<Hazelcast.Models.MemberInfo>",
    "List_ScheduledTaskHandler": "NA",
    "List_CacheEventData": "NA",
    "List_DistributedObjectInfo": "ICollection<Hazelcast.Models.DistributedObjectInfo>",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "ICollection<Hazelcast.Models.IndexOptions>",
    "List_StackTraceElement": "ICollection<Hazelcast.Util.StackTraceElement>",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",
    "List_SqlColumnMetadata": "IList<Hazelcast.Sql.SqlColumnMetadata>",
    "List_CPMember": "ICollection<Hazelcast.CP.CPMember>",
    "List_RaftGroupId": "NA",

    "EntryList_String_String": "ICollection<KeyValuePair<string, string>>",
    "EntryList_String_byteArray": "ICollection<KeyValuePair<string, byte[]>>",
    "EntryList_Long_byteArray": "ICollection<KeyValuePair<long, byte[]>>",
    "EntryList_Integer_UUID": "ICollection<KeyValuePair<int, Guid>>",
    "EntryList_Integer_Long": "ICollection<KeyValuePair<int, long>>",
    "EntryList_Integer_Integer": "ICollection<KeyValuePair<int, int>>",
    "EntryList_UUID_Long": "ICollection<KeyValuePair<Guid, long>>",
    "EntryList_String_EntryList_Integer_Long": "ICollection<KeyValuePair<string, ICollection<KeyValuePair<int, long>>>>",
    "EntryList_UUID_UUID": "ICollection<KeyValuePair<Guid, Guid>>",
    "EntryList_UUID_List_Integer": "ICollection<KeyValuePair<Guid, IList<int>>>",
    "EntryList_Data_Data": "ICollection<KeyValuePair<IData, IData>>",
    "EntryList_Data_List_Data": "ICollection<KeyValuePair<IData, ICollection<IData>>>",
    "EntryList_Data_VectorDocument": "ICollection<KeyValuePair<IData,VectorDocument<IData>>>",

    # below, encode/decode are identical?
    "Set_UUID": "ISet<Guid>",
    "List_SimpleEntryView": "NA",
    "List_ReplicatedMapEntryViewHolder": "NA",
    "List_ListenerConfigHolder": "ICollection<Hazelcast.Protocol.Models.ListenerConfigHolder>",
    "List_WanCustomPublisherConfigHolder": "ICollection<Hazelcast.Protocol.Models.WanCustomPublisherConfigHolder>",
    "List_WanBatchPublisherConfigHolder": "ICollection<Hazelcast.Protocol.Models.WanBatchPublisherConfigHolder>",
    "List_QueryCacheConfigHolder": "ICollection<Hazelcast.Protocol.Models.QueryCacheConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "ICollection<Hazelcast.Models.CacheSimpleEntryListenerOptions>",
    "List_AttributeConfig": "ICollection<Hazelcast.Models.AttributeOptions>",
    "List_PartitioningAttributeConfig": "ICollection<Hazelcast.Models.PartitioningAttributeOptions>",
    "List_VectorSearchResult": "ICollection<Hazelcast.Models.VectorSearchResult<IData, IData>>",
    "List_VectorPair": "Hazelcast.Models.VectorValues",
}

# map types for decoding
_cs_types_decode = {

    # decode as implementation
    "CPMember": "Hazelcast.CP.CPMember",

    # decode as lists
    "List_Long": "IList<long>",
    "List_Integer": "IList<int>",
    "List_UUID": "IList<Guid>",
    "List_List_UUID":"IList<IList<Guid>>",
    "List_String": "IList<string>",
    "List_Xid": "NA",
    "List_Data": "IList<IData>",
    "List_List_Data": "ICollection<ICollection<IData>>",
    "ListCN_Data": "IList<IData>",
    "List_ListCN_Data": "IList<IList<IData>>",
    "List_MemberInfo": "IList<Hazelcast.Models.MemberInfo>",
    "List_ScheduledTaskHandler": "NA",
    "List_CacheEventData": "NA",
    "List_DistributedObjectInfo": "ICollection<Hazelcast.Models.DistributedObjectInfo>",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "IList<Hazelcast.Models.IndexOptions>",
    "List_StackTraceElement": "IList<Hazelcast.Util.StackTraceElement>",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",
    "List_SqlColumnMetadata": "IList<Hazelcast.Sql.SqlColumnMetadata>",
    "List_CPMember": "IList<Hazelcast.CP.CPMember>",

    "EntryList_String_String": "IList<KeyValuePair<string, string>>",
    "EntryList_String_byteArray": "IList<KeyValuePair<string, byte[]>>",
    "EntryList_Long_byteArray": "IList<KeyValuePair<long, byte[]>>",
    "EntryList_Integer_UUID": "IList<KeyValuePair<int, Guid>>",
    "EntryList_Integer_Long": "IList<KeyValuePair<int, long>>",
    "EntryList_Integer_Integer": "IList<KeyValuePair<int, int>>",
    "EntryList_UUID_Long": "IList<KeyValuePair<Guid, long>>",
    "EntryList_String_EntryList_Integer_Long": "IList<KeyValuePair<string, IList<KeyValuePair<int, long>>>>",
    "EntryList_UUID_UUID": "IList<KeyValuePair<Guid, Guid>>",
    "EntryList_UUID_List_Integer": "IList<KeyValuePair<Guid, IList<int>>>",
    "EntryList_Data_Data": "IList<KeyValuePair<IData, IData>>",
    "EntryList_Data_List_Data": "IList<KeyValuePair<IData, IList<IData>>>",

    # below, encode/decode are identical?
    "Set_UUID": "ISet<Guid>",
    "List_SimpleEntryView": "NA",
    "List_ReplicatedMapEntryViewHolder": "NA",
    "List_ListenerConfigHolder": "ICollection<Hazelcast.Protocol.Models.ListenerConfigHolder>",
    "List_WanCustomPublisherConfigHolder": "ICollection<Hazelcast.Protocol.Models.WanCustomPublisherConfigHolder>",
    "List_WanBatchPublisherConfigHolder": "ICollection<Hazelcast.Protocol.Models.WanBatchPublisherConfigHolder>",
    "List_QueryCacheConfigHolder": "ICollection<Hazelcast.Protocol.Models.QueryCacheConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "ICollection<Hazelcast.Models.CacheSimpleEntryListenerOptions>",
    "List_AttributeConfig": "ICollection<Hazelcast.Models.AttributeOptions>",
    "List_PartitioningAttributeConfig": "ICollection<Hazelcast.Models.PartitioningAttributeOptions>",
    "EntryList_Data_VectorDocument": "ICollection<VectorDocument<IData>>",
    "List_VectorSearchResult": "ICollection<Hazelcast.Models.VectorSearchResultEntry<IData, IData>>",
    "List_VectorPair": "ICollection<Hazelcast.Protocol.Models.VectorPair>",
}
