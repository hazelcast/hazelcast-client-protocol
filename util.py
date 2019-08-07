import os
import yaml
import re
from jinja2 import Environment, PackageLoader
from java import java_types_encode, java_types_decode
from enum import Enum
import json, jsonschema

FixedLengthTypes = [
    "boolean",
    "byte",
    "int",
    "long",
    "UUID"
]

FixedMapTypes = [
    'Map_Integer_UUID',
    'Map_String_Long',
    'Map_Integer_Long'
]

FixedListTypes = [
    'List_Integer',
    'List_Long',
    'List_UUID'
]


def java_name(type_name):
    return "".join([capital(part) for part in type_name.replace("(", "").replace(")", "").split("_")])


def is_fixed_type(param):
    return param["type"] in FixedLengthTypes


def capital(txt):
    return txt[0].capitalize() + txt[1:]


def to_upper_snake_case(camel_case_str):
    return re.sub('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', camel_case_str).upper()
    # s1 = re.sub('(.)([A-Z]+[a-z]+)', r'\1_\2', camel_case_str)
    # return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()


def fixed_params(params):
    return [p for p in params if is_fixed_type(p)]


def var_size_params(params):
    return [p for p in params if not is_fixed_type(p)]


def generate_codecs(services, template, output_dir, extension):
    for service in services:
        if "methods" in service:
            methods = service["methods"]
            if methods is None:
                print(type(methods))
            for method in service["methods"]:
                content = template.render(service_name=service["name"], method=method)
                save_file(output_dir + capital(service["name"]) + capital(method["name"]) + 'Codec.' + extension, content)


def item_type(lang_name, param_type):
    if param_type.startswith("List_") or param_type.startswith("ListCN_"):
        return lang_name(param_type.split('_', 1)[1])


def key_type(lang_name, param_type):
    if param_type.startswith("Map_"):
        return lang_name(param_type.split('_', 2)[1])


def value_type(lang_name, param_type):
    if param_type.startswith("Map_"):
        return lang_name(param_type.split('_', 2)[2])


def is_var_sized_list(param_type):
    return param_type.startswith("List_") and param_type not in FixedListTypes


def is_var_sized_list_contains_nullable(param_type):
    return param_type.startswith("ListCN_") and param_type not in FixedListTypes


def is_var_sized_map(param_type):
    return param_type.startswith("Map_") and param_type not in FixedMapTypes


def load_services(protocol_def_dir):
    service_list = os.listdir(protocol_def_dir)
    services = []
    for service_file in service_list:
        with open(protocol_def_dir + service_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.Loader)
            services.append(data)
    return services


def validate_services(services, schema_path):
    valid = True
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
        for service in services:
            try:
                jsonschema.validate(service, schema)
            except jsonschema.ValidationError as e:
                print("Validation error: %s. schema:%s" % (e.message, list(e.relative_schema_path)))
                valid = False
    return valid


def save_file(file, content):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as file:
        file.writelines(content)


class SupportedLanguages(Enum):
    JAVA = 'java'
    # CPP = 'cpp'
    # CS = 'cs'
    # PY = 'py'
    # TS = 'ts'
    # GO = 'go'


output_directories = {
    SupportedLanguages.JAVA: '/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/',
    # SupportedLanguages.CPP: '/hazelcast/generated-sources/src/hazelcast/client/protocol/codec/',
    # SupportedLanguages.CS: '/Hazelcast.Net/Hazelcast.Client.Protocol.Codec/',
    # SupportedLanguages.PY: '/hazelcast/protocol/codec/',
    # SupportedLanguages.TS: '/src/codec/',
    # SupportedLanguages.GO: '/internal/proto/'
}

file_extensions = {
    SupportedLanguages.JAVA: 'java',
    # SupportedLanguages.CPP: 'cpp',  # TODO header files ?
    # SupportedLanguages.CS: 'cs',
    # SupportedLanguages.PY: 'py',
    # SupportedLanguages.TS: 'ts',
    # SupportedLanguages.GO: 'go'
}

language_specific_funcs = {
    'lang_types_encode': {
        SupportedLanguages.JAVA: java_types_encode
    },
    'lang_types_decode': {
        SupportedLanguages.JAVA: java_types_decode
    },
    'lang_name': {
        SupportedLanguages.JAVA: java_name
    }
}


def create_environment(lang):
    env = Environment(loader=PackageLoader(lang.value, '.'))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.keep_trailing_newline = False
    env.filters["capital"] = capital
    env.globals["to_upper_snake_case"] = to_upper_snake_case
    env.globals["fixed_params"] = fixed_params
    env.globals["var_size_params"] = var_size_params
    env.globals["is_var_sized_list"] = is_var_sized_list
    env.globals["is_var_sized_list_contains_nullable"] = is_var_sized_list_contains_nullable
    env.globals["is_var_sized_map"] = is_var_sized_map
    env.globals["item_type"] = item_type
    env.globals["key_type"] = key_type
    env.globals["value_type"] = value_type
    env.globals["lang_types_encode"] = language_specific_funcs['lang_types_encode'][lang]
    env.globals["lang_types_decode"] = language_specific_funcs['lang_types_decode'][lang]
    env.globals["lang_name"] = language_specific_funcs['lang_name'][lang]

    return env
