# Flying Saucers
# Softdev2 pd9
# P05 -- The Bookshelf / Flask Routes
# 2020-06-05

from flask import Flask, render_template, url_for, request, redirect
from utl import databasing as db
from utl import google

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/auth')
def google_auth():
    """Handle Google redirects, callbacks, etc."""
    if 'error' in request.args:
        # failure to authenticate
        print('error in request.args')
        print(request.url)
        return redirect( url_for('home') )
    if 'code' in request.args:
        # then user has already authorized: need to review scopes, exchange for tokens
        print(request.args['code'])
        google.trade_for_tokens( request.args['code'], request.base_url )
        return redirect( url_for('home') )
    else:
        # user has just clicked a "login" link, needs to be redirected to google
        auth_url = google.gen_authlink( request.base_url )
        print(auth_url)
        return redirect( auth_url )

    

if __name__ == '__main__':
    app.debug = True
    app.run()
