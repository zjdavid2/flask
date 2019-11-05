class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    TESTING = False
    DB_SERVER = 'mongodb://localhost:27017'
    SECRET_KEY = "ZQMjAJ3zFroBQfjvJNHE"
    API_KEY = 'taXbcZo1YsLGy4cUAt5WxHkptFd1M139toaMzqOYe9zul6dBfqBSTZZ643io'
    UPLOAD_FOLDER = '/img'
