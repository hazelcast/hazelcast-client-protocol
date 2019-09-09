BOOLEAN = True

BYTE = 113

INT = 25

LONG = -50992225


class UuidHolder:
    def __init__(self, most_sig_bits, least_sig_bits):
        self.most_sig_bits = most_sig_bits
        self.least_sig_bits = least_sig_bits


UUID = UuidHolder(123456789, 987654321)

BYTEARRAY = bytearray([BYTE])

LONGARRAY = [LONG]

STRING = "localhost"

DATA = b'111313123131313131'

ENUM_INT_CACHE_EVENT_TYPE = 1

ENUM_STRING_TIMEUNIT = 'SECONDS'

ENUM_STRING_EXPIRY_POLICY_TYPE = 'CREATED'

objects = {
    'boolean': BOOLEAN,
    'byte': BYTE,
    'int': INT,
    'long': LONG,
    'UUID': UUID,
    'byteArray': BYTEARRAY,
    'longArray': LONGARRAY,
    'String': STRING,
    'Data': DATA,
    'Enum_int_CacheEventType': ENUM_INT_CACHE_EVENT_TYPE,
    'Enum_String_TimeUnit': ENUM_STRING_TIMEUNIT,
    'Enum_String_ExpiryPolicyType': ENUM_STRING_EXPIRY_POLICY_TYPE
}

map_objects = {
    'int': {
        'UUID': {
            INT: UUID
        },
        'long': {
            INT: LONG
        }
    },
    'UUID': {
        'long': {
            UUID: LONG
        }
    }
}

list_objects = {
    'int': [INT],
    'long': [LONG],
    'UUID': [UUID]
}
