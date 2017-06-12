# -*- coding: utf-8 -*-
from Mongo.connection import MongoDBconnection
import pdb


class RaspberryDB(object):
    _conn = None
    def __init__(self):
        self._conn = MongoDBconnection()

    def _getCollection(self,collection):
        return self._conn.getDB()[collection]

    def searchAll(self,collection=None):
        return [ element for element in self._getCollection(collection).find()]

    def searchLogin(self,collection=None,  user=None):
        return [ element for element in self._getCollection(collection).find(
            {
                "user": user
            }
        )]

    def searchStatus(self,collection=None,  ip=None):
        return [ element for element in self._getCollection(collection).find(
            {"ip": ip},{"status":""}
        )]

    def insertGeneric(self,collection,data):
        self._getCollection(collection=collection).insert(dict(data))

    def deleteElement(self,collection,hash):
        return self._getCollection(collection=collection).find_one_and_delete({"hash": hash})

    def updateOrCreate(self,collection,ip,status):
        return self._getCollection(collection=collection).update({"ip": ip},{"ip": ip,"status":status}, upsert=True)

