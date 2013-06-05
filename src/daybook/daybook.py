import ConfigParser

from flask import Flask

import configuration

app = Flask(__name__)
config = configuration.init(app)

@app.route('/')
def api_root():
    return "Welcome to the DayBook Homepage"
    
if __name__ == '__main__':
    app.run(host=app.ip_address, debug=app.debug, threaded=app.threaded, port=int(app.port))
