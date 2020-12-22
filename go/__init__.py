go_reserved_keywords = {"break", "default", "func", "interface", "select", "case", "defer", "go", "map", "struct",
                        "chan", "else", "goto", "package", "switch", "const", "fallthrough", "if", "range", "type",
                        "continue", "for", "import", "return", "var"}

go_ignore_service_list = {"MC", "Sql", "ExecutorService", "TransactionalMap", "TransactionalMultiMap",
                          "TransactionalSet", "TransactionalList", "TransactionalQueue", "Cache", "XATransaction",
                          "Transaction", "ContinuousQuery", "DurableExecutor",
                          "CardinalityEstimator", "ScheduledExecutor", "DynamicConfig", "CPSubsystem"}


def go_types_encode(key):
    try:
        go_type = _go_types_encode[key]
    except KeyError:
        go_type = _go_types_common[key]
    if go_type == "NA":
        raise NotImplementedError("Missing type mapping for '" + key + "'")
    return go_type


def go_types_decode(key):
    try:
        go_type = _go_types_decode[key]
    except KeyError:
        go_type = _go_types_common[key]
    if go_type == "NA":
        raise NotImplementedError("Missing type for '" + key + "'")
    return go_type


def go_get_import_path_holders(param_type):
    return import_paths.get(param_type, [])


class ImportPathHolder:
    def __init__(self, name, path, is_builtin_codec=False, is_custom_codec=False):
        self.name = name
        self.path = path
        self.is_builtin_codec = is_builtin_codec
        self.is_custom_codec = is_custom_codec

    def get_import_statement(self):
        if self.is_builtin_codec == True or self.is_custom_codec == True:
            return "\"github.com/hazelcast/hazelcast-go-client/hazelcast%s\"" % self.path
        return "\"github.com/hazelcast/hazelcast-go-client/hazelcast%s\"" % self.path


