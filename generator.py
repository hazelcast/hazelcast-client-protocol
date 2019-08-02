#!/usr/bin/env python

import time
import argparse

from util import *

start = time.time()

parser = argparse.ArgumentParser(description='Hazelcast Code Generator generates code of client protocol '
                                             'across languages.')

parser.add_argument('-r', '--root-dir',
                    dest='root_dir', action='store',
                    metavar='ROOT_DIRECTORY', default=None,
                    type=str, help='Root directory for the generated codecs (default is ./output/[LANGUAGE])')

parser.add_argument('-l', '--lang',
                    dest='lang', action='store',
                    metavar='LANGUAGE', default='java',
                    choices=[lang.value for lang in SupportedLanguages],
                    type=str, help='Language to generate codecs for (default is java)')

args = parser.parse_args()
lang_str = args.lang
root_dir_arg = args.root_dir
lang = SupportedLanguages[lang_str.upper()]

root_dir = root_dir_arg if root_dir_arg is not None else './output/' + lang_str
output_dir = root_dir + output_directories[lang]

# PWD
dir_path = os.path.dirname(os.path.realpath(__file__))
protocol_defs_path = dir_path + '/protocol-definitions/'

services = load_services(protocol_defs_path)

env = create_environment(lang)

codec_template = env.get_template("codec-template.%s.j2" % lang_str)

for service in services:
    if "methods" in service:
        generate_codecs(service, codec_template, output_dir, file_extensions[lang])

end = time.time()

print("Generator took: %d secs" % (end - start))
print('Generated codecs are at \'%s\'' % os.path.abspath(output_dir))
