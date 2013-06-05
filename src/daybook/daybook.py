import ConfigParser

from flask import abort, Flask, json, redirect, render_template, request, url_for

import configuration

app = Flask(__name__)

configuration.init(app)
configuration.logs(app)

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        button = request.form['button']
        if button  == 'join':
            return redirect(url_for('.diary'))
        elif button == 'login':
            return redirect(url_for('.diary'))
    return render_template('index.html')

@app.route('/diary')
def diary():
    return "VIEW PREVIOUS ENTRIES"

@app.route('/entry')
def entry():
    return "NEW JOURNEY DIARY ENTRY"

@app.route('/join')
def join():
    return "JOIN"

@app.route('/login')
def ogin():
    return "LOGIN"

@app.route('/logout')
def ogout():
    return "LOGOUT"
    
@app.errorhandler(404)
def status_404(exception):
    msg = {"Method": request.method, "URL":request.url}
    app.logger.error(json.dumps(msg))
    app.logger.exception(exception)
    return "404", 404

@app.errorhandler(500)
def status_500(exception):
    msg = {"Method": request.method, "URL":request.url}
    app.logger.error(json.dumps(msg))
    app.logger.exception(exception)
    return "500", 500
    
if __name__ == '__main__':
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']), 
        threaded=app.config['threaded'])
