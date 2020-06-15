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
    collection = db.get_all_shelves()
    collection_books = []
    #print(collection)
    for shelf in collection:
        collection_books.append(db.get_shelf_books(shelf[0]))
    collection_bookinfo = []
    for shelf in collection_books:
            shelfdata = []
            for book in shelf:
                shelfdata.append(db.get_bookinfo(book[0]))
                print("added data to shelf")
            collection_bookinfo.append(shelfdata)
            print("added shelf to collection")
    print("collection:")
    print(collection)
    print("book info collection:")
    print(collection_bookinfo)
    return render_template("home.html", collection=collection, collection_bookinfo=collection_bookinfo)

@app.route('/myshelves', methods=["GET","POST"])
def myshelves():
    if('uid' in session):
        userid = session['uid']
        if(request.form):
            #title = request.form.get('addBook')
            userid = session['uid']
            name = request.form.get("shelfName")
            description = request.form.get("shelfDescription")
            flash([name, description])
            db.add_shelf(userid, name, description)
            #print(title)
            #flash(title)
        collection = db.get_my_shelves(userid)
        collection_books = []
        for shelf in collection:
            collection_books.append(db.get_shelf_books(shelf[0]))
        print(collection_books)
        collection_bookinfo = []
        for shelf in collection_books:
            shelfdata = []
            for book in shelf:
                print(book)
                shelfdata.append(db.get_bookinfo(book[0]))
            collection_bookinfo.append(shelfdata)
        return render_template("myshelves.html", userid=userid, collection=collection, collection_bookinfo=collection_bookinfo)
    else:
        flash("You must log in to view your bookshelves.")
        return redirect( url_for('home'))

@app.route('/newshelf', methods=["GET","POST"])
def newshelf():
    return render_template("newshelf.html")

@app.route("/<shelf_id>/shelf", methods=["GET","POST"])
def shelf(shelf_id):
    shelf_info = db.get_shelf_info(shelf_id)
    name = shelf_info[0][0]
    description = shelf_info[0][1]
    mybooks = db.get_shelf_books(shelf_id)
    mybooks = [ele[0] for ele in mybooks]
    if(mybooks != []):
        bookinfo = [db.get_bookinfo(book) for book in mybooks]
        return render_template("shelf.html", shelf_id=shelf_id, name=name, description=description, bookdata=bookinfo)
    else:
        return render_template("shelf.html", shelf_id=shelf_id, name=name, description=description)

@app.route("/delshelf")
def delete_shelf():
    if ('uid' in session):
        if ('shelf_id' in request.args):
            shelf_id = request.args.get('shelf_id')
            db.del_shelf(shelf_id)
        #flash("deleting: "+str(shelf_id))
        return redirect(url_for("myshelves"))
    flash("You must log in to view your bookshelves.")
    return render_template("home.html")

@app.route('/bookfinder', methods=["GET","POST"])
def bookfinder():
    genres = db.get_genres()
    if (request.form):
        #print(request.form)
        genre = request.form.get("genre")
        min = request.form.get("min")
        max = request.form.get("max")

        result = db.book_finder(genre, int(min), int(max))
        #print(result)
        books = result[0]
        num = int(result[1])
        return render_template("bookfinder.html", genres=genres, num=num, books=books)
    return render_template("bookfinder.html", genres=genres)

@app.route("/<shelf_id>/addbook", methods=["GET","POST"])
def addbook(shelf_id):
    book_name = request.form.get("newBook")
    return redirect(url_for('addbookbookfinder', shelf_id=shelf_id, book_name=book_name))
    #book_ids = db.searchfor_books(book_name)
#    print(book_ids)
    #if book_id != False and:
    #    db.add_book(int(shelf_id), str(book_id))
    #    flash("Added!")
    #return redirect( url_for('shelf', shelf_id=shelf_id))

@app.route("/<shelf_id>/addbookbookfinder/<book_name>", methods=["GET","POST"])
def addbookbookfinder(book_name, shelf_id):
    if(request.form):
        id = request.form['select']
        db.add_book(int(shelf_id), str(id))
        flash("Added!")
        return redirect( url_for('shelf', shelf_id=shelf_id))
    book_ids = db.searchfor_books(book_name)
    if (book_ids != False and len(book_ids) > 1):
        bookinfos = [db.get_bookinfo(book) for book in book_ids]
        return render_template("selectBook.html", shelf_id=shelf_id, book_name=book_name, bookinfos=bookinfos, num=len(book_ids))
    elif (book_ids != False and len(book_ids)) == 1:
        db.add_book(int(shelf_id), str(book_ids[0]))
        flash("Added!")
        return redirect( url_for('shelf', shelf_id=shelf_id))
    return redirect( url_for('shelf', shelf_id=shelf_id))

@app.route("/delbook")
def delbook():
    if ('uid' in session):
        if ('shelf_id' in request.args and 'book_id' in request.args):
            shelfid = request.args.get('shelf_id')
            bookid = request.args.get('book_id')
            db.del_book(shelfid, bookid)
            return redirect( url_for('shelf', shelf_id=shelfid))
        return redirect( url_for('myshelves'))
    return redirect(url_for("home"))

@app.route('/book/<book_id>', methods=["GET","POST"])
def bookdata(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        flash("Please enter a valid book ID.")
        return render_template("book.html")
    data = db.get_bookinfo(book_id)
    book_title = data['title']
    description = data['description']
    rating = data['rating']
    authors = data['authors']
    genres = data['genres']
    pages = data['pages']
    url = data['cover_url']
    author_books = db.searchfor_author(book_id)
    if('uid' in session):
        userid = session['uid']
        shelves = db.get_my_shelves(userid)
        if(request.form):
            bookshelf = request.form.get("shelf")
            #book_id = db.searchfor_book(book_title)
            for shelf in shelves:
                if shelf[1] == bookshelf:
                    shelf_id = shelf[0]
                    return redirect(url_for('addbookbookfinder', book_name=book_title, shelf_id=shelf_id))
        return render_template("book.html", title=book_title, description=description, rating=rating, authors=authors, genres=genres, pages=pages, url=url, shelves=shelves, author_books=author_books)
    return render_template("book.html", title=book_title, description=description, rating=rating, authors=authors, genres=genres, pages=pages, url=url, author_books=author_books)

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

# @app.route("/book/<book_id>")
# def book(book_id):
#     try:
#         book_id = int(book_id)
#     except ValueError:
#         flash("Please enter a valid book ID.")
#         return render_template("book.html")
#     book_data = db.get_bookinfo(int(book_id))
#     print(book_data)
#     return render_template("book.html", book_info = book_data)

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
