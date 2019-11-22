import functools
import struct

from . import reference_objects

from binary import *
from binary.constants import *
from util import *

formats = {
    'boolean': '<?',
    'byte': '<B',
    'int': '<I',
    'long': '<q',
    'short': '<H',
    'enum': '<I',
}

sizes = {
    'boolean': BOOLEAN_SIZE_IN_BYTES,
    'byte': BYTE_SIZE_IN_BYTES,
    'int': INT_SIZE_IN_BYTES,
    'long': LONG_SIZE_IN_BYTES,
    'UUID': UUID_SIZE_IN_BYTES,
    'enum': INT_SIZE_IN_BYTES,
}

id_fmt = "0x%02x%02x%02x"


def read_definition(definition, protocol_defs_path):
    file_path = os.path.join(protocol_defs_path, definition + '.yaml')
    with open(file_path, 'r') as file:
        return yaml.load(file, Loader=yaml.Loader)


def get_custom_type_params(protocol_defs_path):
    custom_codec_defs_path = os.path.join(protocol_defs_path, 'custom')
    if not os.path.exists(custom_codec_defs_path):
        return {}
    definitions = read_definition('Custom', custom_codec_defs_path)
    params = {}
    custom_types = definitions["customTypes"]
    for definition in custom_types:
        params[definition["name"]] = definition["params"]
    return params


class Frame:
    def __init__(self, content, flags=DEFAULT_FLAGS):
        self.content = content
        self.flags = flags

    def encode_frame(self, is_final=False):
        frame_length = SIZE_OF_FRAME_LENGTH_AND_FLAGS + len(self.content)
        b = bytearray(frame_length)
        struct.pack_into(formats['int'], b, FRAME_LENGTH_OFFSET, frame_length)
        flags = self.flags | IS_FINAL_FLAG if is_final else self.flags
        struct.pack_into(formats['short'], b, FLAGS_OFFSET, flags)
        b[SIZE_OF_FRAME_LENGTH_AND_FLAGS:] = self.content
        return b


NULL_FRAME = Frame(bytearray(0), IS_NULL_FLAG)
BEGIN_FRAME = Frame(bytearray(0), BEGIN_DATA_STRUCTURE_FLAG)
END_FRAME = Frame(bytearray(0), END_DATA_STRUCTURE_FLAG)


class ClientMessage:
    def __init__(self):
        self.frames = []

    def add_frame(self, frame):
        self.frames.append(frame)

    def write(self, file):
        n = len(self.frames)
        for i in range(n):
            frame = self.frames[i]
            file.write(struct.pack(formats['int'], SIZE_OF_FRAME_LENGTH_AND_FLAGS + len(frame.content)))
            is_last_frame = i == (n - 1)
            flags = frame.flags | IS_FINAL_FLAG if is_last_frame else frame.flags
            file.write(struct.pack(formats['short'], flags))
            file.write(frame.content)


class Encoder:
    CUSTOM_TYPE_PARAMS = None

    @staticmethod
    def init_custom_type_params(protocol_defs_path):
        Encoder.CUSTOM_TYPE_PARAMS = get_custom_type_params(protocol_defs_path)

    @staticmethod
    def encode_request(request, nullable=False):
        params = request.get("params", [])
        fix_sized_params = fixed_params(params)
        var_sized_params = var_size_params(params)

        client_message = ClientMessage()

        initial_frame = FixSizedEncoder.create_initial_frame(fix_sized_params, request["id"],
                                                             REQUEST_FIX_SIZED_PARAMS_OFFSET, nullable)
        client_message.add_frame(initial_frame)

        VarSizedEncoder.encode_var_sized_frames(var_sized_params, client_message, nullable)
        return client_message

    @staticmethod
    def encode_response(response, nullable=False):
        params = response.get("params", [])
        fix_sized_params = fixed_params(params)
        var_sized_params = var_size_params(params)

        client_message = ClientMessage()

        initial_frame = FixSizedEncoder.create_initial_frame(fix_sized_params, response["id"],
                                                             RESPONSE_FIX_SIZED_PARAMS_OFFSET, nullable)
        client_message.add_frame(initial_frame)

        VarSizedEncoder.encode_var_sized_frames(var_sized_params, client_message, nullable)
        return client_message

    @staticmethod
    def encode_event(event, nullable=False):
        params = event.get("params", [])
        fix_sized_params = fixed_params(params)
        var_sized_params = var_size_params(params)

        client_message = ClientMessage()

        initial_frame = FixSizedEncoder.create_initial_frame(fix_sized_params, event["id"],
                                                             EVENT_FIX_SIZED_PARAMS_OFFSET, nullable)
        initial_frame.flags |= IS_EVENT_FLAG
        client_message.add_frame(initial_frame)

        VarSizedEncoder.encode_var_sized_frames(var_sized_params, client_message, nullable)
        return client_message


