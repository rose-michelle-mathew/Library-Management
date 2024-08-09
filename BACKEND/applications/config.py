class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'mysecretkey'
    SECURITY_PASSWORD_SALT = 'mysecuritypasswordsalt'

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT ="6379"
    CACHE_DEFULT_TIMEOUT = 300
