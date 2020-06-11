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
    if('uid' in session):
        userid = session['uid']
        if(request.form):
            print("here")
            #title = request.form.get('addBook')
            userid = session['uid']
            name = request.form.get("shelfName")
            description = request.form.get("shelfDescription")
            flash([name, description])
            print(userid)
            print(name)
            db.add_shelf(userid, name, description)
            #print(title)
            #flash(title)
        collection = db.get_my_shelves(userid)
        return render_template("myshelves.html", userid = userid, collection = collection)
    else:
        flash("You must log in to view your bookshelves.")
        return render_template("home.html")

@app.route('/newshelf', methods=["GET","POST"])
def newshelf():
    return render_template("newshelf.html")

@app.route("/<shelf_id>/shelf", methods=["GET","POST"])
def shelf(shelf_id):
    print(shelf_id)
    shelf_info = db.get_shelf_info(shelf_id)
    print(shelf_info)
    name = shelf_info[0][0]
    description = shelf_info[0][1]
    mybooks = db.get_shelf_books(shelf_id)
    print(mybooks)
    if(mybooks != []):
        bookdata = [get_bookinfo(id) for id in mybooks[0]]
        print(bookdata)
        return render_template("shelf.html", shelf_id=shelf_id, name=name, description=description, books=bookdata)
    else:
        return render_template("shelf.html", shelf_id=shelf_id, name=name, description=description)

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

@app.route("/<shelf_id>/addbook", methods=["GET","POST"])
def addbook(shelf_id):
    maybeBook = request.form.get("newBook")
    print(shelf_id)
    book_id = db.searchfor_book(maybeBook)
    if book_id != False:
        db.addbook(book_id, shelf_id)
    print(maybeBook)
    print(book_id)
    print("hi")
    flash("mayeb")
    return redirect( url_for('shelf', shelf_id=shelf_id))

@app.route('/book/<title>')
def bookdata(title):
    data = db.searchfor_book(title)
    book_title = data['title']
    description = data['description']
    rating = data['rating']
    authors = data['authors']
    genres = data['genres']
    pages = data['pages']
    url = data['cover_url']
    return render_template("book.html", title=book_title, description=description, rating=rating, authors=authors, genres=genres, pages=pages, url=url)

@app.route('/book/11/22/1963')
def special_case():
    title = '11/22/1963'
    data = db.searchfor_book(title)
    book_title = data['title']
    description = data['description']
    rating = data['rating']
    authors = data['authors']
    genres = data['genres']
    pages = data['pages']
    url = data['cover_url']
    return render_template("book.html", title=book_title, description=description, rating=rating, authors=authors, genres=genres, pages=pages, url=url)

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

if __name__ == '__main__':
    app.debug = True
    app.run()