class PathHolders:
    UUID = ImportPathHolder('UUID', '/core')
    Data = ImportPathHolder('Data', '/protocol/serialization', is_builtin_codec=False, is_custom_codec=False)
    DataCodec = ImportPathHolder("DataCodec", "/protocol/codec/internal", is_builtin_codec=True)
    ByteArrayCodec = ImportPathHolder("ByteArrayCodec", "/protocol/codec/internal", is_builtin_codec=True)
    LongArrayCodec = ImportPathHolder("LongArrayCodec", "/protocol/codec/internal", is_builtin_codec=True)
    Address = ImportPathHolder("Address", "/core")
    AddressCodec = ImportPathHolder("AddressCodec", "/protocol/codec/internal", is_custom_codec=True)
    ErrorHolder = ImportPathHolder("ErrorHolder", "/internal/protocol")
    ErrorHolderCodec = ImportPathHolder("ErrorHolderCodec", "/protocol/codec/internal", is_custom_codec=True)
    StackTraceElement = ImportPathHolder("StackTraceElement", "/internal/protocol")
    StackTraceElementCodec = ImportPathHolder("StackTraceElementCodec",
                                              "/protocol/codec/internal", is_custom_codec=True)
    SimpleEntryView = ImportPathHolder("SimpleEntryView", "/core")
    SimpleEntryViewCodec = ImportPathHolder("SimpleEntryViewCodec", "/protocol/codec/internal",
                                            is_custom_codec=True)
    DistributedObjectInfo = ImportPathHolder("DistributedObjectInfo", "/core")
    DistributedObjectInfoCodec = ImportPathHolder("DistributedObjectInfoCodec", "/protocol/codec/internal",
                                                  is_custom_codec=True)
    MemberInfo = ImportPathHolder("MemberInfo", "/core")
    MemberInfoCodec = ImportPathHolder("MemberInfoCodec", "/protocol/codec/internal", is_custom_codec=True)
    MemberVersion = ImportPathHolder("MemberVersion", "/core")
    MemberVersionCodec = ImportPathHolder("MemberVersionCodec", "/protocol/codec/internal", is_custom_codec=True)
    StringCodec = ImportPathHolder("StringCodec", "/protocol/codec/internal", is_builtin_codec=True)
    ListLongCodec = ImportPathHolder("ListLongCodec", "/protocol/codec/internal", is_builtin_codec=True)
    ListIntegerCodec = ImportPathHolder("ListIntegerCodec", "/protocol/codec/internal", is_builtin_codec=True)
    ListUUIDCodec = ImportPathHolder("ListUUIDCodec", "/protocol/codec/internal", is_builtin_codec=True)
    ListDataCodec = ImportPathHolder("ListDataCodec", "/protocol/codec/internal", is_builtin_codec=True)
    ListMultiFrameCodec = ImportPathHolder("ListMultiFrameCodec", "/protocol/codec/internal",
                                           is_builtin_codec=True)
    EntryListCodec = ImportPathHolder("EntryListCodec", "/protocol/codec/internal", is_builtin_codec=True)
    EntryListLongByteArrayCodec = ImportPathHolder("EntryListLongByteArrayCodec", "/protocol/codec/internal",
                                                   is_builtin_codec=True)
    EntryListIntegerUUIDCodec = ImportPathHolder("EntryListIntegerUUIDCodec", "/protocol/codec/internal",
                                                 is_builtin_codec=True)
    EntryListIntegerLongCodec = ImportPathHolder("EntryListIntegerLongCodec", "/protocol/codec/internal",
                                                 is_builtin_codec=True)
    EntryListIntegerIntegerCodec = ImportPathHolder("EntryListIntegerIntegerCodec", "/protocol/codec/internal",
                                                    is_builtin_codec=True)
    EntryListUUIDLongCodec = ImportPathHolder("EntryListUUIDLongCodec", "/protocol/codec/internal",
                                              is_builtin_codec=True)
    EntryListUUIDUUIDCodec = ImportPathHolder("EntryListUUIDUUIDCodec", "/protocol/codec/internal",
                                              is_builtin_codec=True)
    EntryListUUIDListIntegerCodec = ImportPathHolder("EntryListUUIDListIntegerCodec",
                                                     "/protocol/codec/internal",
                                                     is_builtin_codec=True)
    MapCodec = ImportPathHolder("MapCodec", "/protocol/codec/internal",
                                is_builtin_codec=True)
    CodecUtilCodec = ImportPathHolder("CodecUtil", "/protocol/codec/internal",
                                      is_builtin_codec=True)
    IndexConfig = ImportPathHolder("IndexConfig", "/core")
    IndexConfigCodec = ImportPathHolder("IndexConfigCodec", "/protocol/codec/internal", is_custom_codec=True)
    BitmapIndexOptions = ImportPathHolder("BitmapIndexOptions", "/core")
    BitmapIndexOptionsCodec = ImportPathHolder("BitmapIndexOptionsCodec", "/protocol/codec/internal",
                                               is_custom_codec=True)
    PagingPredicateHolder = ImportPathHolder("PagingPredicateHolder", "/core")
    PagingPredicateHolderCodec = ImportPathHolder("PagingPredicateHolderCodec", "/protocol/codec/internal",
                                                  is_custom_codec=True)
    AnchorDataListHolder = ImportPathHolder("AnchorDataListHolder", "/core")
    AnchorDataListHolderCodec = ImportPathHolder("AnchorDataListHolderCodec", "/protocol/codec/internal",
                                                 is_custom_codec=True)

    EndpointQualifier = ImportPathHolder("EndpointQualifier", "/core", is_builtin_codec=False, is_custom_codec=False)
    EndpointQualifierCodec = ImportPathHolder("EndpointQualifierCodec", "/protocol/codec/internal",
                                              is_custom_codec=True)

    RaftGroupId = ImportPathHolder("RaftGroupId", "/core", is_builtin_codec=False, is_custom_codec=False)
    RaftGroupIdCodec = ImportPathHolder("RaftGroupIdCodec", "/protocol/codec/internal",
                                        is_custom_codec=True)


