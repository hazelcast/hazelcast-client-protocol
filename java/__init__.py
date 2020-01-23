def java_types_encode(key):
    try:
        return _java_types_encode[key]
    except KeyError:
        return _java_types_common[key]


def java_types_decode(key):
    try:
        return _java_types_decode[key]
    except KeyError:
        return _java_types_common[key]


_java_types_common = {
    "boolean": "boolean",
    "int": "int",
    "long": "long",
    "byte": "byte",
    "Integer": "java.lang.Integer",
    "Long": "java.lang.Long",
    "UUID": "java.util.UUID",

    "longArray": "long[]",
    "byteArray": "byte[]",
    "String": "java.lang.String",
    "Data": "com.hazelcast.internal.serialization.Data",

    "Address": "com.hazelcast.cluster.Address",
    "ErrorHolder": "com.hazelcast.client.impl.protocol.exception.ErrorHolder",
    "StackTraceElement": "java.lang.StackTraceElement",
    "SimpleEntryView": "com.hazelcast.map.impl.SimpleEntryView<com.hazelcast.internal.serialization.Data, com.hazelcast.internal.serialization.Data>",
    "RaftGroupId": "com.hazelcast.cp.internal.RaftGroupId",
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
    "DistributedObjectInfo": "com.hazelcast.client.impl.client.DistributedObjectInfo",
    "IndexConfig": "com.hazelcast.config.IndexConfig",
    "AttributeConfig": "com.hazelcast.config.AttributeConfig",
    "ListenerConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder",
    "CacheSimpleEntryListenerConfig": "com.hazelcast.config.CacheSimpleEntryListenerConfig",
    "ClientBwListEntry": "com.hazelcast.internal.management.dto.ClientBwListEntryDTO",

    "Map_String_String": "java.util.Map<java.lang.String, java.lang.String>"
}

_java_types_encode = {
    "CacheEventData": "com.hazelcast.cache.impl.CacheEventData",
    "QueryCacheEventData": "com.hazelcast.map.impl.querycache.event.QueryCacheEventData",
    "ScheduledTaskHandler": "com.hazelcast.scheduledexecutor.ScheduledTaskHandler",
    "Xid": "javax.transaction.xa.Xid",
    "ClientBwListEntry": "com.hazelcast.internal.management.dto.ClientBwListEntryDTO",
    "MemberInfo": "com.hazelcast.internal.cluster.MemberInfo",
    "MemberVersion": "com.hazelcast.version.MemberVersion",
    "MCEvent": "com.hazelcast.internal.management.dto.MCEventDTO",
    "AnchorDataListHolder": "com.hazelcast.client.impl.protocol.codec.holder.AnchorDataListHolder",
    "PagingPredicateHolder": "com.hazelcast.client.impl.protocol.codec.holder.PagingPredicateHolder",

    "List_Long": "java.util.Collection<java.lang.Long>",
    "List_Integer": "java.util.Collection<java.lang.Integer>",
    "List_UUID": "java.util.Collection<java.util.UUID>",
    "List_String": "java.util.Collection<java.lang.String>",
    "List_Xid": "java.util.Collection<javax.transaction.xa.Xid>",
    "List_Data": "java.util.Collection<com.hazelcast.internal.serialization.Data>",
    "ListCN_Data": "java.util.Collection<com.hazelcast.internal.serialization.Data>",
    "List_MemberInfo": "java.util.Collection<com.hazelcast.internal.cluster.MemberInfo>",
    "List_ScheduledTaskHandler": "java.util.Collection<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>",
    "List_CacheEventData": "java.util.Collection<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "java.util.Collection<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "java.util.Collection<com.hazelcast.client.impl.client.DistributedObjectInfo>",
    "List_QueryCacheEventData": "java.util.Collection<com.hazelcast.map.impl.querycache.event.QueryCacheEventData>",
    "List_IndexConfig": "java.util.Collection<com.hazelcast.config.IndexConfig>",
    "List_AttributeConfig": "java.util.Collection<com.hazelcast.config.AttributeConfig>",
    "List_ListenerConfigHolder": "java.util.Collection<com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "java.util.Collection<com.hazelcast.config.CacheSimpleEntryListenerConfig>",
    "List_StackTraceElement": "java.util.Collection<java.lang.StackTraceElement>",
    "List_ClientBwListEntry": "java.util.Collection<com.hazelcast.internal.management.dto.ClientBwListEntryDTO>",
    "List_MCEvent": "java.util.Collection<com.hazelcast.internal.management.dto.MCEventDTO>",

    "EntryList_String_String": "java.util.Collection<java.util.Map.Entry<java.lang.String, java.lang.String>>",
    "EntryList_String_byteArray": "java.util.Collection<java.util.Map.Entry<java.lang.String, byte[]>>",
    "EntryList_Long_byteArray": "java.util.Collection<java.util.Map.Entry<java.lang.Long, byte[]>>",
    "EntryList_Integer_UUID": "java.util.Collection<java.util.Map.Entry<java.lang.Integer, java.util.UUID>>",
    "EntryList_Integer_Long": "java.util.Collection<java.util.Map.Entry<java.lang.Integer, java.lang.Long>>",
    "EntryList_Integer_Integer": "java.util.Collection<java.util.Map.Entry<java.lang.Integer, java.lang.Integer>>",
    "EntryList_UUID_Long": "java.util.Collection<java.util.Map.Entry<java.util.UUID, java.lang.Long>>",
    "EntryList_String_EntryList_Integer_Long": "java.util.Collection<java.util.Map.Entry<java.lang.String, java.util.List<java.util.Map.Entry<java.lang.Integer, java.lang.Long>>>>",
    "EntryList_UUID_Address": "java.util.Collection<java.util.Map.Entry<java.util.UUID, com.hazelcast.cluster.Address>>",
    "EntryList_UUID_List_Integer": "java.util.Collection<java.util.Map.Entry<java.util.UUID, java.util.List<java.lang.Integer>>>",
    "EntryList_Data_Data": "java.util.Collection<java.util.Map.Entry<com.hazelcast.internal.serialization.Data, com.hazelcast.internal.serialization.Data>>",
}

