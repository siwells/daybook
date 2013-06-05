import ConfigParser

from flask import Flask

import configuration

app = Flask(__name__)

configuration.init(app)
configuration.logs(app)

@app.route('/')
def api_root():
    app.logger.info("hello")
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