import_paths = {
    "UUID": [PathHolders.UUID],
    "CodecUtil": PathHolders.CodecUtilCodec,
    "longArray": [PathHolders.LongArrayCodec],
    "byteArray": [PathHolders.ByteArrayCodec],
    "String": [PathHolders.StringCodec],
    "Data": [PathHolders.Data, PathHolders.DataCodec],
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
    "List_Data": [PathHolders.Data, PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    "ListCN_Data": [PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    'List_MemberInfo': [PathHolders.MemberInfo, PathHolders.ListMultiFrameCodec, PathHolders.MemberInfoCodec],
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
    "Map_EndpointQualifier_Address": [PathHolders.MapCodec, PathHolders.EndpointQualifierCodec, PathHolders.AddressCodec]
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
    "Pair": "serialization.Pair",

    "Address": "core.Address",
    "ErrorHolder": "core.ErrorHolder",
    "StackTraceElement": "core.StackTraceElement",
    "MemberInfo": "core.MemberInfo",
    "SimpleEntryView": "protocol.Pair",
    "RaftGroupId": "core.RaftGroupId",
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
    "DistributedObjectInfo": "core.DistributedObjectInfo",
    "IndexConfig": "core.IndexConfig",
    "BitmapIndexOptions": "core.BitmapIndexOptions",
    "AttributeConfig": "NA",
    "ListenerConfigHolder": "NA",
    "CacheSimpleEntryListenerConfig": "NA",
    "ClientBwListEntry": "NA",
    "EndpointQualifier": "core.EndpointQualifier",

    "Map_String_String": "map[string]string",
    "Map_EndpointQualifier_Address": "map[core.EndpointQualifier]core.Address",

    "List_CPMember": "NA"
}

_go_types_encode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "ClientBwListEntry": "NA",
    "MemberInfo": "core.MemberInfo",
    "MemberVersion": "core.MemberVersion",
    "MCEvent": "NA",
    "AnchorDataListHolder": "core.AnchorDataListHolder",
    "PagingPredicateHolder": "core.PagingPredicateHolder",
    "SqlQueryId": "NA",
    "SqlError": "NA",
    "SqlColumnMetadata": "NA",
    "CPMember": "NA",
    "MigrationState": "NA",

    "List_Long": "[]int64",
    "List_Integer": "[]int32",
    "List_UUID": "[]core.UUID",
    "List_String": "[]string",
    "List_Xid": "NA",
    "List_Data": "[]serialization.Data",
    "List_List_Data": "[]serialization.Data",
    "ListCN_Data": "[]serialization.Data",
    "List_ListCN_Data": "NA",
    "List_MemberInfo": "[]core.MemberInfo",
    "List_ScheduledTaskHandler": "NA",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "[]DistributedObjectInfo",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "[]IndexConfig",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "[]StackTraceElement",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",
    "List_SqlColumnMetadata": "NA",

    "EntryList_String_String": "[]protocol.Pair",
    "EntryList_String_byteArray": "[]protocol.Pair",
    "EntryList_Long_byteArray": "[]protocol.Pair",
    "EntryList_Integer_UUID": "[]protocol.Pair",
    "EntryList_Integer_Long": "[]protocol.Pair",
    "EntryList_Integer_Integer": "[]protocol.Pair",
    "EntryList_UUID_Long": "[]protocol.Pair",
    "EntryList_String_EntryList_Integer_Long": "[]protocol.Pair",
    "EntryList_UUID_UUID": "[]protocol.Pair",
    "EntryList_UUID_List_Integer": "[]protocol.Pair",
    "EntryList_Data_Data": "[]protocol.Pair",
    "EntryList_Data_List_Data": "[]protocol.Pair",
}

_go_types_decode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "ClientBwListEntry": "NA",
    "MemberInfo": "core.MemberInfo",
    "MemberVersion": "core.MemberVersion",
    "MCEvent": "NA",
    "AnchorDataListHolder": "core.AnchorDataListHolder",
    "PagingPredicateHolder": "core.PagingPredicateHolder",
    "SqlQueryId": "NA",
    "SqlError": "NA",
    "SqlColumnMetadata": "NA",
    "CPMember": "NA",
    "MigrationState": "NA",

    "List_Long": "[]int64",
    "List_Integer": "[]int32",
    "List_UUID": "[]core.UUID",
    "List_Xid": "NA",
    "List_String": "[]string",
    "List_Data": "[]serialization.Data",
    "List_List_Data": "[]serialization.Data",
    "ListCN_Data": "[]serialization.Data",
    "List_ListCN_Data": "NA",
    "List_MemberInfo": "[]core.MemberInfo",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "[]core.DistributedObjectInfo",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "[]IndexConfig",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "[]StackTraceElement",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",
    "List_ScheduledTaskHandler": "NA",
    "List_SqlColumnMetadata": "NA",
    "List_CPMember": "NA",

    "EntryList_String_String": "[]protocol.Pair",
    "EntryList_String_byteArray": "[]protocol.Pair",
    "EntryList_Long_byteArray": "[]protocol.Pair",
    "EntryList_Integer_UUID": "[]protocol.Pair",
    "EntryList_Integer_Long": "[]protocol.Pair",
    "EntryList_Integer_Integer": "[]protocol.Pair",
    "EntryList_UUID_Long": "[]protocol.Pair",
    "EntryList_String_EntryList_Integer_Long": "[]protocol.Pair",
    "EntryList_UUID_UUID": "[]protocol.Pair",
    "EntryList_UUID_List_Integer": "[]protocol.Pair",
    "EntryList_Data_Data": "[]protocol.Pair",
    "EntryList_Data_List_Data": "[]protocol.Pair",
}
