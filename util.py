import hashlib
import json
import jsonschema
import os
import re
from enum import Enum
from yaml import MarkedYAMLError

import yaml
from jinja2 import Environment, PackageLoader

from binary import FixedLengthTypes, FixedListTypes, FixedEntryListTypes, FixedMapTypes
from java import java_types_encode, java_types_decode
from cs import cs_types_encode, cs_types_decode, cs_escape_keyword


def java_name(type_name):
    return "".join([capital(part) for part in type_name.replace("(", "").replace(")", "").split("_")])


def cs_name(type_name):
    return "".join([capital(part) for part in type_name.replace("(", "").replace(")", "").split("_")])


def param_name(type_name):
    return type_name[0].lower() + type_name[1:]


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
    os.makedirs(output_dir, exist_ok=True)
    id_fmt = "0x%02x%02x%02x"
    for service in services:
        if "methods" in service:
            methods = service["methods"]
            if methods is None:
                print(type(methods))
            for method in service["methods"]:
                method["request"]["id"] = int(id_fmt % (service["id"], method["id"], 0), 16)
                method["response"]["id"] = int(id_fmt % (service["id"], method["id"], 1), 16)
                events = method.get("events", None)
                if events is not None:
                    for i in range(len(events)):
                        method["events"][i]["id"] = int(id_fmt % (service["id"], method["id"], i + 2), 16)

                codec_file_name = capital(service["name"]) + capital(method["name"]) + 'Codec.' + extension
                try:
                    content = template.render(service_name=service["name"], method=method)
                    save_file(os.path.join(output_dir, codec_file_name), content)
                except NotImplementedError:
                    print("[%s] contains missing type mapping so ignoring it." % codec_file_name)


def generate_custom_codecs(services, template, output_dir, extension):
    os.makedirs(output_dir, exist_ok=True)
    for service in services:
        if "customTypes" in service:
            custom_types = service["customTypes"]
            for codec in custom_types:
                codec_file_name = capital(codec["name"]) + 'Codec.' + extension
                try:
                    content = template.render(codec=codec)
                    save_file(os.path.join(output_dir, codec_file_name), content)
                except NotImplementedError:
                    print("[%s] contains missing type mapping so ignoring it." % codec_file_name)


def item_type(lang_name, param_type):
    if param_type.startswith("List_") or param_type.startswith("ListCN_"):
        return lang_name(param_type.split('_', 1)[1])


def key_type(lang_name, param_type):
    return lang_name(param_type.split('_', 2)[1])


def value_type(lang_name, param_type):
    return lang_name(param_type.split('_', 2)[2])


def is_var_sized_list(param_type):
    return param_type.startswith("List_") and param_type not in FixedListTypes


def is_var_sized_list_contains_nullable(param_type):
    return param_type.startswith("ListCN_") and param_type not in FixedListTypes


def is_var_sized_map(param_type):
    return param_type.startswith("Map_") and param_type not in FixedMapTypes


def is_var_sized_entry_list(param_type):
    return param_type.startswith("EntryList_") and param_type not in FixedEntryListTypes


