import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    API_KEY = os.environ.get('ESOLOGS_API_KEY') or 'enter API key here' 
