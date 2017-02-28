# -*- coding: utf-8 -*-
from connection import MongoDBconnection
import pdb


class RaspberryDB(object):
    _conn = None
    def __init__(self):
        self._conn = MongoDBconnection()

    def _getCollection(self,collection):
        return self._conn.getDB()[collection]

    def searchAll(self,collection=None):
        return [ element for element in self._getCollection(collection).find()]

    def searchLogin(self,collection=None, user=None, hash=None):
        return [ element for element in self._getCollection(collection).find(
            {
                "user": user, "hash": hash
            }
        )]

    def insertGeneric(self,collection,data):
        self._getCollection(collection=collection).insert(dict(data))

    def deleteElement(self,collection,hash):
        return self._getCollection(collection=collection).find_one_and_delete({"hash": hash})