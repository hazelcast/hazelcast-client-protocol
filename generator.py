#!/usr/bin/env python

import time

from util import *

start = time.time()

hazelcast_project_root = "../hazelcast4"
output_dir = hazelcast_project_root + "/hazelcast/src/main/java/com/hazelcast/client/impl/protocol/codec/"

# Pwd
__dir__ = os.path.dirname(os.path.realpath(__file__))

dir_path = os.path.dirname(os.path.realpath(__file__))
protocol_defs_path = dir_path + "/protocol-definitions/"
services = load_services(protocol_defs_path)

lang = 'java'
env = create_environment(lang)

codec_template = env.get_template("codec-template.%s.j2" % lang)

for service in services:
    if "methods" in service:
        generate_codecs(service, codec_template, output_dir, lang)


end = time.time()

print("Generator took: %d secs" % (end - start))
