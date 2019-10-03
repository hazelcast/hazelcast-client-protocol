import os
import yaml


def load_services(protocol_def_dir):
    service_list = os.listdir(protocol_def_dir)
    services = []
    for service_file in service_list:
        file_path = os.path.join(protocol_def_dir, service_file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = yaml.load(file, Loader=yaml.Loader)
                services.append(data)
    return services


services = load_services('/Users/hazelcast/hazelcast-client-protocol/protocol-definitions')
services = sorted(services, key=lambda s: s['id'])
counter = 0
for service in services:
    if counter != service['id']:
        print('! ', end='')
    print(counter, service['id'], service['name'])
    m_counter = 1
    for method in service['methods']:
        if m_counter != method['id']:
            print('! ', end='')
        print('\t', m_counter, method['id'], method['name'])
        m_counter += 1
    counter += 1
