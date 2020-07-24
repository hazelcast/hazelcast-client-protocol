ts_reserved_keywords = {'abstract', 'await', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class',
                          'const', 'continue', 'debugger', 'default', 'delete', 'do', 'double', 'else', 'enum',
                          'export', 'extends', 'false', 'final', 'finally', 'float', 'for', 'function', 'goto',
                          'if', 'implements', 'import', 'in', 'instanceof', 'int', 'interface', 'let', 'long',
                          'native', 'new', 'null', 'package', 'private', 'protected', 'public', 'return',
                          'short', 'static', 'super', 'switch', 'synchronized', 'this', 'throw', 'transient',
                          'true', 'try', 'typeof', 'var', 'void', 'volatile', 'while', 'with', 'yield'}

ts_ignore_service_list = {7, 8, 9, 10, 11, 12, 19, 20, 22, 24, 25, 26, 27, 30, 31, 32}


def ts_types_encode(key):
    ts_type = _ts_types[key]
    if ts_type == 'NA':
        raise NotImplementedError('MissingTypeMapping')
    return ts_type


def ts_types_decode(key):
    ts_type = _ts_types[key]
    if ts_type == 'NA':
        raise NotImplementedError('MissingTypeMapping')
    return ts_type


def ts_get_import_path_holders(param_type):
    return import_paths.get(param_type, None)


class ImportPathHolder:
    def __init__(self, name, path, is_builtin_codec=False,
                 is_custom_codec=False, is_internal_file=True,
                 import_as_wildcard=False):
        self.name = name
        self.path = path
        self.is_builtin_codec = is_builtin_codec
        self.is_custom_codec = is_custom_codec
        self.is_internal_file = is_internal_file
        self.import_as_wildcard = import_as_wildcard

    def get_import_statement(self, is_called_from_custom_codec):
        codec_path: str = self.path
        if self.is_internal_file:
            if is_called_from_custom_codec:
                if self.is_builtin_codec:
                    path = '../%s'
                elif self.is_custom_codec:
                    codec_path = codec_path.replace('custom/', '', 1)
                    path = './%s'
                else:
                    path = '../../%s'
            else:
                if self.is_builtin_codec or self.is_custom_codec:
                    path = './%s'
                else:
                    path = '../%s'
            statement = 'import {%s} from \'' + path + '\';'
        else:
            if self.import_as_wildcard:
                statement = 'import * as %s from \'%s\';'
            else:
                statement = 'import {%s} from \'%s\';'
        return statement % (self.name, codec_path)


