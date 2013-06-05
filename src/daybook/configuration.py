import ConfigParser

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
        app.config['log_file'] = config.get("logging", "name")
        app.config['log_location'] = config.get("logging", "location")
        app.config['log_level'] = config.get("logging", "level")
    except:
        print "Could not read configs from: ", config_location

    return config