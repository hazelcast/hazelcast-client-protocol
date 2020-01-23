import struct

from binary import *
from binary.constants import *
from functools import partial
from util import *
from . import reference_objects

formats = {
    'boolean': '<?',
    'byte': '<B',
    'int': '<I',
    'long': '<q',
    'short': '<H',
}

sizes = {
    'boolean': BOOLEAN_SIZE_IN_BYTES,
    'byte': BYTE_SIZE_IN_BYTES,
    'int': INT_SIZE_IN_BYTES,
    'long': LONG_SIZE_IN_BYTES,
    'UUID': UUID_SIZE_IN_BYTES,
}

id_fmt = '0x%02x%02x%02x'


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
    custom_types = definitions['customTypes']
    for definition in custom_types:
        params[definition['name']] = definition['params']
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
            is_last_frame = i == (n - 1)
            file.write(frame.encode_frame(is_last_frame))


class Encoder:
    def __init__(self, protocol_defs_path):
        self.custom_type_params = get_custom_type_params(protocol_defs_path)
        self.custom_type_encoder = CustomTypeEncoder(self, self.custom_type_params)
        self.var_sized_encoder = VarSizedParamEncoder(self)

    def encode(self, message_def, fix_sized_params_offset, set_partition_id=False, is_event=False, is_null_test=False):
        params = message_def.get('params', [])
        fix_sized_params = fixed_params(params)
        var_sized_params = var_size_params(params)

        client_message = ClientMessage()
        initial_frame = FixSizedParamEncoder.create_initial_frame(fix_sized_params, message_def['id'],
                                                                  fix_sized_params_offset, set_partition_id,
                                                                  is_null_test)
        if is_event:
            initial_frame.flags |= IS_EVENT_FLAG
        client_message.add_frame(initial_frame)

        self.var_sized_encoder.encode_var_sized_frames(var_sized_params, client_message, is_null_test)
        return client_message


class FixSizedParamEncoder:
    @staticmethod
    def create_initial_frame(fix_sized_params, message_id, offset, set_partition_id, is_null_test=False):
        content_size = sum([sizes[p['type']] for p in fix_sized_params])
        content = bytearray(offset + content_size)
        struct.pack_into(formats['int'], content, TYPE_FIELD_OFFSET, message_id)
        if set_partition_id:
            struct.pack_into(formats['int'], content, PARTITION_ID_FIELD_OFFSET, -1 & 0xffffffff)
        for param in fix_sized_params:
            value = reference_objects.objects.get(param['type'])
            FixSizedParamEncoder.pack_into(content, offset, param['type'], value, is_null_test and param['nullable'])
            offset += sizes[param['type']]

        return Frame(content, UNFRAGMENTED_MESSAGE)

    @staticmethod
    def encode_fix_sized_entry_list_frame(client_message, key_type, value_type):
        entry_size = sizes[key_type] + sizes[value_type]
        obj = reference_objects.map_objects[key_type][value_type]
        content = bytearray(entry_size * len(obj))
        offset = 0
        for key in obj:
            FixSizedParamEncoder.pack_into(content, offset, key_type, key)
            offset += sizes[key_type]
            FixSizedParamEncoder.pack_into(content, offset, value_type, obj[key])
            offset += sizes[value_type]
        client_message.add_frame(Frame(content))

    @staticmethod
    def encode_fix_sized_list_frame(client_message, item_type):
        obj = reference_objects.list_objects[item_type]
        content = bytearray(sizes[item_type] * len(obj))
        offset = 0
        for item in obj:
            FixSizedParamEncoder.pack_into(content, offset, item_type, item)
            offset += sizes[item_type]
        client_message.add_frame(Frame(content))

    @staticmethod
    def pack_into(buffer, offset, type, value, should_be_null=False):
        if type == 'UUID':
            struct.pack_into(formats['boolean'], buffer, offset, should_be_null)
            if should_be_null:
                return
            offset += sizes['boolean']
            struct.pack_into(formats['long'], buffer, offset, value.most_sig_bits)
            offset += sizes['long']
            struct.pack_into(formats['long'], buffer, offset, value.least_sig_bits)
        else:
            struct.pack_into(formats[type], buffer, offset, value)


