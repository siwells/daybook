import ConfigParser
from flask import Flask

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)
        app.debug = config.get("daybook", "debug")
        app.threaded = config.get("daybook", "threaded")
        app.secret_key = config.get("daybook", "secret_key")
        app.ip_address = config.get("daybook", "ip_address")
        app.port = config.get("daybook", "port")
    except:
        print "Could not read configs from: ", config_location
    return config