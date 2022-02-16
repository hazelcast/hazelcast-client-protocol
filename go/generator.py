import hashlib
import json
import os
import fnmatch
from datetime import datetime

from jinja2 import Environment, PackageLoader

from cpp import get_size, is_trivial
from util import _snake_cased_name_generator, capital, to_upper_snake_case, is_var_sized_list_contains_nullable, \
    fixed_params, var_size_params, new_params, filter_new_params, is_var_sized_list, is_var_sized_entry_list, \
    is_var_sized_map, item_type, key_type, value_type, param_name, java_name
from .config import Config


class GoGenerator:

    filename_gen = _snake_cased_name_generator("go")

    def __init__(self, services, custom_protocol, output_dir, args):
        self.services = services
        self.custom_types = custom_protocol[0]["customTypes"]
        self.output_dir = output_dir
        self.args = args
        config_path = args.go_config
        self.extensibility = True
        if not config_path:
            config_path = os.path.join(current_path(), "config.json")
            self.extensibility = False
        self.config = self.load_config(config_path)
        self.mapping = DEFAULT_MAPPING.copy()
        if self.config.mapping:
            self.mapping.update(self.config.mapping)
        types = DEFAULT_TYPES.copy()
        merge_dict(types, self.config.types)
        self.types_encode = self.make_types_encode(DEFAULT_TYPES)
        self.types_decode = self.make_types_decode(DEFAULT_TYPES)
        self.env = self.make_environment()

    def generate(self):
        for service in self.services:
            self.generate_service(service)
        self.generate_types(self.custom_types)

    def generate_service(self, service):
        template = self.env.get_template("codec-template.j2")
        methods = service.get("methods")
        if methods is None:
            raise NotImplementedError(f"Methods not found for service {service}")
        for method in methods:
            self.generate_method(service, method, template)

    def generate_method(self, service, method, template):
        name = f"{service['name']}.{method['name']}"
        if not self.can_generate_method(name):
            return
        opts = {"base_import_path": self.config.base_import_path}
        method["request"]["id"] = self.make_id(service["id"], method["id"], 0)
        method["response"]["id"] = self.make_id(service["id"], method["id"], 1)
        for i, event in enumerate(method.get("events", [])):
            event["id"] = self.make_id(service["id"], method["id"], i + 2)
        codec_file_name = GoGenerator.filename_gen(service["name"], method["name"])
        try:
            content = template.render(service_name=service["name"], method=method, **opts)
            path = os.path.join(self.output_dir, codec_file_name)
            self.save(path, content)
        except NotImplementedError as e:
            print(f"{codec_file_name} contains missing type mapping so ignoring it. Error: {e}")

    def generate_types(self, codecs):
        template = self.env.get_template("custom-codec-template.j2")
        for codec in codecs:
            self.generate_type(codec, template)

    def generate_type(self, codec, template):
        if not self.can_generate_type(codec["name"]):
            return
        opts = {"base_import_path": self.config.base_import_path}
        codec_file_name = GoGenerator.filename_gen(codec["name"])
        print("Custom:", codec_file_name)
        content = template.render(codec=codec, **opts)
        path = os.path.join(self.output_dir, codec_file_name)
        self.save(path, content)

    def can_generate_method(self, method_name: str) -> bool:
        for filter in self.config.include_methods:
            if fnmatch.fnmatch(method_name.lower(), filter.lower()):
                return True
        return False

    def can_generate_type(self, type_name: str) -> bool:
        for filter in self.config.include_types:
            if fnmatch.fnmatch(type_name.lower(), filter.lower()):
                return True
        return False

    @classmethod
    def load_config(cls, path: str) -> Config:
        with open(path) as f:
            d = json.loads(f.read())
            return Config.from_json(d)

    @classmethod
    def render(cls, service, template, method, **opts):
        return template.render(service_name=service["name"], method=method, **opts)

    @classmethod
    def save(cls, path: str, content: str, mode="w"):
        m = hashlib.md5()
        m.update(content.encode("utf-8"))
        codec_hash = m.hexdigest()
        with open(path, mode, newline=os.linesep) as path:
            path.writelines(content.replace("!codec_hash!", codec_hash))

    @classmethod
    def make_id(cls, service_id, method_id, seq) -> int:
        return int(f"0x{service_id:02x}{method_id:02x}{seq:02x}", 16)

    def make_environment(self):
        env = Environment(
            loader=PackageLoader("go", current_path()),
            extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
        )
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.keep_trailing_newline = False
        env.filters["capital"] = capital
        env.globals["to_upper_snake_case"] = to_upper_snake_case
        env.globals["fixed_params"] = fixed_params
        env.globals["var_size_params"] = var_size_params
        env.globals["new_params"] = new_params
        env.globals["filter_new_params"] = filter_new_params
        env.globals["is_var_sized_list"] = is_var_sized_list
        env.globals["is_var_sized_list_contains_nullable"] = is_var_sized_list_contains_nullable
        env.globals["is_var_sized_entry_list"] = is_var_sized_entry_list
        env.globals["is_var_sized_map"] = is_var_sized_map
        env.globals["item_type"] = item_type
        env.globals["key_type"] = key_type
        env.globals["value_type"] = value_type
        env.globals["lang_types_encode"] = self.go_types_encode
        env.globals["lang_types_decode"] = self.go_types_decode
        env.globals["lang_name"] = java_name
        env.globals["param_name"] = param_name
        env.globals["escape_keyword"] = go_escape_keyword
        env.globals["get_size"] = get_size
        env.globals["is_trivial"] = is_trivial
        env.globals["get_import_path_holders"] = self.go_get_import_statements
        env.globals["augment_enum"] = go_augment_enum
        env.globals["rename_field"] = go_rename_field
        env.globals["copyright_year"] = datetime.now().year
        return env

    def make_import_stmts_mapping(self, types: dict) -> dict:
        bip = self.config.base_import_path
        stmts = {}
        for package, ts in types.get("public", {}).items():
            for t in ts:
                stmts[t] = f"/{package}"
        for package, ts in types.get("internal", {}).items():
            for t in ts:
                stmts[t] = f"/internal/{package}"
        for t, path in stmts.items():
            pp = path.split("/")
            package = pp[-1]
            alias = f"pub{package}"
            if "internal" in pp:
                alias = f"i{package}"
            stmts[t] = f'{alias} "{bip}{path}"'
        if self.extensibility:
            stmts["Data"] = 'iserialization "github.com/hazelcast/hazelcast-go-client"'
        return stmts

    def make_types_encode(self, types: dict):
        res = {}
        for package, ts in types.get("public", {}).items():
            for t in ts:
                res[t] = f"pub{package}.{t}"
        for package, ts in types.get("internal", {}).items():
            for t in ts:
                res[t] = f"i{package}.{t}"
        for from_type, to_type in self.mapping.items():
            res[from_type] = to_type
        # if self.extensibility:
        #     res["Data"] = "hazelcast.Data"
        return res

    make_types_decode = make_types_encode

    # def make_types_decode(self, types: dict):
    #     res = {}
    #     for package, ts in types.get("public", {}).items():
    #         for t in ts:
    #             res[t] = f"pub{package}.{t}"
    #     for package, ts in types.get("internal", {}).items():
    #         for t in ts:
    #             res[t] = f"i{package}.{t}"
    #     for from_type, to_type in self.config.mapping.items():
    #         res[from_type] = to_type
    #     if self.extensibility:
    #         res["Data"] = "hazelcast.Data"
    #     return res

    def go_get_import_statements(self, *args):
        import_map = self.make_import_stmts_mapping(DEFAULT_TYPES)
        import_statements = set()
        for arg in args:
            params = [arg] if isinstance(arg, str) else arg
            for param in params:
                type = param["type"] if isinstance(param, dict) else param
                import_stmt = import_map.get(type)
                if import_stmt is None:
                    # this may be a mapped type
                    mt = self.mapping.get(type)
                    if mt:
                        p = mt.split(".", 1)
                        if len(p) == 2:
                            import_stmt = import_map.get(p[1])
                if import_stmt:
                    import_statements.add(import_stmt)
                if not import_stmt:
                    continue
        # TODO: adapt the proto import path according to GOCE.
        if self.extensibility:
            import_statements.add('proto "github.com/hazelcast/hazelcast-go-client"')
        else:
            import_statements.add('"github.com/hazelcast/hazelcast-go-client/internal/proto"')
        # if args[0] == "SimpleEntryView":
        #     import_statements.remove('iserialization"github.com/hazelcast/hazelcast-go-client/internal/serialization"')
        return sorted(import_statements)

    def go_types_encode(self, key):
        try:
            return self.types_encode[key]
        except KeyError:
            raise NotImplementedError(f"Missing type mapping for '{key}'")

    def go_types_decode(self, key):
        try:
            return self.types_decode[key]
        except KeyError:
            raise NotImplementedError(f"Missing type mapping for '{key}'")


