import keyword

def py_types_encode(key):
    try:
        py_type =_py_types_encode[key]
    except KeyError:
        py_type =_py_types_common[key]
    if py_type == "NA":
        raise NotImplementedError("Missing type Mapping")
    return py_type


py_ignore_service_list = [11, 19, 20, 22, 24, 25, 26, 27, 30, 31, 32]


def py_types_decode(key):
    try:
        py_type = _py_types_decode[key]
    except KeyError:
        py_type = _py_types_common[key]
    if py_type == "NA":
        raise NotImplementedError("Missing type Mapping")
    return py_type


_py_types_common = {
    "boolean": "boolean",
    "int": "int",
    "long": "long",
    "byte": "byte",
    "Integer": "int",
    "Long": "long",
    "UUID": "java.util.UUID",
    "enum": "int",

    "longArray": "long[]",
    "byteArray": "bytearray",
    "String": "str",
    "Data": "com.hazelcast.internal.serialization.Data",

    "Address": "hazelcast.core.Address",
    "ErrorHolder": "hazelcast.protocol.exception.error_holder.ErrorHolder",
    "StackTraceElement": "hazelcast.protocol.stack_trace_element.StackTraceElement",
    "SimpleEntryView": "hazelcast.core.EntryView",
    "RaftGroupId": "NA",
    "WanReplicationRef": "NA",
    "HotRestartConfig": "NA",
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

    "MergePolicyConfig": "NA",
    "CacheConfigHolder": "NA",
    "CacheEventData": "NA",
    "QueryCacheConfigHolder": "NA",
    "DistributedObjectInfo": "hazelcast.core.DistributedObjectInfo",
    "IndexConfig": "hazelcast.config.IndexConfig",
    "BitmapIndexOptions": "hazelcast.config.BitmapIndexOptions",
    "AttributeConfig": "NA",
    "ListenerConfigHolder": "NA",
    "CacheSimpleEntryListenerConfig": "NA",
    "ClientBwListEntry": "NA",
    "EndpointQualifier": "NA",

    "Map_String_String": ""
}

_py_types_encode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "Member": "hazelcast.core.Member",
    "ClientBwListEntry": "NA",
    "MemberInfo": "",
    "MemberVersion": "NA",
    "MCEvent": "NA",
    "AnchorDataListHolder": "NA",
    "PagingPredicateHolder": "NA",

    "List_Long": "",
    "List_Integer": "",
    "List_UUID": "",
    "List_String": "",
    "List_Xid": "NA",
    "List_Data": "",
    "ListCN_Data": "",
    "List_MemberInfo": "",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "",
    "List_QueryCacheEventData": "",
    "List_IndexConfig": "",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",

    "EntryList_String_String": "",
    "EntryList_String_byteArray": "",
    "EntryList_Long_byteArray": "",
    "EntryList_Integer_UUID": "",
    "EntryList_UUID_Long": "",
    "EntryList_String_EntryList_Integer_Long": "",
    "EntryList_Address_List_Integer": "",
    "EntryList_UUID_Address": "",
    "EntryList_UUID_List_Integer": "",
    "EntryList_Data_Data": "",
    "EntryList_Member_List_ScheduledTaskHandler": ""
}

_py_types_decode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "Member": "",
    "ClientBwListEntry": "NA",
    "MemberInfo": "hazelcast.core.MemberInfo",
    "MemberVersion": "hazelcast.core.MemberVersion",
    "MCEvent": "NA",
    "AnchorDataListHolder": "NA",
    "PagingPredicateHolder": "NA",

    "List_Long": "",
    "List_Integer": "",
    "List_UUID": "",
    "List_Xid": "",
    "List_String": "",
    "List_Data": "",
    "ListCN_Data": "",
    "List_MemberInfo": "",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "hazelcast.client.impl.client.DistributedObjectInfo",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "hazelcast.config.IndexConfig",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "hazelcast.util.StackTraceElement",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "",

    "EntryList_String_String": "hazelcast.util.List",
    "EntryList_String_byteArray": "",
    "EntryList_Long_byteArray": "",
    "EntryList_Integer_UUID": "",
    "EntryList_UUID_Long": "",
    "EntryList_String_EntryList_Integer_Long": "",
    "EntryList_Address_List_Integer": "",
    "EntryList_UUID_Address": "",
    "EntryList_Data_Data": "",
    "EntryList_UUID_List_Integer": "",
    "EntryList_Member_List_ScheduledTaskHandler": ""
}


def py_escape_keyword(value):
    if value in keyword.kwlist:
        return "{}_".format(value)
    else:
        return value
