#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import csv

DOCUMENTATION = r'''
---
module: parse_csv_to_inv_dict_info

short_description:
  - This module parses a CSV file with headers in order of:
  - host/fqdn,ansible_user,ansible_password,ansible_become_password,group
  - and then creates a dict obj where the primary key is the group for which
  - the host resides. Each group (key) value is a list of host entries


version_added: "1.0.0"

description:
  - This module takes a path as an arguement, and then opens the CSV
  - file and uses CSV_reader to parse through each row of the CSV. The first row
  - (headers) are ignored. A dictionary object is created for each host entry.
  - We take the host group (row[4]) and check if it exists as a key in the return dictionary.
  - If it does not, we create a key/value pair for this group. The key is the group name, the value
  - is an empty list that will be used to place host entry dict objects into.
  - If the key exists (or it was just made), we place a copy of the host_entry dict
  - into the list corresponding to the group.
  - Essentially, we have a return dictionary obj that will appear in a format like below.
  - This can then be used to render a jinja2 template in another task.


options:
    name:
        description: Create dictionary object from CSV file with ordered headers
        required: true
        type: str

author:
    - Thomas Obarowski (@tjobarow)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test parsing CSV file
  my_namespace.my_collection.parse_csv_to_inv_dict_info:
    path: '/home/tobarows/inventory.csv'
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
my_useful_info:
    description: The dictionary containing information about your system.
    type: dict
    returned: always
    sample: {
        'foo': 'bar',
        'answer': 42,
    }
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        path=module.params['path'],
        message='Parsed the CSV to inventory dictionary object.',
        inventory_dict_info={},
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['inventory_dict_info'] = parseCSV(module.params['path'])

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def parseCSV(path: str):
    inventory_dict = {}
    with open(path,'r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_index = 0
        for row in csv_reader:
            if line_index == 0:
                line_index = line_index + 1
                continue
            host_entry = {
                'host_ip':row[0],
                'ansible_user':row[1],
                'ansible_password':row[2],
                'ansible_become_password':row[3]
            }
            if row[4] in inventory_dict:
                inventory_dict[row[4]].append(host_entry.copy())
            else:
                inventory_dict.update({row[4]:[]})
                inventory_dict[row[4]].append(host_entry.copy())
    return inventory_dict

def main():
    run_module()

if __name__ == '__main__':
    main()