class PathHolders:
    Long = ImportPathHolder('Long', 'long', is_internal_file=False, import_as_wildcard=True)
    UUID = ImportPathHolder('UUID', 'core/UUID')
    Data = ImportPathHolder('Data', 'serialization/Data')
    DataCodec = ImportPathHolder('DataCodec', 'builtin/DataCodec', is_builtin_codec=True)
    ByteArrayCodec = ImportPathHolder('ByteArrayCodec', 'builtin/ByteArrayCodec', is_builtin_codec=True)
    LongArrayCodec = ImportPathHolder('LongArrayCodec', 'builtin/LongArrayCodec', is_builtin_codec=True)
    Address = ImportPathHolder('Address', 'Address')
    AddressCodec = ImportPathHolder('AddressCodec', 'custom/AddressCodec', is_custom_codec=True)
    ErrorHolder = ImportPathHolder('ErrorHolder', 'protocol/ErrorHolder')
    ErrorHolderCodec = ImportPathHolder('ErrorHolderCodec', 'custom/ErrorHolderCodec', is_custom_codec=True)
    StackTraceElement = ImportPathHolder('StackTraceElement', 'protocol/StackTraceElement')
    StackTraceElementCodec = ImportPathHolder('StackTraceElementCodec',
                                              'custom/StackTraceElementCodec', is_custom_codec=True)
    SimpleEntryView = ImportPathHolder('SimpleEntryView', 'core/SimpleEntryView')
    SimpleEntryViewCodec = ImportPathHolder('SimpleEntryViewCodec', 'custom/SimpleEntryViewCodec', is_custom_codec=True)
    DistributedObjectInfo = ImportPathHolder('DistributedObjectInfo', 'DistributedObjectInfo')
    DistributedObjectInfoCodec = ImportPathHolder('DistributedObjectInfoCodec',
                                                  'custom/DistributedObjectInfoCodec', is_custom_codec=True)
    MemberInfo = ImportPathHolder('MemberInfo', 'core/MemberInfo')
    MemberInfoCodec = ImportPathHolder('MemberInfoCodec', 'custom/MemberInfoCodec', is_custom_codec=True)
    MemberVersion = ImportPathHolder('MemberVersion', 'core/MemberVersion')
    MemberVersionCodec = ImportPathHolder('MemberVersionCodec', 'custom/MemberVersionCodec', is_custom_codec=True)
    StringCodec = ImportPathHolder('StringCodec', 'builtin/StringCodec', is_builtin_codec=True)
    ListLongCodec = ImportPathHolder('ListLongCodec', 'builtin/ListLongCodec', is_builtin_codec=True)
    ListIntegerCodec = ImportPathHolder('ListIntegerCodec', 'builtin/ListIntegerCodec', is_builtin_codec=True)
    ListUUIDCodec = ImportPathHolder('ListUUIDCodec', 'builtin/ListUUIDCodec', is_builtin_codec=True)
    ListMultiFrameCodec = ImportPathHolder('ListMultiFrameCodec', 'builtin/ListMultiFrameCodec', is_builtin_codec=True)
    EntryListCodec = ImportPathHolder('EntryListCodec', 'builtin/EntryListCodec', is_builtin_codec=True)
    EntryListLongByteArrayCodec = ImportPathHolder('EntryListLongByteArrayCodec',
                                                   'builtin/EntryListLongByteArrayCodec', is_builtin_codec=True)
    EntryListIntegerUUIDCodec = ImportPathHolder('EntryListIntegerUUIDCodec', 'builtin/EntryListIntegerUUIDCodec',
                                                 is_builtin_codec=True)
    EntryListIntegerLongCodec = ImportPathHolder('EntryListIntegerLongCodec', 'builtin/EntryListIntegerLongCodec',
                                                 is_builtin_codec=True)
    EntryListIntegerIntegerCodec = ImportPathHolder('EntryListIntegerIntegerCodec',
                                                    'builtin/EntryListIntegerIntegerCodec', is_builtin_codec=True)
    EntryListUUIDLongCodec = ImportPathHolder('EntryListUUIDLongCodec', 'builtin/EntryListUUIDLongCodec',
                                              is_builtin_codec=True)
    EntryListUUIDUUIDCodec = ImportPathHolder('EntryListUUIDUUIDCodec', 'builtin/EntryListUUIDUUIDCodec',
                                              is_builtin_codec=True)
    EntryListUUIDListIntegerCodec = ImportPathHolder('EntryListUUIDListIntegerCodec',
                                                     'builtin/EntryListUUIDListIntegerCodec', is_builtin_codec=True)
    MapCodec = ImportPathHolder('MapCodec', 'builtin/MapCodec', is_builtin_codec=True)
    CodecUtil = ImportPathHolder('CodecUtil', 'builtin/CodecUtil', is_builtin_codec=True)
    IndexConfig = ImportPathHolder('IndexConfig', 'config/IndexConfig')
    IndexConfigCodec = ImportPathHolder('IndexConfigCodec', 'custom/IndexConfigCodec', is_custom_codec=True)
    BitmapIndexOptions = ImportPathHolder('BitmapIndexOptions', 'config/BitmapIndexOptions')
    BitmapIndexOptionsCodec = ImportPathHolder('BitmapIndexOptionsCodec', 'custom/BitmapIndexOptionsCodec',
                                               is_custom_codec=True)
    PagingPredicateHolder = ImportPathHolder('PagingPredicateHolder', 'protocol/PagingPredicateHolder')
    PagingPredicateHolderCodec = ImportPathHolder('PagingPredicateHolderCodec', 'custom/PagingPredicateHolderCodec',
                                                  is_custom_codec=True)
    AnchorDataListHolder = ImportPathHolder('AnchorDataListHolder', 'protocol/AnchorDataListHolder')
    AnchorDataListHolderCodec = ImportPathHolder('AnchorDataListHolderCodec', 'custom/AnchorDataListHolderCodec',
                                                 is_custom_codec=True)


