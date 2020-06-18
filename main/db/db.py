import pymongo
import os
import defaults


class Mongo:
    def __init__(self, dbname):
        self._conn = pymongo.MongoClient(
            'mongodb://localhost:' + defaults.defaults['db_port'] + '/')
        self._db = self._conn[dbname]

    def getSongFrequency(self, artist):
        return self._db['lyrics'].find({'artist': artist})

    def saveSongFrequency(self, freqObj):
        self._db['lyrics'].insert_one(freqObj)

    def saveDiscographyFrequency(self, freqObj):
        self._db['artists'].insert_one(freqObj)

    def getDiscographyFrequency(self, artist):
        return self._db['artists'].find({'artist': artist})

    def getArtistCount(self, artist):
        return self._db['artists'].find({'artist': artist}).count()
