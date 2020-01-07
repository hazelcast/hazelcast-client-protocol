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

ENUM = 1

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
    'enum': ENUM
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
        }
    }
}

list_objects = {
    'int': [INT],
    'long': [LONG],
    'UUID': [UUID]
}
