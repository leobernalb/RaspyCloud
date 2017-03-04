import pymongo


config = {
    # MONGO CONFIG
    "USERNAME": None,
    "PASSWORD": None,
    "HOST": "localhost",
    "PORT": 27017,
    "DB_NAME": "raspyCloud",
}


class Config(object):
    def __init__(self):
        self._config = config

class MongoConfig(Config):

    @property
    def username(self):
        return self._config['USERNAME']

    @property
    def password(self):
        return self._config['PASSWORD']

    @property
    def host(self):
        return self._config['HOST']

    @property
    def port(self):
        return self._config['PORT']

    @property
    def db_name(self):
        return self._config['DB_NAME']
