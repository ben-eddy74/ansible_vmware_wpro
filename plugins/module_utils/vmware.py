import subprocess, re

class VMWare:
    def __init__(self) -> None:
        self.wsl = self.__isWsl()
        self.registry = self.__registry()
        self.configfiles = self.__configfiles()
        self.runningvms = self.__runningvms()

    # WSL support
    def isWsl(self):
        return self.wsl

    def towslpath(self, path):
        """Converts a Windows path to the corresponding WSL path"""
        return path.lower().replace('\\', '/').replace('c:', '/mnt/c')

    def __isWsl(self):
        process = subprocess.run('whereis powershell.exe', capture_output=True, shell= True)
        return process.stdout.decode().strip('\r\n') == 'powershell.exe: /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'
    
    # VMware keys from Windows registry
    def getRegistry(self):
        return self.registry
    
    def __registry(self):
        result = dict()
        if self.wsl == False:
            return result
        reg = subprocess.run('reg.exe query "HKLM\SOFTWARE\WOW6432Node\VMware, Inc.\VMware Workstation"', capture_output= True, shell= True)
        for line in reg.stdout.decode().split('\r\n'):
            if '    ' in line:
                values = line.split('   ')
                result[values[1].strip(' ')] = values[3].strip(' ')
        return result

    # Information
    def getInstallPath(self):
        if(self.wsl):
            return self.registry['InstallPath']
        else:
            return '' #TODO: VMware on Linux support

    # Get inventory and preferences
    def getInventory(self):
        inifile = self.configfiles['inventory']
        return self.___dict_from_ini(inifile)

    def getPreferences(self):
        inifile = self.configfiles['preferences']
        return self.___dict_from_ini(inifile)

    def getConfigfiles(self):
        return self.configfiles
    
    def __configfiles(self):
        result = dict()
        if self.wsl:
            appdata = subprocess.run('cmd.exe /c echo %appdata%', capture_output=True, shell= True)
            result['appdata'] = appdata.stdout.decode().strip('\r\n') + '\\VMware\\'
        else:
            pass #TODO: VMware on Linux support

        result['preferences'] = result['appdata'] + "preferences.ini"
        result['inventory'] = result['appdata'] + "inventory.vmls"
        return result;

    # Get running VM's
    def getRunningvms(self):
        return self.runningvms
    
    def __runningvms(self):
        result = dict()
        running = self.vmrun("list")
        for line in running.split('\r\n'):
            if 'Total running VMs' not in line and line != '':
                name = re.findall('.*\\\\(.*)\.vmx', line) #TODO: or forward slash for linux path
                result[name[0]] = line
        return result
    
    # Read vmx configuration and return as a dict
    def getVmxConfig(self, vmxpath):
        return self.___dict_from_ini(vmxpath)

    # Helper function to read an ini file into a dict
    def ___dict_from_ini(self, inifile):
        """Helper function to read an INI file into a dictionary"""
        result = dict()
        if self.wsl:
            inifile = self.towslpath(inifile)
        with open(inifile, 'r') as inifile:
            for line in inifile:
                kv = line.strip('\n').split('=')
                result[kv[0].strip(' ')] = kv[1].strip(' ').strip('"')
        return result

    # Write vmx configuration to ini file
    def setVmxConfig(self, config):
        currentconfig = self.getVmxConfig(self.vmpath)
        for k, v in config.items():
            currentconfig[k] = v

        return self.___dict_to_ini(self.vmpath, currentconfig)
    
    # Helper function to write an ini file into a dict
    def ___dict_to_ini(self, inifile, config):
        if self.wsl:
            inifile = self.towslpath(inifile)
        with open(inifile, 'w') as content:
            for k, v in sorted(config.items()):
                line = '{0} = "{1}"'.format(k, v)
                print(line, file= content)

    # VMware tools wrappers
    def vmrun(self,  args):        
        runnable = '';
        if self.wsl:
            runnable = '"{0}{1}" {2}'.format(self.towslpath(self.registry['InstallPath']), 'vmrun.exe', args)
        else:
            pass #TODO: VMware on Linux support
        result = subprocess.run(runnable, capture_output=True, shell= True)
        return result.stdout.decode()

    def vdiskmanager(self, args):
        runnable = '';
        if self.wsl:
            runnable = '"{0}{1}" {2}'.format(self.towslpath(self.registry['InstallPath']), 'vmware-vdiskmanager.exe', args)
        else:
            pass #TODO: VMware on Linux support
        result = subprocess.run(runnable, capture_output=True, shell= True)
        if result.stderr.decode() != "":
            return result.stderr.decode()
        
        return result.stdout.decode()
    
if __name__ == '__main__':
    vmware= VMWare()
    #print(vmware.isWsl())
    #print(vmware.getRegistry())
    #print(vmware.getPath())
    #print(vmware.getConfigfiles())
    #print(vmware.getRunningvms())
    #print(vmware.getInventory())