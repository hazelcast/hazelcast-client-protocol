cpp_ignore_service_list = {
    "Cache",
    "CardinalityEstimator",
    "Client.addPartitionLostListener",
    "Client.removePartitionLostListener", "Client.getDistributedObjects",
    "Client.addDistributedObjectListener", "Client.removeDistributedObjectListener",
    "Client.deployClasses", "Client.createProxies",
    "Client.addMigrationListener", "Client.removeMigrationListener", "Client.addCPGroupViewListener",
    "Client.tpcAuthentication",
    "CPMap",
    "ContinuousQuery",
    "CPSubsystem",
    "DurableExecutor",
    "DynamicConfig",
    "Experimental",
    "Jet",
    "List.iterator", "List.listIterator",
    "Map.addEntryListenerToKeyWithPredicate", "Map.addPartitionLostListener",
    "Map.removePartitionLostListener", "Map.loadAll", "Map.loadGivenKeys", "Map.fetchKeys",
    "Map.fetchEntries", "Map.aggregate", "Map.aggregateWithPredicate", "Map.project",
    "Map.projectWithPredicate", "Map.fetchNearCacheInvalidationMetadata", "Map.fetchWithQuery",
    "Map.eventJournalSubscribe", "Map.eventJournalRead", "Map.setTtl", "Map.putWithMaxIdle",
    "Map.putTransientWithMaxIdle", "Map.setWithMaxIdle", "Map.putIfAbsentWithMaxIdle",
    "Map.putAllWithMetadata",
    "MC",
    "MultiMap.delete", "MultiMap.putAll",
    "ReplicatedMap.putAllWithMetadata", "ReplicatedMap.fetchEntryViews",
    "ReplicatedMap.endEntryViewIteration",
    "ScheduledExecutor",
    "Sql.execute_reserved", "Sql.fetch_reserved", "Sql.mappingDdl",
    "Topic.publishAll",
    "TransactionalMap.getForUpdate", "TransactionalMap.containsValue",
    "TransactionalQueue.take", "TransactionalQueue.peek",
    "VectorCollection",
    "XATransaction",
}


def cpp_types_encode(key):
    try:
        cpp_type = _cpp_types_encode[key]
    except KeyError:
        try:
            cpp_type = _cpp_types_common[key]
        except KeyError:
            cpp_type = None
    if cpp_type is None or cpp_type == "NA":
        raise NotImplementedError(f"Missing type Mapping for [{key}]")
    return cpp_type


def cpp_types_decode(key):
    try:
        cpp_type = _cpp_types_decode[key]
    except KeyError:
        try:
            cpp_type = _cpp_types_common[key]
        except KeyError:
            cpp_type = None
    if cpp_type is None or cpp_type == "NA":
        raise NotImplementedError(f"Missing type Mapping for [{key}]")
    return cpp_type


def get_size(type):
    try:
        size = _type_size[type]
    except KeyError:
        raise NotImplementedError(f"Missing type size Mapping [{type}]")
    return size


def is_trivial(type):
    try:
        _trivial_types[type]
    except KeyError:
        return 0
    return 1


def cpp_param_name(name):
    """
    Converts camelCase protocol parameter name to snake_case
    """
    result = []

    for i, ch in enumerate(name):
        if ch.isupper():
            if i > 0 and name[i-1].islower():
                result.append('_')
            result.append(ch.lower())
        else:
            result.append(ch)

    return ''.join(result)


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
    "Data": "serialization::pimpl::data",
    "Schema": "serialization::pimpl::schema",

    "Address": "address",
    "Member": "member",
    "MemberVersion": "member::version",
    "Version": "internal::version",
    "ErrorHolder": "Hazelcast.Client.Protocol.ErrorHolder",
    "StackTraceElement": "protocol::codec::StackTraceElement",
    "SimpleEntryView": "map::data_entry_view",
    "RaftGroupId": "cp::raft_group_id",
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
    "List_RaftGroupInfo": "NA",

    "EntryList_Address_List_Integer": "std::vector<std::pair<address, std::vector<int32_t>>>",
    "MapIndexConfig": "NA",

    "SqlQueryId": "sql::impl::query_id",
    "SqlError": "NA",
    "SqlColumnMetadata": "NA",
    "CPMember": "NA",
    "MigrationState": "NA",
    "PartitioningAttributeConfig": "NA",

    "VectorIndexConfig": "NA",
    "VectorPair": "NA",
    "VectorDocument": "NA",
    "EntryList_Data_VectorDocument": "NA",
    "List_VectorPair": "NA",
    "VectorSearchOptions": "NA",
    "VectorSearchResult": "NA",

    "Schema": "serialization::pimpl::schema",
    "List_Schema": "std::vector<serialization::pimpl::schema>",
}

