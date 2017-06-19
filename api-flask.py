import os
import subprocess
from subprocess import Popen, PIPE
from flask import Flask, request
from flask_jsonrpc import JSONRPC
from flask_jsonrpc.site import JSONRPCSite
from werkzeug.utils import secure_filename
from coremodules.sysRp import SysRp
from coremodules.rpCloud import RpCloud
from coremodules.main import Run, Rescute

UPLOAD_FOLDER = '/mnt/img/uploads'
ALLOWED_EXTENSIONS = set(['img', 'zip'])

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

jsonrpcRpiJson = JSONRPC(app, '/api/v1/rpiJson', site=JSONRPCSite(), enable_web_browsable_api=True)
jsonrpcLogin = JSONRPC(app, '/api/v1/login', site=JSONRPCSite(), enable_web_browsable_api=True)
jsonrpcRegister = JSONRPC(app, '/api/v1/register', site=JSONRPCSite(), enable_web_browsable_api=True)
jsonrpcDeploy = JSONRPC(app, '/api/v1/deploy', site=JSONRPCSite(), enable_web_browsable_api=True)
jsonrpcRescute = JSONRPC(app, '/api/v1/rescute', site=JSONRPCSite(), enable_web_browsable_api=True)

######################### JSON-RPC POST ##########################
@jsonrpcLogin.method('login')
def apiLogin(email, password):
    return RpCloud().checkLogin(email, password)

@jsonrpcRegister.method('register')
def apiRegister(firstName, lastName, email, password):
    return RpCloud().register(firstName, lastName, email, password)

@jsonrpcRpiJson.method('generateJson')
def apiGenerateJson(token):
    return SysRp().generateJson(token)

@jsonrpcDeploy.method('run')
def apiRun(token):
    Run(token)
    return "Done"

@jsonrpcRescute.method('rescuteMode')
def apiRescute(token,rescuteMode):
    Rescute(token, rescuteMode)
    return "Done"

##################### GET ##################################
@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return app.send_static_file('dashboard.html')

@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    print(file.filename)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        subprocess.Popen(["mv", "/mnt/img/uploads/" + str(file.filename), "/mnt/img/uploads/fileUploaded.img"], stdout=subprocess.PIPE).communicate()[0]
        return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)