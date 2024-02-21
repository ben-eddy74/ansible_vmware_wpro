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
    cmd:
        description: Specify the operation
        required: true
        type: str
        choices: create, defragment, shrink

author:
    - Eddy Vermoen (@ben-eddy74)
'''

EXAMPLES = r'''
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
        vmdk=dict(type='str', required=True),
        cmd=dict(type='str', required=True, choices=["create", "defragment", "shrink"]),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()