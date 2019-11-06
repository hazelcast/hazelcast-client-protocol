def cs_types_encode(key):
    try:
        return _cs_types_encode[key]
    except KeyError:
        return _cs_types_common[key]


def cs_types_decode(key):
    try:
        return _cs_types_decode[key]
    except KeyError:
        return _cs_types_common[key]

def cs_escape_keyword(value):
    keywords = ["base"];

    if ( value not in keywords ):
        return value

    return "@" + value

_cs_types_common = {
    "boolean": "bool",
    "int": "int",
    "long": "long",
    "byte": "byte",
    "Integer": "int",
    "Long": "long",
    "UUID": "Guid",
    "enum": "int",

    "longArray": "long[]",
    "byteArray": "byte[]",
    "String": "string",
    "Data": "IData",

    "Address": "IO.Address",
    "ErrorHolder": "ErrorHolder",
    "StackTraceElement": "Hazelcast.Util.StackTraceElement",
    "SimpleEntryView": "Hazelcast.Map.SimpleEntryView<IData, IData>",
    "RaftGroupId": "Hazelcast.CP.RaftGroupId",
    "WanReplicationRef": "com.hazelcast.config.WanReplicationRef",
    "HotRestartConfig": "com.hazelcast.config.HotRestartConfig",
    "EventJournalConfig": "com.hazelcast.config.EventJournalConfig",
    "MerkleTreeConfig": "com.hazelcast.config.MerkleTreeConfig",
    "TimedExpiryPolicyFactoryConfig": "com.hazelcast.config.CacheSimpleConfig.ExpiryPolicyFactoryConfig.TimedExpiryPolicyFactoryConfig",
    "MapStoreConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.MapStoreConfigHolder",
    "QueueStoreConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.QueueStoreConfigHolder",
    "RingbufferStoreConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.RingbufferStoreConfigHolder",
    "NearCacheConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.NearCacheConfigHolder",
    "EvictionConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.EvictionConfigHolder",
    "NearCachePreloaderConfig": "com.hazelcast.config.NearCachePreloaderConfig",
    "PredicateConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.PredicateConfigHolder",
    "DurationConfig": "com.hazelcast.config.CacheSimpleConfig.ExpiryPolicyFactoryConfig.DurationConfig",

    "MergePolicyConfig": "com.hazelcast.config.MergePolicyConfig",
    "CacheConfigHolder": "com.hazelcast.client.impl.protocol.codec.holder.CacheConfigHolder",
    "CacheEventData": "com.hazelcast.cache.impl.CacheEventData",
    "QueryCacheConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder",
    "DistributedObjectInfo": "Hazelcast.Client.DistributedObjectInfo",
    "IndexConfig": "com.hazelcast.config.IndexConfig",
    "AttributeConfig": "com.hazelcast.config.AttributeConfig",
    "ListenerConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder",
    "CacheSimpleEntryListenerConfig": "com.hazelcast.config.CacheSimpleEntryListenerConfig",

    "Map_String_String": "IDictionary<string, string>"
}

