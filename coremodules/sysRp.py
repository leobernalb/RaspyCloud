from subprocess import Popen, PIPE
import subprocess
from coremodules.rpCloud import RpCloud
from coremodules.arp import Arp
import unicodedata
import json
import re
import time

class SysRp(object):


    def __init__(self):
        self.rP = RpCloud()
        self.arp = Arp()

    def createPartition(self, token, ip):

        print("####################################### CREATE PARTITION #############################################")
        checked = self.rP.checkLogin(token)
        if (checked):
            ## Dump de la tabla de particiones
            partition = subprocess.Popen(["rsh", ip, "sfdisk", "--dump", "/dev/mmcblk0"],
                                         stdout=subprocess.PIPE).communicate()[0]
            with open('/tmp/tablePartition.part', 'w') as outfile:
                outfile.write(partition.decode("utf-8"))

            sectorStartTwo = subprocess.Popen(["awk", "/^\/dev\/mmcblk0p2/{print $4}", "/tmp/tablePartition.part"],
                                              stdout=subprocess.PIPE).communicate()[0]
            sectorStartTwo = sectorStartTwo.decode("utf-8").replace(",\n","")
            #print(sectorStartTwo)

            sectorTamSizeTwo = subprocess.Popen(["awk", "/^\/dev\/mmcblk0p2/{print $6}", "/tmp/tablePartition.part"],
                                                stdout=subprocess.PIPE).communicate()[0]
            sectorTamSizeTwo = sectorTamSizeTwo.decode("utf-8").replace(",\n", "")
            #print(sectorTamSizeTwo)

            # Para obtener el START3 de la particion nueva = START PARTICION2 + SIZE2
            startNewPartition = int(sectorStartTwo) + int(sectorTamSizeTwo)
            #print(startNewPartition)

            # Tamaño maximo de particion (en sectores) secSizek0 - START particion nueva (calculado antes)
            sectorsSizek0 = subprocess.Popen(["rsh", ip, "blockdev", "--getsize", "/dev/mmcblk0"],
                                             stdout=subprocess.PIPE).communicate()[0]
            sectorsSizek0 = sectorsSizek0.decode("utf-8").replace("\n","")
            #print(sectorsSizek0)

            # Para Obtener el size de la particion nueva = secSizek0 - START particion nueva (calculado antes)
            sectorsSizeNewPartition = int(sectorsSizek0) - int(startNewPartition)
            #print(sectorsSizeNewPartition)

            mmcblk0p3 = subprocess.Popen(["awk", "/^\/dev\/mmcblk0p3/{print $0}", "/tmp/tablePartition.part"],
                                         stdout=subprocess.PIPE).communicate()[0]
            mmcblk0p3 = mmcblk0p3.decode("utf-8").replace("\n", "")
            #print(mmcblk0p3)
            newLine = ("/dev/mmcblk0p3 : start="+ str(startNewPartition) + ", size="+ str(sectorsSizeNewPartition) + ", Id=83")
            subprocess.Popen(["sed", "-i", '/^\/dev\/mmcblk0p3/c' + newLine + "", "/tmp/tablePartition.part"],
                             stdout=subprocess.PIPE).communicate()[0]
            sendPartition = subprocess.Popen(["scp", "/tmp/tablePartition.part", ip + ":/tmp/."], stdout=subprocess.PIPE)
            time.sleep(3)
            subprocess.Popen(("rsh", ip, "sfdisk", "--force", "/dev/mmcblk0", "< /tmp/tablePartition.part"), stdin=sendPartition.stdout).communicate()[0]



            ## Tamaño de sector (en bytes) el famoso 512!!!!!!!!!!!!!!!!!!!!!!!
            #tamSectors = subprocess.Popen(["rsh", ip, "blockdev", "--getss", "/dev/mmcblk0"], stdout=subprocess.PIPE).communicate()[0]
            ## Tamaño maximo de disco (en sectores) eso hay que multiplicarlo por 512
            #secSizek0 = subprocess.Popen(["rsh", ip, "blockdev", "--getsize", "/dev/mmcblk0"], stdout=subprocess.PIPE).communicate()[0]
            # blockdev --getsize64 /dev/mmcblk0 ### El tamaño de la particion ya multiplicado (en bytes!!!!!!!!!!!!!)

            return "Done"

        else:
            return "Invalid Token"



    def formatFileSystemAndMount(self, token, ip):

        checked = self.rP.checkLogin(token)
        if (checked):

            print("####################################### FORMAT PARTITION #############################################")
            subprocess.Popen(["rsh", ip, "umount", "/dev/mmcblk0p3"], stdout=subprocess.PIPE).communicate()[0]
            subprocess.Popen(["rsh", ip, "mkdir", "-p", "/mnt/img"], stdout=subprocess.PIPE).communicate()[0]
            subprocess.Popen(["rsh", ip, "mkfs.ext4", "/dev/mmcblk0p3"], stdout=subprocess.PIPE).communicate()[0]
            subprocess.Popen(["rsh", ip, "mount", "-t", "ext4", "/dev/mmcblk0p3", "/mnt/img/"], stdout=subprocess.PIPE).communicate()[0]
            return "Done"

        else:
            return "Invalid Token"


    def mountImgCompress(self, token, img):
        print("####################################### MOUNT IMG SERVER #############################################")
        checked = self.rP.checkLogin(token)
        if (checked):
            subprocess.Popen(["umount", "/mnt/img/two"], stdout=subprocess.PIPE).communicate()[0]

            # Tamaño de bloque del sistema. Tambien lo podriamos hacer con el comando blockdev pero tenemos que
            # saber tambien el nombre del dispositivo usado. (sda, hda, ...) Lo sacamos directamente de fdisk y la img
            fdisk = subprocess.Popen(('fdisk', '-l', img), stdout=subprocess.PIPE)
            tamBlock = subprocess.check_output(('awk', '/^Uni/{print $6}'), stdin=fdisk.stdout).decode("utf-8")
            tamBlock = tamBlock.replace("\n","")
            #print(tamBlock)

            # Debemos ejecutar de nuevo fdisk porque el flujo de datos no es persistente
            # Obtener el inicio de sector de la particion dos de la imagen deseada
            fdisk = subprocess.Popen(('fdisk', '-l', img), stdout=subprocess.PIPE)
            startSectorsPartitionTwo = subprocess.check_output(('awk', '$1 ~ /img2/ { print $2}'),
                                                               stdin=fdisk.stdout).decode("utf-8")
            startSectorsPartitionTwo = startSectorsPartitionTwo.replace("\n", "")
            #print(startSectorsPartitionTwo)

            # Calculamos el numero de bytes desde donde se montara la imagen
            subprocess.Popen(["mkdir", "-p", "/mnt/img/two"], stdout=subprocess.PIPE).communicate()[0]
            subprocess.Popen(["mount", "-v", "-o", "offset=" + str(int(startSectorsPartitionTwo) * int(tamBlock)), "-t", "ext4", img, "/mnt/img/two"], stdout=subprocess.PIPE)
            subprocess.Popen(["sleep", "3"], stdout=subprocess.PIPE).communicate()[0] ## Espera 3 segundos para asegurarnos que se monta la particion

            # Copiar clave publica RSA
            print("####################################### ADD RSA #############################################")
            subprocess.Popen(["mkdir", "-p", "/mnt/img/two/root/.ssh"], stdout=subprocess.PIPE).communicate()[0]
            subprocess.Popen(["cp", "/root/.ssh/id_rsa.pub", "/mnt/img/two/root/.ssh/authorized_keys"], stdout=subprocess.PIPE).communicate()[0]

            # Empaquetar y comprimit
            print("####################################### COMPRESS IMG #############################################")
            subprocess.Popen(['tar -cvzf /tmp/imagen.tar.gz .'], shell=True, cwd='/mnt/img/two').wait()

            return "Done"
        else:
            return "Invalid Token"



    def sendAndDecompress(self, token, ip):

        checked = self.rP.checkLogin(token)
        if (checked):

            # Envio de img comprimida y descompresion en la rpi
            # Por defecto lee la imagen guardada en /mnt/img/ del servidor y la descomprime en el /mnt/img/ de la rpi
            print("####################################### SEND IMG #############################################")
            subprocess.Popen(["scp", "/tmp/imagen.tar.gz", ip + ":/mnt/img/."], stdout=subprocess.PIPE).communicate()[0]
            print("####################################### DECOMPRESS #############################################")
            subprocess.Popen(["rsh", ip, "tar", "-xvf", "/mnt/img/imagen.tar.gz", "-C", "/mnt/img/."], stdin=subprocess.PIPE).communicate()[0]

        else:
            return "Invalid Token"




    def changePartition(self, token, ip, rescuteMode=True):

        print("####################################### CHANGE PARTITION #############################################")
        checked = self.rP.checkLogin(token)
        if (checked):

            if (rescuteMode):
                # Cambia a Particion minima con Raspbian de 3 --+ 2
                part = "\/dev\/mmcblk0p2"
                subprocess.Popen(["rsh", ip, "sed -i 's|\/dev\/mmcblk0p3|" + part + "|g' /boot/cmdline.txt"],
                                       stdout=subprocess.PIPE).communicate()[0].decode("utf-8").replace("\n", "")
            else:
                # Cambia a Particion nueva de 2 --+ 3
                part = "\/dev\/mmcblk0p3"
                subprocess.Popen(["rsh", ip, "sed -i 's|\/dev\/mmcblk0p2|" + part + "|g' /boot/cmdline.txt"],
                                       stdout=subprocess.PIPE).communicate()[0].decode("utf-8").replace("\n", "")

            return "Done"

        else:
            return "Invalid Token"



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



    def setHostname(self, token, hostnameOld, hostnameNew):

        checked = self.rP.checkLogin(token)

        if(checked):
            # Consultamos el JSON actual
            generatedJson = self.generateJson(token)

            # Vamos hacer la traduccion de hostname -- ip.
            # Recorremos el array de raspberry
            for pi in generatedJson.get("raspberryPi"):

                if(pi.get("hostname") == hostnameOld):

                    dnsIp = pi.get("ip")

            # Cambia el /etc/hostname
            subprocess.Popen(["rsh", "root@" + dnsIp, "echo", hostnameNew, " > /etc/hostname"],
                             stdout=subprocess.PIPE).communicate()[0]
            # Sustituye la linea que empieza por ^127.0.1.1 nombreViejo por 127.0.1.1 nombreNuevo
            subprocess.Popen(["rsh", "root@" + dnsIp, "sed", "-i", '/^127.0.1.1*/c\ 127.0.1.1\\\t' + hostnameNew + "",
                              "/etc/hosts"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8")

            return "Done"
        else:
            return "Invalid Token"




    def generateJson(self, token):


        checked = self.rP.checkLogin(token)
        if (checked):

            listJson = []
            # [1::] se elimina la cabecera

            for i in self.arp.getTable(token)[1::]:
                # Los datos capturados de la tabla ARP son interpretados tipo "Bytes",
                # Para interpretarlos tipo "String" usamos el decode(utf-8)
                i = i.split()
                # Si empieza por una ip

                if (re.match('^10(\.0){2}', i[0]) and re.match('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', i[2])):

                    hostname = self.getHostname(token,i[0])
                    listJson.append({'ip': i[0], 'mac': i[2], 'hostname': hostname})

            # Incluir raspberryPi en el diccionario
            concatJson = {'raspberryPi': ''}
            concatJson['raspberryPi'] = listJson

            # Parsea a JSON
            return concatJson

        else:
            return "Invalid Token"


    def storageJson(self, token):

        # Consultamos el JSON actual
        generatedJson = self.generateJson(token)
        checked = self.rP.checkLogin(token)

        if(checked):

            # Con la opcion 'w' editamos el fichero. Si no existe, lo crea
            with open('Static/start.json', 'w') as outfile:
                json.dump(generatedJson, outfile)

            return "Done"
        else:
            return "Invalid Token"


    def reboot(self, token, hostname):
        print("####################################### REBOOT #############################################")
        checked = self.rP.checkLogin(token)
        if(checked):
            # Consultamos el JSON actual
            generatedJson = self.generateJson(token)

            # Vamos hacer la traduccion de hostname -- ip.
            # Recorremos el array de raspberry
            for pi in generatedJson.get("raspberryPi"):

                if (pi.get("hostname") == hostname):
                    dnsIp2 = pi.get("ip")

            subprocess.Popen(["rsh", "root@" + dnsIp2, 'shutdown --reboot 0 ; exit'], stdout=subprocess.PIPE).communicate()[0]

            print("####################################### MACHINE STATUS #############################################")
            print(self.checkMachine(dnsIp2))

            return "Done"
        else:
            return "Invalid Token"


    def checkMachine(self, ip):

        # Hacemos 30 ping y si recibimos correctamente 5 o mas consideramos que la rpi esta "UP"
        ping = subprocess.Popen(["ping", "-c", "30", ip], stdout=subprocess.PIPE)
        pingNum = subprocess.check_output(('awk', '/received/{print $4}'), stdin=ping.stdout).decode("utf-8").replace("\n","")

        print(pingNum)
        if(int(pingNum) >= 5):
            return "up"
        else:
            return "down"


#########################################
################TEST#####################
########################################
## ENTRADA ##
#rpc = JsonRpc()
#rpc['getHostname'] = SysRp().getHostname
#print(rpc({"jsonrpc": "2.0", "method": "getHostname", "params": {"ip": "10.0.0.11", "token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "getHostname"}))
## SALIDA ##
#{'jsonrpc': '2.0', 'result': 'rpi001', 'id': 'getHostname'}
#{'jsonrpc': '2.0', 'id': 'getHostname', 'result': 'Invalid Token'}

########################################
## ENTRADA ##
#rpc['getArpTable'] = Arp().getTable
#rpc['generateJson'] = SysRp().generateJson
#tableARP = rpc({"jsonrpc": "2.0", "method": "getArpTable", "params": {"token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "getArpTable"})
#GeneratedJson = rpc({"jsonrpc": "2.0", "method": "generateJson", "params": {"token":"8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "generateJson"})
#print(GeneratedJson)
## SALIDA ##
#{'result': '{"raspberryPi": [{"hostname": "rpi003", "ip": "10.0.0.14", "mac": "b8:27:eb:0c:48:42"}, {"hostname": "rpi002", "ip": "10.0.0.13", "mac": "b8:27:eb:53:3e:99"}, {"hostname": "rpi001", "ip": "10.0.0.11", "mac": "b8:27:eb:db:dd:97"}]}', 'jsonrpc': '2.0', 'id': 'generateJson'}
##{'jsonrpc': '2.0', 'id': 'generateJson', 'result': 'Invalid Token'}

########################################
## ENTRADA ##
#rpc['storageJson'] = SysRp().storageJson
#print(rpc({"jsonrpc": "2.0", "method": "storageJson", "params": {"json": GeneratedJson, "token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "storageJson"}))
## SALIDA ##
#{'id': 'storageJson', 'result': 'Done', 'jsonrpc': '2.0'}
#{'jsonrpc': '2.0', 'id': 'storageJson', 'result': 'Invalid Token'}

########################################
## ENTRADA ##
#rpc['setHostname'] = SysRp().setHostname
#print(rpc({"jsonrpc": "2.0", "method": "setHostname", "params": {"hostnameOld": "rpi111", "hostnameNew": "rpi001", "token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "setHostname"}))
## SALIDA ##
#{'id': 'setHostname', 'result': 'Done', 'jsonrpc': '2.0'}
#{'jsonrpc': '2.0', 'id': 'setHostname', 'result': 'Invalid Token'}

########################################
## ENTRADA ##
#rpc['reboot'] = SysRp().reboot
#print(rpc({"jsonrpc": "2.0", "method": "reboot", "params": {"hostname": "rpi111", "token": "8d8be393a73c16638467f3f6e8a35be6e1b12a22281ebac5dc26ef51a6c443d1a96e82eae011c4f6b2544dbdbae0600839df283847ae39925298a7ca6ea27992:387a45b2c2ec4bf880637f49993bbc35"}, "id": "reboot"}))
## SALIDA ##
#{'id': 'reboot', 'result': 'Done', 'jsonrpc': '2.0'}
#{'jsonrpc': '2.0', 'id': 'reboot', 'result': 'Invalid Token'}

