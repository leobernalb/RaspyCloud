import subprocess
import sys
sys.path.append("../")
from rpcloud import RpCloud
from jsonrpc2 import JsonRpc


class SysRp(object):


    def __init__(self):
        self.rP = RpCloud()

    def getHostname(self, token, ip):

        checked = self.rP.checkLogin(token)
        if(checked):
            # Ejecutamos "rsh" para obtener el nombre cada raspberryPi a partir de su IP
            host = subprocess.Popen(["rsh", ip, "hostname"], stdout=subprocess.PIPE).communicate()[0]
            hostname = host.decode("utf-8").replace("\n", "")
            # Para convertir de unicode a string
            return unicodedata.normalize('NFKD', hostname).encode('ascii', 'ignore')

        else:
            return "Invalid Token"



    def setHotname(self, token, ip, hostname):

        pass
#########################################
################TEST#####################
########################################

## ENTRADA ##
rpc = JsonRpc()
rpc['getHostname'] = SysRp().getHostname
print(rpc({"jsonrpc": "2.0", "method": "getHostname", "params": {"ip": "10.0.0.11", "token": "041c65e06039771eee97c0f8b41d678a7837dd48c0d189a146cd4472d5af749969d6f59af8a706170dff1c6473217c6ae9c172b6d33a057866b8746ffed00f96:0059d447166048ad845bf05c70732284"}, "id": "getHostname"}))
## SALIDA ##


########################################
## ENTRADA ##


## SALIDA ##