class CustomTypeEncoder:
    def __init__(self, encoder, custom_type_params):
        self.encoder = encoder
        self.custom_type_params = custom_type_params

    def encode_custom_type(self, client_message, custom_type_name, is_null_test=False):
        if is_null_test:
            client_message.add_frame(NULL_FRAME)
            return

        params = self.custom_type_params.get(custom_type_name, [])

        fix_sized_params = fixed_params(params)
        var_sized_params = var_size_params(params)

        client_message.add_frame(BEGIN_FRAME)

        initial_frame = self.create_initial_frame(custom_type_name, fix_sized_params)
        if initial_frame is not None:
            client_message.add_frame(initial_frame)

        self.encoder.var_sized_encoder.encode_var_sized_frames(var_sized_params, client_message)

        client_message.add_frame(END_FRAME)

    @staticmethod
    def create_initial_frame(custom_type_name, fix_sized_params):
        content_size = sum([sizes[p['type']] for p in fix_sized_params])
        if content_size == 0:
            return None

        content = bytearray(content_size)
        offset = 0

        specific_values = reference_objects.objects.get(custom_type_name, None)
        for param in fix_sized_params:
            specific_value = specific_values.get(param['name'], None) if specific_values is not None else None
            value = specific_value if specific_value is not None else reference_objects.objects.get(param['type'])
            FixSizedParamEncoder.pack_into(content, offset, param['type'], value)
            offset += sizes[param['type']]

        return Frame(content)

    def encoder_for(self, param_type, is_null_test=False):
        return lambda client_message: self.encode_custom_type(client_message, param_type, is_null_test)


