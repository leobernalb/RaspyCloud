import threading
from coremodules.sysRp import SysRp


event = threading.Event()

class ThreadOverHead(threading.Thread):
    def __init__(self, token, img):
        threading.Thread.__init__(self)
        self.o = SysRp()
        self.token = token
        self.img = img

    def run(self):
        self.o.mountImgCompress(self.token, self.img)
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
