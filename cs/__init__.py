cs_reserved_words = {"abstract", "add", "as", "ascending", "async", "await", "base", "bool", "break", "by", "byte",
                     "case", "catch", "char", "checked", "class", "const", "continue", "decimal", "default", "delegate",
                     "descending", "do", "double", "dynamic", "else", "enum", "equals", "explicit", "extern", "false",
                     "finally", "fixed", "float", "for", "foreach", "from", "get", "global", "goto", "group", "if",
                     "implicit", "in", "int", "interface", "internal", "into", "is", "join", "let", "lock", "long",
                     "namespace", "new", "null", "object", "on", "operator", "orderby", "out", "override", "params",
                     "partial", "private", "protected", "public", "readonly", "ref", "remove", "return", "sbyte",
                     "sealed", "select", "set", "short", "sizeof", "stackalloc", "static", "string", "struct", "switch",
                     "this", "throw", "true", "try", "typeof", "uint", "ulong", "unchecked", "unsafe", "ushort",
                     "using", "value", "var", "virtual", "void", "volatile", "where", "while", "yield"}

cs_ignore_service_list = {

    # entire services - correspond to an entire yaml file in protocol-definitions
    "MC", "ExecutorService", "Cache", "XATransaction", "ContinuousQuery",
    "DurableExecutor", "CardinalityEstimator", "ScheduledExecutor", "DynamicConfig",
    "Jet",
    "CPSubsystem", "CPMember",  "CountDownLatch", "Semaphore",
    "Map.replaceAll","Sql.mappingDdl",
    "AtomicLong.apply", "AtomicRef.apply",
    # methods - correspond to entries in yaml files in protocol-definitions
    "Atomic*.apply", "Atomic*.alter", "MultiMap.putAll", "Client.removeMigrationListener", "SQL*_reserved*",
    # custom
    "DataPersistenceConfig", "DiskTierConfig", "TieredStoreConfig", "SqlSummary", "JobAndSqlSummary"
}


def cs_types_encode(key):
    try:
        cs_type = _cs_types_encode[key]
    except KeyError:
        cs_type = _cs_types_common[key]
    if cs_type == "NA":
        raise NotImplementedError("Missing type mapping for '" + key + "'")
    return cs_type


def cs_types_decode(key):
    try:
        cs_type = _cs_types_decode[key]
    except KeyError:
        cs_type = _cs_types_common[key]
    if cs_type == "NA":
        raise NotImplementedError("Missing type for '" + key + "'")
    return cs_type

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

_cs_codec_params = {
    "IndexConfig.bTreeIndexConfig": "BTreeIndexOptions",
    "BTreeIndexConfig.memoryTierConfig": "MemoryTierOptions",
}

_cs_types_common = {
    "boolean": "bool",
    "int": "int",
    "long": "long",
    "byte": "byte",
    "Integer": "int",
    "Long": "long",
    "UUID": "Guid",

    "longArray": "long[]",
    "byteArray": "byte[]",
    "String": "string",
    "Data": "IData",

    "Address": "Hazelcast.Networking.NetworkAddress",
    "ErrorHolder": "Hazelcast.Protocol.Models.ErrorHolder",
    "StackTraceElement": "Hazelcast.Exceptions.StackTraceElement",
    "SimpleEntryView": "Hazelcast.Models.MapEntryStats<IData, IData>",
    "RaftGroupId": "Hazelcast.CP.CPGroupId",
    "WanReplicationRef": "NA",
    "HotRestartConfig": "NA",
    "EventJournalConfig": "NA",
    "MerkleTreeConfig": "NA",
    "TimedExpiryPolicyFactoryConfig": "NA",
    "MapStoreConfigHolder": "NA",
    "QueueStoreConfigHolder": "NA",
    "RingbufferStoreConfigHolder": "NA",
    "NearCacheConfigHolder": "NA",
    "EvictionConfigHolder": "NA",
    "NearCachePreloaderConfig": "NA",
    "PredicateConfigHolder": "NA",
    "DurationConfig": "NA",
    "MigrationState": "NA",

    "Schema":"Hazelcast.Serialization.Compact.Schema",
    "List_Schema":"IEnumerable<Hazelcast.Serialization.Compact.Schema>",
    "FieldDescriptor":"Hazelcast.Serialization.Compact.SchemaField",

    "MergePolicyConfig": "NA",
    "CacheConfigHolder": "NA",
    "CacheEventData": "NA",
    "QueryCacheConfigHolder": "NA",
    "DistributedObjectInfo": "Hazelcast.Models.DistributedObjectInfo",
    "CPDistributedObjectInfo": "NA",
    "IndexConfig": "Hazelcast.Models.IndexOptions",
    "BitmapIndexOptions": "Hazelcast.Models.BitmapIndexOptions",
    "BTreeIndexConfig": "Hazelcast.Models.BTreeIndexOptions",
    "AttributeConfig": "NA",
    "ListenerConfigHolder": "NA",
    "CacheSimpleEntryListenerConfig": "NA",
    "ClientBwListEntry": "NA",
    "EndpointQualifier": "Hazelcast.Models.EndpointQualifier",

    "Map_String_String": "IDictionary<string, string>",
    "Map_EndpointQualifier_Address": "Dictionary<Hazelcast.Models.EndpointQualifier, Hazelcast.Networking.NetworkAddress>",
    "SqlPage": "Hazelcast.Sql.SqlPage",
    "HazelcastJsonValue": "Hazelcast.Core.HazelcastJsonValue",
    "PartitioningAttributeConfig": "NA",
    "WanConsumerConfigHolder": "NA",
    "WanCustomPublisherConfigHolder": "NA",
    "WanBatchPublisherConfigHolder": "NA",
    "AwsConfig": "NA",
    "GcpConfig": "NA",
    "AzureConfig": "NA",
    "KubernetesConfig": "NA",
    "EurekaConfig": "NA",
    "DiscoveryStrategyConfig": "NA",
    "DiscoveryConfig": "NA",
    "WanSyncConfig": "NA",
    "ResourceDefinition": "NA",
    "List_ResourceDefinition": "NA",
}