_cs_types_encode = {
    "CacheEventData": "com.hazelcast.cache.impl.CacheEventData",
    "QueryCacheEventData": "Hazelcast.Map.QueryCacheEventData",
    "ScheduledTaskHandler": "com.hazelcast.scheduledexecutor.ScheduledTaskHandler",
    "Xid": "javax.transaction.xa.Xid",
    "Member": "Core.Member",

    "List_Long": "IEnumerable<long>",
    "List_UUID": "IEnumerable<Guid>",
    "List_String": "IEnumerable<string>",
    "List_Xid": "IEnumerable<javax.transaction.xa.Xid>",
    "List_Data": "IEnumerable<IData>",
    "ListCN_Data": "IEnumerable<IData>",
    "List_Member": "IEnumerable<Core.Member>",
    "List_CacheEventData": "IEnumerable<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "IEnumerable<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "IEnumerable<Hazelcast.Client.DistributedObjectInfo>",
    "List_QueryCacheEventData": "IEnumerable<Hazelcast.Map.QueryCacheEventData>",
    "List_IndexConfig": "IEnumerable<com.hazelcast.config.IndexConfig>",
    "List_AttributeConfig": "IEnumerable<com.hazelcast.config.AttributeConfig>",
    "List_ListenerConfigHolder": "IEnumerable<com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "IEnumerable<com.hazelcast.config.CacheSimpleEntryListenerConfig>",
    "List_StackTraceElement": "IEnumerable<Hazelcast.Util.StackTraceElement>",

    "EntryList_String_String": "IEnumerable<KeyValuePair<string, string>>",
    "EntryList_String_byteArray": "IEnumerable<KeyValuePair<string, byte[]>>",
    "EntryList_Long_byteArray": "IEnumerable<KeyValuePair<long, byte[]>>",
    "EntryList_Integer_UUID": "IEnumerable<KeyValuePair<int, Guid>>",
    "EntryList_UUID_Long": "IEnumerable<KeyValuePair<Guid, long>>",
    "EntryList_String_EntryList_Integer_Long": "IEnumerable<KeyValuePair<string, IEnumerable<KeyValuePair<int, long>>>>",
    "EntryList_Address_List_Integer": "IEnumerable<KeyValuePair<IO.Address, IEnumerable<int>>>",
    "EntryList_Data_Data": "IEnumerable<KeyValuePair<IData, IData>>",
    "EntryList_Member_List_ScheduledTaskHandler": "IEnumerable<KeyValuePair<Core.Member, IEnumerable<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>>>"
}

_cs_types_decode = {
    "CacheEventData": "com.hazelcast.cache.impl.CacheEventDataImpl",
    "QueryCacheEventData": "Hazelcast.Map.QueryCacheEventData",
    "ScheduledTaskHandler": "com.hazelcast.scheduledexecutor.impl.ScheduledTaskHandlerImpl",
    "Xid": "com.hazelcast.transaction.impl.xa.SerializableXID",
    "Member": "Core.Member",

    "List_Long": "IList<long>",
    "List_UUID": "IList<Guid>",
    "List_Xid": "IList<javax.transaction.xa.Xid>",
    "List_String": "IList<string>",
    "List_Data": "IList<IData>",
    "ListCN_Data": "IList<IData>",
    "List_Member": "IList<Core.Member>",
    "List_CacheEventData": "IList<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "IList<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "IList<Hazelcast.Client.DistributedObjectInfo>",
    "List_QueryCacheEventData": "IList<Hazelcast.Map.QueryCacheEventData>",
    "List_IndexConfig": "IList<com.hazelcast.config.IndexConfig>",
    "List_AttributeConfig": "IList<com.hazelcast.config.AttributeConfig>",
    "List_ListenerConfigHolder": "IList<com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "IList<com.hazelcast.config.CacheSimpleEntryListenerConfig>",
    "List_StackTraceElement": "IList<Hazelcast.Util.StackTraceElement>",

    "EntryList_String_String": "IList<KeyValuePair<string, string>>",
    "EntryList_String_byteArray": "IList<KeyValuePair<string, byte[]>>",
    "EntryList_Long_byteArray": "IList<KeyValuePair<long, byte[]>>",
    "EntryList_Integer_UUID": "IList<KeyValuePair<int, Guid>>",
    "EntryList_UUID_Long": "IList<KeyValuePair<Guid, long>>",
    "EntryList_String_EntryList_Integer_Long": "IList<KeyValuePair<string, IList<KeyValuePair<int, long>>>>",
    "EntryList_Address_List_Integer": "IList<KeyValuePair<IO.Address, IList<int>>>",
    "EntryList_Data_Data": "IList<KeyValuePair<IData, IData>>",
    "EntryList_Member_List_ScheduledTaskHandler": "IList<KeyValuePair<Core.Member, IList<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>>>"
}