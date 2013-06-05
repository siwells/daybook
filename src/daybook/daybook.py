import ConfigParser
import logging

from flask import Flask

import configuration

app = Flask(__name__)
config = configuration.init(app)
log_pathname = app.config['log_location'] + app.config['log_file']
logging.basicConfig(filename=log_pathname, level=logging.getLevelName( app.config['log_level'] ))
log = logging.getLogger('daybook')

@app.route('/')
def api_root():
    return "Welcome to the DayBook Homepage"
    
if __name__ == '__main__':
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']), 
        threaded=app.config['threaded'])