_cs_types_encode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "ClientBwListEntry": "NA",
    "MemberInfo": "Hazelcast.Models.MemberInfo",
    "MemberVersion": "Hazelcast.Models.MemberVersion",
    "MCEvent": "NA",
    "AnchorDataListHolder": "Hazelcast.Protocol.Models.AnchorDataListHolder",
    "PagingPredicateHolder": "Hazelcast.Protocol.Models.PagingPredicateHolder",
    "CPMember": "Hazelcast.CP.ICPMember",
    "MigrationState": "NA",
    "Capacity": "Hazelcast.Models.Capacity",
    "MemoryTierConfig": "Hazelcast.Models.MemoryTierOptions",
    "BTreeIndexConfig": "Hazelcast.Models.BTreeIndexOptions",

    "SqlQueryId": "Hazelcast.Sql.SqlQueryId",
    "SqlError": "Hazelcast.Sql.SqlError",
    "SqlColumnMetadata": "Hazelcast.Sql.SqlColumnMetadata",

    "List_Long": "ICollection<long>",
    "List_Integer": "ICollection<int>",
    "List_UUID": "ICollection<Guid>",
    "List_String": "ICollection<string>",
    "List_Xid": "NA",
    "List_Data": "ICollection<IData>",
    "List_List_Data": "ICollection<ICollection<IData>>",
    "ListCN_Data": "ICollection<IData>",
    "List_ListCN_Data": "ICollection<ICollection<IData>>",
    "List_MemberInfo": "ICollection<Hazelcast.Models.MemberInfo>",
    "List_ScheduledTaskHandler": "NA",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "ICollection<Hazelcast.Models.DistributedObjectInfo>",
    "List_CPDistributedObjectInfo": "NA",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "ICollection<Hazelcast.Models.IndexOptions>",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "ICollection<Hazelcast.Util.StackTraceElement>",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",
    "List_SqlColumnMetadata": "IList<Hazelcast.Sql.SqlColumnMetadata>",
    "List_CPMember": "ICollection<Hazelcast.CP.ICPMember>",

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

    "Set_UUID": "ISet<Guid>",
    "List_PartitioningAttributeConfig": "NA",
    "List_SimpleEntryView": "NA",
    "List_ReplicatedMapEntryViewHolder": "NA",
}

_cs_types_decode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "ClientBwListEntry": "NA",
    "MemberInfo": "Hazelcast.Models.MemberInfo",
    "MemberVersion": "Hazelcast.Models.MemberVersion",
    "MCEvent": "NA",
    "AnchorDataListHolder": "Hazelcast.Protocol.Models.AnchorDataListHolder",
    "PagingPredicateHolder": "Hazelcast.Protocol.Models.PagingPredicateHolder",
    "SqlQueryId": "Hazelcast.Sql.SqlQueryId",
    "SqlError": "Hazelcast.Sql.SqlError",
    "SqlColumnMetadata": "Hazelcast.Sql.SqlColumnMetadata",
    "CPMember": "Hazelcast.CP.CPMemberInfo",
    "Capacity": "Hazelcast.Models.Capacity",
    "MemoryTierConfig": "Hazelcast.Models.MemoryTierOptions",
    "BTreeIndexConfig": "Hazelcast.Models.BTreeIndexOptions",

    "List_Long": "IList<long>",
    "List_Integer": "IList<int>",
    "List_UUID": "IList<Guid>",
    "List_Xid": "NA",
    "List_String": "IList<string>",
    "List_Data": "IList<IData>",
    "List_List_Data": "ICollection<ICollection<IData>>",
    "ListCN_Data": "IList<IData>",
    "List_ListCN_Data": "IList<IList<IData>>",
    "List_MemberInfo": "IList<Hazelcast.Models.MemberInfo>",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "ICollection<Hazelcast.Models.DistributedObjectInfo>",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "IList<Hazelcast.Models.IndexOptions>",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "IList<Hazelcast.Util.StackTraceElement>",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",
    "List_ScheduledTaskHandler": "NA",
    "List_SqlColumnMetadata": "IList<Hazelcast.Sql.SqlColumnMetadata>",
    "List_CPMember": "IList<Hazelcast.CP.CPMemberInfo>",

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

    "Set_UUID": "ISet<Guid>",
    "List_PartitioningAttributeConfig": "NA",
    "List_SimpleEntryView": "NA",
    "List_ReplicatedMapEntryViewHolder": "NA",
}
