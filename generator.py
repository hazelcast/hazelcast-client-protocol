#!/usr/bin/env python3

import time
import argparse

from util import *

PROTOCOL_VERSION = 2.0

start = time.time()

parser = argparse.ArgumentParser(description='Hazelcast Code Generator generates code of client protocol '
                                             'across languages.')

parser.add_argument('-r', '--root-dir',
                    dest='root_dir', action='store',
                    metavar='ROOT_DIRECTORY', default=None,
                    type=str, help='Root directory for the generated codecs (default value is ./output/[LANGUAGE])')

parser.add_argument('-l', '--lang',
                    dest='lang', action='store',
                    metavar='LANGUAGE', default='java',
                    choices=[lang.value for lang in SupportedLanguages],
                    type=str, help='Language to generate codecs for (default default is java)')

parser.add_argument('-p', '--protocol-definitions-path',
                    dest='proto_path', action='store',
                    metavar='PROTOCOL_DEFS_PATH', default=None,
                    type=str, help='Path of protocol definitions directory (default value is ./protocol-definitions)')

parser.add_argument('-o', '--output-dir',
                    dest='out_dir', action='store',
                    metavar='OUTPUT_DIRECTORY', default=None,
                    type=str, help='Path of the output directory relative to the '
                                   'root directory (default value is set according to the selected '
                                   'language)')

parser.add_argument('-n', '--namespace',
                    dest='namespace', action='store',
                    metavar='NAMESPACE', default=None,
                    type=str, help='Namespace for the generated codecs (default value is inferred from the '
                                   'selected language)')


args = parser.parse_args()
lang_str_arg = args.lang
root_dir_arg = args.root_dir
proto_path_arg = args.proto_path
out_dir_arg = args.out_dir
namespace_arg = args.namespace

lang = SupportedLanguages[lang_str_arg.upper()]


curr_dir = os.path.dirname(os.path.realpath(__file__))

root_dir = root_dir_arg if root_dir_arg is not None else os.path.join(curr_dir, 'output', lang_str_arg)
relative_output_dir = out_dir_arg if out_dir_arg is not None else output_directories[lang]
output_dir = os.path.join(root_dir, relative_output_dir)

protocol_defs_path = proto_path_arg if proto_path_arg is not None else os.path.join(curr_dir, 'protocol-definitions')
custom_protocol_defs_path = os.path.join(protocol_defs_path, 'custom')

schema_path = os.path.join(curr_dir, 'schema', 'protocol-schema.json')
custom_codec_schema_path = os.path.join(curr_dir, 'schema', 'custom-codec-schema.json')

protocol_defs = load_services(protocol_defs_path)
protocol_defs = sorted(protocol_defs, key=lambda proto_def: proto_def['id'])
if not validate_services(protocol_defs, schema_path):
    exit(-1)

env = create_environment(lang, namespace_arg)

codec_template = env.get_template("codec-template.%s.j2" % lang_str_arg)

generate_codecs(protocol_defs, codec_template, output_dir, file_extensions[lang])
print('Generated codecs are at \'%s\'' % os.path.abspath(output_dir))

if os.path.exists(custom_protocol_defs_path):
    custom_protocol_defs = load_services(custom_protocol_defs_path)
    if not validate_custom_protocol_definitions(custom_protocol_defs, custom_codec_schema_path):
        exit(-1)

    custom_codec_template = env.get_template("custom-codec-template.%s.j2" % lang_str_arg)
    custom_codec_output_dir = os.path.join(output_dir, 'custom')
    generate_custom_codecs(custom_protocol_defs, custom_codec_template, custom_codec_output_dir,
                           file_extensions[lang])
    print('Generated custom codecs are at \'%s\'' % custom_codec_output_dir)

end = time.time()

print("Generator took: %d secs" % (end - start))
