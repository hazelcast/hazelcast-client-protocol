class UuidHolder:
    def __init__(self, most_sig_bits, least_sig_bits):
        self.most_sig_bits = most_sig_bits
        self.least_sig_bits = least_sig_bits

BOOLEAN = True

BYTE = 113

INT = 25

LONG = -50992225

UUID = UuidHolder(123456789, 987654321)

BYTEARRAY = bytearray([BYTE])

LONGARRAY = [LONG]

STRING = "localhost"

DATA = b'111313123131313131'

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
    'DurationConfig': {
        'timeUnit': 1
    },
    'TimedExpiryPolicyFactoryConfig': {
        'expiryPolicyType': 1
    },
    'ClientBwListEntry': {
        'type': 1
    },
    'CacheEventData': {
        'cacheEventType': 1
    },
    'IndexConfig': {
        'type': 1
    }
}

map_objects = {
    'int': {
        'UUID': {
            INT: UUID
        },
        'long': {
            INT: LONG
        },
        'int': {
            INT: INT
        }
    },
    'UUID': {
        'long': {
            UUID: LONG
        },
        'UUID': {
            UUID: UUID
        }
    }
}

list_objects = {
    'int': [INT],
    'long': [LONG],
    'UUID': [UUID]
}
