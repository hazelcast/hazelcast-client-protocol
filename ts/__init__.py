def ts_types_encode(key):
    try:
        return _ts_types_encode[key]
    except KeyError:
        return _ts_types_common[key]


def ts_types_decode(key):
    try:
        return _ts_types_decode[key]
    except KeyError:
        return _ts_types_common[key]


_ts_types_common = {
    "boolean": "boolean",
    "int": "number",
    "long": "Long",
    "byte": "number",
    "Integer": "number",
    "Long": "Long",
    "UUID": "UUID",

    "longArray": "Array<Long>",
    "String": "string",
    "Data": "Data",

    "Xid": "Xid",
    "Member": "Member",
    "Address": "Address",
    "SimpleEntryView": "EntryView<Data, Data>",
    "RaftGroupId": "RaftGroupId",
    "QueryCacheEventData": "QueryCacheEventData",
    "WanReplicationRef": "WanReplicationRef",
    "HotRestartConfig": "HotRestartConfig",
    "EventJournalConfig": "EventJournalConfig",
    "MerkleTreeConfig": "MerkleTreeConfig",
    "TimedExpiryPolicyFactoryConfig": "TimedExpiryPolicyFactoryConfig",
    "MapStoreConfigHolder": "MapStoreConfigHolder",
    "QueueStoreConfigHolder": "QueueStoreConfigHolder",
    "RingbufferStoreConfigHolder": "RingbufferStoreConfigHolder",
    "NearCacheConfigHolder": "NearCacheConfigHolder",
    "EvictionConfigHolder": "EvictionConfigHolder",

    "CacheEventData": "CacheEventData",
    "QueryCacheConfigHolder": "QueryCacheConfigHolder",
    "DistributedObjectInfo": "DistributedObjectInfo",
    "MapIndexConfig": "MapIndexConfig",
    "MapAttributeConfig": "MapAttributeConfig",
    "ListenerConfigHolder": "ListenerConfigHolder",
    "CacheSimpleEntryListenerConfig": "CacheSimpleEntryListenerConfig",
    "ScheduledTaskHandler": "ScheduledTaskHandler"
}

_ts_types_encode = {
    "List_Long": "Array<Long>",
    "List_UUID": "Array<UUID>",
    "List_String": "Array<string>",
    "List_Xid": "Array<Xid>",
    "List_Data": "Array<Data>",
    "ListCN_Data": "Array<Data>",
    "List_Member": "Array<Member>",
    "List_CacheEventData": "Array<CacheEventData>",
    "List_QueryCacheConfigHolder": "Array<QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "Array<DistributedObjectInfo>",
    "List_QueryCacheEventData": "Array<QueryCacheEventData>",
    "List_MapIndexConfig": "Array<MapIndexConfig>",
    "List_MapAttributeConfig": "Array<MapAttributeConfig>",
    "List_ListenerConfigHolder": "Array<ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "Array<CacheSimpleEntryListenerConfig>",

    "Map_String_String": "Array<[string, string]>",
    "Map_String_byteArray": "Array<[string, Buffer]>",
    "Map_Integer_UUID": "Array<[number, UUID]>",
    "Map_String_Long": "Array<[string, Long]>",
    "Map_String_Map_Integer_Long": "Array<[string, Array<[number,Long]>]>",
    "Map_Address_List_Integer": "Array<[Address, Array<number>]>",
    "Map_Data_Data": "Array<[Data,Data]>",
    "Map_Member_List_ScheduledTaskHandler": "Array<[Member, Array<ScheduledTaskHandler>]>"
}

_ts_types_decode = {
    "List_Long": "Array<Long>",
    "List_UUID": "Array<UUID>",
    "List_String": "string[]",
    "List_Xid": "Array<Xid>",
    "List_Data": "Array<Data>",
    "ListCN_Data": "Array<Data>",
    "List_Member": "Array<Member>",
    "List_CacheEventData": "Array<CacheEventData>",
    "List_QueryCacheConfigHolder": "Array<QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "Array<DistributedObjectInfo>",
    "List_QueryCacheEventData": "Array<QueryCacheEventData>",
    "List_MapIndexConfig": "Array<MapIndexConfig>",
    "List_MapAttributeConfig": "Array<MapAttributeConfig>",
    "List_ListenerConfigHolder": "Array<ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "Array<CacheSimpleEntryListenerConfig>",

    "Map_String_String": "Array<[string,string]>",
    "Map_String_byteArray": "Array<[string,Buffer]>",
    "Map_Integer_UUID": "Array<[number,UUID]>",
    "Map_String_Long": "Array<[string,Long]>",
    "Map_String_Map_Integer_Long": "Array<[string, Array<[number,Long]>]>",
    "Map_Address_List_Integer": "Array<[Address, Array<number>]>",
    "Map_Data_Data": "Array<[Data,Data]>",
    "Map_Member_List_ScheduledTaskHandler": "Array<[Member, Array<ScheduledTaskHandler>]>"
}
