go_reserved_keywords = {"break", "default", "func", "interface", "select", "case", "defer", "go", "map", "struct",
                        "chan", "else", "goto", "package", "switch", "const", "fallthrough", "if", "range", "type",
                        "continue", "for", "import", "return", "var"}

go_ignore_service_list = {"MC", "Sql", "ExecutorService", "TransactionalMap", "TransactionalMultiMap",
                          "TransactionalSet", "TransactionalList", "TransactionalQueue", "Cache", "XATransaction",
                          "Transaction", "ContinuousQuery", "DurableExecutor",
                          "CardinalityEstimator", "ScheduledExecutor", "DynamicConfig", "CPSubsystem"}


def go_types_encode(key):
    try:
        return _go_types_encode[key]
    except KeyError:
        return _go_types_common[key]


def go_types_decode(key):
    try:
        return _go_types_decode[key]
    except KeyError:
        return _go_types_common[key]


def go_get_import_path_holders(param_type):
    return import_paths.get(param_type, [])


class ImportPathHolder:
    def __init__(self, name, path, is_builtin_codec=False, is_custom_codec=False):
        self.name = name
        self.path = path
        self.is_builtin_codec = is_builtin_codec,
        self.is_custom_codec = is_custom_codec

    def get_import_statement(self):
        return "from hazelcast.%s import %s" % (self.path, self.name)


class PathHolders:
    DataCodec = ImportPathHolder("DataCodec", "protocol.builtin")
    ByteArrayCodec = ImportPathHolder("ByteArrayCodec", "protocol.builtin")
    LongArrayCodec = ImportPathHolder("LongArrayCodec", "protocol.builtin")
    Address = ImportPathHolder("Address", "core")
    AddressCodec = ImportPathHolder("AddressCodec", "protocol.codec.custom.address_codec")
    ErrorHolder = ImportPathHolder("ErrorHolder", "protocol")
    ErrorHolderCodec = ImportPathHolder("ErrorHolderCodec", "protocol.codec.custom.error_holder_codec")
    StackTraceElement = ImportPathHolder("StackTraceElement", "protocol")
    StackTraceElementCodec = ImportPathHolder("StackTraceElementCodec",
                                              "protocol.codec.custom.stack_trace_element_codec")
    SimpleEntryView = ImportPathHolder("SimpleEntryView", "core")
    SimpleEntryViewCodec = ImportPathHolder("SimpleEntryViewCodec", "protocol.codec.custom.simple_entry_view_codec")
    DistributedObjectInfo = ImportPathHolder("DistributedObjectInfo", "core")
    DistributedObjectInfoCodec = ImportPathHolder("DistributedObjectInfoCodec",
                                                  "protocol.codec.custom.distributed_object_info_codec")
    MemberInfo = ImportPathHolder("MemberInfo", "core")
    MemberInfoCodec = ImportPathHolder("MemberInfoCodec", "protocol.codec.custom.member_info_codec")
    MemberVersion = ImportPathHolder("MemberVersion", "core")
    MemberVersionCodec = ImportPathHolder("MemberVersionCodec", "protocol.codec.custom.member_version_codec")
    StringCodec = ImportPathHolder("StringCodec", "protocol.builtin", )
    ListLongCodec = ImportPathHolder("ListLongCodec", "protocol.builtin")
    ListIntegerCodec = ImportPathHolder("ListIntegerCodec", "protocol.builtin")
    ListUUIDCodec = ImportPathHolder("ListUUIDCodec", "protocol.builtin")
    ListDataCodec = ImportPathHolder("ListDataCodec", "protocol.builtin")
    ListMultiFrameCodec = ImportPathHolder("ListMultiFrameCodec", "protocol.builtin")
    EntryListCodec = ImportPathHolder("EntryListCodec", "protocol.builtin")
    EntryListLongByteArrayCodec = ImportPathHolder("EntryListLongByteArrayCodec", "protocol.builtin")
    EntryListIntegerUUIDCodec = ImportPathHolder("EntryListIntegerUUIDCodec", "protocol.builtin")
    EntryListIntegerLongCodec = ImportPathHolder("EntryListIntegerLongCodec", "protocol.builtin")
    EntryListIntegerIntegerCodec = ImportPathHolder("EntryListIntegerIntegerCodec", "protocol.builtin")
    EntryListUUIDLongCodec = ImportPathHolder("EntryListUUIDLongCodec", "protocol.builtin")
    EntryListUUIDUUIDCodec = ImportPathHolder("EntryListUUIDUUIDCodec", "protocol.builtin")
    EntryListUUIDListIntegerCodec = ImportPathHolder("EntryListUUIDListIntegerCodec", "protocol.builtin")
    MapCodec = ImportPathHolder("MapCodec", "protocol.builtin")
    CodecUtil = ImportPathHolder("CodecUtil", "protocol.builtin")
    IndexConfig = ImportPathHolder("IndexConfig", "config")
    IndexConfigCodec = ImportPathHolder("IndexConfigCodec", "protocol.codec.custom.index_config_codec")
    BitmapIndexOptions = ImportPathHolder("BitmapIndexOptions", "config")
    BitmapIndexOptionsCodec = ImportPathHolder("BitmapIndexOptionsCodec",
                                               "protocol.codec.custom.bitmap_index_options_codec")
    PagingPredicateHolder = ImportPathHolder("PagingPredicateHolder", "protocol")
    PagingPredicateHolderCodec = ImportPathHolder("PagingPredicateHolderCodec",
                                                  "protocol.codec.custom.paging_predicate_holder_codec")
    AnchorDataListHolder = ImportPathHolder("AnchorDataListHolder", "protocol")
    AnchorDataListHolderCodec = ImportPathHolder("AnchorDataListHolderCodec",
                                                 "protocol.codec.custom.anchor_data_list_holder_codec")
    EndpointQualifier = ImportPathHolder("EndpointQualifier", "protocol")
    EndpointQualifierCodec = ImportPathHolder("EndpointQualifierCodec",
                                              "protocol.codec.custom.endpoint_qualifier_codec")
    RaftGroupId = ImportPathHolder("RaftGroupId", "protocol")
    RaftGroupIdCodec = ImportPathHolder("RaftGroupIdCodec", "protocol.codec.custom.raft_group_id_codec")


