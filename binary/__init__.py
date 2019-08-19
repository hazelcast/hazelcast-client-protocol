FixedLengthTypes = [
    "boolean",
    "byte",
    "int",
    "long",
    "UUID"
]

VarLengthTypes = [
    'byteArray',
    'longArray',
    'String',
    'Data'
]

FixedMapTypes = [
    'Map_Integer_UUID',
    'Map_UUID_Long',
    'Map_Integer_Long'
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
    'Member',
    'QueryCacheEventData',
    'RaftGroupId',
    'ScheduledTaskHandler',
    'SimpleEntryView',
    'WanReplicationRef',
    'Xid'
]

CustomConfigTypes = [
    'CacheSimpleEntryListenerConfig',
    'EventJournalConfig',
    'EvictionConfigHolder',
    'HotRestartConfig',
    'ListenerConfigHolder',
    'AttributeConfig',
    'MapIndexConfig',
    'MapStoreConfigHolder',
    'MerkleTreeConfig',
    'NearCacheConfigHolder',
    'NearCachePreloaderConfig',
    'PredicateConfigHolder',
    'QueryCacheConfigHolder',
    'QueueStoreConfigHolder',
    'RingbufferStoreConfigHolder',
    'TimedExpiryPolicyFactoryConfig'
]

VarLengthMapTypes = [
    'Map_String_String',
    'Map_String_byteArray',
    'Map_String_Map_Integer_Long',
    'Map_Address_List_Integer',
    'Map_Data_Data',
    'Map_Member_List_ScheduledTaskHandler'
]

VarLengthListTypes = [
    'List_Address',
    'List_byteArray',
    'List_CacheEventData',
    'List_CacheSimpleEntryListenerConfig',
    'List_Data',
    'List_DistributedObjectInfo',
    'List_ListenerConfigHolder',
    'List_AttributeConfig',
    'List_MapIndexConfig',
    'List_Member',
    'List_QueryCacheConfigHolder',
    'List_QueryCacheEventData',
    'List_ScheduledTaskHandler',
    'List_String',
    'List_Xid',
]

AllTypes = FixedLengthTypes + VarLengthTypes + FixedMapTypes + FixedListTypes + CustomTypes + CustomConfigTypes \
           + VarLengthMapTypes + VarLengthListTypes
