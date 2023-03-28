import keyword
import re


def py_types_encode_decode(t):
    if t not in _py_types:
        raise NotImplementedError("Missing type Mapping for %s" % t)


_pattern1 = re.compile("(.)([A-Z][a-z]+)")
_pattern2 = re.compile("([a-z0-9])([A-Z])")


def py_param_name(type_name, check_for_keywords=True):
    type_name = _pattern1.sub(r"\1_\2", type_name)
    type_name = _pattern2.sub(r"\1_\2", type_name).lower()
    if check_for_keywords and keyword.iskeyword(type_name):
        return "_%s" % type_name
    return type_name


def py_get_import_path_holders(param_type):
    return import_paths.get(param_type, [])


_private_custom_types = {"SqlError", "SqlQueryId"}


def py_custom_type_name(name):
    if name in _private_custom_types:
        return "_" + name
    return name


_decoder_requires_to_object_fn = {"SqlPage"}


def py_decoder_requires_to_object_fn(param_type):
    return param_type in _decoder_requires_to_object_fn


def py_to_object_fn_in_decode(params):
    for param in params:
        if py_decoder_requires_to_object_fn(param["type"]):
            return True

    return False


py_ignore_service_list = {
    "Cache",
    "CardinalityEstimator",
    "Client.addPartitionLostListener",
    "Client.createProxies",
    "Client.removeMigrationListener",
    "Client.removePartitionLostListener",
    "Client.triggerPartitionAssignment",
    "ContinuousQuery",
    "CPSubsystem",
    "DurableExecutor",
    "DynamicConfig",
    "ExecutorService.cancelOnMember",
    "ExecutorService.cancelOnPartition",
    "Map.addPartitionLostListener",
    "Map.eventJournalRead",
    "Map.eventJournalSubscribe",
    "Map.removeAll",
    "Map.removePartitionLostListener",
    "Map.submitToKey",
    "Map.replaceAll",
    "MultiMap.delete",
    "MC",
    "Queue.drainTo",
    "ReplicatedMap.addNearCacheEntryListener",
    "ScheduledExecutor",
    "Sql.execute_reserved",
    "Sql.fetch_reserved",
    "Sql.mappingDdl",
    "TransactionalMap.containsValue",
    "XATransaction",
    "Jet",
}


class ImportPathHolder:
    def __init__(self, name, path):
        self.name = name
        self.path = path

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
    SetUUIDCodec = ImportPathHolder("SetUUIDCodec", "protocol.builtin")
    ListDataCodec = ImportPathHolder("ListDataCodec", "protocol.builtin")
    ListMultiFrameCodec = ImportPathHolder("ListMultiFrameCodec", "protocol.builtin")
    ListCNDataCodec = ImportPathHolder("ListCNDataCodec", "protocol.builtin")
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
    EndpointQualifier = ImportPathHolder("EndpointQualifier", "core")
    EndpointQualifierCodec = ImportPathHolder("EndpointQualifierCodec",
                                              "protocol.codec.custom.endpoint_qualifier_codec")
    RaftGroupId = ImportPathHolder("RaftGroupId", "protocol")
    RaftGroupIdCodec = ImportPathHolder("RaftGroupIdCodec", "protocol.codec.custom.raft_group_id_codec")
    SqlQueryId = ImportPathHolder("_SqlQueryId", "sql")
    SqlQueryIdCodec = ImportPathHolder("SqlQueryIdCodec", "protocol.codec.custom.sql_query_id_codec")
    SqlColumnMetadata = ImportPathHolder("SqlColumnMetadata", "sql")
    SqlColumnMetadataCodec = ImportPathHolder("SqlColumnMetadataCodec", "protocol.codec.custom.sql_column_metadata_codec")
    SqlError = ImportPathHolder("_SqlError", "sql")
    SqlErrorCodec = ImportPathHolder("SqlErrorCodec", "protocol.codec.custom.sql_error_codec")
    SqlPageCodec = ImportPathHolder("SqlPageCodec", "protocol.builtin")
    Schema = ImportPathHolder("Schema", "serialization.compact")
    SchemaCodec = ImportPathHolder("SchemaCodec", "protocol.codec.custom.schema_codec")
    FieldDescriptor = ImportPathHolder("FieldDescriptor", "serialization.compact")
    FieldDescriptorCodec = ImportPathHolder("FieldDescriptorCodec", "protocol.codec.custom.field_descriptor_codec")


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
    "Set_UUID": [PathHolders.SetUUIDCodec],
    "List_String": [PathHolders.ListMultiFrameCodec, PathHolders.StringCodec],
    "List_Data": [PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    "ListCN_Data": [PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    "List_MemberInfo": [PathHolders.ListMultiFrameCodec, PathHolders.MemberInfoCodec],
    "List_DistributedObjectInfo": [PathHolders.ListMultiFrameCodec, PathHolders.DistributedObjectInfoCodec],
    "List_StackTraceElement": [PathHolders.ListMultiFrameCodec, PathHolders.StackTraceElementCodec],
    "List_SqlColumnMetadata": [PathHolders.ListMultiFrameCodec, PathHolders.SqlColumnMetadataCodec],
    "List_FieldDescriptor": [PathHolders.ListMultiFrameCodec, PathHolders.FieldDescriptorCodec],
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
                                      PathHolders.AddressCodec],
    "SqlQueryId": [PathHolders.SqlQueryId, PathHolders.SqlQueryIdCodec],
    "SqlColumnMetadata": [PathHolders.SqlColumnMetadata, PathHolders.SqlColumnMetadataCodec],
    "SqlError": [PathHolders.SqlError, PathHolders.SqlErrorCodec],
    "SqlPage": [PathHolders.SqlPageCodec],
    "Schema": [PathHolders.Schema, PathHolders.SchemaCodec],
    "FieldDescriptor": [PathHolders.FieldDescriptor, PathHolders.FieldDescriptorCodec],
}

_py_types = {
    "boolean",
    "byte",
    "int",
    "long",
    "UUID",

    "byteArray",
    "longArray",
    "String",
    "Data",

    "Address",
    "DistributedObjectInfo",
    "SimpleEntryView",
    "ErrorHolder",
    "StackTraceElement",
    "MemberInfo",
    "MemberVersion",
    "EndpointQualifier",
    "RaftGroupId",
    "AnchorDataListHolder",
    "PagingPredicateHolder",
    "SqlQueryId",
    "SqlColumnMetadata",
    "SqlError",
    "SqlPage",
    "Schema",
    "FieldDescriptor",

    "IndexConfig",
    "BitmapIndexOptions",

    "List_Integer",
    "List_Long",
    "List_UUID",
    "Set_UUID",

    "List_byteArray",
    "List_Data",
    "List_DistributedObjectInfo",
    "List_MemberInfo",
    "List_String",
    "List_StackTraceElement",
    "ListCN_Data",
    "List_SqlColumnMetadata",
    "List_FieldDescriptor",

    "EntryList_UUID_Long",

    "EntryList_String_String",
    "EntryList_UUID_List_Integer",
    "EntryList_Data_Data",
    "EntryList_Data_List_Data",

    "Map_String_String",
    "Map_EndpointQualifier_Address",
}


def py_escape_keyword(value):
    if value in keyword.kwlist:
        return "%s_" % value
    else:
        return value
