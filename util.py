import os
import yaml
import re
from jinja2 import Environment, PackageLoader
from java import java_types


def load_services(protocol_def_dir):
    service_list = os.listdir(protocol_def_dir)
    services = []
    for service_file in service_list:
        with open(protocol_def_dir + service_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.Loader)
            services.append(data)
    return services


def save_file(file, content):
    with open(file, 'w') as file:
        file.writelines(content)


def create_environment(lang):
    env = Environment(loader=PackageLoader(lang, '.'))
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.keep_trailing_newline = False
    env.filters["capital"] = capital
    env.globals["to_upper_snake_case"] = to_upper_snake_case
    env.globals["fixed_params"] = fixed_params
    env.globals["var_size_params"] = var_size_params
    env.globals["lang_types"] = java_types
    env.globals["lang_name"] = java_name
    env.globals["item_type"] = item_type
    env.globals["value_type"] = value_type
    env.globals["key_type"] = key_type
    return env


FixedLengthTypes = [
    "boolean",
    "int",
    "long",
    "byte",
    "Integer",
    "UUID"
]


def item_type(param_type):
    return param_type.split("_", 2)[1]


def key_type(param_type):
    return param_type.split("_", 3)[1]


def value_type(param_type):
    return param_type.split("_", 3)[2]


def java_name(type_name):
    return type_name.replace("_", "").replace("(", "").replace(")", "")


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


def generate_message_types(service, template, output_dir, lang):
    content = template.render(service=service)
    save_file(output_dir + capital(service["name"]) + 'MessageType.' + lang, content)


def generate_codecs(service, template, output_dir, lang):
    methods = service["methods"]
    if methods is None:
        print(type(methods))
    for method in service["methods"]:
        content = template.render(service_name=service["name"], method=method)
        save_file(output_dir + capital(service["name"]) + capital(method["name"]) + 'Codec.' + lang, content)