class FixSizedEncoder:
    @staticmethod
    def create_initial_frame(fix_sized_params, message_id, offset, nullable=False):
        frame_size = sum([sizes[p["type"]] for p in fix_sized_params])
        frame = bytearray(offset + frame_size)
        struct.pack_into(formats['int'], frame, TYPE_FIELD_OFFSET, message_id)
        for param in fix_sized_params:
            FixSizedEncoder.pack_into(frame, offset, param["type"], nullable=nullable and param["nullable"])
            offset += sizes[param["type"]]

        return Frame(frame, UNFRAGMENTED_MESSAGE)

    @staticmethod
    def encode_fix_sized_entry_list_frame(client_message, key_type, value_type):
        entry_size = sizes[key_type] + sizes[value_type]
        obj = reference_objects.map_objects[key_type][value_type]
        content = bytearray(entry_size * len(obj))
        offset = 0
        for key in obj:
            FixSizedEncoder.pack_into(content, offset, key_type, key)
            offset += sizes[key_type]
            FixSizedEncoder.pack_into(content, offset, value_type, obj[key])
            offset += sizes[value_type]
        client_message.add_frame(Frame(content))

    @staticmethod
    def encode_fix_sized_list_frame(client_message, item_type):
        obj = reference_objects.list_objects[item_type]
        content = bytearray(sizes[item_type] * len(obj))
        offset = 0
        for item in obj:
            FixSizedEncoder.pack_into(content, offset, item_type, item)
        client_message.add_frame(Frame(content))

    @staticmethod
    def pack_into(buffer, offset, type, value=None, nullable=False):
        val = reference_objects.objects[type] if value is None else value
        if type == 'UUID':
            struct.pack_into(formats["boolean"], buffer, offset, nullable)
            if nullable:
                return
            offset += sizes["boolean"]
            struct.pack_into(formats["long"], buffer, offset, val.most_sig_bits)
            offset += sizes["long"]
            struct.pack_into(formats["long"], buffer, offset, val.least_sig_bits)
        else:
            struct.pack_into(formats[type], buffer, offset, val)


class CustomTypeEncoder:
    @staticmethod
    def encode_custom_type(client_message, type, nullable=False):
        if nullable:
            client_message.add_frame(NULL_FRAME)
            return

        params = Encoder.CUSTOM_TYPE_PARAMS.get(type, [])

        fix_sized_params = fixed_params(params)
        var_sized_params = var_size_params(params)

        client_message.add_frame(BEGIN_FRAME)

        initial_frame = CustomTypeEncoder.create_initial_frame(fix_sized_params, nullable)
        if initial_frame is not None:
            client_message.add_frame(initial_frame)

        VarSizedEncoder.encode_var_sized_frames(var_sized_params, client_message, nullable)

        client_message.add_frame(END_FRAME)

    @staticmethod
    def create_initial_frame(fix_sized_params, nullable=False):
        frame_size = sum([sizes[p["type"]] for p in fix_sized_params])
        if frame_size == 0:
            return None
        frame = bytearray(frame_size)
        offset = 0
        for param in fix_sized_params:
            FixSizedEncoder.pack_into(frame, offset, param["type"], nullable=nullable and param["nullable"])
            offset += sizes[param["type"]]

        return Frame(frame, DEFAULT_FLAGS)

    @staticmethod
    def encoder_for(type, nullable=False):
        return lambda client_message: CustomTypeEncoder.encode_custom_type(client_message, type, nullable)


