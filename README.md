# Ansible Collection - ben_eddy74.vmware_wpro

Documentation for the collection.

## Modules

vmware_wpro_info:
    provides information about VMware Workstation Pro
    options:
        inventory: yes -> include inventory data
        preferences: yes -> include preferences/settings

vmware_wpro_clone:
    clone a virtual machine to a new virtual machine
    options:
        name: name of the new vm
        template: name of the vm to be cloned
        snapshot: clone a snapshot of template
        clone: full or linked

vmware_wpro_vm_power:
    power commands
    options:
        name: name of the vm to manage
        state: started | stopped | reset | paused | unpaused
        startwith: gui, nogui (used by started)
        force: true, false (used by stopped and reset)

## Dev

To test a module during development, use the following command from the collection folder:

```shell
ANSIBLE_LIBRARY=./plugins ansible -m vmware_wpro_info localhost
```

To provide arguments:

```shell
ANSIBLE_LIBRARY=./plugins ansible -m vmware_wpro_info -a "inventory=yes preferences=yes" localhost
```

In case of modifications in module_utils, deploy the collection first before testing the module:

```shell
ansible-galaxy collection build --force
ansible-galaxy collection install . --force
```

To avoid going through Ansible, another way is to create an arguments file in the tests folder and run the following command from the collection's plugins folder:

```shell
 python -m modules.vmware_wpro_info ../tests/info.json  | jq
 ```

## Preprod

To test a module from a playbook, build and install the module first:

```shell
ansible-galaxy collection build --force
ansible-galaxy collection install . --force
```

Then the module can be used from a playbook:

```shell
ansible-playbook test.yml -vvv
```


https://www.sanbarrow.com/vmx.html
