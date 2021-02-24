CLIENT_VERSION = 4

go_reserved_keywords = {"break", "default", "func", "interface", "select", "case", "defer", "go", "map", "struct",
                        "chan", "else", "goto", "package", "switch", "const", "fallthrough", "if", "range", "type",
                        "continue", "for", "import", "return", "var"}

go_ignore_service_list = {"MC", "Sql", "ExecutorService", "TransactionalMap", "TransactionalMultiMap",
                          "TransactionalSet", "TransactionalList", "TransactionalQueue", "Cache", "XATransaction",
                          "Transaction", "ContinuousQuery", "DurableExecutor",
                          "CardinalityEstimator", "ScheduledExecutor", "DynamicConfig", "CPSubsystem"}


def go_escape_keyword(value):
    if value not in go_reserved_keywords:
        return value
    return "_" + value


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


def go_get_import_statements(*args):
    import_statements = set()
    for arg in args:
        params = [arg] if isinstance(arg, str) else arg
        for param in params:
            type = param["type"] if isinstance(param, dict) else param
            for path_holder in import_paths.get(type, []):
                if path_holder.path:
                    import_statements.add(path_holder.import_statement)
    return import_statements


class ImportPathHolder:
    def __init__(self, name, path, is_builtin_codec=False, is_custom_codec=False):
        self.name = name
        self.path = path
        self.is_builtin_codec = is_builtin_codec
        self.is_custom_codec = is_custom_codec

    @property
    def import_statement(self):
        if not self.path:
            return ""
        return '''"github.com/hazelcast/hazelcast-go-client/v%s/internal%s"''' % (CLIENT_VERSION, self.path)


class PathHolders:
    Address = ImportPathHolder("Address", "/core")
    AddressCodec = ImportPathHolder("AddressCodec", "", is_custom_codec=True)
    AnchorDataListHolder = ImportPathHolder("AnchorDataListHolder", "")
    AnchorDataListHolderCodec = ImportPathHolder("AnchorDataListHolderCodec", "", is_custom_codec=True)
    BitmapIndexOptions = ImportPathHolder("BitmapIndexOptions", "/config")
    BitmapIndexOptionsCodec = ImportPathHolder("BitmapIndexOptionsCodec", "", is_custom_codec=True)
    ByteArrayCodec = ImportPathHolder("ByteArrayCodec", "", is_builtin_codec=True)
    CodecUtilCodec = ImportPathHolder("CodecUtil", "", is_builtin_codec=True)
    Data = ImportPathHolder('Data', '/serialization')
    DataCodec = ImportPathHolder("DataCodec", "", is_builtin_codec=True)
    DistributedObjectInfo = ImportPathHolder("DistributedObjectInfo", "/core")
    DistributedObjectInfoCodec = ImportPathHolder("DistributedObjectInfoCodec", "", is_custom_codec=True)
    # EndpointQualifier = ImportPathHolder("EndpointQualifier", "/protocol")
    EndpointQualifierCodec = ImportPathHolder("EndpointQualifierCodec", "", is_custom_codec=True)
    EntryListCodec = ImportPathHolder("EntryListCodec", "", is_builtin_codec=True)
    EntryListIntegerIntegerCodec = ImportPathHolder("EntryListIntegerIntegerCodec", "", is_builtin_codec=True)
    EntryListIntegerLongCodec = ImportPathHolder("EntryListIntegerLongCodec", "", is_builtin_codec=True)
    EntryListIntegerUUIDCodec = ImportPathHolder("EntryListIntegerUUIDCodec", "", is_builtin_codec=True)
    EntryListLongByteArrayCodec = ImportPathHolder("EntryListLongByteArrayCodec", "", is_builtin_codec=True)
    EntryListUUIDListIntegerCodec = ImportPathHolder("EntryListUUIDListIntegerCodec", "", is_builtin_codec=True)
    EntryListUUIDLongCodec = ImportPathHolder("EntryListUUIDLongCodec", "", is_builtin_codec=True)
    EntryListUUIDUUIDCodec = ImportPathHolder("EntryListUUIDUUIDCodec", "", is_builtin_codec=True)
    ErrorHolder = ImportPathHolder("ErrorHolder", "")
    ErrorHolderCodec = ImportPathHolder("ErrorHolderCodec", "", is_custom_codec=True)
    IndexConfig = ImportPathHolder("IndexConfig", "/core")
    IndexConfigCodec = ImportPathHolder("IndexConfigCodec", "", is_custom_codec=True)
    ListDataCodec = ImportPathHolder("ListDataCodec", "", is_builtin_codec=True)
    ListIntegerCodec = ImportPathHolder("ListIntegerCodec", "", is_builtin_codec=True)
    ListLongCodec = ImportPathHolder("ListLongCodec", "", is_builtin_codec=True)
    ListMultiFrameCodec = ImportPathHolder("ListMultiFrameCodec", "", is_builtin_codec=True)
    ListUUIDCodec = ImportPathHolder("ListUUIDCodec", "", is_builtin_codec=True)
    LongArrayCodec = ImportPathHolder("LongArrayCodec", "", is_builtin_codec=True)
    MapCodec = ImportPathHolder("MapCodec", "", is_builtin_codec=True)
    MemberInfo = ImportPathHolder("MemberInfo", "/core")
    MemberInfoCodec = ImportPathHolder("MemberInfoCodec", "", is_custom_codec=True)
    MemberVersion = ImportPathHolder("MemberVersion", "/core")
    MemberVersionCodec = ImportPathHolder("MemberVersionCodec", "", is_custom_codec=True)
    PagingPredicateHolder = ImportPathHolder("PagingPredicateHolder", "/core")
    PagingPredicateHolderCodec = ImportPathHolder("PagingPredicateHolderCodec", "", is_custom_codec=True)
    RaftGroupId = ImportPathHolder("RaftGroupId", "")
    RaftGroupIdCodec = ImportPathHolder("RaftGroupIdCodec", "", is_custom_codec=True)
    SimpleEntryView = ImportPathHolder("SimpleEntryView", "/core")
    SimpleEntryViewCodec = ImportPathHolder("SimpleEntryViewCodec", "", is_custom_codec=True)
    StackTraceElement = ImportPathHolder("StackTraceElement", "")
    StackTraceElementCodec = ImportPathHolder("StackTraceElementCodec", "", is_custom_codec=True)
    StringCodec = ImportPathHolder("StringCodec", "", is_builtin_codec=True)
    UUID = ImportPathHolder('UUID', '/core')


