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
    return "_%s" % value


def go_types_encode(key):
    try:
        go_type = _go_types_encode[key]
    except KeyError:
        try:
            go_type = _go_types_common[key]
        except KeyError:
            go_type = "NA"
    if go_type == "NA":
        raise NotImplementedError("Missing type mapping for '" + key + "'")
    return go_type


def go_types_decode(key):
    try:
        go_type = _go_types_decode[key]
    except KeyError:
        try:
            go_type = _go_types_common[key]
        except KeyError:
            go_type = "NA"
    if go_type == "NA":
        raise NotImplementedError("Missing type for '" + key + "'")
    return go_type


def go_get_import_statements(*args):
    import_statements = set()
    for arg in args:
        params = [arg] if isinstance(arg, str) else arg
        for param in params:
            type = param["type"] if isinstance(param, dict) else param
            for path_holder in import_paths.get(type, []):
                if path_holder.name.endswith("Codec"):
                    continue
                path = path_holder.import_statement
                if path is not None:
                    import_statements.add(path)
    import_statements.add('"github.com/hazelcast/hazelcast-go-client/internal/proto"')
    if args[0] == "SimpleEntryView":
        import_statements.remove('iserialization"github.com/hazelcast/hazelcast-go-client/internal/serialization"')
    return sorted(import_statements)


class ImportPathHolder:
    def __init__(self, name, path, is_builtin_codec=False, is_custom_codec=False):
        self.name = name
        self.path = path

    @property
    def import_statement(self):
        if not self.path:
            return ""
        return '''"github.com/hazelcast/hazelcast-go-client%s"''' % self.path


class InternalImportPathHolder:
    def __init__(self, name, path, alias="", is_builtin_codec=False, is_custom_codec=False):
        self.name = name
        self.path = path
        self.alias = alias

    @property
    def import_statement(self):
        if self.path is None:
            return ""
        alias = "%s " % self.alias if self.alias else ""
        return '''%s"github.com/hazelcast/hazelcast-go-client/internal%s"''' % (self.alias, self.path)


