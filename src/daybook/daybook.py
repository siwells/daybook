# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import ConfigParser

from flask import abort, Flask, flash, json, redirect, render_template, request, url_for, _request_ctx_stack

import configuration

app = Flask(__name__)

configuration.init(app)
configuration.logs(app)

from flask.ext.babel import Babel, gettext
babel = Babel(app)

from datetime import datetime
from functools import wraps

LANGUAGES = {
    'ca': 'Catalan',
    'en': 'English',
    'es': 'Español',
    'fi': 'Finnish',
    'it': 'Italian'
}

def setlocale(f):
    @wraps(f)
    def new_f(*args, **kwargs):
        lang = request.args.get('lang', None)
        if lang is not None:
            ctx = _request_ctx_stack.top
            ctx.babel_locale = lang
        return f(*args, **kwargs)
    return new_f

@babel.localeselector
def get_locale():
    #user = getattr(g, 'user', None)
    #if user is not None:
    #    return user.locale
    return request.accept_languages.best_match(LANGUAGES.keys())

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        print request.method, request.path
        print request.form
        button = request.form['button']
        if button  == 'join':
            msg = gettext("An email has been sent to {kwarg} so that you can verify your email address. Please follow the instructions in the email. Once you have confirmed your email account you will be able to log in.").format(kwarg=request.form['email'])
            flash(msg)
            return render_template('index.html')
        elif button == 'login':
            #return render_template('diary.html')
            return redirect(url_for('.dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    entry_list = [
        {
            "id": "1",
            "date": "Wednesday, 7th August, 2013"
        },
        {
            "id": "2",
            "date": "Thursday, 8th August, 2013"
        },
        {
            "id": "3",
            "date": "Friday, 9th August, 2013"
        },
        {
            "id": "4",
            "date": "Saturday, 10th August, 2013"
        }
    ]

    #print entry_list
    print json.dumps(entry_list)
    
    return render_template('dashboard.html', entry_list = entry_list)

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
                    "no": "1",
                    "duration": "50"
                },
                 {
                    "rating": "5", 
                    "mode": "bke", 
                    "no": "2",
                    "duration": "30"
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
                    "no": "1",
                    "duration": "45"
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
        msg = gettext("Your journey entry was added to your diary")
        flash(msg)
        return redirect( url_for('.dashboard') )
    
    return render_template('entry.html')

@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        print request.method, request.path
        print request.form

        msg = gettext("An email was sent to {arg}").format(arg=request.form['email'])
        flash(msg)

        return redirect(url_for('.root'))

    return render_template('recover.html')

@app.route('/logout')
def logout():
    return redirect( url_for('.root') )

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')

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

