# -*- coding: utf-8 -*-
import pymongo
from Mongo.settings import MongoConfig


class MongoDBconnection(object):

    _nameDB = None

    def __init__(self):
        self._connectionDB()

    def _connectionDB(self):
        configuration = MongoConfig()
        mongoClient = pymongo.MongoClient(host=configuration.host, port=configuration.port)
        
        # Sin autenticacion
        db = mongoClient[configuration.db_name]

        # Si mongo requiere autenticacion con usuario y contrasenna
        if configuration.username is not None:
            db.authenticate(configuration.username, password=configuration.password)

        # Devolvemos la bbdd usada. En nuestro caso "rpCloud"
        self._nameDB = db

    def getDB(self):
        return self._nameDB
