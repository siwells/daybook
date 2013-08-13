# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import ConfigParser

from flask import abort, Flask, flash, json, jsonify, redirect, render_template, request, session, url_for, _request_ctx_stack

import configuration

app = Flask(__name__)

configuration.init(app)
configuration.logs(app)

from flask.ext.babel import Babel, gettext
babel = Babel(app)

LANGUAGES = {
    'ca': 'Catalan',
    'en': 'English',
    'de': 'Deutsch',
    'es': 'Español',
    'fi': 'Finnish',
    'it': 'Italian'
}

from datetime import datetime
from functools import wraps

import db

userdb = db.init_db(app.config["userdb_name"], app.config["userdb_ipaddress"] + ":" + app.config["userdb_port"])
db.add_views(userdb)
datadb = db.init_db(app.config["datadb_name"], app.config["datadb_ipaddress"] + ":" + app.config["datadb_port"])

import data
import users


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

def requires_login(f):
    """
    Checks whether the user is logged in. If so display requested page. Otherwise redirect to index page.

    Used by HTML based pages to ensure that only logged in users can access protected resources.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect(url_for('.root', next=request.path))
        return f(*args, **kwargs)
    return decorated

def check_auth(email, password):
    """
    Checks the user's email and password against the user db
    """
    if users.check_password(userdb, email, password):
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
def root():
    #print "lang: ", request.accept_languages.best_match(LANGUAGES.keys())
    if request.method == 'POST':
#        print request.method, request.path
#        print request.form
        button = request.form['button']
        if button  == 'join':
#            print request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password'], request.form['password_confirmation']

            if request.form['password'] == request.form['password_confirmation']:
#                print 'Passes Match - Creating new account'
                lang = request.accept_languages.best_match(LANGUAGES.keys())

                users.add_user(userdb, request.form['email'], request.form['password'], request.form['first_name'], request.form['last_name'], lang)

                

                msg = gettext("An email has been sent to {kwarg} so that you can verify your email address. Please follow the instructions in the email. Once you have confirmed your email account you will be able to log in.").format(kwarg=request.form['email'])
            else:
                msg = gettext("The supplied passwords do not match. Please ensure that you type the same password into both the password box and the confirmation box.")

            flash(msg)


           
        elif button == 'login':
#            print request.form['email'], request.form['password']

            if check_auth(request.form['email'], request.form['password']):
                session['email'] = request.form['email']
                session['uuid'] = users.get_uuid(userdb, session['email'])
                session['logged_in'] = True
                return redirect(request.args['next'] if 'next' in request.args else url_for('.dashboard'))
            
            msg = gettext("The supplied password was incorrect")
            flash(msg)
            return render_template('index.html')
            #return redirect(url_for('.dashboard'))


    try:
        if session['cookie_notified']:
            return render_template('index.html')
    except KeyError:
        alertlist = [
            {
                "msg":gettext('This site uses cookies. By continuing to browse the site you are agreeing to our use of cookies.'),
                "type":"cookie_notification",
            }
        ]
        return render_template('index.html', alertlist = alertlist)

@app.route('/dashboard')
@requires_login
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
    #print json.dumps(entry_list)
    
    return render_template('dashboard.html', entry_list = entry_list)

@app.route('/diary')
@requires_login
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
    
#    print diary_entries
#    print json.dumps(diary_entries)
    return render_template('diary.html', diary_entries = diary_entries, diary = json.dumps(diary_entries))

@app.route('/entry', methods=['GET', 'POST'])
@requires_login
def entry():
    if request.method == 'POST':
#        print request.method, request.path
#        print request.form

        date = request.form['date_day'] +":"+ request.form['date_month'] +":"+ request.form['date_year']
        time = request.form['time_hour'] +":"+ request.form['time_minute']
        duration = request.form['duration_hour'] +":"+ request.form['duration_minute']

        current_leg = 1
        morelegs = True
        legs = []

        while morelegs is True:
            mode_str = "mode_"+str(current_leg)
            rating_str = "rating_"+str(current_leg)
            hour_str = "leg_duration_hour_"+str(current_leg)
            min_str = "leg_duration_minute_"+str(current_leg)

            leg_mode = request.form.get(mode_str, False)
            if leg_mode is False:
                morelegs = False
            else:
                leg_duration = request.form[hour_str] +":"+ request.form[min_str]

                leg = {"rating": request.form[rating_str], "mode": leg_mode, "duration": leg_duration, "no": current_leg}
                legs.append(leg)

                current_leg = current_leg + 1
       
        entry = {"origin": request.form['origin'], "destination": request.form['destination'], "overall_rating": request.form['overall_rating'], "notes": request.form['notes'], "date": date, "time": time, "duration": duration, "legs": legs}

        data.add_entry(datadb, session['uuid'], entry)

        msg = gettext("Your journey entry was added to your diary")
        flash(msg)
        return redirect( url_for('.dashboard') )
    
    return render_template('entry.html')

@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
#        print request.method, request.path
#        print request.form

        msg = gettext("An email was sent to {arg}").format(arg=request.form['email'])
        flash(msg)

        return redirect(url_for('.root'))

    return render_template('recover.html')

@app.route('/cookiestatus', methods=['POST'])
def response():
    session['cookie_notified'] = True
    reply = {'status':'ok'}
    return jsonify(reply)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('email')
    session.pop('uuid')
    return redirect( url_for('.root') )

@app.route('/settings', methods=['GET', 'POST'])
@requires_login
def settings():
    if request.method == "POST":
#        print request.method, request.path
#        print request.form

        button = request.form['button']
        if button  == 'update_pw_button':
            current = request.form['existing_pass']
            pw1 = request.form['new_pass_one']
            pw2 = request.form['new_pass_two']
            print pw1, pw2
            if pw1 == pw2:
                msg = gettext("Your password has been updated")
            else:
                msg = gettext("Please ensure that your new passwords match")
            flash(msg)
        
        elif button == 'update_lang_button':
            print "lang"
            msg = gettext("Your default language settings have been updated")
            flash(msg)

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