_java_types_decode = {
    "CacheEventData": "com.hazelcast.cache.impl.CacheEventDataImpl",
    "QueryCacheEventData": "com.hazelcast.map.impl.querycache.event.DefaultQueryCacheEventData",
    "ScheduledTaskHandler": "com.hazelcast.scheduledexecutor.impl.ScheduledTaskHandlerImpl",
    "Xid": "com.hazelcast.transaction.impl.xa.SerializableXID",
    "ClientBwListEntry": "com.hazelcast.internal.management.dto.ClientBwListEntryDTO",
    "MemberInfo": "com.hazelcast.internal.cluster.MemberInfo",
    "MemberVersion": "com.hazelcast.version.MemberVersion",
    "MCEvent": "com.hazelcast.internal.management.dto.MCEventDTO",
    "AnchorDataListHolder": "com.hazelcast.client.impl.protocol.codec.holder.AnchorDataListHolder",
    "PagingPredicateHolder": "com.hazelcast.client.impl.protocol.codec.holder.PagingPredicateHolder",

    "List_Long": "java.util.List<java.lang.Long>",
    "List_Integer": "java.util.List<java.lang.Integer>",
    "List_UUID": "java.util.List<java.util.UUID>",
    "List_Xid": "java.util.List<javax.transaction.xa.Xid>",
    "List_String": "java.util.List<java.lang.String>",
    "List_Data": "java.util.List<com.hazelcast.internal.serialization.Data>",
    "ListCN_Data": "java.util.List<com.hazelcast.internal.serialization.Data>",
    "List_MemberInfo": "java.util.List<com.hazelcast.internal.cluster.MemberInfo>",
    "List_CacheEventData": "java.util.List<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "java.util.List<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "java.util.List<com.hazelcast.client.impl.client.DistributedObjectInfo>",
    "List_QueryCacheEventData": "java.util.List<com.hazelcast.map.impl.querycache.event.DefaultQueryCacheEventData>",
    "List_IndexConfig": "java.util.List<com.hazelcast.config.IndexConfig>",
    "List_AttributeConfig": "java.util.List<com.hazelcast.config.AttributeConfig>",
    "List_ListenerConfigHolder": "java.util.List<com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "java.util.List<com.hazelcast.config.CacheSimpleEntryListenerConfig>",
    "List_StackTraceElement": "java.util.List<java.lang.StackTraceElement>",
    "List_ClientBwListEntry": "java.util.List<com.hazelcast.internal.management.dto.ClientBwListEntryDTO>",
    "List_MCEvent": "java.util.List<com.hazelcast.internal.management.dto.MCEventDTO>",
    "List_ScheduledTaskHandler": "java.util.Collection<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>",

    "EntryList_String_String": "java.util.List<java.util.Map.Entry<java.lang.String, java.lang.String>>",
    "EntryList_String_byteArray": "java.util.List<java.util.Map.Entry<java.lang.String, byte[]>>",
    "EntryList_Long_byteArray": "java.util.List<java.util.Map.Entry<java.lang.Long, byte[]>>",
    "EntryList_Integer_UUID": "java.util.List<java.util.Map.Entry<java.lang.Integer, java.util.UUID>>",
    "EntryList_Integer_Long": "java.util.List<java.util.Map.Entry<java.lang.Integer, java.util.Long>>",
    "EntryList_Integer_Integer": "java.util.List<java.util.Map.Entry<java.lang.Integer, java.lang.Integer>>",
    "EntryList_UUID_Long": "java.util.List<java.util.Map.Entry<java.util.UUID, java.lang.Long>>",
    "EntryList_String_EntryList_Integer_Long": "java.util.List<java.util.Map.Entry<java.lang.String, java.util.List<java.util.Map.Entry<java.lang.Integer, java.lang.Long>>>>",
    "EntryList_UUID_Address": "java.util.List<java.util.Map.Entry<java.util.UUID, com.hazelcast.cluster.Address>>",
    "EntryList_UUID_List_Integer": "java.util.List<java.util.Map.Entry<java.util.UUID, java.util.List<java.lang.Integer>>>",
    "EntryList_Data_Data": "java.util.List<java.util.Map.Entry<com.hazelcast.internal.serialization.Data, com.hazelcast.internal.serialization.Data>>",
}
