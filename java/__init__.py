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
    "String": "java.lang.String",
    "Data": "com.hazelcast.nio.serialization.Data",

    "Xid": "javax.transaction.xa.Xid",
    "Member": "com.hazelcast.cluster.Member",
    "Address": "com.hazelcast.nio.Address",
    "SimpleEntryView": "com.hazelcast.map.impl.SimpleEntryView<com.hazelcast.nio.serialization.Data,com.hazelcast.nio.serialization.Data>",
    "RaftGroupId": "com.hazelcast.cp.internal.RaftGroupId",
    "QueryCacheEventData": "com.hazelcast.map.impl.querycache.event.QueryCacheEventData",
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

    "CacheEventData": "com.hazelcast.cache.impl.CacheEventData",
    "QueryCacheConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder",
    "DistributedObjectInfo": "com.hazelcast.client.impl.client.DistributedObjectInfo",
    "MapIndexConfig": "com.hazelcast.config.MapIndexConfig",
    "MapAttributeConfig": "com.hazelcast.config.MapAttributeConfig",
    "ListenerConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder",
    "CacheSimpleEntryListenerConfig": "com.hazelcast.config.CacheSimpleEntryListenerConfig",
    "ScheduledTaskHandler": "com.hazelcast.scheduledexecutor.ScheduledTaskHandler"
}

_java_types_encode = {
    "List_Long": "java.util.Collection<java.lang.Long>",
    "List_UUID": "java.util.Collection<java.util.UUID>",
    "List_String": "java.util.Collection<java.lang.String>",
    "List_Xid": "java.util.Collection<javax.transaction.xa.Xid>",
    "List_Data": "java.util.Collection<com.hazelcast.nio.serialization.Data>",
    "List_Member": "java.util.Collection<com.hazelcast.cluster.Member>",
    "List_CacheEventData": "java.util.Collection<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "java.util.Collection<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "java.util.Collection<com.hazelcast.client.impl.client.DistributedObjectInfo>",
    "List_QueryCacheEventData": "java.util.Collection<com.hazelcast.map.impl.querycache.event.QueryCacheEventData>",
    "List_MapIndexConfig": "java.util.Collection<com.hazelcast.config.MapIndexConfig>",
    "List_MapAttributeConfig": "java.util.Collection<com.hazelcast.config.MapAttributeConfig>",
    "List_ListenerConfigHolder": "java.util.Collection<com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "java.util.Collection<com.hazelcast.config.CacheSimpleEntryListenerConfig>",

    "Map_String_String": "java.util.Collection<java.util.Map.Entry<java.lang.String,java.lang.String>>",
    "Map_String_byteArray": "java.util.Collection<java.util.Map.Entry<java.lang.String,byte[]>>",
    "Map_Integer_UUID": "java.util.Collection<java.util.Map.Entry<java.lang.Integer,java.util.UUID>>",
    "Map_String_Long": "java.util.Collection<java.util.Map.Entry<java.lang.String,java.lang.Long>>",
    "Map_String_Map_Integer_Long": "java.util.Collection<java.util.Map.Entry<java.lang.String,java.util.List<java.util.Map.Entry<java.lang.Integer,java.lang.Long>>>>",
    "Map_Address_List_Integer": "java.util.Collection<java.util.Map.Entry<com.hazelcast.nio.Address,java.util.List<java.lang.Integer>>>",
    "Map_Data_Data": "java.util.Collection<java.util.Map.Entry<com.hazelcast.nio.serialization.Data,com.hazelcast.nio.serialization.Data>>",
    "Map_Member_List_ScheduledTaskHandler": "java.util.Collection<java.util.Map.Entry<com.hazelcast.cluster.Member,java.util.List<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>>>"
}

_java_types_decode = {
    "List_Long": "java.util.List<java.lang.Long>",
    "List_UUID": "java.util.List<java.util.UUID>",
    "List_Xid": "java.util.List<javax.transaction.xa.Xid>",
    "List_String": "java.util.List<java.lang.String>",
    "List_Data": "java.util.List<com.hazelcast.nio.serialization.Data>",
    "List_Member": "java.util.List<com.hazelcast.cluster.Member>",
    "List_CacheEventData": "java.util.List<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "java.util.List<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "java.util.List<com.hazelcast.client.impl.client.DistributedObjectInfo>",
    "List_QueryCacheEventData": "java.util.List<com.hazelcast.map.impl.querycache.event.QueryCacheEventData>",
    "List_MapIndexConfig": "java.util.List<com.hazelcast.config.MapIndexConfig>",
    "List_MapAttributeConfig": "java.util.List<com.hazelcast.config.MapAttributeConfig>",
    "List_ListenerConfigHolder": "java.util.List<com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "java.util.List<com.hazelcast.config.CacheSimpleEntryListenerConfig>",

    "Map_String_String": "java.util.List<java.util.Map.Entry<java.lang.String, java.lang.String>>",
    "Map_String_byteArray": "java.util.List<java.util.Map.Entry<java.lang.String,byte[]>>",
    "Map_Integer_UUID": "java.util.List<java.util.Map.Entry<java.lang.Integer, java.util.UUID>>",
    "Map_String_Long": "java.util.List<java.util.Map.Entry<java.lang.String, java.lang.Long>>",
    "Map_String_Map_Integer_Long": "java.util.List<java.util.Map.Entry<java.lang.String, java.util.List<java.util.Map.Entry<java.lang.Integer, java.lang.Long>>>>",
    "Map_Address_List_Integer": "java.util.List<java.util.Map.Entry<com.hazelcast.nio.Address, java.util.List<java.lang.Integer>>>",
    "Map_Data_Data": "java.util.List<java.util.Map.Entry<com.hazelcast.nio.serialization.Data, com.hazelcast.nio.serialization.Data>>",
    "Map_Member_List_ScheduledTaskHandler": "java.util.List<java.util.Map.Entry<com.hazelcast.cluster.Member, java.util.List<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>>>"
}
