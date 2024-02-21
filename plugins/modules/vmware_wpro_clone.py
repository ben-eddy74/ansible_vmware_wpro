#!/usr/bin/python

# Copyright: (c) 2023, Eddy Vermoen (@ben-eddy74)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vmware_wpro_clone

short_description: Clone a virtual machine
version_added: "1.0.0"

description: This module clones a virtual machine to a new virtual machine

options:
    name:
        description: The name of the new virtual machine
        required: true
        type: str
    template:
        description: The name of the virtual machine to be cloned
        required: true
        type: str
    clone:
        description: Create a full or linked clone
        type: str
        choices: full, linked
        default: full
    snapshot:
        description: Name of the template VM snapshot to clone
        type: str

author:
    - Eddy Vermoen (@ben-eddy74)
'''

EXAMPLES = r'''
- name: Clone virtual machine 'Windows Server 2019' to 'My Windows Server'
  ben_eddy74.vmware_wpro.vmware_wpro_clone:
    name: My Windows Server
    template: Windows Server 2019
'''

RETURN = r'''
cloneresult:
    description: Is empty when successful. Otherwise it will contain the error message
    type: bool
    returned: always
    sample: '
    "changed": false,
    "cloneresult": "Error: The snapshot already exists",
    "invocation": {
        "module_args": {
        "name": "Test",
        "template": "Windows Server 2019"
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
        template=dict(type='str', required=True),
        clone=dict(type='str', required=False, choices=['full', 'linked'], default= 'full'),
        snapshot=dict(type='str', required=False, default='')
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    vm = VM(module.params['name'])
    vmtemplate = VM(module.params['template'])
    
    if module.check_mode:
        if vm.exists() == False:
            result['changed'] = True
        module.exit_json(**result)
    
    cloneresult = vmtemplate.cloneTo(targetname= module.params['name'], option= module.params['clone'], snapshot= module.params['snapshot'])
    cloneresult = cloneresult.strip('\r\n')

    result['failed'] = "Error" in cloneresult
    result['changed'] = "" == cloneresult
    result['cloneresult'] = cloneresult

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()