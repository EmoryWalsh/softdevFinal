# Flying Saucers
# Softdev2 pd9
# P05 -- The Bookshelf / Databasing Methods
# 2020-06-05
import sqlite3
import atexit
import os
DIR = os.path.dirname(__file__) or '.'
DIR += '/'

db = sqlite3.connect(DIR+'../saucer.db')
c = db.cursor()
atexit.register(lambda: db.close()) # idk if this is necessary


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
            ['uid','INTEGER PRIMARY KEY'],
            ['email','TEXT'],
            ['username','TEXT'],
            ['access_token','TEXT']
            ] ,
        'bookshelves' : [
            ['shelf_id','INTEGER PRIMARY KEY'],
            ['uid','INTEGER'],
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
    for table in tables:
        command = 'CREATE TABLE IF NOT EXISTS %s (%s)' % (table,', '.join(map(lambda col: ' '.join(col),tables[table])) )
        c.execute(command)
    db.commit()
    return True

# =============== USERS DATABASE ===============

def update_user(uid,username,email,token):
    """Either add a new user to the database, or updates the existing entry for them.
    Returns boolean `fresh`, True if user is added for the first time, False otherwise
    """
    c.execute(
        'INSERT OR REPLACE INTO users (uid,username,email,access_token) VALUES (?,?,?,?);',
        (int(uid),username,email,token)
        )
    db.commit()
    pass

def get_token(uid):
    """Returns current access token for a specified uid"""
    c.execute('SELECT access_token FROM users WHERE uid=?;',(int(uid),))
    db.commit()
    res = c.fetchone()
    if res:
        return res[0]
    raise NonexistentUserException('uid not found')

def get_userinfo(uid):
    """Returns {username, email} for a specified uid"""
    c.execute('SELECT username,email FROM users WHERE uid=?;',(int(uid),))
    db.commit()
    res = c.fetchone()
    if res:
        return {'username':res[0],'email':res[1]}
    raise NonexistentUserException('uid not found')

# =============== STARTUP FUNCTION CALLS ===============
init_tables()


# =============== TEST CODE ===============
# update_user(3000000001,'bobama','bobama@gmail.com','eifadkmaskmdfdxc')
# update_user('58689492321','bobama','barack@gmail.com','jlfkeskdldfj')
# print(get_token('3000000001'))
# print(get_userinfo(58689492321))
