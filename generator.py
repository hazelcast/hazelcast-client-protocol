#!/usr/bin/env python3

import argparse
import time
from os.path import abspath, exists

from jinja2 import TemplateNotFound

from binary.util import binary_output_directories, test_output_directories
from binary_generator import get_binary_templates, save_binary_files, save_test_files
from util import *

start = time.time()

parser = argparse.ArgumentParser(
    description="Hazelcast Code Generator generates code of client protocol across languages."
)

parser.add_argument(
    "-r",
    "--root-dir",
    dest="root_dir",
    action="store",
    metavar="ROOT_DIRECTORY",
    default=None,
    type=str,
    help="Root directory for the generated codecs (default value is ./output/[LANGUAGE])",
)

parser.add_argument(
    "-l",
    "--lang",
    dest="lang",
    action="store",
    metavar="LANGUAGE",
    default="java",
    choices=[lang.value for lang in SupportedLanguages],
    type=str,
    help="Language to generate codecs for (default default is java)",
)

parser.add_argument(
    "-p",
    "--protocol-definitions-path",
    dest="proto_path",
    action="store",
    metavar="PROTOCOL_DEFS_PATH",
    default=None,
    type=str,
    help="Path of protocol definitions directory (default value is ./protocol-definitions)",
)

parser.add_argument(
    "-o",
    "--output-dir",
    dest="out_dir",
    action="store",
    metavar="OUTPUT_DIRECTORY",
    default=None,
    type=str,
    help="Path of the output directory relative to the "
    "root directory (default value is set according to the selected "
    "language)",
)

parser.add_argument(
    "-n",
    "--namespace",
    dest="namespace",
    action="store",
    metavar="NAMESPACE",
    default=None,
    type=str,
    help="Namespace for the generated codecs (default value is inferred from the "
    "selected language)",
)

parser.add_argument(
    "-b",
    "--binary-output-dir",
    dest="bin_out_dir",
    action="store",
    metavar="BINARY_OUTPUT_DIRECTORY",
    default=None,
    type=str,
    help="Path of the output directory relative to the "
    "root directory for the binary file.(default value is set according to the selected "
    "language)",
)

parser.add_argument(
    "-t",
    "--test-output-dir",
    dest="test_out_dir",
    action="store",
    metavar="TEST_OUTPUT_DIRECTORY",
    default=None,
    type=str,
    help="Path of the output directory relative to the "
    "root directory for the binary compatibility test files.(default value is "
    "set according to the selected language)",
)

parser.add_argument(
    "--no-binary",
    dest="no_binary",
    action="store_true",
    default=False,
    help="Flag to signal that binary compatibility files and tests"
    "should not be generated. These files are generated by default.",
)

parser.add_argument(
    "--no-id-check",
    dest="no_id_check",
    action="store_true",
    default=False,
    help="Flag to signal that no sequential id check for service or method definitions "
    "should be performed. These checks are done by default.",
)

args = parser.parse_args()

lang = SupportedLanguages[args.lang.upper()]

curr_dir = dirname(realpath(__file__))

root_dir = args.root_dir or join(curr_dir, "output", lang.value)
relative_output_dir = args.out_dir or codec_output_directories[lang]
codec_output_dir = join(root_dir, relative_output_dir)

protocol_defs_path = args.proto_path or join(curr_dir, "protocol-definitions")
custom_protocol_defs_path = join(protocol_defs_path, "custom")

schema_path = join(curr_dir, "schema", "protocol-schema.json")
custom_codec_schema_path = join(curr_dir, "schema", "custom-codec-schema.json")

protocol_defs = load_services(protocol_defs_path)
custom_protocol_defs = None

if exists(custom_protocol_defs_path):
    custom_protocol_defs = load_services(custom_protocol_defs_path)

protocol_versions = sorted(
    get_protocol_versions(protocol_defs, custom_protocol_defs),
    key=lambda ver: get_version_as_number(ver),
)

protocol_defs = sorted(protocol_defs, key=lambda proto_def: proto_def["id"])

if not validate_services(protocol_defs, schema_path, args.no_id_check):
    exit(-1)

if custom_protocol_defs and not validate_custom_protocol_definitions(
    custom_protocol_defs, custom_codec_schema_path
):
    exit(-1)

env = create_environment(lang, args.namespace)

if lang != SupportedLanguages.MD:
    codec_template = env.get_template("codec-template.%s.j2" % lang.value)
    generate_codecs(protocol_defs, custom_protocol_defs, codec_template, codec_output_dir, lang, env)
    print("Generated codecs are at '%s'" % abspath(codec_output_dir))

if custom_protocol_defs:
    if lang != SupportedLanguages.MD and lang != SupportedLanguages.CPP:
        custom_codec_template = env.get_template("custom-codec-template.%s.j2" % lang.value)
        relative_custom_codec_output_dir = args.out_dir or custom_codec_output_directories[lang]
        custom_codec_output_dir = join(root_dir, relative_custom_codec_output_dir)

        generate_custom_codecs(
            custom_protocol_defs,
            custom_codec_template,
            custom_codec_output_dir,
            lang,
            env,
        )
        print("Generated custom codecs are at '%s'" % custom_codec_output_dir)
    elif lang == SupportedLanguages.MD:
        documentation_template = env.get_template("documentation-template.j2")
        generate_documentation(
            protocol_defs,
            custom_protocol_defs,
            documentation_template,
            codec_output_dir,
        )
        print("Generated documentation is at '%s'" % abspath(codec_output_dir))

if not args.no_binary and lang != SupportedLanguages.MD:
    relative_test_output_dir = args.test_out_dir or test_output_directories.get(lang, None)
    relative_binary_output_dir = args.bin_out_dir or binary_output_directories.get(lang, None)

    # If both of them are not defined, that means the
    # protocol binary compatibility tests are not implemented
    # for that language yet.
    not_implemented = relative_binary_output_dir is None or relative_test_output_dir is None

    try:
        if not_implemented:
            raise NotImplementedError()

        test_output_dir = join(root_dir, relative_test_output_dir)
        binary_output_dir = join(root_dir, relative_binary_output_dir)
        binary_templates = get_binary_templates(lang)
        for version in protocol_versions:
            save_test_files(test_output_dir, lang, version, protocol_defs, binary_templates)
            save_binary_files(binary_output_dir, protocol_defs_path, version, protocol_defs)
        print("Generated binary compatibility files are at '%s'" % binary_output_dir)
        print("Generated binary compatibility tests are at '%s'" % test_output_dir)
    except TemplateNotFound as e:
        print(
            "Binary compatibility test cannot be generated because the templates for the selected "
            "language cannot be loaded. Verify that the '%s' exists." % e
        )
    except NotImplementedError:
        pass
    except Exception as e:
        print("Binary compatibility tests cannot be generated. Error:", e)

end = time.time()

print("Generator took: %d secs" % (end - start))