class VarSizedEncoder:
    @staticmethod
    def encode_var_sized_frames(var_sized_params, client_message, nullable=False):
        for param in var_sized_params:
            type = param['type']
            VarSizedEncoder.encode_var_sized_frame(client_message, type, nullable and param["nullable"])

    @staticmethod
    def encode_var_sized_frame(client_message, type, nullable=False):
        if nullable:
            client_message.add_frame(NULL_FRAME)
            return
        if is_var_sized_list(type) or is_var_sized_list_contains_nullable(type):
            item_type = type.split('_', 1)[1]
            VarSizedEncoder.encode_multi_frame_list(client_message, VarSizedEncoder.encoder_for(item_type))
        elif is_var_sized_map(type) or is_var_sized_entry_list(type):
            key_type = type.split('_', 2)[1]
            value_type = type.split('_', 2)[2]
            VarSizedEncoder.encode_multi_frame_map(client_message, VarSizedEncoder.encoder_for(key_type),
                                                   VarSizedEncoder.encoder_for(value_type))
        else:
            VarSizedEncoder.encoder_for(type)(client_message)

    @staticmethod
    def encode_multi_frame_list(client_message, encoder):
        client_message.add_frame(BEGIN_FRAME)

        encoder(client_message)

        client_message.add_frame(END_FRAME)

    @staticmethod
    def encode_multi_frame_map(client_message, key_encoder, value_encoder):
        client_message.add_frame(BEGIN_FRAME)

        key_encoder(client_message)
        value_encoder(client_message)

        client_message.add_frame(END_FRAME)

    @staticmethod
    def encode_byte_array_frame(client_message):
        client_message.add_frame(Frame(reference_objects.BYTEARRAY))

    @staticmethod
    def encode_long_array_frame(client_message):
        content = bytearray(len(reference_objects.LONGARRAY) * LONG_SIZE_IN_BYTES)
        offset = 0
        for l in reference_objects.LONGARRAY:
            struct.pack_into(formats["long"], content, offset, l)
            offset += LONG_SIZE_IN_BYTES

        client_message.add_frame(Frame(content))

    @staticmethod
    def encode_string_frame(client_message, value=None):
        if value is None:
            value = reference_objects.STRING
        client_message.add_frame(Frame(value.encode('utf-8')))

    @staticmethod
    def encode_data_frame(client_message):
        client_message.add_frame(Frame(reference_objects.DATA))

    @staticmethod
    def encode_long_byte_array_entry_list(client_message):
        client_message.add_frame(BEGIN_FRAME)
        VarSizedEncoder.encode_byte_array_frame(client_message)
        client_message.add_frame(END_FRAME)
        FixSizedEncoder.encode_fix_sized_list_frame(client_message, 'long')

    @staticmethod
    def encoder_for(type):
        encoder = VarSizedEncoder.encoders.get(type, None)
        if encoder is not None:
            return encoder
        if (type in CustomTypes) or (type in CustomConfigTypes):
            return CustomTypeEncoder.encoder_for(type)


VarSizedEncoder.encoders = {
    'byteArray': VarSizedEncoder.encode_byte_array_frame,
    'longArray': VarSizedEncoder.encode_long_array_frame,
    'String': VarSizedEncoder.encode_string_frame,
    'Data': VarSizedEncoder.encode_data_frame,
    'EntryList_Integer_UUID': functools.partial(FixSizedEncoder.encode_fix_sized_entry_list_frame,
                                                key_type='int', value_type='UUID'),
    'EntryList_UUID_Long': functools.partial(FixSizedEncoder.encode_fix_sized_entry_list_frame,
                                             key_type='UUID', value_type='long'),
    'EntryList_Integer_Long': functools.partial(FixSizedEncoder.encode_fix_sized_entry_list_frame,
                                                key_type='int', value_type='long'),
    'EntryList_Long_byteArray': VarSizedEncoder.encode_long_byte_array_entry_list,
    'List_Integer': functools.partial(FixSizedEncoder.encode_fix_sized_list_frame, item_type='int'),
    'List_Long': functools.partial(FixSizedEncoder.encode_fix_sized_list_frame, item_type='long'),
    'List_UUID': functools.partial(FixSizedEncoder.encode_fix_sized_list_frame, item_type='UUID'),
    'List_ScheduledTaskHandler': functools.partial(VarSizedEncoder.encode_multi_frame_list,
                                                   encoder=CustomTypeEncoder.encoder_for('ScheduledTaskHandler'))
}

test_output_directories = {
    SupportedLanguages.JAVA: 'hazelcast/src/test/java/com/hazelcast/client/protocol/compatibility',
    # SupportedLanguages.CPP: '',
    # SupportedLanguages.CS: '',
    # SupportedLanguages.PY: '',
    # SupportedLanguages.TS: '',
    # SupportedLanguages.GO: '',
}

binary_output_directories = {
    SupportedLanguages.JAVA: 'hazelcast/src/test/resources',
    # SupportedLanguages.CPP: '',
    # SupportedLanguages.CS: '',
    # SupportedLanguages.PY: '',
    # SupportedLanguages.TS: '',
    # SupportedLanguages.GO: '',
}

