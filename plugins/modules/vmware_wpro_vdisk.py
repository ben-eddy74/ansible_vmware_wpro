#!/usr/bin/python

# Copyright: (c) 2023, Eddy Vermoen (@ben-eddy74)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vmware_wpro_vdisk

short_description: Virtual Disk management
version_added: "1.0.0"

description: This module manages virtual disks

options:
    vmdk:
        description: The path of the virtual disk file
        required: true
        type: str
    create:
        description: Create a new virtual disk
        type: dict
        options:
            adapter:
                descripion: Adapter type
                type: str
                choices: ide, buslogic, lsilogic
                default: lsilogic
            size:
                descripion: Disk size, for example 500MB or 16GB
                type: str
                required: true
            disktype:
                descripion: Specifies the disk type
                type: int
                choices:
                    0: single growable virtual disk
                    1: growable virtual disk split into multiple files
                    2: preallocated virtual disk
                    3: preallocated virtual disk split into multiple files
                default: 0
    cmd:
        description: Speficies disk operation
        type: str
        choices: defragment, shrink

author:
    - Eddy Vermoen (@ben-eddy74)
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.ben_eddy74.vmware_wpro.plugins.module_utils.vmware_vdisk import VDisk
except:
    from module_utils.vmware_vdisk import VDisk

def run_module():

    module_args = dict(
        vmdk=dict(type='str', required=True),
        create=dict(type='dict', options=dict(
            adapter=dict(type='str', choices=["ide", "buslogic", "lsilogic"], default='lsilogic'),
            size=dict(type='str', required=True),
            disktype=dict(type='int', choices=[0,1,2,3], default= 0)
            )
        ),
        cmd=dict(type='str', choices=["defragment", "shrink"]),
    )

    result = dict(
        changed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        mutually_exclusive=[
            ("create", "cmd")
        ],
        supports_check_mode=True
    )

    vdisk = VDisk(module.params["vmdk"])
    result['exists'] = vdisk.exists()

    if module.check_mode:
        module.exit_json(**result)

    if module.params['create'] != None:
        result['vdisk'] = vdisk.create(size= module.params['create']['size'], adaptertype= module.params['create']['adapter'], disktype= module.params['create']['disktype'])
        result['changed'] = 'Virtual disk creation successful' in result['vdisk']
    elif module.params['cmd'] == 'shrink':
        result['vdisk'] = vdisk.shrink()
        result['changed'] = 'Shrink completed successfully.' in result['vdisk']
    elif module.params['cmd'] == 'defragment':
        result['vdisk'] = vdisk.defragment()
        result['changed'] = 'Defragmentation completed successfully.' in result['vdisk']
    else:
        module.fail_json("Unknown command")

    if 'Failed' in result['vdisk']:
        module.fail_json(result['vdisk'])

    result['changed'] = 'Virtual disk creation successful' in result['vdisk']
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()