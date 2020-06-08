# Flying Saucers
# Softdev2 pd9
# P05 -- The Bookshelf / Databasing Methods
# 2020-06-05
import sqlite3
import atexit
import os
DIR = os.path.dirname(__file__) or '.'
DIR += '/'

DB_FILENAME=DIR+'../dat/saucer.db'

def init_tables():
    tables = {
        'books' : [
            ['book_id','INTEGER PRIMARY KEY'],
            ['title','TEXT'],
            ['cover_url','TEXT'],
            ['description','TEXT'],
            ['rating','REAL'],
            ['rating_count','INTEGER']
            ] ,
        'users' : [
            ['uid','TEXT UNIQUE'], # its always gonna be a really big number but-LEAVE IT AS A STRING!
            ['email','TEXT'],
            ['username','TEXT'],
            ['access_token','TEXT']
            ] ,
        'bookshelves' : [
            ['shelf_id','INTEGER PRIMARY KEY'],
            ['uid','TEXT'],
            ['title','TEXT'],
            ['description','TEXT']
            ] ,
        'authors' : [
            ['book_id','INTEGER'],
            ['author','TEXT']
            ] ,
        'genres' : [
            ['book_id','INTEGER'],
            ['genre','TEXT']
            ] ,
        'shelfbooks' : [
            ['book_id','INTEGER'],
            ['shelf_id','INTEGER']
            ]
        }
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    for table in tables:
        command = 'CREATE TABLE IF NOT EXISTS %s (%s)' % (table,', '.join(map(lambda col: ' '.join(col),tables[table])) )
        c.execute(command)
    db.commit()
    db.close()
    return True

# =============== USERS DATABASE ===============

def update_user(uid,username,email,token):
    """Either add a new user to the database, or updates the existing entry for them.
    """
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute(
        'INSERT OR REPLACE INTO users (uid,username,email,access_token) VALUES (?,?,?,?);',
        (uid,username,email,token)
        )
    db.commit()
    db.close()

def get_token(uid):
    """Returns current access token for a specified uid"""
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute('SELECT access_token FROM users WHERE uid=?;',(uid,))
    res = c.fetchone()
    db.close()
    if res:
        return res[0]
    raise KeyError('uid not found')

def get_userinfo(uid):
    """Returns {username, email} for a specified uid"""
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute('SELECT username,email FROM users WHERE uid=?;',(uid,))
    db.commit()
    res = c.fetchone()
    db.close()
    if res:
        return {'username':res[0],'email':res[1]}
    raise KeyError('uid not found')

# =============== BOOKS/GENRES/AUTHORS DATABASE ===============

def get_bookinfo(book_id):
    """Return {title,description,rating,authors,genres,rating_count,cover_url} for a specified book_id"""
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute('SELECT title,cover_url,description,rating,rating_count FROM books WHERE book_id=?;',(book_id,))
    bookdata = c.fetchone()
    c.execute('SELECT author FROM authors WHERE book_id=?;',(book_id,))
    authors = list(map(lambda res: res[0], c.fetchone()))
    c.execute('SELECT genre FROM genres WHERE book_id=?;',(book_id,))
    genres = list(map(lambda res: res[0], c.fetchone()))
    return {
        'title':bookdata[0],
        'description':bookdata[2],
        'rating':bookdata[3],
        'authors':authors,
        'genres':genres,
        'rating_count':bookdata[4],
        'cover_url':bookdata[1]
        }

def searchfor_book():
    pass


# =============== STARTUP FUNCTION CALLS ===============
init_tables()


# =============== TEST CODE ===============
# update_user(3000000001,'bobama','bobama@gmail.com','eifadkmaskmdfdxc')
# update_user('58689492321','bobama','barack@gmail.com','jlfkeskdldfj')
# print(get_token('3000000001'))
# print(get_userinfo(58689492321))
