import threading
from coremodules.sysRp import SysRp


class Thread(threading.Thread):
    def __init__(self, token, hostname, ip):
        threading.Thread.__init__(self)
        self.o = SysRp()
        self.token = token
        self. hostname = hostname
        self.ip = ip

    def run(self):

        self.o.createPartition(self.token, self.ip)
        self.o.reboot(self.token, self.hostname)
        self.o.formatFileSystemAndMount(self.token, self.ip)

