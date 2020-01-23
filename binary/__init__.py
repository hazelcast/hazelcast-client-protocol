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
    'Data'
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
]

CustomConfigTypes = [
    'CacheSimpleEntryListenerConfig',
    'EventJournalConfig',
    'EvictionConfigHolder',
    'HotRestartConfig',
    'ListenerConfigHolder',
    'AttributeConfig',
    'IndexConfig',
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
    'EntryList_UUID_List_Integer',
    'EntryList_Data_Data',
]

VarLengthMapTypes = [
    'Map_String_String',
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
]

AllTypes = FixedLengthTypes + VarLengthTypes + FixedEntryListTypes + FixedMapTypes + FixedListTypes \
           + CustomTypes + CustomConfigTypes + VarLengthEntryListTypes + VarLengthMapTypes + VarLengthListTypes