class PathHolders:
    Address = ImportPathHolder("Address", "/cluster")
    AddressCodec = InternalImportPathHolder("AddressCodec", None, is_custom_codec=True)
    AnchorDataListHolder = InternalImportPathHolder("AnchorDataListHolder", "")
    AnchorDataListHolderCodec = InternalImportPathHolder("AnchorDataListHolderCodec", "", is_custom_codec=True)
    BitmapIndexOptions = ImportPathHolder("BitmapIndexOptions", "/types")
    BitmapIndexOptionsCodec = InternalImportPathHolder("BitmapIndexOptionsCodec", None, is_custom_codec=True)
    ByteArrayCodec = InternalImportPathHolder("ByteArrayCodec", "", is_builtin_codec=True)
    CodecUtilCodec = InternalImportPathHolder("CodecUtil", "", is_builtin_codec=True)
    Data = InternalImportPathHolder('Data', '/serialization', 'iserialization')
    DataCodec = InternalImportPathHolder("DataCodec", "", is_builtin_codec=True)
    DistributedObjectInfo = ImportPathHolder("DistributedObjectInfo", "/types")
    DistributedObjectInfoCodec = InternalImportPathHolder("DistributedObjectInfoCodec", None, is_custom_codec=True)
    EndpointQualifier = ImportPathHolder("EndpointQualifier", "/cluster")
    EndpointQualifierCodec = InternalImportPathHolder("EndpointQualifierCodec", None, is_custom_codec=True)
    EntryListCodec = InternalImportPathHolder("EntryListCodec", "", is_builtin_codec=True)
    EntryListIntegerIntegerCodec = InternalImportPathHolder("EntryListIntegerIntegerCodec", "", is_builtin_codec=True)
    EntryListIntegerLongCodec = InternalImportPathHolder("EntryListIntegerLongCodec", "", is_builtin_codec=True)
    EntryListIntegerUUIDCodec = InternalImportPathHolder("EntryListIntegerUUIDCodec", "", is_builtin_codec=True)
    EntryListLongByteArrayCodec = InternalImportPathHolder("EntryListLongByteArrayCodec", "", is_builtin_codec=True)
    EntryListUUIDListIntegerCodec = InternalImportPathHolder("EntryListUUIDListIntegerCodec", "", is_builtin_codec=True)
    EntryListUUIDLongCodec = InternalImportPathHolder("EntryListUUIDLongCodec", "", is_builtin_codec=True)
    EntryListUUIDUUIDCodec = InternalImportPathHolder("EntryListUUIDUUIDCodec", "", is_builtin_codec=True)
    ErrorHolder = InternalImportPathHolder("ErrorHolder", "/proto")
    ErrorHolderCodec = InternalImportPathHolder("ErrorHolderCodec", "", is_custom_codec=True)
    IndexConfig = ImportPathHolder("IndexConfig", "/types")
    IndexConfigCodec = InternalImportPathHolder("IndexConfigCodec", "", is_custom_codec=True)
    ListDataCodec = InternalImportPathHolder("ListDataCodec", "", is_builtin_codec=True)
    ListIntegerCodec = InternalImportPathHolder("ListIntegerCodec", "", is_builtin_codec=True)
    ListLongCodec = InternalImportPathHolder("ListLongCodec", "", is_builtin_codec=True)
    ListMultiFrameCodec = InternalImportPathHolder("ListMultiFrameCodec", None, is_builtin_codec=True)
    ListUUIDCodec = InternalImportPathHolder("ListUUIDCodec", "", is_builtin_codec=True)
    LongArrayCodec = InternalImportPathHolder("LongArrayCodec", "", is_builtin_codec=True)
    MapCodec = InternalImportPathHolder("MapCodec", None, is_builtin_codec=True)
    MemberInfo = ImportPathHolder("MemberInfo", "/cluster")
    MemberInfoCodec = InternalImportPathHolder("MemberInfoCodec", "", is_custom_codec=True)
    MemberVersion = ImportPathHolder("MemberVersion", "/cluster")
    MemberVersionCodec = InternalImportPathHolder("MemberVersionCodec", None, is_custom_codec=True)
    PagingPredicateHolder = InternalImportPathHolder("PagingPredicateHolder", "")
    PagingPredicateHolderCodec = InternalImportPathHolder("PagingPredicateHolderCodec", "", is_custom_codec=True)
    RaftGroupId = InternalImportPathHolder("RaftGroupId", "")
    RaftGroupIdCodec = InternalImportPathHolder("RaftGroupIdCodec", "", is_custom_codec=True)
    SimpleEntryView = ImportPathHolder("SimpleEntryView", "/types")
    SimpleEntryViewCodec = InternalImportPathHolder("SimpleEntryViewCodec", None, is_custom_codec=True)
    StackTraceElement = InternalImportPathHolder("StackTraceElement", "/hzerrors", alias="ihzerrors")
    StackTraceElementCodec = InternalImportPathHolder("StackTraceElementCodec", None, is_custom_codec=True)
    StringCodec = InternalImportPathHolder("StringCodec", None, is_builtin_codec=True)
    UUID = ImportPathHolder("UUID", "/types")


