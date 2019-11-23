from pymongo import MongoClient
from functools import wraps
from config import Config
from flask import g


class Connect(object):
    @staticmethod
    def get_connection():
        if Config.TESTING:
            return MongoClient(Config.DB_SERVER).Development
        else:
            return MongoClient(Config.DB_SERVER).Production


def db_connection_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.db = Connect.get_connection()
        return f(*args, **kwargs)

    return decorated_function
