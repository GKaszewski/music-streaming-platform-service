import os

class Config(object):
    SECRET_KEY = os.environ.get('key.txt') or 'asdghbhkjhturiyihkbnmnvb'