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

# =============== STARTUP FUNCTION CALLS ===============
init_tables()
