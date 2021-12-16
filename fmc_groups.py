import fmc_cfg


server = fmc_cfg.fmc.server
api_base_path = fmc_cfg.fmc.api_base_path


def create_net_object(name, net, des=''):
    return {
        'name': name,
        'description': des,
        'type': 'Network',
        'value': net,
    }


def addNetObject(name, id):
    return {
        'name': name,
        'id': id
    }


def create_net_group(name, des=''):
    return {
        'name': name,
        'description': des,
        'type': 'NetworkGroup',
        'overridable': True
    }


def get_net_objects():
    return fmc_cfg.fmc.GetApiCall(server + '/' + api_base_path + '/object/networks')


def get_net_groups():
    return fmc_cfg.fmc.GetApiCall(server + '/' + api_base_path + '/object/networkgroups')


def get_fqdn_objects():
    return fmc_cfg.fmc.GetApiCall(server + '/' + api_base_path + '/object/fqdn')


def get_hosts_groups():
    return fmc_cfg.fmc.GetApiCall(server + '/' + api_base_path + '/object/hosts')


def create_full_group(group_name, networks):
    object_group = {
        'name': group_name,
        'type': 'NetworkGroup',
        'overridable': True,
        'objects': []
    }
    for n in networks:
        resp = fmc_cfg.fmc.PostApiCall(server + '/' + api_base_path + '/object/networks',
                        create_net_object(n[0], n[1], n[2]))
        if resp is None:
            networks = fmc_cfg.fmc.GetApiCall(server + '/' + api_base_path + '/object/networks')
            try:
                for net in networks['items']:
                    if net['name'] == n[0]:
                        object_group['objects'].append(addNetObject(net['name'], net['id']))
            except Exception as e:
                print(e)
        object_group['objects'].append(addNetObject(resp['name'], resp['id']))
    return fmc_cfg.fmc.PostApiCall(server + '/' + api_base_path + '/object/networkgroups', object_group)


if __name__ == '__main__':
    # Read in file with parsing
    # Create global dictionary
    with open('groups.csv', 'r', encoding='utf-8-sig') as c:
        csv = c.readlines()
    objects = {}
    group = ''
    for c in csv:
        split = c.split(',')
        if split[0] != '':
            group = split[0].strip()
            objects.update({group: []})
        if split[3].endswith('\n'):
            split[3] = split[3][:-1]
        objects[group].append([split[1], split[2], split[3]])
    for k, v in objects.items():
        create_full_group(k, v)
    # net = fmc.PostApiCall(fmc.server + '/' + fmc.api_base_path + '/object/networks', net_obj)
    # obj = fmc.GetApiCall(fmc.server + '/' + fmc.api_base_path + '/object/networks')
    # net = fmc.PostApiCall(fmc.server + '/' + fmc.api_base_path + '/object/networkgroups', net_group)