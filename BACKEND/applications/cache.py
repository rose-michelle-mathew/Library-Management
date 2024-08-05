# applications/cache.py
from flask_caching import Cache

cache = Cache()

def init_app(app):
    # Configure cache here
    cache.init_app(app)
