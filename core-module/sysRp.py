import subprocess
import sys
sys.path.append("../")
from rpcloud import RpCloud
from arp import Arp
from jsonrpc2 import JsonRpc
import unicodedata
import json
import re

class SysRp(object):


    def __init__(self):
        self.rP = RpCloud()
        self.rpc = JsonRpc()
        self.arp = Arp()

    def getHostname(self, token, ip):

        checked = self.rP.checkLogin(token)
        if(checked):
            # Ejecutamos "rsh" para obtener el nombre cada raspberryPi a partir de su IP
            host = subprocess.Popen(["rsh", ip, "hostname"], stdout=subprocess.PIPE).communicate()[0]
            hostname = host.decode("utf-8").replace("\n", "")
            # Para convertir de unicode a string
            return unicodedata.normalize('NFKD', hostname).encode('ascii', 'ignore').decode("utf-8")

        else:
            return "Invalid Token"



    def setHotname(self, token, ip, hostname):

        pass



    def generateJson(self, token, tableArp):

        self.rpc['getHostname'] = SysRp().getHostname

        checked = self.rP.checkLogin(token)
        if (checked):

            listJson = []
            # [1::] se elimina la cabecera
            for i in tableArp.get('result')[1::]:
                # Los datos capturados de la tabla ARP son interpretados tipo "Bytes",
                # Para interpretarlos tipo "String" usamos el decode(utf-8)
                i = i.decode("utf-8").split()
                # Si empieza por una ip

                if (re.match('^10(\.0){2}', i[0]) and re.match('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', i[2])):
                    hostname = self.rpc(
                        {"jsonrpc": "2.0", "method": "getHostname", "params": {"ip": i[0], "token": token},
                         "id": "getHostname"})
                    listJson.append({'ip': i[0], 'mac': i[2], 'hostname': hostname.get('result')})

            # Incluir raspberryPi en el diccionario
            concatJson = {'raspberryPi': ''}
            concatJson['raspberryPi'] = listJson

            # Parsea a JSON
            return json.dumps(concatJson)

        else:
            return "Invalid Token"


#########################################
################TEST#####################
########################################

## ENTRADA ##
rpc = JsonRpc()
rpc['getHostname'] = SysRp().getHostname
#print(rpc({"jsonrpc": "2.0", "method": "getHostname", "params": {"ip": "192.168.1.2", "token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "getHostname"}))
## SALIDA ##


########################################
## ENTRADA ##
rpc['generateJson'] = SysRp().generateJson
rpc['getArpTable'] = Arp().getTable
#tableARP = rpc({"jsonrpc": "2.0", "method": "getArpTable", "params": {"token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "getArpTable"})
#print(rpc({"jsonrpc": "2.0", "method": "generateJson", "params": {"tableArp": tableARP, "token":"8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "generateJson"}))
## SALIDA ##
