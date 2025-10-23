import unittest
from collections import namedtuple

from go.generator import merge_dict


class GoGeneratorTestCase(unittest.TestCase):

    def test_merge_dict(self):
        case = namedtuple("case", ["msg", "a", "b", "target"])
        test_cases = [
            # case(
            #     msg="a and b are empty",
            #     a={},
            #     b={},
            #     target={},
            # ),
            # case(
            #     msg="only a is empty",
            #     a={},
            #     b={"k1": "v1"},
            #     target={"k1": "v1"},
            # ),
            # case(
            #     msg="only b is empty",
            #     a={"k1": "v1"},
            #     b={},
            #     target={"k1": "v1"},
            # ),
            # case(
            #     msg="both a and b are simple dicts",
            #     a={"ka1": "va1", "k1": "v1"},
            #     b={"kb1": "vb1", "k1": "v2"},
            #     target={"ka1": "va1", "kb1": "vb1", "k1": "v2"}
            # ),
            # case(
            #     msg="a is nested dict, b is simple dict",
            #     a={"ka1": "va1", "k1": {"ka21", "va21"}},
            #     b={"kb1": "vb1", "k1": "v2"},
            #     target={"ka1": "va1", "kb1": "vb1", "k1": "v2"}
            # ),
            # case(
            #     msg="a is simple dict, b is nested dict",
            #     a={"ka1": "va1", "k1": "v1"},
            #     b={"kb1": "vb1", "k1": {"kb21", "vb21"}},
            #     target={"ka1": "va1", "kb1": "vb1", "k1": {"kb21", "vb21"}}
            # ),
            # case(
            #     msg="both a and be are non-overlapping nested dicts",
            #     a={"ka1": "va1", "ka2": {"ka21", "va21"}, "k1": "v1"},
            #     b={"kb1": "vb1", "kb2": {"kb21", "vb21"}, "k1": "v1"},
            #     target={"ka1": "va1", "ka2": {"ka21", "va21"}, "kb2": {"kb21", "vb21"}, "kb1": "vb1", "k1": "v1"}
            # ),
            case(
                msg="both a and be are overlapping nested dicts",
                a={"k2": {"k21": "va21", "ka21": "va21"}},
                b={"k2": {"k21": "vb21", "kb21": "vb21"}},
                target={"k2": {"k21": "vb21", "ka21": "va21", "kb21": "vb21"}}
            ),
            case(
                msg="",
                a={
                    "builtin": [
                        "ByteArrayCodec", "CodecUtil", "DataCodec",
                    ],
                    "public": {
                        "cluster": ["Address", "EndpointQualifier", "MemberInfo", "MemberVersion"],
                        "sql": ["ListSqlColumnMetadata", "SqlColumnMetadata"],
                        "types": [
                            "BitmapIndexOptions", "DistributedObjectInfo", "IndexConfig",
                            "SimpleEntryView", "UUID"
                        ],
                    },
                    "internal": {
                        "hzerrors": ["StackTraceElement"],
                        "serialization": ["Data"],
                        "sql": ["Error",  "Page", "QueryID"]
                    }
                },
                b={
                    "public": {
                        "control": ["EventJournalConfig"]
                    }
                },
                target={
                    "builtin": [
                        "ByteArrayCodec", "CodecUtil", "DataCodec",
                    ],
                    "public": {
                        "cluster": ["Address", "EndpointQualifier", "MemberInfo", "MemberVersion"],
                        "control": ["EventJournalConfig"],
                        "sql": ["ListSqlColumnMetadata", "SqlColumnMetadata"],
                        "types": [
                            "BitmapIndexOptions", "DistributedObjectInfo", "IndexConfig",
                            "SimpleEntryView", "UUID"
                        ],
                    },
                    "internal": {
                        "hzerrors": ["StackTraceElement"],
                        "serialization": ["Data"],
                        "sql": ["Error",  "Page", "QueryID"]
                    }
                }
            )
        ]
        for case in test_cases:
            with self.subTest(msg=case.msg):
                merge_dict(case.a, case.b)
                self.assertEqual(case.a, case.target)


if __name__ == '__main__':
    unittest.main()
