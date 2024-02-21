#!/usr/bin/python

# Copyright: (c) 2023, Eddy Vermoen (@ben-eddy74)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: vmware_wpro_vm

short_description: Virtual machine management
version_added: "1.0.0"

description: This module returns information about a virtual machine

options:
    name:
        description: The name of the virtual machine
        required: true
        type: str

author:
    - Eddy Vermoen (@ben-eddy74)
'''

EXAMPLES = r'''
- name: Get VM Details
  ben_eddy74.vmware_wpro.vmware_wpro_vm:
    name: My Windows Server
'''

RETURN = r'''
"vm": {
    "config": {
        ".encoding": "UTF-8",
        "cleanShutdown": "TRUE",
        "config.version": "8",
        "cpuid.coresPerSocket": "4",
        "displayName": "My Windows Server",
        "ehci.pciSlotNumber": "34",
        "ehci.present": "TRUE",
        "ethernet0.addressType": "generated",
        "ethernet0.connectionType": "nat",
        "ethernet0.generatedAddress": "00:0c:29:7a:42:c7",
        "ethernet0.generatedAddressOffset": "0",
        "ethernet0.pciSlotNumber": "192",
        "ethernet0.present": "TRUE",
        "ethernet0.virtualDev": "e1000e",
        "extendedConfigFile": "My Windows Server.vmxf",
        "floppy0.present": "FALSE",
        "guestInfo.detailed.data": "architecture",
        "guestOS": "windows8srv-64",
        "guestOS.detailed.data": "",
        "hpet0.present": "TRUE",
        "mem.hotadd": "TRUE",
        "memsize": "16384",
        "monitor.phys_bits_used": "45",
        "numvcpus": "8",
        "nvram": "My Windows Server.nvram",
        "pciBridge0.pciSlotNumber": "17",
        "pciBridge0.present": "TRUE",
        "pciBridge4.functions": "8",
        "pciBridge4.pciSlotNumber": "21",
        "pciBridge4.present": "TRUE",
        "pciBridge4.virtualDev": "pcieRootPort",
        "pciBridge5.functions": "8",
        "pciBridge5.pciSlotNumber": "22",
        "pciBridge5.present": "TRUE",
        "pciBridge5.virtualDev": "pcieRootPort",
        "pciBridge6.functions": "8",
        "pciBridge6.pciSlotNumber": "23",
        "pciBridge6.present": "TRUE",
        "pciBridge6.virtualDev": "pcieRootPort",
        "pciBridge7.functions": "8",
        "pciBridge7.pciSlotNumber": "24",
        "pciBridge7.present": "TRUE",
        "pciBridge7.virtualDev": "pcieRootPort",
        "policy.vm.mvmtid": "",
        "powerType.powerOff": "soft",
        "powerType.powerOn": "soft",
        "powerType.reset": "soft",
        "powerType.suspend": "soft",
        "sata0.pciSlotNumber": "36",
        "sata0.present": "TRUE",
        "sata0:0.connectionStatus": "4",
        "sata0:0.deviceType": "cdrom-image",
        "sata0:0.fileName": "C:\\Software\\Microsoft\\Windows_server_2019.iso",
        "sata0:0.present": "TRUE",
        "sata0:1.deviceType": "cdrom-image",
        "sata0:1.fileName": "C:\\Software\\Microsoft\\SQL_Server_2019.iso",
        "sata0:1.startConnected": "TRUE",
        "scsi0.pciSlotNumber": "160",
        "scsi0.present": "TRUE",
        "scsi0.sasWWID": "50 05 05 6f 3a b4 e1 60",
        "scsi0.virtualDev": "lsisas1068",
        "scsi0:0.fileName": "Windows Server 2019.vmdk",
        "scsi0:0.present": "TRUE",
        "scsi0:0.redo": "",
        "softPowerOff": "FALSE",
        "sound.autoDetect": "TRUE",
        "sound.fileName": "-1",
        "sound.pciSlotNumber": "33",
        "sound.present": "TRUE",
        "sound.virtualDev": "hdaudio",
        "svga.guestBackedPrimaryAware": "TRUE",
        "svga.vramSize": "268435456",
        "tools.remindInstall": "FALSE",
        "tools.syncTime": "FALSE",
        "tools.upgrade.policy": "useGlobal",
        "toolsInstallManager.lastInstallError": "0",
        "toolsInstallManager.updateCounter": "4",
        "usb.pciSlotNumber": "32",
        "usb.present": "TRUE",
        "usb_xhci.pciSlotNumber": "224",
        "usb_xhci.present": "TRUE",
        "usb_xhci:4.deviceType": "hid",
        "usb_xhci:4.parent": "-1",
        "usb_xhci:4.port": "4",
        "usb_xhci:4.present": "TRUE",
        "uuid.bios": "56 4d 11 bf 3a b4 e1 66-c6 c6 56 64 46 7a 42 c7",
        "uuid.location": "56 4d 11 bf 3a b4 e1 66-c6 c6 56 64 46 7a 42 c7",
        "vc.uuid": "",
        "vcpu.hotadd": "TRUE",
        "virtualHW.productCompatibility": "hosted",
        "virtualHW.version": "19",
        "vm.genid": "-3068161240631987066",
        "vm.genidX": "-4902902128106419388",
        "vmci0.id": "349967709",
        "vmci0.pciSlotNumber": "35",
        "vmci0.present": "TRUE",
        "vmotion.checkpointFBSize": "4194304",
        "vmotion.checkpointSVGAPrimarySize": "268435456",
        "vmotion.svga.graphicsMemoryKB": "262144",
        "vmotion.svga.mobMaxSize": "268435456"
    },
    "name": "My Windows Server",
    "vmx": "c:\\vmware\\My Windows Server\\My Windows Server.vmx"
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.ben_eddy74.vmware_wpro.plugins.module_utils.vmware_vm import VM
except:
    from module_utils.vmware_vm import VM

def run_module():

    module_args = dict(
        name=dict(type='str', required=True),
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

    if module.check_mode:
        module.exit_json(**result)

    result['vm'] = vm.facts()
    
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()