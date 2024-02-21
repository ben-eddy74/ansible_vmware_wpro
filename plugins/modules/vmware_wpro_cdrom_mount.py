#!/usr/bin/python

# Copyright: (c) 2023, Eddy Vermoen (@ben-eddy74)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vmware_wpro_cdrom_mount

short_description: Mount a cdrom or iso file to a virtual machine
version_added: "1.0.0"

description: This module mounts a virtual disk to a virtual machine

options:
    name:
        description: The name of the virtual machine to attach the virtual disk to
        required: true
        type: str
    path:
        description: The path to iso file, driveletter or device-name
        required: true
        type: str
    devicehost:
        description: Set the device host, for example sata0:1
        required: true
        type: str
    devicetype:
        description: Set the device type
        type: str
        default: cdrom-image
    present:
        description: Present the device to the GUI and to the virtual machine
        type: bool
        default: true
    startConnected:
        description: Device is connected at bootup of VM
        type: bool
        default: true

author:
    - Eddy Vermoen (@ben-eddy74)
'''

EXAMPLES = r'''
- name: Get VM Details
  ben_eddy74.vmware_wpro.vmware_wpro_vdisk_mount:
    name: my virtual machine
    path: c:\\vmware\\my virtual machine\\windows.iso
    devicehost: sata0:1
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
        path=dict(type='str', required=True),
        devicehost=dict(type='str', required=True),
        deviceType =dict(type='str', default="cdrom-image"),
        present=dict(type='bool', default=True),
        startConnected=dict(type='bool', default=True)
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
    config[module.params['devicehost'] + '.fileName'] = module.params['path']
    config[module.params['devicehost'] + '.deviceType'] = module.params['deviceType']
    config[module.params['devicehost'] + '.present'] = "TRUE" if module.params['present'] else "FALSE"
    config[module.params['devicehost'] + '.startConnected'] = "TRUE" if module.params['startConnected'] else "FALSE"
    
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