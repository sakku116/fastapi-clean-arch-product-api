from pymongo import MongoClient
from pymongo.database import Database

def getMongoDB(uri: str, db_name: str) -> Database:
    conn = MongoClient(uri)
    return conn[db_name]