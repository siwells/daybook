import ConfigParser

from flask import abort, Flask, json, redirect, render_template, request, url_for

import configuration

app = Flask(__name__)

configuration.init(app)
configuration.logs(app)

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        print request.method, request.path
        print request.form
        button = request.form['button']
        if button  == 'join':
            return render_template('verify.html')
        elif button == 'login':
            return render_template('diary.html')
            #return redirect(url_for('.diary'))
    return render_template('index.html')

@app.route('/diary')
def diary():
    diary_entries = [
        {
            "id":"1",
            "date": "Friday 7th June 2013", 
            "time": "09:00",
            "destination": "home",
            "duration":"90",
            "legs": [
                {
                    "rating": "1", 
                    "mode": "bus", 
                    "no": "1"
                },
                 {
                    "rating": "5", 
                    "mode": "bke", 
                    "no": "2"
                }
            ], 
            "notes": "the quick", 
            "origin": "away", 
            "overall_rating": "5"
        },
        {
            "id": "2",
            "date": "Saturday 8th June 2013", 
            "time": "16:00",
            "destination": "away",
            "duration":"45",
            "legs": [
                {
                    "rating": "2", 
                    "mode": "m", 
                    "no": "1"
                }
            ], 
            "notes": "brown fox", 
            "origin": "home", 
            "overall_rating": "3"
        }

    ]
    
    print diary_entries
    print json.dumps(diary_entries)
    return render_template('diary.html', diary_entries = diary_entries, diary = json.dumps(diary_entries))

@app.route('/entry', methods=['GET', 'POST'])
def entry():
	if request.method == 'POST':
		print request.method, request.path
		print request.form
	return render_template('entry.html')

@app.route('/join')
def join():
    return "JOIN"

@app.route('/login')
def login():
    return "LOGIN"

@app.route('/logout')
def logout():
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

