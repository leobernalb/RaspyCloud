from Mongo.helper import RaspberryDB
import hashlib, uuid


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


    def checkPassword(self, token, user_password):
        # Split por : para obtener el salt
        password, salt = token.split(':')
        # Devuelve TRUE or FALSE en jsonRPC
        return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()


    def checkLogin(self, token):
        conn = RaspberryDB()
        searched = conn.searchLogin(collection="login",  hash=token)
        # Si la busqueda es [] devuelve False
        if len(searched) == 0:
            return False
        else:
            # Si la busqueda tiene 1 elemento, devuelve True
            return True


    def logout(self, token):
        # Encuentra elemento en BD y elimina
        conn = RaspberryDB()
        foundUser = conn.deleteElement(collection="login", hash=token)
        # Si encuentra el hash de usuario y lo borra, devuelve "OK"
        if foundUser != None:
            return "Ok"
        # Si no encuentra el Hash de usuario, devuelve "None"





#########################################
################TEST#####################
########################################

## ENTRADA ##
#rpc = JsonRpc()
#rpc['login'] = RpCloud().login
#resultLogin = rpc({"jsonrpc": "2.0", "method": "login", "params": {"user": "leo", "password": "abc123."}, "id": "login"})
#print(resultLogin)
## SALIDA ##
## {'jsonrpc': '2.0', 'id': 'login', 'result': '6200b907743c3270995860bb4c0423adb7c4c7d8adee2dcdababebb467f2a6d775ba2460e263ef5fb50ce8dc041140ea432367c3d6a9393f9fbae74b44740797:8b5e0bfb6c9e4a018b54acbe15f618e6'}

########################################
## ENTRADA ##
#rpc['checkPassword'] = RpCloud().checkPassword
#print(rpc({"jsonrpc": "2.0", "method": "checkPassword", "params": {"token": "c07f4789cd9b3338bf35ea21ff353f3bd181c528d8e980dd27fc0ee10143c7307b15bc796bf20ee0a9743a7d61ae2e0dc093ad034afc6a16b62f207060fe925b:d45774ad1dae49d48bcb795cb0d9372d",
# "user_password": "abc123."}, "id": "checkPassword"}))
## SALIDA ##
## {'jsonrpc': '2.0', 'id': 'checkPassword', 'result': True}
## {'jsonrpc': '2.0', 'id': 'checkPassword', 'result': False}

########################################
## ENTRADA ##
#rpc['checkLogin'] = RpCloud().checkLogin
#print(rpc({"jsonrpc": "2.0", "method": "checkLogin", "params": {"token": "c07f4789cd9b3338bf35ea21ff353f3bd181c528d8e980dd27fc0ee10143c7307b15bc796bf20ee0a9743a7d61ae2e0dc093ad034afc6a16b62f207060fe925b:d45774ad1dae49d48bcb795cb0d9372d"}, "id": "checkLogin"}))
## SALIDA ##
#{'jsonrpc': '2.0', 'id': 'checkLogin', 'result': True}
#{'jsonrpc': '2.0', 'id': 'checkLogin', 'result': False}

########################################
## ENTRADA ##
#rpc['logout'] = RpCloud().logout
#print(rpc({"jsonrpc": "2.0", "method": "logout", "params": {"token":"041c65e06039771eee97c0f8b41d678a7837dd48c0d189a146cd4472d5af749969d6f59af8a706170dff1c6473217c6ae9c172b6d33a057866b8746ffed00f96:0059d447166048ad845bf05c70732284"}, "id": "logout"}))
## SALIDA ##
# {'jsonrpc': '2.0', 'id': 'logout', 'result': 'Ok'}
# {'jsonrpc': '2.0', 'id': 'logout', 'result': None}

