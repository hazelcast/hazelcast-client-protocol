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
from cs import cs_types_encode, cs_types_decode, cs_escape_keyword, cs_ignore_service_list
from py import py_types_encode, py_types_decode, py_escape_keyword, py_ignore_service_list

MAJOR_VERSION_MULTIPLIER = 10000
MINOR_VERSION_MULTIPLIER = 100
PATCH_VERSION_MULTIPLIER = 1


def java_name(type_name):
    return "".join([capital(part) for part in type_name.replace("(", "").replace(")", "").split("_")])


def cs_name(type_name):
    return "".join([capital(part) for part in type_name.replace("(", "").replace(")", "").split("_")])


def py_name(type_name):
    return "".join([part for part in type_name.replace("(","").replace("(","").split("_")])


def param_name(type_name):
    return type_name[0].lower() + type_name[1:]


def py_param_name(type_name):
    return re.sub("_", "", type_name)


def is_fixed_type(param):
    return param["type"] in FixedLengthTypes


def capital(txt):
    return txt[0].capitalize() + txt[1:]


def to_upper_snake_case(camel_case_str):
    return re.sub('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', camel_case_str).upper()
    # s1 = re.sub('(.)([A-Z]+[a-z]+)', r'\1_\2', camel_case_str)
    # return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()


def version_to_number(major, minor, patch=0):
    return MAJOR_VERSION_MULTIPLIER * major + MINOR_VERSION_MULTIPLIER * minor + PATCH_VERSION_MULTIPLIER * patch


def get_version_as_number(version):
    if not isinstance(version, str):
        version = str(version)
    return version_to_number(*map(int, version.split('.')))


def snake_case(camel_case_str):
    return re.sub('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', camel_case_str).lower()


def fixed_params(params):
    return [p for p in params if is_fixed_type(p)]


def var_size_params(params):
    return [p for p in params if not is_fixed_type(p)]


def new_params(since, params):
    """
    Returns the list of parameters that are added later than given version.
    Because the method should precede all the parameters that are added
    latter, a simple equality check between the versions that the method and
    the parameter is added is enough.
    """
    return [p for p in params if p['since'] != since]


def filter_new_params(params, version):
    """
    Returns the filtered list of parameters such that,
    the resulting list contains only the ones that are added
    before or at the same time with the given version.
    """
    version_as_number = get_version_as_number(version)
    return [p for p in params if version_as_number >= get_version_as_number(p['since'])]


def generate_codecs(services, template, output_dir, lang):
    os.makedirs(output_dir, exist_ok=True)
    id_fmt = "0x%02x%02x%02x"
    for service in services:
        if service["id"] in language_service_ignore_list[lang]:
            print("[%s] is in ignore list so ignoring it." % service["name"])
            continue
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
                if lang.name == 'PY':
                    codec_file_name = snake_case(service["name"]) + "_" + snake_case(method["name"]) + '_codec.' + \
                                      file_extensions[lang]
                else:
                    codec_file_name = capital(service["name"]) + capital(method["name"]) + 'Codec.' + file_extensions[
                        lang]
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
                if extension == "py":
                    codec_file_name = snake_case(codec["name"]) + '_codec.' + extension
                else:
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


def validate_services(services, schema_path, no_id_check, protocol_versions):
    valid = True
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
        for i in range(len(services)):
            service = services[i]
            # Validate against the schema.
            if not validate_against_schema(service, schema):
                return False

            if not no_id_check:
                # Validate id ordering of services.
                service_id = service['id']
                if i != service_id:
                    print('Check the service id of the %s. Expected: %s, found: %s.' % (
                        service['name'], i, service_id))
                    valid = False
                # Validate id ordering of service methods.
                methods = service['methods']
                for j in range(len(methods)):
                    method = methods[j]
                    method_id = method['id']
                    if (j + 1) != method_id:
                        print('Check the method id of %s#%s. Expected: %s, found: %s' % (
                            service['name'], method['name'], (j + 1), method_id))
                        valid = False
                    request_params = method['request'].get('params', [])
                    method_name = service['name'] + "#" + method['name']
                    if not is_parameters_ordered_and_semantically_correct(method['since'], method_name + '#request',
                                                                          request_params, protocol_versions):
                        valid = False
                    response_params = method['response'].get('params', [])
                    if not is_parameters_ordered_and_semantically_correct(method['since'], method_name + '#response',
                                                                          response_params, protocol_versions):
                        valid = False
                    events = method.get('events', [])
                    for event in events:
                        event_params = event.get('params', [])
                        if not is_parameters_ordered_and_semantically_correct(event['since'],
                                                                              method_name + '#' + event['name']
                                                                              + '#event',
                                                                              event_params, protocol_versions):
                            valid = False
    return valid


def is_semantically_correct_param(version, protocol_versions):
    is_semantically_correct = True
    if version != protocol_versions[0]:
        # Not 2.0
        if version % MINOR_VERSION_MULTIPLIER == 0:
            # Minor version
            if (version - MINOR_VERSION_MULTIPLIER) not in protocol_versions:
                # since is set to 2.x but 2.(x-1) is not in the protocol definitions
                is_semantically_correct = False
        elif version % PATCH_VERSION_MULTIPLIER == 0:
            # Patch version
            if (version - PATCH_VERSION_MULTIPLIER) not in protocol_versions:
                # since is set to 2.x.y but 2.x.(y-1) is not in the protocol definitions
                is_semantically_correct = False
    return is_semantically_correct


