from subprocess import Popen, PIPE
import subprocess
import json
import re
import unicodedata
from jsonrpc2 import JsonRpc

rpc = JsonRpc()

def broadcast():
    # Detectar si el proceso ya esta en uso
    # Subprocess no permite usar "|" por lo que tenemos que ejecutarlo en dos pasos
    command1 = Popen(["ps","-e"], stdout = PIPE)
    command2 = Popen(["grep", "ping"], stdin = command1.stdout, stdout= PIPE)
    command1.stdout.close()
    result = (command2.communicate()[0])

    if len(result) is 0:
        # Si result es 0, no se ha ejecutado
        print({'jsonrpc': '2.0', 'result': 'In process', 'id': 'broadcast'})
        subprocess.Popen(["ping","10.0.0.255","-b","-I","eth0","-c","5 >/dev/null"], stdout=subprocess.PIPE).communicate()[0]

        return "Done"
    else:
        # Si result es 1, el ping a broadcast ya se ha ejecutado
        return "In process"

rpc['broadcast'] = broadcast

## Entrada: ##
##print(rpc({"jsonrpc": "2.0", "method": "broadcast", "id": "broadcast"}))

## Salida: ##
## {'jsonrpc': '2.0', 'result': 'Done', 'id': 'broadcast'}
## {'jsonrpc': '2.0', 'result': 'In process', 'id': 'broadcast'}


def hostname(ip):
    # Ejecutamos "rsh" para obtener el nombre cada raspberryPi a partir de su IP
    host = subprocess.Popen(["rsh",ip,"hostname"], stdout=subprocess.PIPE).communicate()[0]
    hostname = host.decode("utf-8").replace("\n", "")
    # Para convertir de unicode a string
    return unicodedata.normalize('NFKD', hostname).encode('ascii','ignore')

rpc['hostname'] = hostname

## Entrada: ##
##print(rpc({"jsonrpc": "2.0", "method": "hostname", "params": {"ip": "192.168.1.2"}, "id": "hostname"}))

## Salida: ##
## {'jsonrpc': '2.0', 'id': 'hostname', 'result': 'rpi001'}


def generaJsonRaspberry():
    # Consulta la tabla ARP
    output = subprocess.Popen(["arp"], stdout=subprocess.PIPE).communicate()[0]

    # splitlines transforma a lista haciendo split por \n
    listRow = output.splitlines()

    listJson = []
    # [1::] se elimina la cabecera
    for i in listRow[1::]:
        # Los datos capturados de la tabla ARP son interpretados tipo "Bytes",
        # Para interpretarlos tipo "String" usamos el decode(utf-8)
        i = i.decode("utf-8").split( )
        # Si empieza por una ip

        if(re.match('^10(\.0){2}',i[0]) and re.match('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',i[2])):

            hostname = rpc({"jsonrpc": "2.0", "method": "hostname", "params": {"ip": i[0]}, "id": "hostname"})
            listJson.append({'ip': i[0], 'mac': i[2], 'hostname': hostname.get('result')})

    # Incluir raspberryPi en el diccionario
    concatJson = {'raspberryPi' : ''}
    concatJson['raspberryPi'] = listJson

    # Parsea a JSON
    return json.dumps(concatJson)


rpc['generaJsonRaspberry'] = generaJsonRaspberry

## Entrada: ##
jsonRaspberry = rpc({"jsonrpc": "2.0", "method": "generaJsonRaspberry", "id": "generaJsonRaspberry"})
print(jsonRaspberry)

## Salida: ##
## {"raspberryPi": [{"ip": "10.0.0.13", "mac": "b8:27:eb:53:3e:99", "hostname": "rpi002"}, {"ip": "10.0.0.11", "mac": "b8:27:eb:db:dd:97", "hostname": "rpi001"}]}


def guardarJson(json):
    # Con la opcion 'w' editamos el fichero. Si no existe, lo crea
    archi=open('start.json','w')
    archi.write(json.get("result"))
    archi.close()

    return "Done"

rpc['guardarJson'] = guardarJson

## Entrada: ##
##print(rpc({"jsonrpc": "2.0", "method": "guardarJson", "params": {"json": jsonRaspberry}, "id": "guardarJson"}))

## Salida: ##
## {'jsonrpc': '2.0', 'id': 'guardarJson', 'result': 'Done'}
