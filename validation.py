import requests
import yaml
import json


def updatemxl3fwrules(apikey, networkid, fwrules, syslogDefaultRule=False,
                      suppressprint=False):
    base_url = 'https://api.meraki.com/api/v0'

    calltype = 'MX L3 Firewall'
    puturl = '{0}/networks/{1}/l3FirewallRules'.format(str(base_url),
                                                       str(networkid))
    headers = {
        'x-cisco-meraki-api-key': format(str(apikey)),
        'Content-Type': 'application/json'
    }

    putdata = {'rules': fwrules}

    putdata['syslogDefaultRule'] = syslogDefaultRule
    putdata = json.dumps(putdata)
    dashboard = requests.put(puturl, data=putdata, headers=headers)
    print('')
    print(dashboard)
    print('')
    print(dashboard.text)
    return dashboard.status_code


def load_toc():
    toc = requests.get('https://raw.githubusercontent.com/RMON-Networks/rmon_fw_rule_definitions/master/TOC.YAML')
    toc = yaml.load(toc.text)
    for x in toc:
        print(x)
    print('')
    return toc


def check_yaml(url, meraki_api_key, net_id, all_rules):
    rules = requests.get(url)
    rules = yaml.load_all(rules.text)
    for rule in rules:
        temp_rules = list(all_rules)
        temp_rules.append(rule)
        res = updatemxl3fwrules(meraki_api_key, net_id, temp_rules,
                                syslogDefaultRule=False)
        if res == 200:
            all_rules.append(rule)
    return all_rules


def run_module():
    meraki_api_key = input('Enter Meraki API Key: ')
    net_id = input('Enter Meraki Net ID: ')
    toc = load_toc()
    base_url = 'https://raw.githubusercontent.com/RMON-Networks/rmon_fw_rule_definitions/master/FirewallRules/'
    all_rules = []
    for x in toc:
        url = base_url + x
        print('')
        print('')
        print(x)
        all_rules = check_yaml(url, meraki_api_key, net_id, all_rules)


def main():
    run_module()


if __name__ == '__main__':
    main()
