go_reserved_words = ["type", "break", "default", "func", "interface",
                     "select", "case", "defer", "go", "map", "struct",
                     "goto", "chan", "else", "switch", "package", "if",
                     "fallthrough", "range", "continue", "const", "for",
                     "import", "return", "var"]

go_ignore_service_list = [7, 8, 9, 10, 11, 12, 19, 20, 22, 24, 25, 26, 27, 28, 30, 31, 32]


def go_types_encode(key):
    try:
        go_type = _go_types_encode[key]
    except KeyError:
        go_type = _go_types_common[key]
    if go_type == "NA":
        raise NotImplementedError("Missing type Mapping")
    return go_type


def go_types_decode(key):
    try:
        go_type = _go_types_decode[key]
    except KeyError:
        go_type = _go_types_common[key]
    if go_type == "NA":
        raise NotImplementedError("Missing type Mapping")
    return go_type


def go_escape_keyword(value):
    if value in go_reserved_words:
        return "_" + value
    return value


_go_types_common = {
    "boolean": "bool",
    "int": "int32",
    "long": "int64",
    "byte": "byte",
    "Integer": "int32",
    "Long": "int64",
    "UUID": "bufutil.Uuid",

    "longArray": "[]int64",
    "byteArray": "[]byte",
    "ByteArray": "[]byte",
    "String": "string",
    "Data": "bufutil.Data",

    "Address": "Address",
    "ErrorHolder": "ErrorHolder",
    "StackTraceElement": "StackTraceElement",
    "SimpleEntryView": "SimpleEntryView",
    "RaftGroupId": "NA",
    "WanReplicationRef": "NA",
    "HotRestartConfig": 'NA',
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
    "List_MemberInfo": "[]interface{}",
    "PagingPredicateHolder": "NA",
    "MemberVersion": "NA",
    "MCEvent": "NA",

    "MergePolicyConfig": "NA",
    "CacheConfigHolder": "NA",
    "CacheEventData": "NA",
    "QueryCacheConfigHolder": "NA",
    "DistributedObjectInfo": "DistributedObjectInfo",
    "IndexConfig": "IndexConfig",
    "AttributeConfig": "NA",
    "ListenerConfigHolder": "NA",
    "CacheSimpleEntryListenerConfig": "NA",
    "ClientBwListEntry": "NA",
    "AnchorDataListHolder": "NA",

    "Map_String_String": "map[string]string",
    "EntryList_UUID_List_Integer": "[]*bufutil.Pair",
    "EntryList_Integer_Integer": "NA",
    "List_Integer": "NA",

}

_go_types_encode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "Member": "proto.Member",
    "ClientBwListEntry": "NA",

    "List_Long": "[]int64",
    "List_UUID": "[]string",
    "List_Xid": "NA",
    "List_String": "[]string",
    "List_Data": "[]bufutil.Data",
    "ListCN_Data": "[]bufutil.Data",
    "List_Member": "[]Member",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "[]DistributedObjectInfo",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "[]IndexConfig",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "NA",
    "List_ClientBwListEntry": "NA",

    "EntryList_String_String": "[]*bufutil.Pair",
    "EntryList_String_byteArray": "[]*bufutil.Pair",
    "EntryList_Long_byteArray": "[]*bufutil.Pair",
    "EntryList_Integer_UUID": "[]*bufutil.Pair",
    "EntryList_UUID_Long": "[]*bufutil.Pair",
    "EntryList_String_EntryList_Integer_Long": "[[]map[string]string][]map[int]int64",
    "EntryList_Data_Data": "[]*bufutil.Pair",
    "EntryList_Member_List_ScheduledTaskHandler": "NA"
}

_go_types_decode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "Member": "Member",
    "ClientBwListEntry": "NA",
    "List_Long": "[]int64",
    "List_UUID": "[]string",
    "List_Xid": "NA",
    "List_String": "[]string",
    "List_Data": "[]bufutil.Data",
    "ListCN_Data": "[]bufutil.Data",
    "List_Member": "[]Member",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "[]DistributedObjectInfo",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "[]IndexConfig",
    "List_AttributeConfig": "[]AttributeConfig",
    "List_ListenerConfigHolder": "[]ListenerConfigHolder",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "[]StackTraceElement",
    "List_ClientBwListEntry": "NA",

    "EntryList_String_String": "[]*bufutil.Pair",
    "EntryList_String_byteArray": "[]*bufutil.Pair",
    "EntryList_Long_byteArray": "[]*bufutil.Pair",
    "EntryList_Integer_UUID": "[]*bufutil.Pair",
    "EntryList_UUID_Long": "[]*bufutil.Pair",
    "EntryList_String_EntryList_Integer_Long": "[[]map[string]string][]map[int]int64",
    "EntryList_Data_Data": "[]*bufutil.Pair",
    "EntryList_Member_List_ScheduledTaskHandler": "NA"
    
    '[]map[string][]map[int]int64'
}
