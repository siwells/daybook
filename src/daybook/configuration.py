import ConfigParser
import logging

from logging.handlers import RotatingFileHandler

from flask import Flask

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)
        
        app.config['DEBUG'] = config.get("daybook", "debug")
        app.config['threaded'] = config.get("daybook", "threaded")
        app.config['SECRET_KEY'] = config.get("daybook", "secret_key")
        app.config['ip_address'] = config.get("daybook", "ip_address")
        app.config['port'] = config.get("daybook", "port")

        app.config['db_name'] = config.get("userdb", "name")
        app.config['db_ipaddress'] = config.get("userdb", "ip_address")
        app.config['db_port'] = config.get("userdb", "port")

        app.config['log_file'] = config.get("logging", "name")
        app.config['log_location'] = config.get("logging", "location")
        app.config['log_level'] = config.get("logging", "level")
    except:
        print "Could not read configs from: ", config_location

def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes=1024* 1024 * 10 , backupCount=1024)
    file_handler.setLevel( app.config['log_level'] )
    formatter = logging.Formatter("%(levelname)s | %(asctime)s |  %(module)s | %(funcName)s | %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