import_paths = {
    "CodecUtil": PathHolders.CodecUtil,
    "longArray": [PathHolders.LongArrayCodec],
    "byteArray": [PathHolders.ByteArrayCodec],
    "String": [PathHolders.StringCodec],
    "Data": [PathHolders.DataCodec],
    "Address": [PathHolders.Address, PathHolders.AddressCodec],
    "ErrorHolder": [PathHolders.ErrorHolder, PathHolders.ErrorHolderCodec],
    "StackTraceElement": [PathHolders.StackTraceElement, PathHolders.StackTraceElementCodec],
    "SimpleEntryView": [PathHolders.SimpleEntryView, PathHolders.SimpleEntryViewCodec],
    "DistributedObjectInfo": [PathHolders.DistributedObjectInfo, PathHolders.DistributedObjectInfoCodec],
    "MemberInfo": [PathHolders.MemberInfo, PathHolders.MemberInfoCodec],
    "MemberVersion": [PathHolders.MemberVersion, PathHolders.MemberVersionCodec],
    "RaftGroupId": [PathHolders.RaftGroupId, PathHolders.RaftGroupIdCodec],
    "List_Long": [PathHolders.ListLongCodec],
    "List_Integer": [PathHolders.ListIntegerCodec],
    "List_UUID": [PathHolders.ListUUIDCodec],
    "List_String": [PathHolders.ListMultiFrameCodec, PathHolders.StringCodec],
    "List_Data": [PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    "ListCN_Data": [PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    "List_MemberInfo": [PathHolders.ListMultiFrameCodec, PathHolders.MemberInfoCodec],
    "List_DistributedObjectInfo": [PathHolders.ListMultiFrameCodec, PathHolders.DistributedObjectInfoCodec],
    "List_StackTraceElement": [PathHolders.ListMultiFrameCodec, PathHolders.StackTraceElementCodec],
    "EntryList_String_String": [PathHolders.EntryListCodec, PathHolders.StringCodec],
    "EntryList_String_byteArray": [PathHolders.EntryListCodec, PathHolders.StringCodec, PathHolders.ByteArrayCodec],
    "EntryList_Long_byteArray": [PathHolders.EntryListLongByteArrayCodec],
    "EntryList_Integer_UUID": [PathHolders.EntryListIntegerUUIDCodec],
    "EntryList_Integer_Long": [PathHolders.EntryListIntegerLongCodec],
    "EntryList_Integer_Integer": [PathHolders.EntryListIntegerIntegerCodec],
    "EntryList_UUID_Long": [PathHolders.EntryListUUIDLongCodec],
    "EntryList_String_EntryList_Integer_Long": [PathHolders.EntryListCodec, PathHolders.StringCodec,
                                                PathHolders.EntryListIntegerLongCodec],
    "EntryList_UUID_UUID": [PathHolders.EntryListUUIDUUIDCodec],
    "EntryList_UUID_List_Integer": [PathHolders.EntryListUUIDListIntegerCodec],
    "EntryList_Data_Data": [PathHolders.EntryListCodec, PathHolders.DataCodec],
    "EntryList_Data_List_Data": [PathHolders.EntryListCodec, PathHolders.DataCodec, PathHolders.ListDataCodec],
    "Map_String_String": [PathHolders.MapCodec, PathHolders.StringCodec],
    "IndexConfig": [PathHolders.IndexConfig, PathHolders.IndexConfigCodec],
    "ListIndexConfig": [PathHolders.IndexConfigCodec, PathHolders.ListMultiFrameCodec],
    "BitmapIndexOptions": [PathHolders.BitmapIndexOptions, PathHolders.BitmapIndexOptionsCodec],
    "AnchorDataListHolder": [PathHolders.AnchorDataListHolder, PathHolders.AnchorDataListHolderCodec],
    "PagingPredicateHolder": [PathHolders.PagingPredicateHolder, PathHolders.PagingPredicateHolderCodec],
    "EndpointQualifier": [PathHolders.EndpointQualifier, PathHolders.EndpointQualifierCodec],
    "Map_EndpointQualifier_Address": [PathHolders.MapCodec, PathHolders.EndpointQualifierCodec,
                                      PathHolders.AddressCodec]
}

_go_types_common = {
    "boolean": "bool",
    "int": "int32",
    "long": "int64",
    "byte": "byte",
    "Integer": "int32",
    "Long": "int64",
    "UUID": "core.UUID",

    "longArray": "[]int64",
    "byteArray": "[]byte",
    "String": "string",
    "Data": "serialization.Data",

    "Address": "core.Address",
    "ErrorHolder": "com.hazelcast.client.impl.protocol.exception.ErrorHolder",
    "StackTraceElement": "StackTraceElement",
    "SimpleEntryView": "Pair",
    "RaftGroupId": "NA",
    "WanReplicationRef": "NA",
    "HotRestartConfig": "NA",
    "EventJournalConfig": "NA",
    "MerkleTreeConfig": "NA",
    "TimedExpiryPolicyFactoryConfig": "NA",
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
    "MapStoreConfigHolder": "NA",
    "DistributedObjectInfo": "NA",
    "IndexConfig": "NA",
    "BitmapIndexOptions": "NA",
    "AttributeConfig": "NA",
    "ListenerConfigHolder": "NA",
    "CacheSimpleEntryListenerConfig": "NA",
    "ClientBwListEntry": "NA",
    "EndpointQualifier": "NA",

    "Map_String_String": "NA",
    "Map_EndpointQualifier_Address": "NA",

    "List_CPMember": "NA"
}

_go_types_encode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "ClientBwListEntry": "NA",
    "MemberInfo": "NA",
    "MemberVersion": "NA",
    "MCEvent": "NA",
    "AnchorDataListHolder": "NA",
    "PagingPredicateHolder": "NA",
    "SqlQueryId": "NA",
    "SqlError": "NA",
    "SqlColumnMetadata": "NA",
    "CPMember": "NA",
    "MigrationState": "NA",

    "List_Long": "java.util.Collection<java.lang.Long>",
    "List_Integer": "java.util.Collection<java.lang.Integer>",
    "List_UUID": "java.util.Collection<java.util.UUID>",
    "List_String": "[]string",
    "List_Xid": "java.util.Collection<javax.transaction.xa.Xid>",
    "List_Data": "[]serialization.Data",
    "List_List_Data": "java.util.Collection<java.util.Collection<com.hazelcast.internal.serialization.Data>>",
    "ListCN_Data": "java.util.Collection<com.hazelcast.internal.serialization.Data>",
    "List_ListCN_Data": "java.util.Collection<java.util.Collection<com.hazelcast.internal.serialization.Data>>",
    "List_MemberInfo": "java.util.Collection<com.hazelcast.internal.cluster.MemberInfo>",
    "List_ScheduledTaskHandler": "java.util.Collection<com.hazelcast.scheduledexecutor.ScheduledTaskHandler>",
    "List_CacheEventData": "java.util.Collection<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "java.util.Collection<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "java.util.Collection<com.hazelcast.client.impl.client.DistributedObjectInfo>",
    "List_QueryCacheEventData": "java.util.Collection<com.hazelcast.map.impl.querycache.event.QueryCacheEventData>",
    "List_IndexConfig": "java.util.Collection<com.hazelcast.config.IndexConfig>",
    "List_AttributeConfig": "java.util.Collection<com.hazelcast.config.AttributeConfig>",
    "List_ListenerConfigHolder": "java.util.Collection<com.hazelcast.client.impl.protocol.task.dynamicconfig.ListenerConfigHolder>",
    "List_CacheSimpleEntryListenerConfig": "java.util.Collection<com.hazelcast.config.CacheSimpleEntryListenerConfig>",
    "List_StackTraceElement": "java.util.Collection<java.lang.StackTraceElement>",
    "List_ClientBwListEntry": "java.util.Collection<com.hazelcast.internal.management.dto.ClientBwListEntryDTO>",
    "List_MCEvent": "java.util.Collection<com.hazelcast.internal.management.dto.MCEventDTO>",
    "List_SqlColumnMetadata": "java.util.List<com.hazelcast.sql.SqlColumnMetadata>",

    "EntryList_String_String": "java.util.Collection<java.util.Map.Entry<java.lang.String, java.lang.String>>",
    "EntryList_String_byteArray": "java.util.Collection<java.util.Map.Entry<java.lang.String, byte[]>>",
    "EntryList_Long_byteArray": "java.util.Collection<java.util.Map.Entry<java.lang.Long, byte[]>>",
    "EntryList_Integer_UUID": "java.util.Collection<java.util.Map.Entry<java.lang.Integer, java.util.UUID>>",
    "EntryList_Integer_Long": "java.util.Collection<java.util.Map.Entry<java.lang.Integer, java.lang.Long>>",
    "EntryList_Integer_Integer": "java.util.Collection<java.util.Map.Entry<java.lang.Integer, java.lang.Integer>>",
    "EntryList_UUID_Long": "map[core.UUID]int64",
    "EntryList_String_EntryList_Integer_Long": "java.util.Collection<java.util.Map.Entry<java.lang.String, java.util.List<java.util.Map.Entry<java.lang.Integer, java.lang.Long>>>>",
    "EntryList_UUID_UUID": "java.util.Collection<java.util.Map.Entry<java.util.UUID, java.util.UUID>>",
    "EntryList_UUID_List_Integer": "java.util.Collection<java.util.Map.Entry<java.util.UUID, java.util.List<java.lang.Integer>>>",
    "EntryList_Data_Data": "java.util.Collection<java.util.Map.Entry<com.hazelcast.internal.serialization.Data, com.hazelcast.internal.serialization.Data>>",
    "EntryList_Data_List_Data": "java.util.Collection<java.util.Map.Entry<com.hazelcast.internal.serialization.Data, java.util.Collection<com.hazelcast.internal.serialization.Data>>>",
}

_go_types_decode = {
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
    "CPMember": "com.hazelcast.cp.internal.CPMemberInfo",
    "MigrationState": "com.hazelcast.internal.partition.MigrationStateImpl",

    "List_Long": "java.util.List<java.lang.Long>",
    "List_Integer": "java.util.List<java.lang.Integer>",
    "List_UUID": "java.util.List<java.util.UUID>",
    "List_Xid": "java.util.List<javax.transaction.xa.Xid>",
    "List_String": "[]string",
    "List_Data": "[]serialization.Data",
    "List_List_Data": "java.util.List<java.util.List<com.hazelcast.internal.serialization.Data>>",
    "ListCN_Data": "java.util.List<com.hazelcast.internal.serialization.Data>",
    "List_ListCN_Data": "java.util.List<java.util.List<com.hazelcast.internal.serialization.Data>>",
    "List_MemberInfo": "java.util.List<com.hazelcast.internal.cluster.MemberInfo>",
    "List_CacheEventData": "java.util.List<com.hazelcast.cache.impl.CacheEventData>",
    "List_QueryCacheConfigHolder": "java.util.List<com.hazelcast.client.impl.protocol.task.dynamicconfig.QueryCacheConfigHolder>",
    "List_DistributedObjectInfo": "[]core.DistributedObjectInfo",
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
}
