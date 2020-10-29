from django.conf import settings
from pymongo import MongoClient

mongodb = settings.MONGO_DATABASES


class Mongo(object):

    @staticmethod
    def get_db(mogo_instance='mongoi3t'):

        host = mongodb[mogo_instance]['host']
        port = mongodb[mogo_instance]['port']
        user = mongodb[mogo_instance]['user']
        passwd = mongodb[mogo_instance]['password']
        database = mongodb[mogo_instance]['database']

        uri = f"mongodb://{user}:{passwd}@{host}:{port}/{database}"

        return MongoClient(uri)[database]