import_paths = {
    'CodecUtil': PathHolders.CodecUtil,
    'long': [PathHolders.Long],
    'Long': [PathHolders.Long],
    'UUID': [PathHolders.UUID],
    'longArray': [PathHolders.Long, PathHolders.LongArrayCodec],
    'byteArray': [PathHolders.ByteArrayCodec],
    'String': [PathHolders.StringCodec],
    'Data': [PathHolders.Data, PathHolders.DataCodec],
    'Address': [PathHolders.Address, PathHolders.AddressCodec],
    'ErrorHolder': [PathHolders.ErrorHolder, PathHolders.ErrorHolderCodec],
    'StackTraceElement': [PathHolders.StackTraceElement, PathHolders.StackTraceElementCodec],
    'SimpleEntryView': [PathHolders.SimpleEntryView, PathHolders.Data, PathHolders.SimpleEntryViewCodec],
    'DistributedObjectInfo': [PathHolders.DistributedObjectInfo, PathHolders.DistributedObjectInfoCodec],
    'MemberInfo': [PathHolders.MemberInfo, PathHolders.MemberInfoCodec],
    'MemberVersion': [PathHolders.MemberVersion, PathHolders.MemberVersionCodec],
    'List_Long': [PathHolders.Long, PathHolders.ListLongCodec],
    'List_Integer': [PathHolders.ListIntegerCodec],
    'List_UUID': [PathHolders.UUID, PathHolders.ListUUIDCodec],
    'List_String': [PathHolders.ListMultiFrameCodec, PathHolders.StringCodec],
    'List_Data': [PathHolders.Data, PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    'ListCN_Data': [PathHolders.Data, PathHolders.ListMultiFrameCodec, PathHolders.DataCodec],
    'List_MemberInfo': [PathHolders.MemberInfo, PathHolders.ListMultiFrameCodec, PathHolders.MemberInfoCodec],
    'List_DistributedObjectInfo': [PathHolders.DistributedObjectInfo, PathHolders.ListMultiFrameCodec,
                                   PathHolders.DistributedObjectInfoCodec],
    'List_StackTraceElement': [PathHolders.StackTraceElement, PathHolders.ListMultiFrameCodec,
                               PathHolders.StackTraceElementCodec],
    'EntryList_String_String': [PathHolders.EntryListCodec, PathHolders.StringCodec],
    'EntryList_String_byteArray': [PathHolders.EntryListCodec, PathHolders.StringCodec, PathHolders.ByteArrayCodec],
    'EntryList_Long_byteArray': [PathHolders.EntryListLongByteArrayCodec, PathHolders.Long],
    'EntryList_Integer_UUID': [PathHolders.EntryListIntegerUUIDCodec, PathHolders.UUID],
    'EntryList_Integer_Long': [PathHolders.EntryListIntegerLongCodec, PathHolders.Long],
    'EntryList_Integer_Integer': [PathHolders.EntryListIntegerIntegerCodec],
    'EntryList_UUID_Long': [PathHolders.EntryListUUIDLongCodec, PathHolders.UUID, PathHolders.Long],
    'EntryList_String_EntryList_Integer_Long': [PathHolders.EntryListCodec, PathHolders.StringCodec,
                                                PathHolders.EntryListIntegerLongCodec, PathHolders.Long],
    'EntryList_UUID_UUID': [PathHolders.EntryListUUIDUUIDCodec, PathHolders.UUID],
    'EntryList_UUID_List_Integer': [PathHolders.EntryListUUIDListIntegerCodec, PathHolders.UUID],
    'EntryList_Data_Data': [PathHolders.EntryListCodec, PathHolders.DataCodec, PathHolders.Data],
    'Map_String_String': [PathHolders.MapCodec, PathHolders.StringCodec],
    'IndexConfig': [PathHolders.IndexConfig, PathHolders.IndexConfigCodec],
    'ListIndexConfig': [PathHolders.IndexConfig, PathHolders.IndexConfigCodec, PathHolders.ListMultiFrameCodec],
    'BitmapIndexOptions': [PathHolders.BitmapIndexOptions, PathHolders.BitmapIndexOptionsCodec],
    'AnchorDataListHolder': [PathHolders.AnchorDataListHolder, PathHolders.AnchorDataListHolderCodec],
    'PagingPredicateHolder': [PathHolders.PagingPredicateHolder, PathHolders.PagingPredicateHolderCodec],
}

_ts_types = {
    "boolean": "boolean",
    "int": "number",
    "long": "Long",
    "byte": "number",
    "Integer": "number",
    "Long": "Long",
    "UUID": "UUID",

    "longArray": "Long[]",
    "byteArray": "Buffer",
    "String": "string",
    "Data": "Data",
    "Address": "Address",
    "ErrorHolder": "ErrorHolder",
    "StackTraceElement": "StackTraceElement",
    "SimpleEntryView": "SimpleEntryView<Data, Data>",
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
    "DistributedObjectInfo": "DistributedObjectInfo",
    "IndexConfig": "IndexConfig",
    "BitmapIndexOptions": "BitmapIndexOptions",
    "AttributeConfig": "NA",
    "ListenerConfigHolder": "NA",
    "CacheSimpleEntryListenerConfig": "NA",
    "ClientBwListEntry": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "MemberInfo": "MemberInfo",
    "MemberVersion": "MemberVersion",
    "MCEvent": "NA",
    "AnchorDataListHolder": "AnchorDataListHolder",
    "PagingPredicateHolder": "PagingPredicateHolder",

    "List_Long": "Long[]",
    "List_Integer": "number[]",
    "List_UUID": "UUID[]",
    "List_String": "string[]",
    "List_Xid": "NA",
    "List_Data": "Data[]",
    "ListCN_Data": "Data[]",
    "List_MemberInfo": "MemberInfo[]",
    "List_ScheduledTaskHandler": "NA",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "DistributedObjectInfo[]",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "IndexConfig[]",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "StackTraceElement[]",
    "List_ClientBwListEntry": "NA",
    "List_MCEvent": "NA",

    "EntryList_String_String": "Array<[string, string]>",
    "EntryList_String_byteArray": "Array<[string, Buffer]>",
    "EntryList_Long_byteArray": "Array<[Long, number[]]>",
    "EntryList_Integer_UUID": "Array<[number, UUID]>",
    "EntryList_Integer_Long": "Array<[number, Long]>",
    "EntryList_Integer_Integer": "Array<[number, number]>",
    "EntryList_UUID_Long": "Array<[UUID, Long]>",
    "EntryList_String_EntryList_Integer_Long": "Array<[string, Array<[number, Long]>]>",
    "EntryList_UUID_UUID": "Array<[UUID, UUID]>",
    "EntryList_UUID_List_Integer": "Array<[UUID, number[]]>",
    "EntryList_Data_Data": "Array<[Data, Data]>",
    "EntryList_Data_List_Data": "Array<[Data, Data[]]>",

    "Map_String_String": "Map<string, string>",
}
