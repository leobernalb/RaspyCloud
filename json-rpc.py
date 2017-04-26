from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from coremodules.arp import Arp
from coremodules.rpCloud import RpCloud
from coremodules.sysRp import SysRp
from coremodules.threads import Thread
from coremodules.threads import ThreadOverHead


@Request.application
def application(request):
    arpObject = Arp()
    rpCloudObject = RpCloud()
    sysRpObject = SysRp()
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher['scanARP'] = arpObject.scan
    dispatcher['getArpTable'] = arpObject.getTable
    dispatcher['login'] = rpCloudObject.login
    dispatcher['checkPassword'] = rpCloudObject.checkPassword
    dispatcher['checkLogin'] = rpCloudObject.checkLogin
    dispatcher['logout'] = rpCloudObject.logout
    dispatcher['getHostname'] = sysRpObject.getHostname
    dispatcher['reboot'] = sysRpObject.reboot
    dispatcher['setHostname'] = sysRpObject.setHostname
    dispatcher['generateJson'] = sysRpObject.generateJson
    dispatcher['storageJson'] = sysRpObject.storageJson


    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


#if __name__ == '__main__':
#    run_simple('localhost', 8001, application)


class Run(object):
    def __init__(self, token):
        self.rP = RpCloud()
        self.arp = Arp()
        self.sys = SysRp()
        # Inicia la app
        self.start(token)

    def start(self, token):
        checked = self.rP.checkLogin(token)
        if(checked):
            # Consultamos el JSON actual (peticion ARP)
            generatedJson = self.sys.generateJson(token)

            # Ejecuta un hilo para montar y comprimir la imagen en el servidor
            threadOverHead1 = ThreadOverHead(token, "/mnt/img/minimalRaspyCloud.img")
            threadOverHead1.start()

            for pi in generatedJson.get("raspberryPi"):
                # Crea un hilo por cada raspberryPi
                hThread1 = Thread(token, pi.get("hostname"), pi.get("ip"))
                hThread1.start()

            return "Done"
        else:
            return "Invalid Token"


Run("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35")