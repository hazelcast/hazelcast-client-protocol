#!/usr/bin/env python3

import argparse

from binary.util import *

parser = argparse.ArgumentParser(description='Hazelcast Protocol Compatibility Generator generates '
                                             'files related to the binary compatibility of client '
                                             'protocol across protocol versions.')

parser.add_argument('-r', '--root-dir',
                    dest='root_dir', action='store',
                    metavar='ROOT_DIRECTORY', default=None,
                    type=str, help='Root directory for the generated files (default value is '
                                   '../output/binary/[LANGUAGE])')

parser.add_argument('-l', '--lang',
                    dest='lang', action='store',
                    metavar='LANGUAGE', default='java',
                    choices=[lang.value for lang in SupportedLanguages],
                    type=str, help='Language to generate files for (default default is java)')

parser.add_argument('-p', '--protocol-definitions-path',
                    dest='proto_path', action='store',
                    metavar='PROTOCOL_DEFS_PATH', default=None,
                    type=str, help='Path of protocol definitions directory (default value is ../protocol-definitions)')

parser.add_argument('-b', '--binary-output-dir',
                    dest='bin_out_dir', action='store',
                    metavar='BINARY_OUTPUT_DIRECTORY', default=None,
                    type=str, help='Path of the output directory relative to the '
                                   'root directory for the binary file.(default value is set according to the selected '
                                   'language)')

parser.add_argument('-t', '--test-output-dir',
                    dest='test_out_dir', action='store',
                    metavar='TEST_OUTPUT_DIRECTORY', default=None,
                    type=str, help='Path of the output directory relative to the '
                                   'root directory for the test file.(default value is set according to the selected '
                                   'language)')

parser.add_argument('-n', '--namespace',
                    dest='namespace', action='store',
                    metavar='NAMESPACE', default=None,
                    type=str, help='Namespace for the generated codecs (default value is inferred from the '
                                   'selected language)')

parser.add_argument('-v', '--version',
                    dest='version', action='store',
                    metavar='VERSION', default='2.0',
                    type=str, help='Version of the protocol to generate files for. (default value is the version '
                                   'of the protocol)')

args = parser.parse_args()
lang_str_arg = args.lang
root_dir_arg = args.root_dir
proto_path_arg = args.proto_path
test_out_dir_arg = args.test_out_dir
bin_out_dir_arg = args.bin_out_dir
namespace_arg = args.namespace
version_arg = args.version

lang = SupportedLanguages[lang_str_arg.upper()]

curr_dir = os.path.dirname(os.path.realpath(__file__))

root_dir = root_dir_arg if root_dir_arg is not None else os.path.join(curr_dir, 'output', lang_str_arg)
relative_test_output_dir = test_out_dir_arg if test_out_dir_arg is not None else test_output_directories[lang]
relative_binary_output_dir = bin_out_dir_arg if bin_out_dir_arg is not None else binary_output_directories[lang]
test_output_dir = os.path.join(root_dir, relative_test_output_dir)
binary_output_dir = os.path.join(root_dir, relative_binary_output_dir)

protocol_defs_path = proto_path_arg if proto_path_arg is not None else os.path.join(curr_dir, 'protocol-definitions')

count = 0
services = load_services(protocol_defs_path)
services = sorted(services, key=lambda s: s['id'])
os.makedirs(binary_output_dir, exist_ok=True)
with open(os.path.join(binary_output_dir, version_arg + '.protocol.compatibility.binary'), 'wb') as binary:
    with open(os.path.join(binary_output_dir, version_arg + '.protocol.compatibility.null.binary'), 'wb') as null_binary:
        for service in services:
            methods = service["methods"]
            for method in methods:
                method["request"]["id"] = int(id_fmt % (service["id"], method["id"], 0), 16)
                method["response"]["id"] = int(id_fmt % (service["id"], method["id"], 1), 16)
                events = method.get("events", None)
                if events is not None:
                    for i in range(len(events)):
                        method["events"][i]["id"] = int(id_fmt % (service["id"], method["id"], i + 2), 16)
                request = Encoder.encode_request(method["request"])
                null_request = Encoder.encode_request(method["request"], True)
                request.write(binary)
                null_request.write(null_binary)
                response = Encoder.encode_response(method["response"])
                null_response = Encoder.encode_response(method["response"], True)
                response.write(binary)
                null_response.write(null_binary)
                if events is not None:
                    for e in events:
                        event = Encoder.encode_event(e)
                        null_event = Encoder.encode_event(e, True)
                        event.write(binary)
                        null_event.write(null_binary)

env = create_environment_for_binary_generator(lang, version_arg)

client_template = env.get_template('client-binary-compatibility-template.j2')
member_template = env.get_template('member-binary-compatibility-template.j2')

class_name = '{type}Compatibility{null}Test_' + '_'.join(version_arg.split('.')) + '.java'

os.makedirs(test_output_dir, exist_ok=True)
with open(os.path.join(test_output_dir, class_name.format(type='Client', null='')), 'w') as f:
    f.write(client_template.render(services=services))

with open(os.path.join(test_output_dir, class_name.format(type='Client', null='Null')), 'w') as f:
    f.write(client_template.render(services=services, test_nullable=True))

with open(os.path.join(test_output_dir, class_name.format(type='Member', null='')), 'w') as f:
    f.write(member_template.render(services=services))

with open(os.path.join(test_output_dir, class_name.format(type='Member', null='Null')), 'w') as f:
    f.write(member_template.render(services=services, test_nullable=True))
