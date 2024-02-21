#!/usr/bin/python

# Copyright: (c) 2023, Eddy Vermoen (@ben-eddy74)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vmware_wpro_vm_power

short_description: Virtual machine power commands
version_added: "1.0.0"

description: This module contains power commands

options:
    name:
        description: The name of the virtual machine
        required: true
        type: str
    state:
        description:
            - If C(started), the virtual machine will be started
            - If C(stopped), the virtual machine will be stoppped
            - If C(reset), the virtual machine will be reset
            - If C(paused), the virtual machine will be paused
            - If C(unpaused), the virtual machine will be unpaused
        required: true
        type: str
    parameter:
        description: Additional parameter depending on desired state
            - started: gui, nogui (default)
            - stopped: hard, soft (default)
            - reset: hard, soft (default)
author:
    - Eddy Vermoen (@ben-eddy74)
'''

EXAMPLES = r'''
- name: Start VM
  ben_eddy74.vmware_wpro.vmware_wpro_vm_power:
    name: My Windows Server
    state: started

- name: Force VM to stop
  ben_eddy74.vmware_wpro.vmware_wpro_vm_power:
    name: My Windows Server
    state: stopped
    parameter: hard
'''

RETURN = r'''
vm:
    description: 
    type: 
    returned: always
    sample: '
        "changed": true,
        "result": "",
        "before: "",
        "after: "",
        "invocation": {
            "module_args": {
            "name": "My Windows Server",
            "state": "stopped",
            "parameter": "hard"
            }
        }
    '
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.ben_eddy74.vmware_wpro.plugins.module_utils.vmware_vm import VM
except:
    from module_utils.vmware_vm import VM

def run_module():

    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=True, choices=['started', 'stopped', 'reset', 'paused','unpaused']),
        startwith=dict(type='str', choices=['gui', 'nogui'], default='nogui'),
        force=dict(type='bool', default= False)
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    vm = VM(module.params['name'])

    if vm.exists() == False:
        module.fail_json("VM {} not found".format(module.params['name']))

    expected_state = module.params['state'].casefold()
    current_state = vm.getPowerState()
    forced = 'hard' if module.params['force'] == True else 'soft'

    result['before'] = current_state
    result['after'] = expected_state

    if module.check_mode:
        result['changed'] = (expected_state != current_state)
        module.exit_json(**result)

    if current_state == 'started' and expected_state == 'unpaused':
        module.exit_json(**result)

    if current_state != expected_state:
        if expected_state == 'started':
            result['msg'] = vm.start(module.params['startwith']).strip('\r\n')
        elif expected_state == 'stopped':
            result['msg'] = vm.stop(forced).strip('\r\n')
        elif expected_state == 'reset':
            result['msg'] = vm.reset(forced).strip('\r\n')
        elif expected_state == 'paused':
            result['msg'] = vm.pause().strip('\r\n')
        elif expected_state == 'unpaused':
            result['msg'] = vm.unpause().strip('\r\n')
        else:
            module.fail_json("Unkown state")
        
        if "Error" in result['msg']:
            module.fail_json(result['msg'])
        else:          
            result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()