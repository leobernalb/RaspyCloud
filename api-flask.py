from flask import Flask, request
from flask_jsonrpc import JSONRPC
from flask_jsonrpc.site import JSONRPCSite
from coremodules.sysRp import SysRp
from coremodules.rpCloud import RpCloud

app = Flask(__name__, static_url_path='/static')
jsonrpcRpiJson = JSONRPC(app, '/api/v1/rpiJson', site=JSONRPCSite(), enable_web_browsable_api=True)
jsonrpcLogin = JSONRPC(app, '/api/v1/login', site=JSONRPCSite(), enable_web_browsable_api=True)

######################### JSON-RPC POST ##########################
@jsonrpcLogin.method('login')
def apiLogin(username, password):
    return RpCloud().checkLogin(username, password)

@jsonrpcRpiJson.method('generateJson')
def apiGenerateJson(token):
    return SysRp().generateJson(token)

##################### GET ##################################
@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return app.send_static_file('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)

#o = RpCloud()
#print(o.checkPassword("c07f4789cd9b3338bf35ea21ff353f3bd181c528d8e980dd27fc0ee10143c7307b15bc796bf20ee0a9743a7d61ae2e0dc093ad034afc6a16b62f207060fe925b:d45774ad1dae49d48bcb795cb0d9372d", "abc123."))

#o = RpCloud()
#print(o.checkLogin("gema", "gemaeslamejor"))

#print(o.login("gema", "gemaeslamejor"))
