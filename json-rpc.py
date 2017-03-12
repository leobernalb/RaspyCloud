from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from coremodules.arp import Arp
from coremodules.rpCloud import RpCloud
from coremodules.sysRp import SysRp


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher['scanARP'] = Arp().scan
    dispatcher['login'] = RpCloud().login
    dispatcher['checkPassword'] = RpCloud().checkPassword
    dispatcher['checkLogin'] = RpCloud().checkLogin
    dispatcher['logout'] = RpCloud().logout
    dispatcher['getHostname'] = SysRp().getHostname

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 8001, application)