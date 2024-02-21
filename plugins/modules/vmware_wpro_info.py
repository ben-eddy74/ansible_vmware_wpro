#!/usr/bin/python

# Copyright: (c) 2023, Eddy Vermoen (@ben-eddy74)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vmware_wpro_info

short_description: Information about VMware Workstation Pro
version_added: "1.0.0"

description: This module returns information about local VMware Workstation Pro installation,
             like installation path, product version and running virtual machines.
             VMware inventory and preferences can be included using the appropriate options.
             Windows Subsystem for Linux environment is supported, 
             which means you can use Ansible and this collection to manage VMware on the same machine.

options:
    inventory:
        description: Include the content of VMware inventory
        required: false
        type: bool
    preferences:
        description: Include the content of VMware preferences
        required: false
        type: bool

author:
    - Eddy Vermoen (@ben-eddy74)
'''

EXAMPLES = r'''
# Get information about VMware Workstation pro
- name: Get VMware Workstation Pro information
  ben_eddy74.vmware_wpro.vmware_wpro_info:

# Include inventory
- name: Get VMware Workstation Pro information with inventory
  ben_eddy74.vmware_wpro.vmware_wpro_info:
    inventory: true

# Include preferences
- name: Get VMware Workstation Pro information with preferences
  ben_eddy74.vmware_wpro.vmware_wpro_info:
    preferences: true
'''

RETURN = r'''
vmware-wpro:
    description: Information about VMware Workstation Pro
    type: collection
    returned: always
    sample: '
        "changed": false,
        "vmware-wpro": {
            "configfiles": {
                "appdata": "C:\\Users\\Admin\\AppData\\Roaming\\VMware\\",
                "inventory": "C:\\Users\\Admin\\AppData\\Roaming\\VMware\\inventory.vmls",
                "preferences": "C:\\Users\\Admin\\AppData\\Roaming\\VMware\\preferences.ini"
            },
            "registry": {
                "InstallPath": "C:\\Program Files (x86)\\VMware\\VMware Workstation\\",
                "InstallPath64": "C:\\Program Files (x86)\\VMware\\VMware Workstation\\x64\\",
                "ProductCode": "{5FC6CE70-EE9B-410E-9BD3-48B2EAC83056}",
                "ProductVersion": "16.2.5.20904516"
            },
            "runningvms": {},
            "wsl": true
        }
    '
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.ben_eddy74.vmware_wpro.plugins.module_utils.vmware import VMWare
except:
    from module_utils.vmware import VMWare

def run_module():

    module_args = dict(
        inventory=dict(type='bool', required=False, default=False),
        preferences=dict(type='bool', required=False, default=False)
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    vminfo = dict()

    vmware = VMWare()
    
    vminfo['wsl'] = vmware.isWsl()
    vminfo['registry'] = vmware.getRegistry()
    vminfo['configfiles'] = vmware.getConfigfiles()
    vminfo['runningvms'] = vmware.getRunningvms()

    if module.params['inventory']:
        vminfo['inventory'] = vmware.getInventory()
    
    if module.params['preferences']:
        vminfo['preferences'] = vmware.getPreferences()
    
    result['vmware-wpro'] = vminfo;

    if module.check_mode:
        module.exit_json(**result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()