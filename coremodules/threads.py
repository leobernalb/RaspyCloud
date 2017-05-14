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
        self.o.createPartition(self.token, self.ip)
        self.o.reboot(self.token, self.hostname)
        self.o.formatFileSystemAndMount(self.token, self.ip)
        event.wait()
        self.o.sendAndDecompress(self.token, self.ip)
        self.o.changePartition(self.token, self.ip, False)
        print(self.o.reboot(self.token, self.hostname))
        #print(self.o.checkMachine(self.ip))


class ThreadRescuteMode(threading.Thread):
    def __init__(self, token, hostname, ip):
        threading.Thread.__init__(self)
        self.o = SysRp()
        self.token = token
        self. hostname = hostname
        self.ip = ip

    def run(self):
        self.o.changePartition(self.token, self.ip, True)
        print(self.o.reboot(self.token, self.hostname))
