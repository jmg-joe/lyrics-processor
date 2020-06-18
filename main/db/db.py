import pymongo
import os
import defaults
print(defaults.defaults)

class Mongo:
    def __init__(self, dbname):
        self._conn = pymongo.MongoClient(
            'mongodb://localhost:' + defaults.defaults['db_port'] + '/')
        self._db = self._conn[dbname]

    def getFrequencyObj(self, artist):
        return self._db['lyrics'].find({'artist': artist})

    def saveFrequencyObj(self, freqObj):
        self._db['lyrics'].insert_one(freqObj)

    def saveMasterFreq(self, freqObj):
       self._db['artists'].insert_one(freqObj)
    
    def getMasterFreq(self, artist):
        return self._db['artists'].find({'artist': artist})
        
    def getArtistCount(self, artist):
        return self._db['lyrics'].find({'artist': artist}).count()
    
