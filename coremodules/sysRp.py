from subprocess import Popen, PIPE
from Mongo.helper import RaspberryDB
import subprocess
from coremodules.rpCloud import RpCloud
from coremodules.arp import Arp
import unicodedata
import json
import re
import time

class SysRp(object):


    def __init__(self):
        self.conn = RaspberryDB()
        self.rP = RpCloud()
        self.arp = Arp()

    def createPartition(self, ip):
        # Status # Creating partitions
        self.conn.updateOrCreate(collection="status", ip=ip, status="Creating partitions")

        print("####################################### CREATE PARTITION #############################################")

        ## Dump de la tabla de particiones
        partition = subprocess.Popen(["rsh", ip, "sfdisk", "--dump", "/dev/mmcblk0"],
                                     stdout=subprocess.PIPE).communicate()[0]
        with open('/tmp/tablePartition'+ip+'.part', 'w') as outfile:
            outfile.write(partition.decode("utf-8"))

        sectorStartTwo = subprocess.Popen(["awk", "/^\/dev\/mmcblk0p2/{print $4}", "/tmp/tablePartition"+ip+".part"],
                                          stdout=subprocess.PIPE).communicate()[0]
        sectorStartTwo = sectorStartTwo.decode("utf-8").replace(",\n","")
        #print(sectorStartTwo)

        sectorTamSizeTwo = subprocess.Popen(["awk", "/^\/dev\/mmcblk0p2/{print $6}", "/tmp/tablePartition"+ip+".part"],
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

        mmcblk0p3 = subprocess.Popen(["awk", "/^\/dev\/mmcblk0p3/{print $0}", "/tmp/tablePartition"+ip+".part"],
                                     stdout=subprocess.PIPE).communicate()[0]
        mmcblk0p3 = mmcblk0p3.decode("utf-8").replace("\n", "")
        #print(mmcblk0p3)
        newLine = ("/dev/mmcblk0p3 : start="+ str(startNewPartition) + ", size="+ str(sectorsSizeNewPartition) + ", Id=83")
        subprocess.Popen(["sed", "-i", '/^\/dev\/mmcblk0p3/c' + newLine + "", "/tmp/tablePartition"+ip+".part"],
                         stdout=subprocess.PIPE).communicate()[0]
        sendPartition = subprocess.Popen(["scp", "/tmp/tablePartition"+ip+".part", ip + ":/tmp/."], stdout=subprocess.PIPE)
        time.sleep(3)
        subprocess.Popen(("rsh", ip, "sfdisk", "--force", "/dev/mmcblk0", "< /tmp/tablePartition"+ip+".part"), stdin=sendPartition.stdout).communicate()[0]



        ## Tamaño de sector (en bytes) el famoso 512!!!!!!!!!!!!!!!!!!!!!!!
        #tamSectors = subprocess.Popen(["rsh", ip, "blockdev", "--getss", "/dev/mmcblk0"], stdout=subprocess.PIPE).communicate()[0]
        ## Tamaño maximo de disco (en sectores) eso hay que multiplicarlo por 512
        #secSizek0 = subprocess.Popen(["rsh", ip, "blockdev", "--getsize", "/dev/mmcblk0"], stdout=subprocess.PIPE).communicate()[0]
        # blockdev --getsize64 /dev/mmcblk0 ### El tamaño de la particion ya multiplicado (en bytes!!!!!!!!!!!!!)



    def formatFileSystemAndMount(self, ip):
        # Status # Formatting
        self.conn.updateOrCreate(collection="status", ip=ip, status="Formatting")

        print("####################################### FORMAT PARTITION #############################################")
        subprocess.Popen(["rsh", ip, "umount", "/dev/mmcblk0p3"], stdout=subprocess.PIPE).communicate()[0]
        subprocess.Popen(["rsh", ip, "mkdir", "-p", "/mnt/img"], stdout=subprocess.PIPE).communicate()[0]
        subprocess.Popen(["rsh", ip, "mkfs.ext4", "/dev/mmcblk0p3"], stdout=subprocess.PIPE).communicate()[0]
        subprocess.Popen(["rsh", ip, "mount", "-t", "ext4", "/dev/mmcblk0p3", "/mnt/img/"], stdout=subprocess.PIPE).communicate()[0]



    def mountImgCompress(self, token):
        # Status # Deploying
        generatedJson = self.generateJson(token)

        for pi in generatedJson.get("raspberryPi"):
            self.conn.updateOrCreate(collection="status", ip=pi.get("ip"), status="Deploying")
            # Eliminamos todos los status e Insertamos datos en Mongo dentro de la collection STATUS
        #    self.conn.deleteDocuments(collection="status")
         #   self.conn.insertGeneric(collection="status", data=data)

        img = "/mnt/img/uploads/fileUploaded.img"
        print("####################################### MOUNT IMG SERVER #############################################")

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
        # Eliminamos el /var/lib/dhcp/* para limpiar el registro de ip por DHCP
        subprocess.Popen(["rm", "-r", "/mnt/img/two/var/lib/dhcp/"], stdout=subprocess.PIPE).communicate()[0]

        # Empaquetar y comprimir
        print("####################################### COMPRESS IMG #############################################")
        subprocess.Popen(['tar -czf /tmp/imagen.tar.gz .'], shell=True, cwd='/mnt/img/two').wait()
        print("####################################### FINISHED COMPRESS IMG #############################################")




    def sendAndDecompress(self, ip):
        # Status # Receiving image
        self.conn.updateOrCreate(collection="status", ip=ip, status="Receiving data")

        # Envio de img comprimida y descompresion en la rpi
        # Por defecto lee la imagen guardada en /mnt/img/ del servidor y la descomprime en el /mnt/img/ de la rpi
        print("####################################### SEND IMG #############################################")
        subprocess.Popen(["scp", "/tmp/imagen.tar.gz", ip + ":/mnt/img/."], stdout=subprocess.PIPE).communicate()[0]
        print("####################################### DECOMPRESS #############################################")
        # Status # Decompress
        self.conn.updateOrCreate(collection="status", ip=ip, status="Decompress")
        subprocess.Popen(["rsh", ip, "tar", "-xf", "/mnt/img/imagen.tar.gz", "-C", "/mnt/img/."], stdin=subprocess.PIPE).communicate()[0]





    def changePartition(self, ip, rescuteMode):

        print("####################################### CHANGE PARTITION #############################################")
        # Parseo de string a boolean
        if rescuteMode == 'true':
            rescuteMode = True
        elif rescuteMode == 'false':
            rescuteMode = False

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
        subprocess.Popen(["sleep", "3"], stdout=subprocess.PIPE).communicate()[0]  ## Espera 1 segundos para asegurarnos que se cambia la particion
        return "Done"




    def getHostname(self, ip):


        # Ejecutamos "rsh" para obtener el nombre cada raspberryPi a partir de su IP
        host = subprocess.Popen(["rsh", ip, "hostname"], stdout=subprocess.PIPE).communicate()[0]
        hostname = host.decode("utf-8").replace("\n", "")
        # Para convertir de unicode a string
        return unicodedata.normalize('NFKD', hostname).encode('ascii', 'ignore').decode("utf-8")




    def setHostname(self, token, hostnameOld, hostnameNew):

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





    def generateJson(self, token):

        listJson = []
        # [1::] se elimina la cabecera
        for i in self.arp.getTable(token)[1::]:
            # Los datos capturados de la tabla ARP son interpretados tipo "Bytes",
            # Para interpretarlos tipo "String" usamos el decode(utf-8)
            i = i.split()
            # Si empieza por una ip

            if (re.match('^10(\.0){2}', i[0]) and re.match('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', i[2])):

                # Busca si no hay elemento creado en mongo, lo crea
                if(self.conn.searchStatus(collection="status", ip=i[0]) == []):
                    data = {"ip": i[0], "status": ""}
                    self.conn.insertGeneric(collection="status", data=data)
                disk = self.disk(i[0])
                hostname = self.getHostname(i[0])
                searchedStatus = self.conn.searchStatus(collection="status", ip=i[0])
                listJson.append({'ip': i[0], 'mac': i[2], 'hostname': hostname, 'diskSize': disk[0], 'diskAvail': disk[1], 'diskUse': disk[2], 'status': searchedStatus[0].get('status')})

        # Incluir raspberryPi en el diccionario
        concatJson = {'raspberryPi': ''}
        concatJson['raspberryPi'] = listJson

        # Parsea a JSON
        return concatJson


    def disk(self, ip):

        df = subprocess.Popen(['rsh', ip, 'df', '-h'], stdout=subprocess.PIPE)
        diskSize = subprocess.check_output(("awk", "$6 ~ /^\/$/ {print $2}"), stdin=df.stdout).decode("utf-8").replace("\n","")
        df = subprocess.Popen(['rsh', ip, 'df', '-h'], stdout=subprocess.PIPE)
        diskAvail = subprocess.check_output(("awk", "$6 ~ /^\/$/ {print $4}"), stdin=df.stdout).decode("utf-8").replace("\n","")
        df = subprocess.Popen(['rsh', ip, 'df', '-h'], stdout=subprocess.PIPE)
        diskUse = subprocess.check_output(("awk", "$6 ~ /^\/$/ {print $5}"), stdin=df.stdout).decode("utf-8").replace("\n","")

        return [diskSize, diskAvail, diskUse]


    def storageJson(self, token):

        # Consultamos el JSON actual
        generatedJson = self.generateJson(token)


        # Con la opcion 'w' editamos el fichero. Si no existe, lo crea
        with open('Static/start.json', 'w') as outfile:
            json.dump(generatedJson, outfile)




    def reboot(self, token, hostname):

        print("####################################### REBOOT #############################################")

        # Consultamos el JSON actual
        generatedJson = self.generateJson(token)

        # Vamos hacer la traduccion de hostname -- ip.
        # Recorremos el array de raspberry
        for pi in generatedJson.get("raspberryPi"):

            if (pi.get("hostname") == hostname):
                dnsIp2 = pi.get("ip")
                # Status # Rebooting
                self.conn.updateOrCreate(collection="status", ip=dnsIp2, status="Rebooting")

        subprocess.Popen(["rsh", "root@" + dnsIp2, 'shutdown --reboot 0; exit'], stdout=subprocess.PIPE)

        print(self.checkMachine(dnsIp2))



    def checkMachine(self, ip):
        # Status # Checking
        self.conn.updateOrCreate(collection="status", ip=ip, status="Checking")
        print("####################################### MACHINE STATUS #############################################")
        # Hacemos 30 ping y si recibimos correctamente 5 o mas consideramos que la rpi esta "UP"
        ping = subprocess.Popen(["ping", "-c", "30", ip], stdout=subprocess.PIPE)
        pingNum = subprocess.check_output(('awk', '/received/{print $4}'), stdin=ping.stdout).decode("utf-8").replace("\n","")

        print(pingNum)
        if(int(pingNum) >= 5):
            # Status # Installed
            self.conn.updateOrCreate(collection="status", ip=ip, status="Installed")
            return "up"
        else:
            return "down"
