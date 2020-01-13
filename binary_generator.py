#!/usr/bin/env python3

from binary.util import *
from jinja2.exceptions import TemplateNotFound


def get_binary_templates(lang, version):
    env = create_environment_for_binary_generator(lang, version)
    templates = {}
    try:
        templates['Client'] = env.get_template('client-binary-compatibility-template.j2')
        templates['Member'] = env.get_template('member-binary-compatibility-template.j2')
    except TemplateNotFound as err:
        return err, None
    return None, templates


def save_binary_files(binary_output_dir, protocol_defs_path, version, services):
    os.makedirs(binary_output_dir, exist_ok=True)
    with open(os.path.join(binary_output_dir, version + '.protocol.compatibility.binary'), 'wb') as binary_file:
        with open(os.path.join(binary_output_dir, version + '.protocol.compatibility.null.binary'),
                  'wb') as null_binary_file:
            _generate_binary_files(binary_file, null_binary_file, protocol_defs_path, services)


def save_test_files(test_output_dir, lang, version, services, templates):
    os.makedirs(test_output_dir, exist_ok=True)
    class_name = binary_test_names[lang](version)

    for test_type in ['Client', 'Member']:
        for test_null_type in ['', 'Null']:
            with open(os.path.join(test_output_dir, class_name.format(type=test_type, null=test_null_type)), 'w', newline='\n') as f:
                f.write(templates[test_type].render(services=services, test_nullable=test_null_type == 'Null'))


def _generate_binary_files(binary_file, null_binary_file, protocol_defs_path, services):
    encoder = Encoder(protocol_defs_path)
    for service in services:
        methods = service['methods']
        for method in methods:
            method['request']['id'] = int(id_fmt % (service['id'], method['id'], 0), 16)
            method['response']['id'] = int(id_fmt % (service['id'], method['id'], 1), 16)
            events = method.get('events', None)
            if events is not None:
                for i in range(len(events)):
                    method['events'][i]['id'] = int(id_fmt % (service['id'], method['id'], i + 2), 16)
            request = encoder.encode(method['request'], REQUEST_FIX_SIZED_PARAMS_OFFSET)
            null_request = encoder.encode(method['request'], REQUEST_FIX_SIZED_PARAMS_OFFSET, is_null_test=True)
            request.write(binary_file)
            null_request.write(null_binary_file)
            response = encoder.encode(method['response'], RESPONSE_FIX_SIZED_PARAMS_OFFSET)
            null_response = encoder.encode(method['response'], RESPONSE_FIX_SIZED_PARAMS_OFFSET, is_null_test=True)
            response.write(binary_file)
            null_response.write(null_binary_file)
            if events is not None:
                for e in events:
                    event = encoder.encode(e, EVENT_FIX_SIZED_PARAMS_OFFSET, True)
                    null_event = encoder.encode(e, EVENT_FIX_SIZED_PARAMS_OFFSET, True, True)
                    event.write(binary_file)
                    null_event.write(null_binary_file)
