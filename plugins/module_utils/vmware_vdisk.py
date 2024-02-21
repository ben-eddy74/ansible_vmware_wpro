import os.path

try:
    from ansible_collections.ben_eddy74.vmware_wpro.plugins.module_utils.vmware import VMWare
except:
    from module_utils.vmware import VMWare

class VDisk(VMWare):
    
    def __init__(self, vmdk) -> None:
        super().__init__()
        self.vmdk = vmdk

    def exists(self):
        vmdk = self.towslpath(self.vmdk) if self.wsl else self.vmdk
        result = True if os.path.isfile(vmdk) else False
        return result;

    def create(self, size, adaptertype= 'lsilogic', disktype= 0):
        result = self.vdiskmanager("-c -a {0} -s {1} -t {2} \"{3}\"".format(adaptertype, size, disktype, self.vmdk))
        return result
    
    def shrink(self):
        result = self.vdiskmanager("-k \"{0}\"".format(self.vmdk))
        return result

    def defragment(self):
        result = self.vdiskmanager("-d \"{0}\"".format(self.vmdk))
        return result

if __name__ == '__main__':
    vdisk= VDisk()