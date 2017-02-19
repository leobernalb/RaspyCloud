import sys
sys.path.append("../")
from Mongo.helper import RaspberryDB
import hashlib, uuid
from jsonrpc2 import JsonRpc


class RpCloud(object):


    def __init__(self):
        """Attributes"""
        # Generamos una semilla distinta para cada usuario
        self.salt = uuid.uuid4().hex

    def login(self, user="admin", password="admin"):
        conn = RaspberryDB()
        # Generaramos el Hash de usuario en sha512 con el siguiente formato salt + password : salt
        self.user = user
        self.hash = hashlib.sha512(self.salt.encode() + password.encode()).hexdigest() + ':' + self.salt
        data = {"user": self.user, "hash": self.hash}
        # Insertamos datos en Mongo dentro de la collection LOGIN
        conn.insertGeneric(collection="login",data=data)
        # Devuelve en Hash en jsonRPC
        return self.hash


    def checkPassword(self, hash, user_password):
        # Split por : para obtener el salt
        password, salt = hash.split(':')
        # Devuelve TRUE or FALSE en jsonRPC
        return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()

    def checkLogin(self, user, hash):
        conn = RaspberryDB()
        searched = conn.searchLogin(collection="login", user=user, hash=hash)
        # Si la busqueda es [] devuelve False
        if len(searched) == 0:
            return False
        else:
            # Si la busqueda tiene 1 elemento, devuelve True
            return True

    def logout(self, hash):
        # Encuentra elemento en BD y elimina
        conn = RaspberryDB()
        foundUser = conn.deleteElement(collection="login", hash=hash)
        # Si encuentra el hash de usuario y lo borra, devuelve "OK"
        if foundUser != None:
            return "Ok"
        # Si no encuentra el Hash de usuario, devuelve "None"


#########################################
################TEST#####################
########################################

## ENTRADA ##
rpc = JsonRpc()
rpc['login'] = RpCloud().login
#resultLogin = rpc({"jsonrpc": "2.0", "method": "login", "params": {"user": "leo", "password": "abc123."}, "id": "login"})
#print(resultLogin)
## SALIDA ##
## {'jsonrpc': '2.0', 'id': 'login', 'result': '6200b907743c3270995860bb4c0423adb7c4c7d8adee2dcdababebb467f2a6d775ba2460e263ef5fb50ce8dc041140ea432367c3d6a9393f9fbae74b44740797:8b5e0bfb6c9e4a018b54acbe15f618e6'}

########################################
## ENTRADA ##
rpc['checkPassword'] = RpCloud().checkPassword
#print(rpc({"jsonrpc": "2.0", "method": "checkPassword", "params": {"hash": "10becdae5417723d7478a354471428844dd78edad1ef77db23ecd09e1a98483f0f3ada4c8363f4a8c1be4d03037540568b6a5c1c5c0e693081dd03c9afeb449e:7764913e770c4083a224c06bbb88c547",
# "user_password": "abc123."}, "id": "checkPassword"}))
## SALIDA ##
## {'jsonrpc': '2.0', 'id': 'checkPassword', 'result': True}
## {'jsonrpc': '2.0', 'id': 'checkPassword', 'result': False}

########################################
## ENTRADA ##
rpc['checkLogin'] = RpCloud().checkLogin
#print(rpc({"jsonrpc": "2.0", "method": "checkLogin", "params": {"user": "leo",
# "hash": "10becdae5417723d7478a354471428844dd78edad1ef77db23ecd09e1a98483f0f3ada4c8363f4a8c1be4d03037540568b6a5c1c5c0e693081dd03c9afeb449e:7764913e770c4083a224c06bbb88c547"}, "id": "checkLogin"}))
## SALIDA ##
#{'jsonrpc': '2.0', 'id': 'checkLogin', 'result': True}
#{'jsonrpc': '2.0', 'id': 'checkLogin', 'result': False}

########################################
## ENTRADA ##
rpc['logout'] = RpCloud().logout
# print(rpc({"jsonrpc": "2.0", "method": "logout", "params": {"hash":"9b34b05476f9059eca6f618cced59aefe9ab789da990318fc6927e407267b2c671af21696bb43f8f5af99cac60c0dc87b201078608366c4cc925020ead87a8dd:52083f84890840069ed7e075d7e0b65a"}, "id": "logout"}))
## SALIDA ##
# {'jsonrpc': '2.0', 'id': 'logout', 'result': 'Ok'}
# {'jsonrpc': '2.0', 'id': 'logout', 'result': None}