import_paths = {
    "Address": [PathHolders.Address, PathHolders.AddressCodec],
    "AnchorDataListHolder": [PathHolders.AnchorDataListHolder, PathHolders.AnchorDataListHolderCodec],
    "BitmapIndexOptions": [PathHolders.BitmapIndexOptions, PathHolders.BitmapIndexOptionsCodec],
    "CodecUtil": PathHolders.CodecUtilCodec,
    "Data": [PathHolders.Data, PathHolders.DataCodec],
    "DistributedObjectInfo": [PathHolders.DistributedObjectInfo, PathHolders.DistributedObjectInfoCodec],
    "EndpointQualifier": [PathHolders.EndpointQualifier],
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
    "List_DistributedObjectInfo": [PathHolders.ListMultiFrameCodec, PathHolders.DistributedObjectInfo, PathHolders.DistributedObjectInfoCodec],
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
    "Address": "cluster.Address",
    "AnchorDataListHolder": "NA",
    # "AttributeConfig": "NA",
    "BitmapIndexOptions": "types.BitmapIndexOptions",
    # "CacheConfigHolder": "NA",
    # "CacheEventData": "NA",
    # "CacheSimpleEntryListenerConfig": "NA",
    # "ClientBwListEntry": "NA",
    "Data": "*iserialization.Data",
    "DistributedObjectInfo": "types.DistributedObjectInfo",
    # "DurationConfig": "NA",
    "EndpointQualifier": "cluster.EndpointQualifier",
    "ErrorHolder": "proto.ErrorHolder",
    # "EventJournalConfig": "NA",
    # "EvictionConfigHolder": "NA",
    # "HotRestartConfig": "NA",
    "IndexConfig": "types.IndexConfig",
    "Integer": "int32",
    # "List_CPMember": "NA",
    # "ListenerConfigHolder": "NA",
    "Long": "int64",
    # "MapStoreConfigHolder": "NA",
    "Map_EndpointQualifier_Address": "map[cluster.EndpointQualifier]cluster.Address",
    "Map_String_String": "map[string]string",
    "MemberInfo": "cluster.MemberInfo",
    # "MergePolicyConfig": "NA",
    # "MerkleTreeConfig": "NA",
    # "NearCacheConfigHolder": "NA",
    # "NearCachePreloaderConfig": "NA",
    "Pair": "proto.Pair",
    # "PredicateConfigHolder": "NA",
    # "QueryCacheConfigHolder": "NA",
    # "QueueStoreConfigHolder": "NA",
    # "RaftGroupId": "proto.RaftGroupId",
    # "RingbufferStoreConfigHolder": "NA",
    "SimpleEntryView": "*types.SimpleEntryView",
    "StackTraceElement": "ihzerrors.StackTraceElement",
    "String": "string",
    # "TimedExpiryPolicyFactoryConfig": "NA",
    "UUID": "types.UUID",
    # "WanReplicationRef": "NA",
    "boolean": "bool",
    "byte": "byte",
    "byteArray": "[]byte",
    "int": "int32",
    "long": "int64",
    "longArray": "[]int64",
}

_go_types_encode = {
    # "AnchorDataListHolder": "proto.AnchorDataListHolder",
    "AnchorDataListHolder": "NA",
    # "CPMember": "NA",
    # "CacheEventData": "NA",
    # "ClientBwListEntry": "NA",
    "EntryList_Data_Data": "[]proto.Pair",
    "EntryList_Data_List_Data": "[]proto.Pair",
    "EntryList_Integer_Integer": "[]proto.Pair",
    "EntryList_Integer_Long": "[]proto.Pair",
    "EntryList_Integer_UUID": "[]proto.Pair",
    "EntryList_Long_byteArray": "[]proto.Pair",
    "EntryList_String_EntryList_Integer_Long": "[]proto.Pair",
    "EntryList_String_String": "[]proto.Pair",
    "EntryList_String_byteArray": "[]proto.Pair",
    "EntryList_UUID_List_Integer": "[]proto.Pair",
    "EntryList_UUID_Long": "[]proto.Pair",
    "EntryList_UUID_UUID": "[]proto.Pair",
    # "ListCN_Data": "[]*iserialization.Data",
    "List_AttributeConfig": "NA",
    # "List_CacheEventData": "NA",
    # "List_CacheSimpleEntryListenerConfig": "NA",
    # "List_ClientBwListEntry": "NA",
    "List_Data": "[]*iserialization.Data",
    "List_DistributedObjectInfo": "[]types.DistributedObjectInfo",
    "List_IndexConfig": "[]types.IndexConfig",
    "List_Integer": "[]int32",
    # "List_ListCN_Data": "NA",
    "List_List_Data": "[]*iserialization.Data",
    # "List_ListenerConfigHolder": "NA",
    "List_Long": "[]int64",
    # "List_MCEvent": "NA",
    "List_MemberInfo": "[]cluster.MemberInfo",
    # "List_QueryCacheConfigHolder": "NA",
    # "List_QueryCacheEventData": "NA",
    # "List_ScheduledTaskHandler": "NA",
    # "List_SqlColumnMetadata": "NA",
    "List_StackTraceElement": "[]ihzerrors.StackTraceElement",
    "List_String": "[]string",
    "List_UUID": "[]types.UUID",
    # "List_Xid": "NA",
    # "MCEvent": "NA",
    "MemberInfo": "cluster.MemberInfo",
    "MemberVersion": "cluster.MemberVersion",
    # "MigrationState": "NA",
    # "PagingPredicateHolder": "proto.PagingPredicateHolder",
    "PagingPredicateHolder": "NA",
    # "QueryCacheEventData": "NA",
    # "ScheduledTaskHandler": "NA",
    # "SqlColumnMetadata": "NA",
    # "SqlError": "NA",
    # "SqlQueryId": "NA",
    # "Xid": "NA",
}