class VarSizedParamEncoder:
    def __init__(self, encoder):
        self.encoder = encoder
        self.var_sized_encoders = {
            'byteArray': self.encode_byte_array_frame,
            'longArray': self.encode_long_array_frame,
            'String': self.encode_string_frame,
            'Data': self.encode_data_frame,
            'EntryList_Integer_UUID': partial(FixSizedParamEncoder.encode_fix_sized_entry_list_frame,
                                              key_type='int', value_type='UUID'),
            'EntryList_UUID_Long': partial(FixSizedParamEncoder.encode_fix_sized_entry_list_frame,
                                           key_type='UUID', value_type='long'),
            'EntryList_Integer_Long': partial(FixSizedParamEncoder.encode_fix_sized_entry_list_frame,
                                              key_type='int', value_type='long'),
            'EntryList_Integer_Integer': partial(FixSizedParamEncoder.encode_fix_sized_entry_list_frame,
                                                 key_type='int', value_type='int'),
            'EntryList_Long_byteArray': self.encode_long_byte_array_entry_list,
            'EntryList_UUID_Address': self.encode_uuid_address_entry_list,
            'EntryList_UUID_List_Integer': self.encode_uuid_integer_list_entry_list,
            'List_Integer': partial(FixSizedParamEncoder.encode_fix_sized_list_frame, item_type='int'),
            'List_Long': partial(FixSizedParamEncoder.encode_fix_sized_list_frame, item_type='long'),
            'List_UUID': partial(FixSizedParamEncoder.encode_fix_sized_list_frame, item_type='UUID'),
            'List_ScheduledTaskHandler': partial(self.encode_multi_frame_list, encoder=self.encoder.custom_type_encoder
                                                 .encoder_for('ScheduledTaskHandler'))
        }

    def encode_var_sized_frames(self, var_sized_params, client_message, is_null_test=False):
        for param in var_sized_params:
            param_type = param['type']
            self.encode_var_sized_frame(client_message, param_type, is_null_test and param['nullable'])

    def encode_var_sized_frame(self, client_message, param_type, nullable=False):
        if nullable:
            client_message.add_frame(NULL_FRAME)
            return

        if is_var_sized_list(param_type) or is_var_sized_list_contains_nullable(param_type):
            item_type = param_type.split('_', 1)[1]
            self.encode_multi_frame_list(client_message, self.encoder_for(item_type))
        elif is_var_sized_map(param_type) or is_var_sized_entry_list(param_type):
            key_type = param_type.split('_', 2)[1]
            value_type = param_type.split('_', 2)[2]
            self.encode_multi_frame_map(client_message, self.encoder_for(key_type), self.encoder_for(value_type))
        else:
            self.encoder_for(param_type)(client_message)

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
        for item in reference_objects.LONGARRAY:
            struct.pack_into(formats['long'], content, offset, item)
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
        VarSizedParamEncoder.encode_byte_array_frame(client_message)
        client_message.add_frame(END_FRAME)
        FixSizedParamEncoder.encode_fix_sized_list_frame(client_message, 'long')

    def encode_uuid_address_entry_list(self, client_message):
        client_message.add_frame(BEGIN_FRAME)
        self.encoder.custom_type_encoder.encode_custom_type(client_message, 'Address')
        client_message.add_frame(END_FRAME)
        FixSizedParamEncoder.encode_fix_sized_list_frame(client_message, 'UUID')

    def encode_uuid_integer_list_entry_list(self, client_message):
        client_message.add_frame(BEGIN_FRAME)
        self.encode_var_sized_frame(client_message, 'List_Integer')
        client_message.add_frame(END_FRAME)
        FixSizedParamEncoder.encode_fix_sized_list_frame(client_message, 'UUID')

    def encoder_for(self, param_type):
        encoder = self.var_sized_encoders.get(param_type, None)
        if encoder is not None:
            return encoder
        if (param_type in CustomTypes) or (param_type in CustomConfigTypes):
            return self.encoder.custom_type_encoder.encoder_for(param_type)


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
    'EntryList_Integer_Integer': 'aListOfIntegerToInteger',
    'List_Integer': 'aListOfIntegers',
    'List_Long': 'aListOfLongs',
    'List_UUID': 'aListOfUUIDs',
    'Address': 'anAddress',
    'CacheEventData': 'aCacheEventData',
    'DistributedObjectInfo': 'aDistributedObjectInfo',
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
    'MCEvent': 'aMCEvent',
    'EntryList_String_String': 'aListOfStringToString',
    'EntryList_String_byteArray': 'aListOfStringToByteArray',
    'EntryList_Long_byteArray': 'aListOfLongToByteArray',
    'EntryList_String_EntryList_Integer_Long': 'aListOfStringToListOfIntegerToLong',
    'EntryList_UUID_Address': 'aListOfUUIDToAddress',
    'EntryList_UUID_List_Integer': 'aListOfUUIDToListOfIntegers',
    'EntryList_Data_Data': 'aListOfDataToData',
    'Map_String_String': 'aMapOfStringToString',
    'List_byteArray': 'aListOfByteArrays',
    'List_CacheEventData': 'aListOfCacheEventData',
    'List_CacheSimpleEntryListenerConfig': 'aListOfCacheSimpleEntryListenerConfigs',
    'List_Data': 'aListOfData',
    'ListCN_Data': 'aListOfData',
    'List_DistributedObjectInfo': 'aListOfDistributedObjectInfo',
    'List_ListenerConfigHolder': 'aListOfListenerConfigHolders',
    'List_AttributeConfig': 'aListOfAttributeConfigs',
    'List_IndexConfig': 'aListOfIndexConfigs',
    'List_MemberInfo': 'aListOfMemberInfos',
    'List_QueryCacheConfigHolder': 'aListOfQueryCacheConfigHolders',
    'List_QueryCacheEventData': 'aListOfQueryCacheEventData',
    'List_ScheduledTaskHandler': 'aListOfScheduledTaskHandler',
    'List_String': 'aListOfStrings',
    'List_Xid': 'aListOfXids',
    'List_StackTraceElement': 'aListOfStackTraceElements',
    'List_ClientBwListEntry': 'aListOfClientBwListEntries',
    'List_MCEvent': 'aListOfMCEvents',
    'MergePolicyConfig': 'aMergePolicyConfig',
    'CacheConfigHolder': 'aCacheConfigHolder',
    'AnchorDataListHolder': 'anAnchorDataListHolder',
    'PagingPredicateHolder': 'aPagingPredicateHolder',
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
