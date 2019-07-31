#!/usr/bin/env python

import time
import argparse

from enum import Enum
from util import *


class SupportedLanguages(Enum):
    JAVA = 'java'
    CPP = 'cpp'
    CS = 'cs'
    PY = 'py'
    NODE = 'node'
    GO = 'go'


output_directories = {
    SupportedLanguages.JAVA: '/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/',
    SupportedLanguages.CPP: '/hazelcast/generated-sources/src/hazelcast/client/protocol/codec/',
    SupportedLanguages.CS: '/Hazelcast.Net/Hazelcast.Client.Protocol.Codec/',
    SupportedLanguages.PY: '/hazelcast/protocol/codec/',
    SupportedLanguages.NODE: '/src/codec/',
    SupportedLanguages.GO: '/internal/proto/'
}

file_extensions = {
    SupportedLanguages.JAVA: 'java',
    SupportedLanguages.CPP: 'cpp',  # TODO header files ?
    SupportedLanguages.CS: 'cs',
    SupportedLanguages.PY: 'py',
    SupportedLanguages.NODE: 'ts',
    SupportedLanguages.GO: 'go'
}

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
                    type=str, help='Language to generate codecs for (default is Java)')

args = parser.parse_args()

start = time.time()

root = args.root_dir if args.root_dir is not None else './output/' + args.lang
lang = args.lang
output_dir = root + output_directories[SupportedLanguages[lang.upper()]]

# Pwd
__dir__ = os.path.dirname(os.path.realpath(__file__))

dir_path = os.path.dirname(os.path.realpath(__file__))
protocol_defs_path = dir_path + '/protocol-definitions/'
services = load_services(protocol_defs_path)

env = create_environment(lang)

codec_template = env.get_template("codec-template.%s.j2" % lang)

for service in services:
    if "methods" in service:
        generate_codecs(service, codec_template, output_dir, file_extensions[SupportedLanguages[lang.upper()]])

end = time.time()

print("Generator took: %d secs" % (end - start))
