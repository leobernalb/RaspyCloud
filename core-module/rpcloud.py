import sys
sys.path.append("../")
from Mongo.helper import HashtagMDB
import hashlib, uuid
from jsonrpc2 import JsonRpc


class RpCloud(object):


    def __init__(self):
        """Attributes"""
        self.salt = uuid.uuid4().hex

    def login(self, user="admin", password="admin"):
        conn = HashtagMDB()

        self.user = user
        self.hash = hashlib.sha512(self.salt.encode() + password.encode()).hexdigest() + ':' + self.salt
        data = {"user": self.user, "hash": self.hash}
        conn.insertGeneric(collection="login",data=data)
        return self.hash


    def checkPassword(self,hash, user_password):
        password, salt = hash.split(':')
        return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()


    def logout(self):
        return self.salt


#########################################
################TEST#####################
########################################

## ENTRADA ##
rpc = JsonRpc()
rpc['login'] = RpCloud().login
resultLogin = rpc({"jsonrpc": "2.0", "method": "login", "params": {"user": "leo", "password": "abc123."}, "id": "login"})
print(resultLogin)
## SALIDA ##
## {'jsonrpc': '2.0', 'id': 'login', 'result': '6200b907743c3270995860bb4c0423adb7c4c7d8adee2dcdababebb467f2a6d775ba2460e263ef5fb50ce8dc041140ea432367c3d6a9393f9fbae74b44740797:8b5e0bfb6c9e4a018b54acbe15f618e6'}

########################################
## ENTRADA ##
rpc['checkPassword'] = RpCloud().checkPassword
#print(rpc({"jsonrpc": "2.0", "method": "checkPassword", "params": {"hash": resultLogin.get('result'), "user_password": "abc123."}, "id": "checkPassword"}))
## SALIDA ##
## {'jsonrpc': '2.0', 'id': 'checkPassword', 'result': True}
## {'jsonrpc': '2.0', 'id': 'checkPassword', 'result': False}
########################################
## ENTRADA ##
rpc['logout'] = RpCloud().logout
#print(rpc({"jsonrpc": "2.0", "method": "logout", "id": "logout"}))
## SALIDA ##
