from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import hashlib
import subprocess

from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]


def checkPassword(token, user_password):
    # Split por : para obtener el salt
    password, salt = token.split(':')
    # Devuelve TRUE or FALSE en jsonRPC
    return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()

@dispatcher.add_method
def scan():

    output = subprocess.Popen(["arp"], stdout=subprocess.PIPE).communicate()[0]
    return output



@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s
    dispatcher['checkPassword'] = checkPassword
    dispatcher['scanARP'] = scan

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)