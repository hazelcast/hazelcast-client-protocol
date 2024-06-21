FixSizedTypes = [
    "boolean",
    "byte",
    "int",
    "long",
    "UUID",
    "float",
]

VarSizedTypes = [
    'byteArray',
    'longArray',
    'floatArray',
    'String',
    'Data',
    'SqlPage',
]

FixSizedEntryListTypes = [
    'EntryList_Integer_UUID',
    'EntryList_UUID_Long',
    'EntryList_Integer_Long',
    'EntryList_Integer_Integer',
    'EntryList_Long_byteArray',
    'EntryList_UUID_UUID',
    'EntryList_UUID_List_Integer',
]

FixSizedMapTypes = [
]

FixSizedListTypes = [
    'List_Integer',
    'List_Long',
    'List_UUID'
]

FixSizedSetTypes = [
    'Set_UUID',
]

CustomTypes = [
    'Address',
    'CacheEventData',
    'DistributedObjectInfo',
    'QueryCacheEventData',
    'RaftGroupId',
    'ScheduledTaskHandler',
    'SimpleEntryView',
    'ReplicatedMapEntryViewHolder',
    'WanReplicationRef',
    'Xid',
    'ErrorHolder',
    'StackTraceElement',
    'ClientBwListEntry',
    'MemberInfo',
    'MemberVersion',
    'Version',
    'MCEvent',
    'AnchorDataListHolder',
    'PagingPredicateHolder',
    'EndpointQualifier',
    'SqlQueryId',
    'SqlError',
    'SqlColumnMetadata',
    'JobAndSqlSummary',
    'SqlSummary',
    'CPMember',
    'MigrationState',
    'FieldDescriptor',
    'Schema',
    'HazelcastJsonValue',
    'VectorDocument',
    'VectorSearchOptions',
    'VectorSearchResult',
    "VectorPair",
]

CustomConfigTypes = [
    'CacheSimpleEntryListenerConfig',
    'EventJournalConfig',
    'EvictionConfigHolder',
    'HotRestartConfig',
    'ListenerConfigHolder',
    'AttributeConfig',
    'IndexConfig',
    'BitmapIndexOptions',
    'BTreeIndexConfig',
    'MapStoreConfigHolder',
    'MerkleTreeConfig',
    'NearCacheConfigHolder',
    'NearCachePreloaderConfig',
    'PredicateConfigHolder',
    'QueryCacheConfigHolder',
    'QueueStoreConfigHolder',
    'RingbufferStoreConfigHolder',
    'TimedExpiryPolicyFactoryConfig',
    'DurationConfig',
    'MergePolicyConfig',
    'CacheConfigHolder',
    'DataPersistenceConfig',
    'Capacity',
    'MemoryTierConfig',
    'DiskTierConfig',
    'TieredStoreConfig',
    "PartitioningAttributeConfig",
    "WanConsumerConfigHolder",
    "WanCustomPublisherConfigHolder",
    "WanBatchPublisherConfigHolder",
    "AwsConfig",
    "GcpConfig",
    "AzureConfig",
    "KubernetesConfig",
    "EurekaConfig",
    "DiscoveryConfig",
    "DiscoveryStrategyConfig",
    "WanSyncConfig",
    "ResourceDefinition",
    "VectorCollectionConfig",
    "VectorIndexConfig"
]

VarSizedEntryListTypes = [
    'EntryList_String_String',
    'EntryList_String_byteArray',
    'EntryList_String_EntryList_Integer_Long',
    'EntryList_Data_Data',
    'EntryList_Data_List_Data',
    'EntryList_Data_VectorDocument'
]

VarSizedMapTypes = [
    'Map_String_String',
    'Map_EndpointQualifier_Address',
    'Map_String_Data',
    'Map_RaftGroupId_List_UUID',
]

VarSizedListTypes = [
    'List_byteArray',
    'List_CacheEventData',
    'List_CacheSimpleEntryListenerConfig',
    'List_Data',
    'List_DistributedObjectInfo',
    'List_ListenerConfigHolder',
    'List_AttributeConfig',
    'List_IndexConfig',
    'List_MemberInfo',
    'List_QueryCacheConfigHolder',
    'List_QueryCacheEventData',
    'List_ScheduledTaskHandler',
    'List_String',
    'List_Xid',
    'List_StackTraceElement',
    'List_ClientBwListEntry',
    'List_MCEvent',
    'List_SqlColumnMetadata',
    'List_JobAndSqlSummary',
    'List_CPMember',
    'List_RaftGroupId',
    'ListCN_Data',
    'List_List_Data',
    'List_FieldDescriptor',
    'List_PartitioningAttributeConfig',
    'List_WanCustomPublisherConfigHolder',
    'List_WanBatchPublisherConfigHolder',
    'List_SimpleEntryView',
    'List_ReplicatedMapEntryViewHolder',
    'List_VectorPair',
]

AllTypes = FixSizedTypes + VarSizedTypes + FixSizedEntryListTypes \
           + FixSizedMapTypes + FixSizedListTypes + FixSizedSetTypes \
           + CustomTypes + CustomConfigTypes + VarSizedEntryListTypes \
           + VarSizedMapTypes + VarSizedListTypes