def current_path():
    return os.path.split(os.path.abspath(__file__))[0]


go_reserved_keywords = {"break", "default", "func", "interface", "select", "case", "defer", "go", "map", "struct",
                        "chan", "else", "goto", "package", "switch", "const", "fallthrough", "if", "range", "type",
                        "continue", "for", "import", "return", "var"}

DEFAULT_TYPES = {
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
}


_go_enum = {
    ("BitmapIndexOptions", "uniqueKeyTransformation"): "types.UniqueKeyTransformation",
    ("EndpointQualifier", "type"): "cluster.EndpointQualifierType",
    ("IndexConfig", "type"): "types.IndexType",
}

_go_field = {
    ("SimpleEntryView", "ttl"): "TTL",
    ("MemberInfo", "uuid"): "UUID",
}


def go_escape_keyword(value):
    if value not in go_reserved_keywords:
        return value
    return "_%s" % value


def go_augment_enum(codec, param):
    cast_type = _go_enum.get((codec, param["name"]))
    if cast_type:
        return "%s(%s)" % (cast_type, go_escape_keyword(param["name"]))
    return go_escape_keyword(param["name"])


def go_rename_field(codec, param):
    name = param["name"]
    field_name = _go_field.get((codec, name))
    if field_name:
        return field_name
    return "%s%s" % (name[0].upper(), name[1:])


def merge_dict(d1, d2: dict):
    root = d1
    for k, v in d2.items():
        if k in d1:
            if isinstance(d1[k], dict) and isinstance(v, dict):
                merge_dict(d1[k], v)
                continue
        root[k] = v


DEFAULT_MAPPING = {
    "boolean": "bool",
    "byte": "byte",
    "EntryList_Data_Data": "[]proto.Pair",
    "EntryList_Integer_Integer": "[]proto.Pair",
    "int": "int32",
    "ListCN_Data": "[]iserialization.Data",
    "List_Data": "[]iserialization.Data",
    "List_IndexConfig": "[]pubtypes.IndexConfig",
    "List_ListCN_Data": "[]iserialization.Data",
    "List_QueryCacheConfigHolder": "[]QueryCacheConfigHolder",
    "List_SqlColumnMetadata": "[]isql.ColumnMetadata",
    "long": "int64",
    "SqlError": "isql.Error",
    "SqlPage": "isql.Page",
    "SqlQueryId": "isql.QueryID",
    "String": "string",
}
