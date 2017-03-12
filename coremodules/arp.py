import subprocess
from coremodules.rpCloud import RpCloud



class Arp(object):


    def __init__(self):
        self.rP = RpCloud()

    def scan(self, token):

        checked = self.rP.checkLogin(token)
        if(checked):
            print({'jsonrpc': '2.0', 'result': 'In process', 'id': 'broadcast'})
            subprocess.Popen(["ping", "10.0.0.255", "-b", "-I", "enp3s0", "-c", "5 >/dev/null"],
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
            return output.decode("utf-8").splitlines()


        else:
            return "Invalid Token"
#########################################
################TEST#####################
########################################

## ENTRADA ##
#rpc = JsonRpc()
#rpc['scanARP'] = Arp().scan
#print(rpc({"jsonrpc": "2.0", "method": "scanARP", "params": {"token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "scanARP"}))
## SALIDA ##
#{'id': 'scanARP', 'jsonrpc': '2.0', 'result': 'Done'}
#{'jsonrpc': '2.0', 'id': 'scanARP', 'result': 'Invalid Token'}

########################################
## ENTRADA ##
#rpc['getArpTable'] = Arp().getTable
#print(rpc({"jsonrpc": "2.0", "method": "getArpTable", "params": {"token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "getArpTable"}))
## SALIDA ##
#{'id': 'getArpTable', 'result': ['gateway ether 54:67:51:96:0e:bb 10.0.0.13 eth0', 'gateway ether b8:27:eb:db:dd:97 10.0.0.11 eth0', 'Address HWtype HWaddress Flags Mask Iface'], 'jsonrpc': '2.0'}
##{'jsonrpc': '2.0', 'id': 'getArpTable', 'result': 'Invalid Token'}
