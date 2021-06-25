FixedLengthTypes = [
    "boolean",
    "byte",
    "int",
    "long",
    "UUID",
]

VarLengthTypes = [
    'byteArray',
    'longArray',
    'String',
    'Data',
    'SqlPage'
]

FixedEntryListTypes = [
    'EntryList_Integer_UUID',
    'EntryList_UUID_Long',
    'EntryList_Integer_Long',
    'EntryList_Integer_Integer',
    'EntryList_Long_byteArray',
    'EntryList_UUID_UUID',
    'EntryList_UUID_List_Integer',
]

FixedMapTypes = [
]

FixedListTypes = [
    'List_Integer',
    'List_Long',
    'List_UUID'
]

CustomTypes = [
    'Address',
    'CacheEventData',
    'DistributedObjectInfo',
    'QueryCacheEventData',
    'RaftGroupId',
    'ScheduledTaskHandler',
    'SimpleEntryView',
    'WanReplicationRef',
    'Xid',
    'ErrorHolder',
    'StackTraceElement',
    'ClientBwListEntry',
    'MemberInfo',
    'MemberVersion',
    'MCEvent',
    'AnchorDataListHolder',
    'PagingPredicateHolder',
    'EndpointQualifier',
    'SqlQueryId',
    'SqlError',
    'SqlColumnMetadata',
    'CPMember',
    'MigrationState',
    'FieldDescriptor',
    'Schema'
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
]

VarLengthEntryListTypes = [
    'EntryList_String_String',
    'EntryList_String_byteArray',
    'EntryList_String_EntryList_Integer_Long',
    'EntryList_Data_Data',
    'EntryList_Data_List_Data',
]

VarLengthMapTypes = [
    'Map_String_String',
    'Map_EndpointQualifier_Address',
]

VarLengthListTypes = [
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
    'List_CPMember'
    'ListCN_Data',
    'List_List_Data',
    'List_FieldDescriptor'
]

AllTypes = FixedLengthTypes + VarLengthTypes + FixedEntryListTypes + FixedMapTypes + FixedListTypes \
           + CustomTypes + CustomConfigTypes + VarLengthEntryListTypes + VarLengthMapTypes + VarLengthListTypes
