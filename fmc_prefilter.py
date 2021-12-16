import fmc_api
import fmc_cfg
import fmc_groups

server = fmc_cfg.fmc.server
api_base_path = fmc_cfg.fmc.api_base_path

policies = []


def get_net_group(name):
    groups = fmc_groups.get_net_groups()
    for g in groups['items']:
        if g['name'] == name:
            return g
    networks = fmc_groups.get_net_objects()
    for n in networks['items']:
        if n['name'] == name:
            return n
    hosts = fmc_groups.get_hosts_objects()
    for h in hosts['items']:
        if h['name'] == name:
            return h
    fqdns = fmc_groups.get_fqdn_objects()
    for f in fqdns['items']:
        if f['name'] == name:
            return f


def get_policy_id(name):
    get_prefilter_policies()
    for p in policies:
        if p['name'] == name:
            return p['id']


def make_rule_json(name, source, dest, action):
    source_net = get_net_group(source)
    dest_net = get_net_group(dest)
    return {
        'name': name,
        'type': 'PrefilterRule',
        'sourceNetworks': {'objects': [source_net]},
        'destinationNetworks': {'objects': [dest_net]},
        'action': action,
        'ruleType': 'PREFILTER',
        'enabled': True
    }


def create_prefilter_rule(policy_name, name, source, dest, action):
    pol_id = get_policy_id(policy_name)
    if not pol_id:
        create_prefilter_policy(policy_name, 'Script Generated Prefilter Policy')
        pol_id = get_policy_id(policy_name)
    return fmc_cfg.fmc.PostApiCall(server + '/' + api_base_path + '/policy/prefilterpolicies/' +
                           pol_id + '/prefilterrules',
                           make_rule_json(name, source, dest, action))


def make_policy_json(name, des):
    return {
        'name': name,
        'type': 'PrefilterPolicy',
        'description': des
    }


def create_prefilter_policy(name, des):
    return fmc_cfg.fmc.PostApiCall(server + '/' + api_base_path + '/policy/prefilterpolicies',
                           make_policy_json(name, des))


def get_prefilter_policies():
    pol = fmc_cfg.fmc.GetApiCall(server + '/' + api_base_path + '/policy/prefilterpolicies')
    for p in pol['items']:
        policies.append({'name': p['name'], 'id': p['id']})


def get_prefilter_policy_rules(name):
    get_prefilter_policies()
    pol_id = ''
    for p in policies:
        if p['name'] == name:
            pol_id = p['id']
    if pol_id != '':
        data = fmc_cfg.fmc.GetApiCall(server + '/' + api_base_path + '/policy/prefilterpolicies/' + pol_id +
                                      '/prefilterrules')
        return fmc_cfg.fmc.GetApiCall(server + '/' + api_base_path + '/policy/prefilterpolicies/' + pol_id +
                                      '/prefilterrules/' + data['items'][0]['id'])


if __name__ == '__main__':
    # data = get_prefilter_policy_rules('test')
    data = create_prefilter_rule('test', 'example-2', 'group-demo2', 'group-demo3', 'ANALYZE')
    # data = create_prefilter_policy('test', 'test pre policy')