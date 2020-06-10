# Flying Saucers
# Softdev2 pd9
# P05 -- The Bookshelf / Flask Routes
# 2020-06-05

from flask import Flask, render_template, request, session, url_for, redirect, flash

import os

from utl import databasing as db,csvparsing, google


app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/myshelves', methods=["GET","POST"])
def myshelves():
    return render_template("myshelves.html")

@app.route('/newshelf', methods=["GET","POST"])
def newshelf():
    if(request.form):
        title = request.form.get('addBook')
        print("HIS")
        print(title)
        flash(title)
    return render_template("newshelf.html")

@app.route('/bookfinder', methods=["GET","POST"])
def bookfinder():
    genres = db.get_genres()
    if (request.form):
        #print(request.form)
        genre = request.form.get("genre")
        min = request.form.get("min")
        max = request.form.get("max")

        result = db.book_finder(genre, int(min), int(max))
        books = result[0]
        num = int(result[1])
        #print(books)
        return render_template("bookfinder.html", genres=genres, num=num, books=books)
    return render_template("bookfinder.html", genres=genres)

@app.route('/help')
def help():
    return render_template("help.html")

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
        # TODO @kiran: review scopes!
        # print(request.args['code'])
        session['uid'] = google.trade_for_tokens( request.args['code'], request.base_url )
        userinfo = db.get_userinfo(session['uid'])
        flash('You have been logged in. Welcome, {0[username]}!'.format(userinfo))
        return redirect( url_for('home') )
    else:
        # user has just clicked a "login" link, needs to be redirected to google
        if 'uid' in session:
            flash('You are already logged in!')
            return redirect( url_for('home') )
        auth_url = google.gen_authlink( request.base_url )
        # print(auth_url)
        return redirect( auth_url )

@app.route("/logout")
def logout():
    if 'uid' in session: #checks that a user is logged into a session
        session.pop('uid') #logs the user out of the session
        flash("You have been logged out.")
        return redirect(url_for('home'))

    flash("You are already logged out.")
    return redirect(url_for('home'))

@app.route("/<shelf_id>/shelf", methods=["POST"])
def shelf(shelf_id):
    # idk how to access uid
    userid = session['uid']
    name = request.form.get("shelfName")
    description = request.form.get("shelfDesc")
    db.add_shelf(userid, name, description)
    # may need to create template for adding a shelf and I don't know how to add access the shelf id
    return render_template("shelf.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
