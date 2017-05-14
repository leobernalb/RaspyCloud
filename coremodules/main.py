from coremodules.arp import Arp
from coremodules.rpCloud import RpCloud
from coremodules.sysRp import SysRp
from coremodules.threads import Thread
from coremodules.threads import ThreadOverHead
from coremodules.threads import ThreadRescuteMode


class Run(object):
    def __init__(self, token):
        self.rP = RpCloud()
        self.arp = Arp()
        self.sys = SysRp()
        # Inicia la app
        self.start(token)

    def start(self, token):

        # Consultamos el JSON actual (peticion ARP)
        generatedJson = self.sys.generateJson(token)

        # Ejecuta un hilo para montar y comprimir la imagen en el servidor
        threadOverHead1 = ThreadOverHead(token)
        threadOverHead1.start()

        for pi in generatedJson.get("raspberryPi"):
            # Crea un hilo por cada raspberryPi
            hThread1 = Thread(token, pi.get("hostname"), pi.get("ip"))
            hThread1.start()
        return "Done"


class Rescute(object):
    def __init__(self, token):
        self.rP = RpCloud()
        self.arp = Arp()
        self.sys = SysRp()
        # Inicia la app
        self.start(token)

    def start(self, token):

        # Consultamos el JSON actual (peticion ARP)
        generatedJson = self.sys.generateJson(token)

        for pi in generatedJson.get("raspberryPi"):
            # Crea un hilo por cada raspberryPi
            hThreadRescute = ThreadRescuteMode(token, pi.get("hostname"), pi.get("ip"))
            hThreadRescute.start()
        return "Done"