import_paths = {
    "Address": [PathHolders.Address, PathHolders.AddressCodec],
    "AnchorDataListHolder": [PathHolders.AnchorDataListHolder, PathHolders.AnchorDataListHolderCodec],
    "BitmapIndexOptions": [PathHolders.BitmapIndexOptions, PathHolders.BitmapIndexOptionsCodec],
    "CodecUtil": PathHolders.CodecUtilCodec,
    "Data": [PathHolders.Data, PathHolders.DataCodec],
    "DistributedObjectInfo": [PathHolders.DistributedObjectInfo, PathHolders.DistributedObjectInfoCodec],
    "EntryList_Data_Data": [PathHolders.EntryListCodec, PathHolders.DataCodec],
    "EntryList_Data_List_Data": [PathHolders.EntryListCodec, PathHolders.DataCodec, PathHolders.ListDataCodec],
    "EntryList_Integer_Integer": [PathHolders.EntryListIntegerIntegerCodec],
    "EntryList_Integer_Long": [PathHolders.EntryListIntegerLongCodec],
    "EntryList_Integer_UUID": [PathHolders.EntryListIntegerUUIDCodec],
    "EntryList_Long_byteArray": [PathHolders.EntryListLongByteArrayCodec],
    "EntryList_String_EntryList_Integer_Long": [PathHolders.EntryListCodec, PathHolders.StringCodec, PathHolders.EntryListIntegerLongCodec],
    "EntryList_String_String": [PathHolders.EntryListCodec, PathHolders.StringCodec],
    "EntryList_String_byteArray": [PathHolders.EntryListCodec, PathHolders.StringCodec, PathHolders.ByteArrayCodec],
    "EntryList_UUID_List_Integer": [PathHolders.EntryListUUIDListIntegerCodec],
    "EntryList_UUID_Long": [PathHolders.EntryListUUIDLongCodec],
    "EntryList_UUID_UUID": [PathHolders.EntryListUUIDUUIDCodec],
    "ErrorHolder": [PathHolders.ErrorHolder, PathHolders.ErrorHolderCodec],
    "IndexConfig": [PathHolders.IndexConfig, PathHolders.IndexConfigCodec],
    "ListCN_Data": [PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    "ListIndexConfig": [PathHolders.IndexConfigCodec, PathHolders.ListMultiFrameCodec],
    "List_Data": [PathHolders.Data, PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    "List_DistributedObjectInfo": [PathHolders.ListMultiFrameCodec, PathHolders.DistributedObjectInfoCodec],
    "List_Integer": [PathHolders.ListIntegerCodec],
    "List_Long": [PathHolders.ListLongCodec],
    "List_StackTraceElement": [PathHolders.ListMultiFrameCodec, PathHolders.StackTraceElementCodec],
    "List_String": [PathHolders.ListMultiFrameCodec, PathHolders.StringCodec],
    "List_UUID": [PathHolders.ListUUIDCodec],
    "Map_EndpointQualifier_Address": [PathHolders.MapCodec, PathHolders.EndpointQualifierCodec, PathHolders.AddressCodec],
    "Map_String_String": [PathHolders.MapCodec, PathHolders.StringCodec],
    "MemberInfo": [PathHolders.MemberInfo, PathHolders.MemberInfoCodec],
    "MemberVersion": [PathHolders.MemberVersion, PathHolders.MemberVersionCodec],
    "PagingPredicateHolder": [PathHolders.PagingPredicateHolder, PathHolders.PagingPredicateHolderCodec],
    "RaftGroupId": [PathHolders.RaftGroupId, PathHolders.RaftGroupIdCodec],
    "SimpleEntryView": [PathHolders.SimpleEntryView, PathHolders.SimpleEntryViewCodec],
    "StackTraceElement": [PathHolders.StackTraceElement, PathHolders.StackTraceElementCodec],
    "String": [PathHolders.StringCodec],
    "UUID": [PathHolders.UUID],
    "byteArray": [PathHolders.ByteArrayCodec],
    "longArray": [PathHolders.LongArrayCodec],
    'List_MemberInfo': [PathHolders.MemberInfo, PathHolders.ListMultiFrameCodec, PathHolders.MemberInfoCodec],
}

_go_types_common = {
    "Address": "core.Address",
    "AttributeConfig": "NA",
    "BitmapIndexOptions": "config.BitmapIndexOptions",
    "CacheConfigHolder": "NA",
    "CacheEventData": "NA",
    "CacheSimpleEntryListenerConfig": "NA",
    "ClientBwListEntry": "NA",
    "Data": "serialization.Data",
    "DistributedObjectInfo": "core.DistributedObjectInfo",
    "DurationConfig": "NA",
    "EndpointQualifier": "protocol.EndpointQualifier",
    "ErrorHolder": "protocol.ErrorHolder",
    "EventJournalConfig": "NA",
    "EvictionConfigHolder": "NA",
    "HotRestartConfig": "NA",
    "IndexConfig": "config.IndexConfig",
    "Integer": "int32",
    "List_CPMember": "NA",
    "ListenerConfigHolder": "NA",
    "Long": "int64",
    "MapStoreConfigHolder": "NA",
    "Map_EndpointQualifier_Address": "map[protocol.EndpointQualifier]core.Address",
    "Map_String_String": "map[string]string",
    "MemberInfo": "core.MemberInfo",
    "MergePolicyConfig": "NA",
    "MerkleTreeConfig": "NA",
    "NearCacheConfigHolder": "NA",
    "NearCachePreloaderConfig": "NA",
    "Pair": "serialization.Pair",
    "PredicateConfigHolder": "NA",
    "QueryCacheConfigHolder": "NA",
    "QueueStoreConfigHolder": "NA",
    "RaftGroupId": "protocol.RaftGroupId",
    "RingbufferStoreConfigHolder": "NA",
    "SimpleEntryView": "core.SimpleEntryView",
    "StackTraceElement": "protocol.StackTraceElement",
    "String": "string",
    "TimedExpiryPolicyFactoryConfig": "NA",
    "UUID": "core.UUID",
    "WanReplicationRef": "NA",
    "boolean": "bool",
    "byte": "byte",
    "byteArray": "[]byte",
    "int": "int32",
    "long": "int64",
    "longArray": "[]int64",
}

_go_types_encode = {
    "AnchorDataListHolder": "protocol.AnchorDataListHolder",
    "CPMember": "NA",
    "CacheEventData": "NA",
    "ClientBwListEntry": "NA",
    "EntryList_Data_Data": "[]protocol.Pair",
    "EntryList_Data_List_Data": "[]protocol.Pair",
    "EntryList_Integer_Integer": "[]protocol.Pair",
    "EntryList_Integer_Long": "[]protocol.Pair",
    "EntryList_Integer_UUID": "[]protocol.Pair",
    "EntryList_Long_byteArray": "[]protocol.Pair",
    "EntryList_String_EntryList_Integer_Long": "[]protocol.Pair",
    "EntryList_String_String": "[]protocol.Pair",
    "EntryList_String_byteArray": "[]protocol.Pair",
    "EntryList_UUID_List_Integer": "[]protocol.Pair",
    "EntryList_UUID_Long": "[]protocol.Pair",
    "EntryList_UUID_UUID": "[]protocol.Pair",
    "ListCN_Data": "[]serialization.Data",
    "List_AttributeConfig": "NA",
    "List_CacheEventData": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_ClientBwListEntry": "NA",
    "List_Data": "[]serialization.Data",
    "List_DistributedObjectInfo": "[]DistributedObjectInfo",
    "List_IndexConfig": "[]IndexConfig",
    "List_Integer": "[]int32",
    "List_ListCN_Data": "NA",
    "List_List_Data": "[]serialization.Data",
    "List_ListenerConfigHolder": "NA",
    "List_Long": "[]int64",
    "List_MCEvent": "NA",
    "List_MemberInfo": "[]core.MemberInfo",
    "List_QueryCacheConfigHolder": "NA",
    "List_QueryCacheEventData": "NA",
    "List_ScheduledTaskHandler": "NA",
    "List_SqlColumnMetadata": "NA",
    "List_StackTraceElement": "[]protocol.StackTraceElement",
    "List_String": "[]string",
    "List_UUID": "[]core.UUID",
    "List_Xid": "NA",
    "MCEvent": "NA",
    "MemberInfo": "core.MemberInfo",
    "MemberVersion": "core.MemberVersion",
    "MigrationState": "NA",
    "PagingPredicateHolder": "protocol.PagingPredicateHolder",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "SqlColumnMetadata": "NA",
    "SqlError": "NA",
    "SqlQueryId": "NA",
    "Xid": "NA",
}

_go_types_decode = {
    "AnchorDataListHolder": "protocol.AnchorDataListHolder",
    "CPMember": "NA",
    "CacheEventData": "NA",
    "ClientBwListEntry": "NA",
    "EntryList_Data_Data": "[]protocol.Pair",
    "EntryList_Data_List_Data": "[]protocol.Pair",
    "EntryList_Integer_Integer": "[]protocol.Pair",
    "EntryList_Integer_Long": "[]protocol.Pair",
    "EntryList_Integer_UUID": "[]protocol.Pair",
    "EntryList_Long_byteArray": "[]protocol.Pair",
    "EntryList_String_EntryList_Integer_Long": "[]protocol.Pair",
    "EntryList_String_String": "[]protocol.Pair",
    "EntryList_String_byteArray": "[]protocol.Pair",
    "EntryList_UUID_List_Integer": "[]protocol.Pair",
    "EntryList_UUID_Long": "[]protocol.Pair",
    "EntryList_UUID_UUID": "[]protocol.Pair",
    "ListCN_Data": "[]serialization.Data",
    "List_AttributeConfig": "NA",
    "List_CPMember": "NA",
    "List_CacheEventData": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_ClientBwListEntry": "NA",
    "List_Data": "[]serialization.Data",
    "List_DistributedObjectInfo": "[]core.DistributedObjectInfo",
    "List_IndexConfig": "[]IndexConfig",
    "List_Integer": "[]int32",
    "List_ListCN_Data": "NA",
    "List_List_Data": "[]serialization.Data",
    "List_ListenerConfigHolder": "NA",
    "List_Long": "[]int64",
    "List_MCEvent": "NA",
    "List_MemberInfo": "[]core.MemberInfo",
    "List_QueryCacheConfigHolder": "NA",
    "List_QueryCacheEventData": "NA",
    "List_ScheduledTaskHandler": "NA",
    "List_SqlColumnMetadata": "NA",
    "List_StackTraceElement": "[]protocol.StackTraceElement",
    "List_String": "[]string",
    "List_UUID": "[]core.UUID",
    "List_Xid": "NA",
    "MCEvent": "NA",
    "MemberInfo": "core.MemberInfo",
    "MemberVersion": "core.MemberVersion",
    "MigrationState": "NA",
    "PagingPredicateHolder": "protocol.PagingPredicateHolder",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "SqlColumnMetadata": "NA",
    "SqlError": "NA",
    "SqlQueryId": "NA",
    "Xid": "NA",
}
