cpp_ignore_service_list = {"Cache", "XATransaction", "ContinuousQuery", "DurableExecutor", "CardinalityEstimator",
                           "ScheduledExecutor", "DynamicConfig", "MC", "Sql", "CPSubsystem"}


def cpp_types_encode(key):
    try:
        cpp_type = _cpp_types_encode[key]
    except KeyError:
        cpp_type = _cpp_types_common[key]
    if cpp_type == "NA":
        raise NotImplementedError("Missing type Mapping")
    return cpp_type


def cpp_types_decode(key):
    try:
        cpp_type = _cpp_types_decode[key]
    except KeyError:
        cpp_type = _cpp_types_common[key]
    if cpp_type == "NA":
        raise NotImplementedError("Missing type Mapping")
    return cpp_type


def get_size(type):
    try:
        size = _type_size[type]
    except KeyError:
        raise NotImplementedError("Missing type size mapping")
    return size


def is_trivial(type):
    try:
        _trivial_types[type]
    except KeyError:
        return 0
    return 1


"""
def cpp_escape_keyword(value):
    if value not in cpp_reserved_words:
        return value
    return "@" + value
 """

_type_size = {
    "boolean": "ClientMessage::UINT8_SIZE",
    "int": "ClientMessage::INT32_SIZE",
    "long": "ClientMessage::INT64_SIZE",
    "byte": "ClientMessage::UINT8_SIZE",
    "Integer": "ClientMessage::INT32_SIZE",
    "Long": "ClientMessage::UINT64_SIZE",
    "UUID": "ClientMessage::UUID_SIZE",
}

_cpp_types_common = {
    "boolean": "bool",
    "int": "int32_t",
    "long": "int64_t",
    "byte": "byte",
    "Integer": "int32_t",
    "Long": "int64_t",
    "UUID": "boost::uuids::uuid",

    "longArray": "std::vector<int64_t>",
    "byteArray": "std::vector<byte>",
    "String": "std::string",
    "Data": "Data",

    "Address": "Address",
    "Member": "Member",
    "ErrorHolder": "Hazelcast.Client.Protocol.ErrorHolder",
    "StackTraceElement": "protocol::codec::StackTraceElement",
    "SimpleEntryView": "map::DataEntryView",
    "RaftGroupId": "raft_group_id",
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
    "DistributedObjectInfo": "NA",
    "IndexConfig": "config::index_config",
    "BitmapIndexOptions": "NA",
    "AttributeConfig": "NA",
    "ListenerConfigHolder": "NA",
    "CacheSimpleEntryListenerConfig": "NA",
    "ClientBwListEntry": "NA",
    "EndpointQualifier": "NA",

    "Map_String_String": "std::unordered_map<std::string, std::string>",
    "Map_EndpointQualifier_Address": "NA",

    "EntryList_Address_List_Integer": "std::vector<std::pair<Address, std::vector<int32_t>>>",
    "MapIndexConfig": "NA",

    "SqlQueryId": "NA",
    "SqlError": "NA",
    "SqlColumnMetadata": "NA",
    "CPMember": "NA",
}

_cpp_types_encode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "ClientBwListEntry": "NA",
    "MemberInfo": "Member",
    "MemberVersion": "Hazelcast.Core.MemberVersion",
    "MCEvent": "NA",
    "AnchorDataListHolder": "codec::holder::anchor_data_list",
    "PagingPredicateHolder": "codec::holder::paging_predicate_holder",

    "List_Long": "std::vector<int64_t>",
    "List_Member": "std::vector<Member>",
    "List_Integer": "std::vector<int32_t>",
    "List_UUID": "std::vector<boost::uuids::uuid>",
    "List_String": "std::vector<std::string>",
    "List_Xid": "NA",
    "List_Data": "std::vector<Data>",
    "ListCN_Data": "std::vector<Data>",
    "List_MemberInfo": "std::vector<Member>",
    "List_ScheduledTaskHandler": "NA",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "NA",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "NA",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "std::vector<protocol::codec::StackTraceElement>",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",

    "EntryList_String_String": "std::vector<std::pair<std::string, std::string>>",
    "EntryList_String_byteArray": "std::vector<std::pair<std::string, std::vector<byte>>>",
    "EntryList_Long_byteArray": "std::vector<std::pair<int64_t, std::vector<byte>>>",
    "EntryList_Integer_UUID": "std::vector<std::pair<int32_t, boost::uuids::uuid>>",
    "EntryList_Integer_Long": "std::vector<std::pair<int32_t, int64_t>>",
    "EntryList_Integer_Integer": "std::vector<std::pair<int32_t, int32_t>>",
    "EntryList_UUID_Long": "std::vector<std::pair<boost::uuids::uuid, int64_t>>",
    "EntryList_String_EntryList_Integer_Long": "std::vector<std::pair<std::string, std::vector<std::pair<int32_t, int64_t>>>>",
    "EntryList_UUID_List_Integer": "std::vector<std::pair<boost::uuids::uuid, std::vector<int>>>",
    "EntryList_Data_Data": "std::vector<std::pair<Data, Data>>",
    "EntryList_Data_List_Data": "std::vector<std::pair<Data, std::vector<Data>>>",
}

_cpp_types_decode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "ClientBwListEntry": "NA",
    "MemberInfo": "Member",
    "MemberVersion": "Hazelcast.Core.MemberVersion",
    "MCEvent": "NA",
    "AnchorDataListHolder": "codec::holder::anchor_data_list",
    "PagingPredicateHolder": "codec::holder::paging_predicate_holder",

    "List_Long": "std::vector<int64_t>",
    "List_Integer": "std::vector<int>",
    "List_UUID": "std::vector<boost::uuids::uuid>",
    "List_Member": "std::vector<Member>",
    "List_Xid": "NA",
    "List_String": "std::vector<std::string>",
    "List_Data": "std::vector<Data>",
    "ListCN_Data": "std::vector<Data>",
    "List_MemberInfo": "std::vector<Member>",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "NA",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "NA",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "std::vector<protocol::codec::StackTraceElement>",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",
    "List_ScheduledTaskHandler": "NA",

    "EntryList_String_String": "std::vector<std::pair<std::string, std::string>>",
    "EntryList_String_byteArray": "std::vector<std::pair<std::string, std::vector<byte>>>",
    "EntryList_Long_byteArray": "std::vector<std::pair<int64_t, std::vector<byte>>>",
    "EntryList_Integer_UUID": "std::vector<std::pair<int32_t, boost::uuids::uuid>>",
    "EntryList_Integer_Long": "std::vector<std::pair<int32_t, int64_t>>",
    "EntryList_Integer_Integer": "std::vector<std::pair<int32_t, int32_t>>",
    "EntryList_UUID_Long": "std::vector<std::pair<boost::uuids::uuid, int64_t>>",
    "EntryList_String_EntryList_Integer_Long": "std::vector<std::pair<std::string, std::vector<std::pair<int32_t, int64_t>>>>",
    "EntryList_UUID_List_Integer": "std::vector<std::pair<boost::uuids::uuid, std::vector<int>>>",
    "EntryList_Data_Data": "std::vector<std::pair<Data, Data>>"
}

_trivial_types = {
    "boolean": "bool",
    "int": "int32_t",
    "long": "int64_t",
    "byte": "byte",
    "Integer": "int32_t",
    "Long": "int64_t",
    "UUID": "boost::uuids::uuid",
}
