from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from coremodules.arp import Arp
from coremodules.rpCloud import RpCloud
from coremodules.sysRp import SysRp


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


if __name__ == '__main__':
    run_simple('localhost', 8001, application)
