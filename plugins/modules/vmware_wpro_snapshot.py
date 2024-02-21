#!/usr/bin/python

# Copyright: (c) 2023, Eddy Vermoen (@ben-eddy74)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vmware_wpro_snapshot

short_description: Manage snapshots of virtual machines
version_added: "1.0.0"

description: This module manages snapshots of virtual machines

options:
    name:
        description: Name of the virtual machine
        required: true
        type: string
    action:
        description: Action to execute. Can be list, snapshot, delete, revert
        required: true
        type: string
        default: list
    snapshot:
        description: Snapshot name
        required: true van action is create, delete or revert
        type: string

author:
    - Eddy Vermoen (@ben-eddy74)
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''

import os
from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.ben_eddy74.vmware_wpro.plugins.module_utils.vmware_vm import VM
except:
    from module_utils.vmware_vm import VM

def run_module():

    module_args = dict(
        name=dict(type='str', required=True),
        action=dict(type='str', default="list", choices=["list", "create", "delete", "revert"]),
        snapshot=dict(type='str', required=False) #TODO: required when action is "create", "delete", "revert"
    )

    result = dict(
        changed=False,
        snapshots= []
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ('action', 'create', (['snapshot'])),
            ('action', 'delete', (['snapshot'])),
            ('action', 'revert', (['snapshot']))
        ]
    )

    vm = VM(module.params['name'])
    snapshots = vm.getSnapshots().split(os.linesep)

    total_snapshots = snapshots.pop(0)
    result['total'] = total_snapshots
    result['snapshots'] = snapshots

    action = module.params['action']

    if action == 'create' and module.params['snapshot'] in snapshots:
        module.exit_json(**result)
    
    if module.check_mode or action == 'list':
        module.exit_json(**result)

    if action == 'create':
        vm.createSnapshot('"{}"'.format(module.params['snapshot']))
        result['changed'] = True

    if action == 'delete' and module.params['snapshot'] in snapshots:
        vm.deleteSnapshot('"{}"'.format(module.params['snapshot']))
        result['changed'] = True

    if action == 'revert' and module.params['snapshot'] in snapshots:
        vm.revertSnapshot('"{}"'.format(module.params['snapshot']))
        result['changed'] = True

    snapshots = vm.getSnapshots().split(os.linesep)
    total_snapshots = snapshots.pop(0)
    result['total'] = total_snapshots
    result['snapshots'] = snapshots

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()