def load_services(protocol_def_dir):
    service_list = os.listdir(protocol_def_dir)
    services = []
    for service_file in service_list:
        file_path = os.path.join(protocol_def_dir, service_file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                try:
                    data = yaml.load(file, Loader=yaml.Loader)
                except MarkedYAMLError as err:
                    print(err)
                    exit(-1)
                services.append(data)
    return services


def validate_services(services, schema_path, check_service_id):
    valid = True
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
        for i in range(len(services)):
            service = services[i]
            # Validate id ordering of services.
            service_id = service.get('id', None)
            if check_service_id and i != service_id:
                print('Check the service id of the %s. Expected: %s, found: %s.' % (
                    service.get('name', None), i, service_id))
                valid = False
            # Validate id ordering of service methods.
            methods = service.get('methods', [])
            for j in range(len(methods)):
                method = methods[j]
                method_id = method.get('id', None)
                if (j + 1) != method_id:
                    print('Check the method id of %s#%s. Expected: %s, found: %s' % (
                        service.get('name', None), method.get('name', None), (j + 1), method_id))
                    valid = False
            # Validate against the schema.
            if not validate_against_schema(service, schema):
                valid = False
    return valid


def validate_custom_protocol_definitions(services, schema_path):
    valid = True
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
    for service in services:
        if not validate_against_schema(service, schema):
            valid = False
    return valid


def validate_against_schema(service, schema):
    try:
        jsonschema.validate(service, schema)
    except jsonschema.ValidationError as e:
        print("Validation error on %s: %s" % (service.get('name', None), e))
        return False
    return True


def save_file(file, content):
    m = hashlib.md5()
    m.update(content.encode("utf-8"))
    codec_hash = m.hexdigest()
    with open(file, 'w') as file:
        file.writelines(content.replace('!codec_hash!', codec_hash))


class SupportedLanguages(Enum):
    JAVA = 'java'
    # CPP = 'cpp'
    CS = 'cs'
    # PY = 'py'
    # TS = 'ts'
    # GO = 'go'


codec_output_directories = {
    SupportedLanguages.JAVA: 'hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/',
    # SupportedLanguages.CPP: 'hazelcast/generated-sources/src/hazelcast/client/protocol/codec/',
    SupportedLanguages.CS: 'Hazelcast.Net/Hazelcast.Client.Protocol.Codec/',
    # SupportedLanguages.PY: 'hazelcast/protocol/codec/',
    # SupportedLanguages.TS: 'src/codec/',
    # SupportedLanguages.GO: 'internal/proto/'
}

custom_codec_output_directories = {
    SupportedLanguages.JAVA: 'hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/custom/',
    # SupportedLanguages.CPP: 'hazelcast/generated-sources/src/hazelcast/client/protocol/codec/',
    SupportedLanguages.CS: 'Hazelcast.Net/Hazelcast.Client.Protocol.Codec.Custom/',
    # SupportedLanguages.PY: 'hazelcast/protocol/codec/',
    # SupportedLanguages.TS: 'src/codec/',
    # SupportedLanguages.GO: 'internal/proto/'
}

file_extensions = {
    SupportedLanguages.JAVA: 'java',
    # SupportedLanguages.CPP: 'cpp',  # TODO header files ?
    SupportedLanguages.CS: 'cs',
    # SupportedLanguages.PY: 'py',
    # SupportedLanguages.TS: 'ts',
    # SupportedLanguages.GO: 'go'
}

language_specific_funcs = {
    'lang_types_encode': {
        SupportedLanguages.JAVA: java_types_encode,
        SupportedLanguages.CS: cs_types_encode,
    },
    'lang_types_decode': {
        SupportedLanguages.JAVA: java_types_decode,
        SupportedLanguages.CS: cs_types_decode,
    },
    'lang_name': {
        SupportedLanguages.JAVA: java_name,
        SupportedLanguages.CS: cs_name,
    },
    'param_name': {
        SupportedLanguages.JAVA: param_name,
        SupportedLanguages.CS: param_name,
    },
    'escape_keyword': {
        SupportedLanguages.JAVA: lambda x: x,
        SupportedLanguages.CS: cs_escape_keyword,
    },
}


def create_environment(lang, namespace):
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
    env.globals["is_var_sized_entry_list"] = is_var_sized_entry_list
    env.globals["is_var_sized_map"] = is_var_sized_map
    env.globals["item_type"] = item_type
    env.globals["key_type"] = key_type
    env.globals["value_type"] = value_type
    env.globals["lang_types_encode"] = language_specific_funcs['lang_types_encode'][lang]
    env.globals["lang_types_decode"] = language_specific_funcs['lang_types_decode'][lang]
    env.globals["lang_name"] = language_specific_funcs['lang_name'][lang]
    env.globals["namespace"] = namespace
    env.globals["param_name"] = language_specific_funcs['param_name'][lang]
    env.globals["escape_keyword"] = language_specific_funcs['escape_keyword'][lang]

    return env
