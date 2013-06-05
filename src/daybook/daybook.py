import ConfigParser
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

import configuration

app = Flask(__name__)
config = configuration.init(app)

log_pathname = app.config['log_location'] + app.config['log_file']
file_handler = RotatingFileHandler(log_pathname, maxBytes=1024* 1024 * 100 , backupCount=1024)
file_handler.setLevel( app.config['log_level'] )
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s")
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

@app.route('/')
def api_root():
    return "Welcome to the DayBook Homepage"

@app.route('/join')
def api_login():
    return "JOIN"

@app.route('/login')
def api_login():
    return "LOGIN"

@app.route('/logout')
def api_logout():
    return "LOGOUT"
    
if __name__ == '__main__':
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']), 
        threaded=app.config['threaded'])
