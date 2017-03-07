import subprocess
import sysRp
sysRp.path.append("../")
from rpcloud import RpCloud
from jsonrpc2 import JsonRpc


class Arp(object):


    def __init__(self):
        self.rP = RpCloud()

    def scan(self, token):

        checked = self.rP.checkLogin(token)
        if(checked):
            print({'jsonrpc': '2.0', 'result': 'In process', 'id': 'broadcast'})
            subprocess.Popen(["ping", "10.0.0.255", "-b", "-I", "eth0", "-c", "5 >/dev/null"],
                             stdout=subprocess.PIPE).communicate()[0]
            return "Done"
        else:
            return "Invalid Token"



    def getTable(self, token):

        checked = self.rP.checkLogin(token)
        if(checked):
            # Consulta la tabla ARP
            output = subprocess.Popen(["arp"], stdout=subprocess.PIPE).communicate()[0]

            # splitlines transforma a lista haciendo split por \n
            return output.splitlines()

        else:
            return "Invalid Token"
#########################################
################TEST#####################
########################################

## ENTRADA ##
rpc = JsonRpc()
rpc['scanARP'] = Arp().scan
#print(rpc({"jsonrpc": "2.0", "method": "scanARP", "params": {"token": "041c65e06039771eee97c0f8b41d678a7837dd48c0d189a146cd4472d5af749969d6f59af8a706170dff1c6473217c6ae9c172b6d33a057866b8746ffed00f96:0059d447166048ad845bf05c70732284"}, "id": "scanARP"}))
## SALIDA ##
#{'id': 'scanARP', 'jsonrpc': '2.0', 'result': 'Done'}
#{'jsonrpc': '2.0', 'id': 'scanARP', 'result': 'Invalid Token'}

########################################
## ENTRADA ##
rpc['getArpTable'] = Arp().getTable
#print(rpc({"jsonrpc": "2.0", "method": "getArpTable", "params": {"token": "041c65e06039771eee97c0f8b41d678a7837dd48c0d189a146cd4472d5af749969d6f59af8a706170dff1c6473217c6ae9c172b6d33a057866b8746ffed00f96:0059d447166048ad845bf05c70732284"}, "id": "getArpTable"}))
## SALIDA ##
#{'id': 'getArpTable', 'result': [b'gateway ether 54:67:51:96:0e:bb 10.0.0.13 eth0', b'gateway ether b8:27:eb:db:dd:97 10.0.0.11 eth0', b'Address HWtype HWaddress Flags Mask Iface'], 'jsonrpc': '2.0'}
# #{'jsonrpc': '2.0', 'id': 'getArpTable', 'result': 'Invalid Token'}

