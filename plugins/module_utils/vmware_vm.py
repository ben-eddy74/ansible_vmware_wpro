import os.path

try:
    from ansible_collections.ben_eddy74.vmware_wpro.plugins.module_utils.vmware import VMWare
except:
    from module_utils.vmware import VMWare

class VM(VMWare):
    
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.vmpath = self.__getPath()

    # State information
    
    def facts(self):
        return dict(
            name= self.name,
            vmx= self.vmpath,
            config= self.getVmxConfig(self.vmpath)
        )

    def exists(self):
        return self.vmpath != ''
    
    def getPath(self):
        return self.vmpath
    
    def __getPath(self):
        inventory = self.getInventory()
        vmxfile = '/' + self.name + ".vmx"
        if self.wsl:
            vmxfile = vmxfile.replace("/", "\\")

        for key, value in inventory.items():
            if vmxfile.casefold() in value.casefold():
                return value.casefold()
        
        defaultvmpath = self.getPreferences()['prefvmx.defaultVMPath']
        vmpath = "{0}/{1}/{1}.vmx".format(defaultvmpath, self.name)
        if self.wsl:
            vmpathwsl = self.towslpath(vmpath)
            if os.path.isfile(vmpathwsl):
                return vmpath.replace("/", "\\");
        else:
            if os.path.isfile(vmpath):
                return vmpath;
        return ''
    
    def getPowerState(self):
        running = self.getRunningvms()
        for key, value in running.items():
            if value.casefold() == self.vmpath.casefold():
                #Test to see if VM is paused
                pausetest = self.execute('-gu guest -gp guest listProcessesInGuest')
                if 'virtual machine is paused' in pausetest:
                    return 'paused'
                return "started"
        return "stopped"
    
    # Power commands

    def start(self, param= 'nogui'):
        return self.execute('start', param);

    def stop(self, param= 'soft'):
        return self.execute('stop', param);

    def reset(self, param= 'soft'):
        return self.execute('reset', param);

    def suspend(self, param= 'soft'):
        return self.execute('suspend', param);

    def pause(self):
        return self.execute('pause');

    def unpause(self):
        return self.execute('unpause');

    # Snapshot commands
    def getSnapshots(self):
        return self.execute('listSnapshots')

    def createSnapshot(self, name):
        return self.execute('snapshot', name)

    def deleteSnapshot(self, name):
        return self.execute('deleteSnapshot', name)

    def revertSnapshot(self, name):
        return self.execute('revertToSnapshot', name)

    # General commands

    def cloneTo(self, targetname, option= 'full', snapshot= ''):
        if self.exists() == False:
            raise Exception("Template VM does not exist")
        targetvmpath = self.getPreferences()['prefvmx.defaultVMPath']
        targetvmpath = "{0}/{1}/{1}.vmx".format(targetvmpath, targetname)
        if self.wsl:
            targetvmpath = targetvmpath.replace("/", "\\")
        cmd = ' '.join(['clone', '"{}"'.format(self.vmpath), '"{}"'.format(targetvmpath), '-cloneName="{}"'.format(targetname), option])
        if snapshot != '':
            cmd = '%s -snapshot="%s"' % (cmd, snapshot)
        result = self.vmrun(cmd)
        return result

    # Helper function to execute vmrun commands
    def execute(self, command, parameter= ''):
        result = self.vmrun(' '.join([command, '"{}" {}'.format(self.vmpath, parameter)]))
        return result.strip('\n').replace('\r', '');

if __name__ == '__main__':
    vm= VM('Test')
    #print(vmware.isWsl())
    #print(vmware.getRegistry())
    #print(vmware.getPath())
    #print(vmware.getConfigfiles())
    #print(vmware.getRunningvms())
    print(vm.exists())
    print(vm.getPath())
    print(vm.getPowerState())
    #print(vm.cloneTo("test"))