_cpp_types_encode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "ClientBwListEntry": "NA",
    "MemberInfo": "member",
    "MemberVersion": "member::version",
    "MCEvent": "NA",
    "AnchorDataListHolder": "codec::holder::anchor_data_list",
    "PagingPredicateHolder": "codec::holder::paging_predicate_holder",

    "List_Long": "std::vector<int64_t>",
    "List_Member": "std::vector<member>",
    "List_Integer": "std::vector<int32_t>",
    "List_UUID": "std::vector<boost::uuids::uuid>",
    "List_List_UUID": "std::vector<std::vector<boost::uuids::uuid>>",
    "List_String": "std::vector<std::string>",
    "List_Xid": "NA",
    "List_Data": "std::vector<serialization::pimpl::data>",
    "ListCN_Data": "std::vector<serialization::pimpl::data>",
    "List_MemberInfo": "std::vector<member>",
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
    "List_Schema": "std::vector<serialization::pimpl::schema>",

    "EntryList_String_String": "std::vector<std::pair<std::string, std::string>>",
    "EntryList_String_byteArray": "std::vector<std::pair<std::string, std::vector<byte>>>",
    "EntryList_Long_byteArray": "std::vector<std::pair<int64_t, std::vector<byte>>>",
    "EntryList_Integer_UUID": "std::vector<std::pair<int32_t, boost::uuids::uuid>>",
    "EntryList_Integer_Long": "std::vector<std::pair<int32_t, int64_t>>",
    "EntryList_Integer_Integer": "std::vector<std::pair<int32_t, int32_t>>",
    "EntryList_UUID_Long": "std::vector<std::pair<boost::uuids::uuid, int64_t>>",
    "EntryList_String_EntryList_Integer_Long": "std::vector<std::pair<std::string, std::vector<std::pair<int32_t, int64_t>>>>",
    "EntryList_UUID_List_Integer": "std::vector<std::pair<boost::uuids::uuid, std::vector<int>>>",
    "EntryList_Data_Data": "std::vector<std::pair<serialization::pimpl::data, serialization::pimpl::data>>",
    "EntryList_Data_List_Data": "std::vector<std::pair<serialization::pimpl::data, std::vector<serialization::pimpl::data>>>",

    "Set_UUID": "NA",
    "List_PartitioningAttributeConfig": "NA",
    "List_SimpleEntryView": "NA",
    "List_ReplicatedMapEntryViewHolder": "NA",
}

_cpp_types_decode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "ClientBwListEntry": "NA",
    "MemberInfo": "member",
    "MemberVersion": "member::version",
    "MCEvent": "NA",
    "AnchorDataListHolder": "codec::holder::anchor_data_list",
    "PagingPredicateHolder": "codec::holder::paging_predicate_holder",

    "List_Long": "std::vector<int64_t>",
    "List_Integer": "std::vector<int>",
    "List_UUID": "std::vector<boost::uuids::uuid>",
    "List_List_UUID": "std::vector<std::vector<boost::uuids::uuid>>",
    "List_Member": "std::vector<member>",
    "List_Xid": "NA",
    "List_String": "std::vector<std::string>",
    "List_Data": "std::vector<serialization::pimpl::data>",
    "ListCN_Data": "std::vector<serialization::pimpl::data>",
    "List_MemberInfo": "std::vector<member>",
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
    "EntryList_Data_Data": "std::vector<std::pair<serialization::pimpl::data, serialization::pimpl::data>>",

    "Set_UUID": "NA",
    "List_PartitioningAttributeConfig": "NA",
    "List_SimpleEntryView": "NA",
    "List_ReplicatedMapEntryViewHolder": "NA",
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
