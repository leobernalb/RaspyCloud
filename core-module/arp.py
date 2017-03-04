import subprocess
import sys
sys.path.append("../")
from rpcloud import RpCloud
from jsonrpc2 import JsonRpc


class Arp(object):


    def __init__(self):
        self.rP = RpCloud()

    def broadcast(self, token):

        checked = self.rP.checkLogin(token)
        if(checked):
            print({'jsonrpc': '2.0', 'result': 'In process', 'id': 'broadcast'})
            subprocess.Popen(["ping", "192.168.1.255", "-b", "-I", "wlp4s0", "-c", "5 >/dev/null"],
                             stdout=subprocess.PIPE).communicate()[0]
            return "Done"
        else:
            return "Invalid Token"

#########################################
################TEST#####################
########################################

## ENTRADA ##
rpc = JsonRpc()
rpc['broadcast'] = Arp().broadcast
print(rpc({"jsonrpc": "2.0", "method": "broadcast", "params": {"token": "041c65e06039771eee97c0f8b41d678a7837dd48c0d189a146cd4472d5af749969d6f59af8a706170dff1c6473217c6ae9c172b6d33a057866b8746ffed00f96:0059d447166048ad845bf05c70732284"}, "id": "broadcast"}))
## SALIDA ##
#{'id': 'broadcast', 'jsonrpc': '2.0', 'result': 'Done'}
#{'jsonrpc': '2.0', 'id': 'broadcast', 'result': 'Invalid Token'}

