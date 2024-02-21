#!/usr/bin/python

# Copyright: (c) 2023, Eddy Vermoen (@ben-eddy74)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vmware_wpro_vdisk_mount

short_description: Mount a virtual disk to a virtual machine
version_added: "1.0.0"

description: This module mounts a virtual disk to a virtual machine

options:
    name:
        description: The name of the virtual machine to attach the virtual disk to
        required: true
        type: str
    vmdk:
        description: The path of the virtual disk file
        required: true
        type: str
    devicehost:
        description: Set the device host, for example sata0:1
        required: true
        type: str
    present:
        description: Present the disk to the GUI and to the virtual machine
        type: bool
        default: true

author:
    - Eddy Vermoen (@ben-eddy74)
'''

EXAMPLES = r'''
- name: Get VM Details
  ben_eddy74.vmware_wpro.vmware_wpro_vdisk_mount:
    name: my virtual machine
    vmdk: c:\\vmware\\my virtual machine\\disk_d.vmdk
    devicehost: nvme0:1
'''

RETURN = r'''

'''

from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.ben_eddy74.vmware_wpro.plugins.module_utils.vmware_vm import VM
except:
    from module_utils.vmware_vm import VM

def run_module():

    module_args = dict(
        name=dict(type='str', required=True),
        vmdk=dict(type='str', required=True),
        devicehost=dict(type='str', required=True),
        present=dict(type='bool', default=True)
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

    config = dict()
    config[module.params['devicehost'] + '.fileName'] = module.params['vmdk']
    config[module.params['devicehost'] + '.present'] = "TRUE" if module.params['present'] else "FALSE"
    
    currentconfig = vm.facts()["config"]

    for k, v in config.items():
        if k in currentconfig:
            if currentconfig[k] != v:
                currentconfig[k] = v
                result['changed'] = True
        else:
            currentconfig[k] = v
            result['changed'] = True

    if module.check_mode:
        module.exit_json(**result)

    if result['changed']:
        vm.setVmxConfig(config)
    
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()