import ConfigParser

from flask import abort, Flask, json, request

import configuration

app = Flask(__name__)

configuration.init(app)
configuration.logs(app)

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
    
@app.errorhandler(404)
def status_404(e):
    msg = {"Method": request.method, "URL":request.url}
    app.logger.error(json.dumps(msg))
    return "404", 404

@app.errorhandler(500)
def status_500(exception):
    app.logger.exception(exception)
    return "500", 500

@app.route('/500')
def raise_500():
    abort(500)
    
if __name__ == '__main__':
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']), 
        threaded=app.config['threaded'])
