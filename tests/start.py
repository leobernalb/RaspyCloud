import subprocess
import json
import re

# subprocess : Biblioteca para capturar comandos del sistema
# Desde la version python 2.4 no se recomienda la biblioteca "os"
# Ping a Broadcast durante 3 segundos para actualizar la cache ARP
subprocess.Popen(["ping","10.0.0.255","-b","-I","eth0","-c","3"], stdout=subprocess.PIPE).communicate()[0]
subprocess.Popen(["sleep","10"], stdout=subprocess.PIPE).communicate()[0]
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
        # Ejecutamos "rsh" para obtener el nombre cada raspberryPi a partir de su IP
        host = subprocess.Popen(["rsh",i[0],"hostname"], stdout=subprocess.PIPE).communicate()[0]
        hostname = host.decode("utf-8").replace("\n", "")
        listJson.append({'ip': i[0], 'mac': i[2], 'hostname': hostname})

# Incluir raspberryPi en el diccionario
concatJson = {'raspberryPi' : ''}
concatJson['raspberryPi'] = listJson

# Parsea a JSON
resJson = json.dumps(concatJson)

def saveJson():
    # Con la opcion 'w' editamos el fichero. Si no existe, lo crea
    archi=open('start.json','w')
    archi.write(resJson)
    archi.close()

saveJson()
