from pymongo import MongoClient


def db_conexion():
    client = MongoClient(host='localhost',
                         port=27017,
                         username='admin',
                         password='mongo')
    db = client['pesrtwc']
    return db
