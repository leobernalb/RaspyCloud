from Mongo.helper import RaspberryDB
import hashlib, uuid


class RpCloud(object):


    def __init__(self):
        """Attributes"""
        # Generamos una semilla distinta para cada usuario
        self.salt = uuid.uuid4().hex


    def register(self, firstName, lastName, email, password):
        conn = RaspberryDB()
        # Generaramos el Hash de usuario en sha512 con el siguiente formato salt + password : salt
        self.hash = hashlib.sha512(self.salt.encode() + password.encode()).hexdigest() + ':' + self.salt
        data = {"firstName": firstName,"lastName": lastName, "email": email, "hash": self.hash}
        # Insertamos datos en Mongo dentro de la collection LOGIN
        conn.insertGeneric(collection="login",data=data)
        # Devuelve en Hash en jsonRPC
        return self.hash


    def checkPassword(self, token, user_password):
        # Split por : para obtener el salt
        password, salt = token.split(':')
        # Devuelve TRUE or FALSE en jsonRPC
        return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()

    def checkLogin(self, email, password):
        conn = RaspberryDB()
        searched = conn.searchLogin(collection="login",  email=email)

        if len(searched) == 0:
            return False
        else:
            # Si la busqueda tiene 1 o mas elementos, buscamos coincidencia entre los hashes de ese usuario
            for i in searched:
                checkpass = self.checkPassword(i.get("hash"), password)
                if checkpass:
                    res = i.get("hash")
                    break
                else:
                    res = False
        return res


    def logout(self, token):
        # Encuentra elemento en BD y elimina
        conn = RaspberryDB()
        foundUser = conn.deleteElement(collection="login", hash=token)
        # Si encuentra el hash de usuario y lo borra, devuelve "OK"
        if foundUser != None:
            return "Ok"
        # Si no encuentra el Hash de usuario, devuelve "None"

