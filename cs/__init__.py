cs_reserved_words = ["abstract", "add", "as", "ascending", "async", "await", "base", "bool", "break", "by", "byte", "case",
                     "catch", "char", "checked", "class", "const", "continue", "decimal", "default", "delegate", "descending",
                     "do", "double", "dynamic", "else", "enum", "equals", "explicit", "extern", "false", "finally", "fixed",
                     "float", "for", "foreach", "from", "get", "global", "goto", "group", "if", "implicit", "in", "int",
                     "interface", "internal", "into", "is", "join", "let", "lock", "long", "namespace", "new", "null", "object",
                     "on", "operator", "orderby", "out", "override", "params", "partial", "private", "protected", "public",
                     "readonly", "ref", "remove", "return", "sbyte", "sealed", "select", "set", "short", "sizeof", "stackalloc",
                     "static", "string", "struct", "switch", "this", "throw", "true", "try", "typeof", "uint", "ulong",
                     "unchecked", "unsafe", "ushort", "using", "value", "var", "virtual", "void", "volatile", "where", "while",
                     "yield"]


def cs_types_encode(key):
    try:
        cs_type = _cs_types_encode[key]
    except KeyError:
        cs_type = _cs_types_common[key]
    if cs_type == "NA":
        raise NotImplementedError("Missing type Mapping")
    return cs_type


def cs_types_decode(key):
    try:
        cs_type = _cs_types_decode[key]
    except KeyError:
        cs_type = _cs_types_common[key]
    if cs_type == "NA":
        raise NotImplementedError("Missing type Mapping")
    return cs_type


def cs_escape_keyword(value):
    if value not in cs_reserved_words:
        return value
    return "@" + value


_cs_types_common = {
    "boolean": "bool",
    "int": "int",
    "long": "long",
    "byte": "byte",
    "Integer": "int",
    "Long": "long",
    "UUID": "Guid",
    "enum": "int",

    "longArray": "long[]",
    "byteArray": "byte[]",
    "String": "string",
    "Data": "IData",

    "Address": "Hazelcast.IO.Address",
    "ErrorHolder": "Hazelcast.Client.Protocol.ErrorHolder",
    "StackTraceElement": "Hazelcast.Util.StackTraceElement",
    "SimpleEntryView": "Hazelcast.Map.SimpleEntryView<IData, IData>",
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
    "DistributedObjectInfo": "Hazelcast.Client.DistributedObjectInfo",
    "IndexConfig": "Hazelcast.Config.IndexConfig",
    "AttributeConfig": "NA",
    "ListenerConfigHolder": "NA",
    "CacheSimpleEntryListenerConfig": "NA",

    "Map_String_String": "IDictionary<string, string>"
}

_cs_types_encode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",
    "Member": "Hazelcast.Core.Member",

    "List_Long": "IEnumerable<long>",
    "List_UUID": "IEnumerable<Guid>",
    "List_String": "IEnumerable<string>",
    "List_Xid": "NA",
    "List_Data": "IEnumerable<IData>",
    "ListCN_Data": "IEnumerable<IData>",
    "List_Member": "IEnumerable<Hazelcast.Core.Member>",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "IEnumerable<Hazelcast.Client.DistributedObjectInfo>",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "IEnumerable<Hazelcast.Config.IndexConfig>",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "IEnumerable<Hazelcast.Util.StackTraceElement>",

    "EntryList_String_String": "IEnumerable<KeyValuePair<string, string>>",
    "EntryList_String_byteArray": "IEnumerable<KeyValuePair<string, byte[]>>",
    "EntryList_Long_byteArray": "IEnumerable<KeyValuePair<long, byte[]>>",
    "EntryList_Integer_UUID": "IEnumerable<KeyValuePair<int, Guid>>",
    "EntryList_Integer_Long": "IEnumerable<KeyValuePair<int, long>>",
    "EntryList_Integer_Integer": "IEnumerable<KeyValuePair<int, int>>",
    "EntryList_UUID_Long": "IEnumerable<KeyValuePair<Guid, long>>",
    "EntryList_String_EntryList_Integer_Long": "IEnumerable<KeyValuePair<string, IEnumerable<KeyValuePair<int, long>>>>",
    "EntryList_UUID_List_Integer": "IEnumerable<KeyValuePair<Guid, IEnumerable<int>>>",
    "EntryList_Data_Data": "IEnumerable<KeyValuePair<IData, IData>>",
}

_cs_types_decode = {
    "CacheEventData": "NA",
    "QueryCacheEventData": "NA",
    "ScheduledTaskHandler": "NA",
    "Xid": "NA",

    "List_Long": "IList<long>",
    "List_UUID": "IList<Guid>",
    "List_Xid": "NA",
    "List_String": "IList<string>",
    "List_Data": "IList<IData>",
    "ListCN_Data": "IList<IData>",
    "List_CacheEventData": "NA",
    "List_QueryCacheConfigHolder": "NA",
    "List_DistributedObjectInfo": "IList<Hazelcast.Client.DistributedObjectInfo>",
    "List_QueryCacheEventData": "NA",
    "List_IndexConfig": "IList<Hazelcast.Config.IndexConfig>",
    "List_AttributeConfig": "NA",
    "List_ListenerConfigHolder": "NA",
    "List_CacheSimpleEntryListenerConfig": "NA",
    "List_StackTraceElement": "IList<Hazelcast.Util.StackTraceElement>",

    "EntryList_String_String": "IList<KeyValuePair<string, string>>",
    "EntryList_String_byteArray": "IList<KeyValuePair<string, byte[]>>",
    "EntryList_Long_byteArray": "IList<KeyValuePair<long, byte[]>>",
    "EntryList_Integer_UUID": "IList<KeyValuePair<int, Guid>>",
    "EntryList_Integer_Long": "IList<KeyValuePair<int, long>>",
    "EntryList_Integer_Integer": "IList<KeyValuePair<int, int>>",
    "EntryList_UUID_Long": "IList<KeyValuePair<Guid, long>>",
    "EntryList_String_EntryList_Integer_Long": "IList<KeyValuePair<string, IList<KeyValuePair<int, long>>>>",
    "EntryList_UUID_List_Integer": "IList<KeyValuePair<Guid, IList<int>>>",
    "EntryList_Data_Data": "IList<KeyValuePair<IData, IData>>"
}