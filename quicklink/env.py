import os
import socket 

from . import constants


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_env():
    hostname = socket.gethostname().upper()  
    return {
        constants.PRODHOST : constants.PRODENV,
        constants.SYSTHOST : constants.SYSTENV,
        constants.TESTHOST : constants.TESTENV,
    }.get(hostname, constants.DEVENV)
    
    
def get_log_level():
    env = get_env()
    return {
        constants.PRODENV : constants.LOGLEVEL_INFO,
        constants.SYSTENV : constants.LOGLEVEL_INFO,
        constants.TESTENV : constants.LOGLEVEL_INFO,
    }.get(env, constants.LOGLEVEL_DEBUG)
    
def get_database():
    test = {}
    syst = {}
    prod = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxx',
        'USER': 'xxx',
        'PASSWORD': 'xxx',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
        }
    }
    dev = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
           
    env = get_env()
    return {
        constants.PRODENV : prod,
        constants.SYSTENV : syst,
        constants.TESTENV : test,
    }.get(env, dev)