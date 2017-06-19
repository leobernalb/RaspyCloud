import threading
from coremodules.sysRp import SysRp


event = threading.Event()

class ThreadOverHead(threading.Thread):
    def __init__(self, token):
        threading.Thread.__init__(self)
        self.o = SysRp()
        self.token = token

    def run(self):
        self.o.mountImgCompress(self.token)
        event.set()


class Thread(threading.Thread):
    def __init__(self, token, hostname, ip):
        threading.Thread.__init__(self)
        self.o = SysRp()
        self.token = token
        self. hostname = hostname
        self.ip = ip

    def run(self):
        self.o.createPartition(self.ip)
        self.o.reboot(self.token, self.hostname)
        self.o.formatFileSystemAndMount(self.ip)
        event.wait()
        self.o.sendAndDecompress(self.ip)
        self.o.changePartition(self.ip, False)
        print(self.o.reboot(self.token, self.hostname))


class ThreadRescuteMode(threading.Thread):
    def __init__(self, token, hostname, ip, mode):
        threading.Thread.__init__(self)
        self.o = SysRp()
        self.token = token
        self. hostname = hostname
        self.ip = ip
        self.mode = mode

    def run(self):
        self.o.changePartition(self.ip, self.mode)
        print(self.o.reboot(self.token, self.hostname))
