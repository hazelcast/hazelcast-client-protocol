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
    "SqlPage": "com.hazelcast.sql.impl.client.SqlPage",

    "Address": "com.hazelcast.cluster.Address",
    "ErrorHolder": "com.hazelcast.client.impl.protocol.exception.ErrorHolder",
    "StackTraceElement": "java.lang.StackTraceElement",
    "SimpleEntryView": "com.hazelcast.map.impl.SimpleEntryView<com.hazelcast.internal.serialization.Data, com.hazelcast.internal.serialization.Data>",
    "ReplicatedMapEntryViewHolder": "com.hazelcast.replicatedmap.impl.record.ReplicatedMapEntryViewHolder",
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
    "CPDistributedObjectInfo": "com.hazelcast.client.cp.internal.CPDistributedObjectInfo",
    "IndexConfig": "com.hazelcast.config.IndexConfig",
    "BitmapIndexOptions": "com.hazelcast.config.BitmapIndexOptions",
    "BTreeIndexConfig": "com.hazelcast.config.BTreeIndexConfig",
    "AttributeConfig": "com.hazelcast.config.AttributeConfig",
    "ListenerConfigHolder": "com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder",
    "CacheSimpleEntryListenerConfig": "com.hazelcast.config.CacheSimpleEntryListenerConfig",
    "ClientBwListEntry": "com.hazelcast.internal.management.dto.ClientBwListEntryDTO",
    "EndpointQualifier": "com.hazelcast.instance.EndpointQualifier",

    "Map_String_String": "java.util.Map<java.lang.String, java.lang.String>",
    "Map_String_Data": "java.util.Map<java.lang.String, com.hazelcast.internal.serialization.Data>",
    "Map_EndpointQualifier_Address": "java.util.Map<com.hazelcast.instance.EndpointQualifier, com.hazelcast.cluster.Address>",

    "List_CPMember": "java.util.Collection<com.hazelcast.cp.CPMember>",
    "Schema": "com.hazelcast.internal.serialization.impl.compact.Schema",
    "FieldDescriptor": "com.hazelcast.internal.serialization.impl.compact.FieldDescriptor",
    "List_FieldDescriptor": "java.util.List<com.hazelcast.internal.serialization.impl.compact.FieldDescriptor>",
    "HazelcastJsonValue": "com.hazelcast.core.HazelcastJsonValue",
    "DataPersistenceConfig": "com.hazelcast.config.DataPersistenceConfig",
    "Capacity": "com.hazelcast.memory.Capacity",
    "MemoryTierConfig": "com.hazelcast.config.MemoryTierConfig",
    "DiskTierConfig": "com.hazelcast.config.DiskTierConfig",
    "TieredStoreConfig": "com.hazelcast.config.TieredStoreConfig",
    "SqlSummary": "com.hazelcast.jet.impl.SqlSummary",
    "PartitioningAttributeConfig": "com.hazelcast.config.PartitioningAttributeConfig",
    "WanConsumerConfigHolder": "com.hazelcast.client.impl.protocol.codec.holder.WanConsumerConfigHolder",
    "WanCustomPublisherConfigHolder": "com.hazelcast.client.impl.protocol.codec.holder.WanCustomPublisherConfigHolder",
    "List_WanCustomPublisherConfigHolder": "java.util.List<com.hazelcast.client.impl.protocol.codec.holder.WanCustomPublisherConfigHolder>",
    "WanBatchPublisherConfigHolder": "com.hazelcast.client.impl.protocol.codec.holder.WanBatchPublisherConfigHolder",
    "List_WanBatchPublisherConfigHolder": "java.util.List<com.hazelcast.client.impl.protocol.codec.holder.WanBatchPublisherConfigHolder>",
    "AwsConfig": "com.hazelcast.config.AwsConfig",
    "GcpConfig": "com.hazelcast.config.GcpConfig",
    "AzureConfig": "com.hazelcast.config.AzureConfig",
    "KubernetesConfig": "com.hazelcast.config.KubernetesConfig",
    "EurekaConfig": "com.hazelcast.config.EurekaConfig",
    "DiscoveryStrategyConfig": "com.hazelcast.client.impl.protocol.codec.holder.DiscoveryStrategyConfigHolder",
    "List_DiscoveryStrategyConfig": "java.util.List<com.hazelcast.client.impl.protocol.codec.holder.DiscoveryStrategyConfigHolder>",
    "DiscoveryConfig": "com.hazelcast.client.impl.protocol.codec.holder.DiscoveryConfigHolder",
    "WanSyncConfig": "com.hazelcast.client.impl.protocol.codec.holder.WanSyncConfigHolder",
    "ResourceDefinition": "com.hazelcast.client.impl.protocol.task.dynamicconfig.ResourceDefinitionHolder",
    "List_ResourceDefinition": "java.util.List<com.hazelcast.client.impl.protocol.task.dynamicconfig.ResourceDefinitionHolder>"
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
    "SqlQueryId": "com.hazelcast.sql.impl.QueryId",
    "SqlError": "com.hazelcast.sql.impl.client.SqlError",
    "SqlColumnMetadata": "com.hazelcast.sql.SqlColumnMetadata",
    "JobAndSqlSummary": "com.hazelcast.jet.impl.JobAndSqlSummary",
    "CPMember": "com.hazelcast.cp.CPMember",
    "MigrationState": "com.hazelcast.partition.MigrationState",

    "List_Long": "java.util.Collection<java.lang.Long>",
    "List_Integer": "java.util.Collection<java.lang.Integer>",
    "List_UUID": "java.util.Collection<java.util.UUID>",
    "List_String": "java.util.Collection<java.lang.String>",
    "List_Xid": "java.util.Collection<javax.transaction.xa.Xid>",
    "List_Data": "java.util.Collection<com.hazelcast.internal.serialization.Data>",
    "List_List_Data": "java.util.Collection<java.util.Collection<com.hazelcast.internal.serialization.Data>>",
    "ListCN_Data": "java.util.Collection<com.hazelcast.internal.serialization.Data>",
    "List_ListCN_Data": "java.util.Collection<java.util.Collection<com.hazelcast.internal.serialization.Data>>",
    "List_MemberInfo": "java.util.Collection<com.hazelcast.internal.cluster.MemberInfo>",
    "List_ScheduledTaskHandler": "java.util.Collection<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>",
    "List_CacheEventData": "java.util.Collection<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "java.util.Collection<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "java.util.Collection<com.hazelcast.client.impl.client.DistributedObjectInfo>",
    "List_CPDistributedObjectInfo": "java.util.Collection<com.hazelcast.client.cp.internal.CPDistributedObjectInfo>",
    "List_QueryCacheEventData": "java.util.Collection<com.hazelcast.map.impl.querycache.event.QueryCacheEventData>",
    "List_IndexConfig": "java.util.Collection<com.hazelcast.config.IndexConfig>",
    "List_AttributeConfig": "java.util.Collection<com.hazelcast.config.AttributeConfig>",
    "List_ListenerConfigHolder": "java.util.Collection<com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "java.util.Collection<com.hazelcast.config.CacheSimpleEntryListenerConfig>",
    "List_StackTraceElement": "java.util.Collection<java.lang.StackTraceElement>",
    "List_ClientBwListEntry": "java.util.Collection<com.hazelcast.internal.management.dto.ClientBwListEntryDTO>",
    "List_MCEvent": "java.util.Collection<com.hazelcast.internal.management.dto.MCEventDTO>",
    "List_SqlColumnMetadata": "java.util.List<com.hazelcast.sql.SqlColumnMetadata>",
    "List_JobAndSqlSummary": "java.util.List<com.hazelcast.jet.impl.JobAndSqlSummary>",
    "List_Schema": "java.util.Collection<com.hazelcast.internal.serialization.impl.compact.Schema>",

    "Set_UUID": "java.util.Collection<java.util.UUID>",

    "EntryList_String_String": "java.util.Collection<java.util.Map.Entry<java.lang.String, java.lang.String>>",
    "EntryList_String_byteArray": "java.util.Collection<java.util.Map.Entry<java.lang.String, byte[]>>",
    "EntryList_Long_byteArray": "java.util.Collection<java.util.Map.Entry<java.lang.Long, byte[]>>",
    "EntryList_Integer_UUID": "java.util.Collection<java.util.Map.Entry<java.lang.Integer, java.util.UUID>>",
    "EntryList_Integer_Long": "java.util.Collection<java.util.Map.Entry<java.lang.Integer, java.lang.Long>>",
    "EntryList_Integer_Integer": "java.util.Collection<java.util.Map.Entry<java.lang.Integer, java.lang.Integer>>",
    "EntryList_UUID_Long": "java.util.Collection<java.util.Map.Entry<java.util.UUID, java.lang.Long>>",
    "EntryList_String_EntryList_Integer_Long": "java.util.Collection<java.util.Map.Entry<java.lang.String, java.util.List<java.util.Map.Entry<java.lang.Integer, java.lang.Long>>>>",
    "EntryList_UUID_UUID": "java.util.Collection<java.util.Map.Entry<java.util.UUID, java.util.UUID>>",
    "EntryList_UUID_List_Integer": "java.util.Collection<java.util.Map.Entry<java.util.UUID, java.util.List<java.lang.Integer>>>",
    "EntryList_Data_Data": "java.util.Collection<java.util.Map.Entry<com.hazelcast.internal.serialization.Data, com.hazelcast.internal.serialization.Data>>",
    "EntryList_Data_List_Data": "java.util.Collection<java.util.Map.Entry<com.hazelcast.internal.serialization.Data, java.util.Collection<com.hazelcast.internal.serialization.Data>>>",
    "List_PartitioningAttributeConfig": "java.util.Collection<com.hazelcast.config.PartitioningAttributeConfig>",
    "List_SimpleEntryView": "java.util.Collection<com.hazelcast.map.impl.SimpleEntryView<com.hazelcast.internal.serialization.Data, com.hazelcast.internal.serialization.Data>>",
    "List_ReplicatedMapEntryViewHolder": "java.util.Collection<com.hazelcast.replicatedmap.impl.record.ReplicatedMapEntryViewHolder>",
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
    "SqlQueryId": "com.hazelcast.sql.impl.QueryId",
    "SqlError": "com.hazelcast.sql.impl.client.SqlError",
    "SqlColumnMetadata": "com.hazelcast.sql.SqlColumnMetadata",
    "JobAndSqlSummary": "com.hazelcast.jet.impl.JobAndSqlSummary",
    "CPMember": "com.hazelcast.cp.internal.CPMemberInfo",
    "MigrationState": "com.hazelcast.internal.partition.MigrationStateImpl",

    "List_Long": "java.util.List<java.lang.Long>",
    "List_Integer": "java.util.List<java.lang.Integer>",
    "List_UUID": "java.util.List<java.util.UUID>",
    "List_Xid": "java.util.List<javax.transaction.xa.Xid>",
    "List_String": "java.util.List<java.lang.String>",
    "List_Data": "java.util.List<com.hazelcast.internal.serialization.Data>",
    "List_List_Data": "java.util.List<java.util.List<com.hazelcast.internal.serialization.Data>>",
    "ListCN_Data": "java.util.List<com.hazelcast.internal.serialization.Data>",
    "List_ListCN_Data": "java.util.List<java.util.List<com.hazelcast.internal.serialization.Data>>",
    "List_MemberInfo": "java.util.List<com.hazelcast.internal.cluster.MemberInfo>",
    "List_CacheEventData": "java.util.List<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "java.util.List<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "java.util.List<com.hazelcast.client.impl.client.DistributedObjectInfo>",
    "List_CPDistributedObjectInfo": "java.util.List<com.hazelcast.client.cp.internal.CPDistributedObjectInfo>",
    "List_QueryCacheEventData": "java.util.List<com.hazelcast.map.impl.querycache.event.DefaultQueryCacheEventData>",
    "List_IndexConfig": "java.util.List<com.hazelcast.config.IndexConfig>",
    "List_AttributeConfig": "java.util.List<com.hazelcast.config.AttributeConfig>",
    "List_ListenerConfigHolder": "java.util.List<com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "java.util.List<com.hazelcast.config.CacheSimpleEntryListenerConfig>",
    "List_StackTraceElement": "java.util.List<java.lang.StackTraceElement>",
    "List_ClientBwListEntry": "java.util.List<com.hazelcast.internal.management.dto.ClientBwListEntryDTO>",
    "List_MCEvent": "java.util.List<com.hazelcast.internal.management.dto.MCEventDTO>",
    "List_ScheduledTaskHandler": "java.util.Collection<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>",
    "List_SqlColumnMetadata": "java.util.List<com.hazelcast.sql.SqlColumnMetadata>",
    "List_JobAndSqlSummary": "java.util.List<com.hazelcast.jet.impl.JobAndSqlSummary>",
    "List_Schema": "java.util.List<com.hazelcast.internal.serialization.impl.compact.Schema>",

    "Set_UUID": "java.util.Set<java.util.UUID>",

    "EntryList_String_String": "java.util.List<java.util.Map.Entry<java.lang.String, java.lang.String>>",
    "EntryList_String_byteArray": "java.util.List<java.util.Map.Entry<java.lang.String, byte[]>>",
    "EntryList_Long_byteArray": "java.util.List<java.util.Map.Entry<java.lang.Long, byte[]>>",
    "EntryList_Integer_UUID": "java.util.List<java.util.Map.Entry<java.lang.Integer, java.util.UUID>>",
    "EntryList_Integer_Long": "java.util.List<java.util.Map.Entry<java.lang.Integer, java.util.Long>>",
    "EntryList_Integer_Integer": "java.util.List<java.util.Map.Entry<java.lang.Integer, java.lang.Integer>>",
    "EntryList_UUID_Long": "java.util.List<java.util.Map.Entry<java.util.UUID, java.lang.Long>>",
    "EntryList_String_EntryList_Integer_Long": "java.util.List<java.util.Map.Entry<java.lang.String, java.util.List<java.util.Map.Entry<java.lang.Integer, java.lang.Long>>>>",
    "EntryList_UUID_UUID": "java.util.List<java.util.Map.Entry<java.util.UUID, java.util.UUID>>",
    "EntryList_UUID_List_Integer": "java.util.List<java.util.Map.Entry<java.util.UUID, java.util.List<java.lang.Integer>>>",
    "EntryList_Data_Data": "java.util.List<java.util.Map.Entry<com.hazelcast.internal.serialization.Data, com.hazelcast.internal.serialization.Data>>",
    "EntryList_Data_List_Data": "java.util.List<java.util.Map.Entry<com.hazelcast.internal.serialization.Data, java.util.List<com.hazelcast.internal.serialization.Data>>>",
    "List_PartitioningAttributeConfig": "java.util.List<com.hazelcast.config.PartitioningAttributeConfig>",
    "List_SimpleEntryView": "java.util.List<com.hazelcast.map.impl.SimpleEntryView<com.hazelcast.internal.serialization.Data, com.hazelcast.internal.serialization.Data>>",
    "List_ReplicatedMapEntryViewHolder": "java.util.List<com.hazelcast.replicatedmap.impl.record.ReplicatedMapEntryViewHolder>",
}