_go_types_decode = {
    # "Address": "cluster.Address",
    # "CPMember": "NA",
    # "CacheEventData": "NA",
    # "ClientBwListEntry": "NA",
    "EntryList_Data_Data": "[]proto.Pair",
    "EntryList_Data_List_Data": "[]proto.Pair",
    "EntryList_Integer_Integer": "[]proto.Pair",
    "EntryList_Integer_Long": "[]proto.Pair",
    "EntryList_Integer_UUID": "[]proto.Pair",
    "EntryList_Long_byteArray": "[]proto.Pair",
    "EntryList_String_EntryList_Integer_Long": "[]proto.Pair",
    "EntryList_String_String": "[]proto.Pair",
    "EntryList_String_byteArray": "[]proto.Pair",
    "EntryList_UUID_List_Integer": "[]proto.Pair",
    "EntryList_UUID_Long": "[]proto.Pair",
    "EntryList_UUID_UUID": "[]proto.Pair",
    # "ListCN_Data": "[]*iserialization.Data",
    "List_AttributeConfig": "NA",
    # "List_CPMember": "NA",
    # "List_CacheEventData": "NA",
    # "List_CacheSimpleEntryListenerConfig": "NA",
    # "List_ClientBwListEntry": "NA",
    "List_Data": "[]*iserialization.Data",
    "List_DistributedObjectInfo": "[]types.DistributedObjectInfo",
    "List_IndexConfig": "[]types.IndexConfig",
    "List_Integer": "[]int32",
    # "List_ListCN_Data": "NA",
    "List_List_Data": "[]*iserialization.Data",
    # "List_ListenerConfigHolder": "NA",
    "List_Long": "[]int64",
    # "List_MCEvent": "NA",
    "List_MemberInfo": "[]cluster.MemberInfo",
    # "List_QueryCacheConfigHolder": "NA",
    # "List_QueryCacheEventData": "NA",
    # "List_ScheduledTaskHandler": "NA",
    # "List_SqlColumnMetadata": "NA",
    "List_StackTraceElement": "[]ihzerrors.StackTraceElement",
    "List_String": "[]string",
    "List_UUID": "[]types.UUID",
    # "List_Xid": "NA",
    # "MCEvent": "NA",
    "MemberInfo": "cluster.MemberInfo",
    "MemberVersion": "cluster.MemberVersion",
    # "MigrationState": "NA",
    # "PagingPredicateHolder": "proto.PagingPredicateHolder",
    # "QueryCacheEventData": "NA",
    # "ScheduledTaskHandler": "NA",
    # "SqlColumnMetadata": "NA",
    # "SqlError": "NA",
    # "SqlQueryId": "NA",
    # "Xid": "NA",
}

    
def go_augment_enum(codec, param):
    cast_type = _go_enum.get((codec, param["name"]))
    if cast_type:
        return "%s(%s)" % (cast_type, go_escape_keyword(param["name"]))
    return go_escape_keyword(param["name"])


_go_enum = {
    ("BitmapIndexOptions", "uniqueKeyTransformation"): "types.UniqueKeyTransformation",
    ("EndpointQualifier", "type"): "cluster.EndpointQualifierType",
    ("IndexConfig", "type"): "types.IndexType",
}

def go_rename_field(codec, param):
    name = param["name"]
    field_name = _go_field.get((codec, name))
    if field_name:
        return field_name
    return "%s%s" % (name[0].upper(), name[1:])

_go_field = {
    ("SimpleEntryView", "ttl"): "TTL",
    ("MemberInfo", "uuid"): "UUID",
}