reference_objects_dict = {
    'boolean': 'aBoolean',
    'byte': 'aByte',
    'int': 'anInt',
    'long': 'aLong',
    'UUID': 'aUUID',
    'byteArray': 'aByteArray',
    'longArray': 'aLongArray',
    'String': 'aString',
    'Data': 'aData',
    'EntryList_Integer_UUID': 'aListOfIntegerToUUID',
    'EntryList_UUID_Long': 'aListOfUuidToLong',
    'EntryList_Integer_Long': 'aListOfIntegerToLong',
    'List_Integer': 'aListOfIntegers',
    'List_Long': 'aListOfLongs',
    'List_UUID': 'aListOfUUIDs',
    'Address': 'anAddress',
    'CacheEventData': 'aCacheEventData',
    'DistributedObjectInfo': 'aDistributedObjectInfo',
    'Member': 'aMember',
    'QueryCacheEventData': 'aQueryCacheEventData',
    'RaftGroupId': 'aRaftGroupId',
    'ScheduledTaskHandler': 'aScheduledTaskHandler',
    'SimpleEntryView': 'aSimpleEntryView',
    'WanReplicationRef': 'aWanReplicationRef',
    'Xid': 'anXid',
    'ErrorHolder': 'anErrorHolder',
    'StackTraceElement': 'aStackTraceElement',
    'CacheSimpleEntryListenerConfig': 'aCacheSimpleEntryListenerConfig',
    'EventJournalConfig': 'anEventJournalConfig',
    'EvictionConfigHolder': 'anEvictionConfigHolder',
    'HotRestartConfig': 'aHotRestartConfig',
    'ListenerConfigHolder': 'aListenerConfigHolder',
    'AttributeConfig': 'aAttributeConfig',
    'IndexConfig': 'anIndexConfig',
    'MapStoreConfigHolder': 'aMapStoreConfigHolder',
    'MerkleTreeConfig': 'aMerkleTreeConfig',
    'NearCacheConfigHolder': 'aNearCacheConfigHolder',
    'NearCachePreloaderConfig': 'aNearCachePreloaderConfig',
    'PredicateConfigHolder': 'aPredicateConfigHolder',
    'QueryCacheConfigHolder': 'aQueryCacheConfigHolder',
    'QueueStoreConfigHolder': 'aQueueStoreConfigHolder',
    'RingbufferStoreConfigHolder': 'aRingbufferStoreConfigHolder',
    'TimedExpiryPolicyFactoryConfig': 'aTimedExpiryPolicyFactoryConfig',
    'DurationConfig': 'aDurationConfig',
    'ClientBwListEntry': 'aClientBwListEntry',
    'EntryList_String_String': 'aListOfStringToString',
    'EntryList_String_byteArray': 'aListOfStringToByteArray',
    'EntryList_Long_byteArray': 'aListOfLongToByteArray',
    'EntryList_String_EntryList_Integer_Long': 'aListOfStringToListOfIntegerToLong',
    'EntryList_Address_List_Integer': 'aListOfAddressToListOfIntegers',
    'EntryList_Data_Data': 'aListOfDataToData',
    'EntryList_Member_List_ScheduledTaskHandler': 'aListOfMemberToListOfScheduledTaskHandlers',
    'Map_String_String': 'aMapOfStringToString',
    'List_Address': 'aListOfAddresses',
    'List_byteArray': 'aListOfByteArrays',
    'List_CacheEventData': 'aListOfCacheEventData',
    'List_CacheSimpleEntryListenerConfig': 'aListOfCacheSimpleEntryListenerConfigs',
    'List_Data': 'aListOfData',
    'ListCN_Data': 'aListOfData',
    'List_DistributedObjectInfo': 'aListOfDistributedObjectInfo',
    'List_ListenerConfigHolder': 'aListOfListenerConfigHolders',
    'List_AttributeConfig': 'aListOfAttributeConfigs',
    'List_IndexConfig': 'aListOfIndexConfigs',
    'List_Member': 'aListOfMembers',
    'List_MemberInfo': 'aListOfMemberInfos',
    'List_QueryCacheConfigHolder': 'aListOfQueryCacheConfigHolders',
    'List_QueryCacheEventData': 'aListOfQueryCacheEventData',
    'List_ScheduledTaskHandler': 'aListOfScheduledTaskHandler',
    'List_String': 'aListOfStrings',
    'List_Xid': 'aListOfXids',
    'List_StackTraceElement': 'aListOfStackTraceElements',
    'List_ClientBwListEntry': 'aListOfClientBwListEntries',
    'MergePolicyConfig': 'aMergePolicyConfig',
    'CacheConfigHolder': 'aCacheConfigHolder',
}


def create_environment_for_binary_generator(lang, version):
    env = Environment(loader=PackageLoader(lang.value + '.binary', '.'))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.keep_trailing_newline = False
    env.filters['capital'] = capital
    env.globals['lang_types_encode'] = language_specific_funcs['lang_types_encode'][lang]
    env.globals['protocol_version'] = version
    env.globals['reference_objects_dict'] = reference_objects_dict
    return env


binary_test_names = {
    SupportedLanguages.JAVA: lambda version: '{type}Compatibility{null}Test_' + '_'.join(version.split('.')) + '.java',
    # SupportedLanguages.CPP: '',
    # SupportedLanguages.CS: '',
    # SupportedLanguages.PY: '',
    # SupportedLanguages.TS: '',
    # SupportedLanguages.GO: '',
}
