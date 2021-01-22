#!/usr/bin/env python3

from os import makedirs
from os.path import join

from binary.util import *


def get_binary_templates(lang):
    env = create_environment_for_binary_generator(lang)
    client_template = env.get_template("client-binary-compatibility-template.j2")
    member_template = env.get_template("member-binary-compatibility-template.j2")

    return {
        "Client": client_template,
        "Member": member_template,
    }


def save_binary_files(binary_output_dir, protocol_defs_path, version, services):
    makedirs(binary_output_dir, exist_ok=True)
    binary_file_path = join(binary_output_dir, version + ".protocol.compatibility.binary")
    null_binary_file_path = join(binary_output_dir, version + ".protocol.compatibility.null.binary")

    with open(binary_file_path, "wb") as binary_file:
        with open(null_binary_file_path, "wb") as null_binary_file:
            _generate_binary_files(
                binary_file, null_binary_file, protocol_defs_path, services, version
            )


def save_test_files(test_output_dir, lang, version, services, templates):
    makedirs(test_output_dir, exist_ok=True)
    class_name = binary_test_names[lang](version)

    for test_type in ["Client", "Member"]:
        for test_null_type in ["", "Null"]:
            file_path = join(
                test_output_dir, class_name.format(type=test_type, null=test_null_type)
            )
            with open(file_path, "w", newline="\n") as f:
                f.write(
                    templates[test_type].render(
                        protocol_version=version,
                        services=services,
                        test_nullable=test_null_type == "Null",
                    )
                )


def _generate_binary_files(binary_file, null_binary_file, protocol_defs_path, services, version):
    encoder = Encoder(protocol_defs_path, version)
    version_as_number = get_version_as_number(version)
    for service in services:
        methods = service["methods"]
        for method in methods:
            if get_version_as_number(method["since"]) > version_as_number:
                continue

            method["request"]["id"] = int(id_fmt % (service["id"], method["id"], 0), 16)
            method["response"]["id"] = int(id_fmt % (service["id"], method["id"], 1), 16)
            events = method.get("events", None)
            if events is not None:
                for i in range(len(events)):
                    method["events"][i]["id"] = int(
                        id_fmt % (service["id"], method["id"], i + 2), 16
                    )
            request = encoder.encode(
                method["request"], REQUEST_FIX_SIZED_PARAMS_OFFSET, set_partition_id=True
            )
            null_request = encoder.encode(
                method["request"],
                REQUEST_FIX_SIZED_PARAMS_OFFSET,
                set_partition_id=True,
                is_null_test=True,
            )
            request.write(binary_file)
            null_request.write(null_binary_file)
            response = encoder.encode(method["response"], RESPONSE_FIX_SIZED_PARAMS_OFFSET)
            null_response = encoder.encode(
                method["response"], RESPONSE_FIX_SIZED_PARAMS_OFFSET, is_null_test=True
            )
            response.write(binary_file)
            null_response.write(null_binary_file)
            if events is not None:
                for e in events:
                    if get_version_as_number(e["since"]) > version_as_number:
                        continue

                    event = encoder.encode(
                        e, EVENT_FIX_SIZED_PARAMS_OFFSET, is_event=True, set_partition_id=True
                    )
                    null_event = encoder.encode(
                        e,
                        EVENT_FIX_SIZED_PARAMS_OFFSET,
                        is_event=True,
                        set_partition_id=True,
                        is_null_test=True,
                    )
                    event.write(binary_file)
                    null_event.write(null_binary_file)
