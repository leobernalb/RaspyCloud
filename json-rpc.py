from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from coremodules.arp import Arp
from coremodules.rpCloud import RpCloud
from coremodules.sysRp import SysRp
from coremodules.threads import Thread


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

o=SysRp()
#o.createPartition("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35","10.0.0.10")
#o.reboot("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35","rpi001")
#o.formatFileSystemAndMount("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35","10.0.0.10")
#o.mountImgCompress("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35","/mnt/img/minimalRaspyCloud.img")
#o.sendAndDecompress("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35","10.0.0.10")
#o.changePartition("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35","10.0.0.10", False)
#print(o.reboot("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35","rpi001"))
#print(o.checkMachine("10.0.0.18"))


hMiHilo = Thread("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35", "rpi001", "10.0.0.10")
hMiHilo.start()

hMiHilo = Thread("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35", "rpi002", "10.0.0.21")
hMiHilo.start()

hMiHilo = Thread("8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35", "rpi003", "10.0.0.17")
hMiHilo.start()