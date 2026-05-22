from functools import lru_cache
from pymongo import MongoClient
from pymongo.database import Database
from django.conf import settings


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient:
    """Returns a singleton MongoDB client with connection pooling."""
    return MongoClient(settings.MONGO_URI, maxPoolSize=10)


def db_conexion() -> Database:
    """Establishes a connection to the MongoDB database (reuses pooled client)."""
    return get_mongo_client()[settings.MONGO_DBNAME]