def is_parameters_ordered_and_semantically_correct(since, name, params, protocol_versions):
    is_ordered = True
    is_semantically_correct = True
    version = get_version_as_number(since)

    if not is_semantically_correct_param(version, protocol_versions):
        method_or_event_name = name[:name.rindex('#')]
        print('Check the since value of the "%s"\n'
              'It is set to version "%s" but this protocol version does '
              'not semantically follow other protocol versions!' % (method_or_event_name, since))
        is_semantically_correct = False

    for param in params:
        param_version = get_version_as_number(param['since'])
        if not is_semantically_correct_param(param_version, protocol_versions):
            print('Check the since value of "%s" field of the "%s".\n'
                  'It is set version "%s" but this protocol version does '
                  'not semantically follow other protocol versions!' % (param['name'], name, param['since']))
            is_semantically_correct = False

        if version > param_version:
            print('Check the since value of "%s" field of the "%s".\n'
                  'Parameters should be in the increasing order of since values!' % (param['name'], name))
            is_ordered = False

        version = param_version
    return is_ordered and is_semantically_correct


def validate_custom_protocol_definitions(definition, schema_path, protocol_versions):
    valid = True
    with open(schema_path, 'r') as schema_file:
        schema = json.load(schema_file)
    custom_types = definition[0]
    if not validate_against_schema(custom_types, schema):
        return False
    for custom_type in custom_types['customTypes']:
        params = custom_type.get('params', [])
        if not is_parameters_ordered_and_semantically_correct(custom_type['since'],
                                                              'CustomTypes#' + custom_type['name'],
                                                              params, protocol_versions):
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
    with open(file, 'w', newline='\n') as file:
        file.writelines(content.replace('!codec_hash!', codec_hash))


def get_protocol_versions(protocol_defs, custom_codec_defs):
    protocol_versions = set()
    if not custom_codec_defs:
        custom_codec_defs = []
    else:
        custom_codec_defs = custom_codec_defs[0]['customTypes']

    for service in protocol_defs:
        for method in service['methods']:
            protocol_versions.add(method['since'])
            for req_param in method['request'].get('params', []):
                protocol_versions.add(req_param['since'])
            for res_param in method['response'].get('params', []):
                protocol_versions.add(res_param['since'])
            for event in method.get('events', []):
                protocol_versions.add(event['since'])
                for event_param in event.get('params', []):
                    protocol_versions.add(event_param['since'])

    for custom_codec in custom_codec_defs:
        protocol_versions.add(custom_codec['since'])
        for param in custom_codec.get('params', []):
            protocol_versions.add(param['since'])

    return map(str, protocol_versions)


class SupportedLanguages(Enum):
    JAVA = 'java'
    # CPP = 'cpp'
    CS = 'cs'
    PY = 'py'
    # TS = 'ts'
    # GO = 'go'


codec_output_directories = {
    SupportedLanguages.JAVA: 'hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/',
    # SupportedLanguages.CPP: 'hazelcast/generated-sources/src/hazelcast/client/protocol/codec/',
    SupportedLanguages.CS: 'Hazelcast.Net/Hazelcast.Client.Protocol.Codec/',
    SupportedLanguages.PY: 'hazelcast/protocol/codec/',
    # SupportedLanguages.TS: 'src/codec/',
    # SupportedLanguages.GO: 'internal/proto/'
}

custom_codec_output_directories = {
    SupportedLanguages.JAVA: 'hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/custom/',
    # SupportedLanguages.CPP: 'hazelcast/generated-sources/src/hazelcast/client/protocol/codec/',
    SupportedLanguages.CS: 'Hazelcast.Net/Hazelcast.Client.Protocol.Codec.Custom/',
    SupportedLanguages.PY: 'hazelcast/protocol/codec/custom/',
    # SupportedLanguages.TS: 'src/codec/',
    # SupportedLanguages.GO: 'internal/proto/'
}

file_extensions = {
    SupportedLanguages.JAVA: 'java',
    # SupportedLanguages.CPP: 'cpp',  # TODO header files ?
    SupportedLanguages.CS: 'cs',
    SupportedLanguages.PY: 'py',
    # SupportedLanguages.TS: 'ts',
    # SupportedLanguages.GO: 'go'
}

language_specific_funcs = {
    'lang_types_encode': {
        SupportedLanguages.JAVA: java_types_encode,
        SupportedLanguages.CS: cs_types_encode,
        SupportedLanguages.PY: py_types_encode,
    },
    'lang_types_decode': {
        SupportedLanguages.JAVA: java_types_decode,
        SupportedLanguages.CS: cs_types_decode,
        SupportedLanguages.PY: py_types_decode,
    },
    'lang_name': {
        SupportedLanguages.JAVA: java_name,
        SupportedLanguages.CS: cs_name,
        SupportedLanguages.PY: py_name,
    },
    'param_name': {
        SupportedLanguages.JAVA: param_name,
        SupportedLanguages.CS: param_name,
        SupportedLanguages.PY: py_param_name,
    },
    'escape_keyword': {
        SupportedLanguages.JAVA: lambda x: x,
        SupportedLanguages.CS: cs_escape_keyword,
        SupportedLanguages.PY: py_escape_keyword,
    },
}

language_service_ignore_list = {
    SupportedLanguages.JAVA: [],
    # SupportedLanguages.CPP: [],
    SupportedLanguages.CS: cs_ignore_service_list,
    SupportedLanguages.PY: py_ignore_service_list,
    # SupportedLanguages.TS: [],
    # SupportedLanguages.GO: []
}


def create_environment(lang, namespace):
    env = Environment(loader=PackageLoader(lang.value, '.'))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.keep_trailing_newline = False
    env.filters["capital"] = capital
    env.globals["to_upper_snake_case"] = to_upper_snake_case
    env.globals["snake_case"] = snake_case
    env.globals["fixed_params"] = fixed_params
    env.globals["var_size_params"] = var_size_params
    env.globals['new_params'] = new_params
    env.globals['filter_new_params'] = filter_new_params
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
