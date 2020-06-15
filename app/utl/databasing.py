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
            ['rating_count','INTEGER'],
            ['pages', 'INTEGER']
            ] ,
        'users' : [
            ['uid','TEXT UNIQUE'], # its always gonna be a really big number but-LEAVE IT AS A STRING!
            ['email','TEXT'],
            ['username','TEXT'],
            ['access_token','TEXT']
            ] ,
        'bookshelves' : [
            ['shelf_id','INTEGER PRIMARY KEY AUTOINCREMENT'],
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
    """Return {title,description,rating,authors,genres,rating_count,cover_url,pages} for a specified book_id"""
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute('SELECT title,cover_url,description,rating,rating_count,pages FROM books WHERE book_id=?;',(book_id,))
    bookdata = c.fetchone()
    #print(bookdata)
    c.execute('SELECT author FROM authors WHERE book_id=?;',(book_id,))
    authors = list(map(lambda res: res, c.fetchone()))
    for authors in authors:
        authors.replace("['", "" )
        authors.replace("']", "")
    c.execute('SELECT genre FROM genres WHERE book_id=?;',(book_id,))
    genres = list(map(lambda res: res, c.fetchall()))
    #print(genres)
    genresList = []
    for genre in genres:
        genre = list(genre)
        #print(genre[0])
        genre[0].replace("('", "" )
        genre[0].replace("',)", "")
        genresList.append(genre[0])
        #print(genre)
    return {
        'id':book_id,
        'title':bookdata[0],
        'description':bookdata[2],
        'rating':bookdata[3],
        'authors':authors,
        'genres':genresList,
        'rating_count':bookdata[4],
        'cover_url':bookdata[1],
        'pages':bookdata[5]
        }

def searchfor_book(book_title):
    """Return book_id for given book_title"""
    book_title = book_title.lower() #book_data.csv titles are uppercase
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    #find book_id associated w book_title (use first instance)
    c.execute('SELECT book_id FROM books WHERE lower(title)=? LIMIT 1;', (book_title,))
    book_id = c.fetchone()
    if (book_id):
        book_id = book_id[0]
        #find book data associated w book_id
        return book_id
    print("Book not found")
    return False

def searchfor_books(book_title):
    """Return book_id for given book_title"""
    book_title = book_title.lower() #book_data.csv titles are uppercase
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    #find book_id associated w book_title (use first instance)
    c.execute('SELECT book_id FROM books WHERE lower(title)=?;', (book_title,))
    books = c.fetchall()
    if books != None:
        bookList = []
        for book in books:
            #print(book)
            bookList.append(book[0])
        #find book data associated w book_id
        return bookList
    print("Book not found")
    return False

def searchfor_author(book_id):
    """Return all book by the author of book_id"""
    bookdata = get_bookinfo(book_id)
    author = bookdata['authors']
    #print(author)
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute('SELECT DISTINCT book_id FROM authors WHERE author=?;',(author,))
    books = c.fetchall()
    if(len(books)>1):
        other_books = []
        for book in books:
            if book[0] != book_id:
                other_books.append(get_bookinfo(book[0]))
        return other_books
    print("No other books by this author found.")
    return None

def get_genres():
    """Returns list of unique genres in book_data.csv"""
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute('SELECT DISTINCT genre FROM genres')
    genres = c.fetchall()
    res = [list(genre)[0].replace("'", "") for genre in genres]
    #print("The converted list of list : " + str(res))
    return res

def book_finder(genre, min_pg, max_pg):
    """Returns list of books that match input queries"""
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute("SELECT book_id FROM genres WHERE genre=? LIMIT 250;", (genre,))
    book_ids = c.fetchall()
    book_ids = [i for n, i in enumerate(book_ids) if i not in book_ids[n + 1:]]
    book_ids = [book_id[0] for book_id in book_ids]
    #print(book_ids)
    out = [] #output: relevant book_ids
    for book_id in book_ids:
        info = get_bookinfo(book_id)
        if info["pages"] and int(info["pages"].split(" ")[0]) >= min_pg and int(info["pages"].split(" ")[0]) <= max_pg:
            out.append(book_id)
            #print(book_id)
    print(str(len(out))+" books found.")
    out = [get_bookinfo(id) for id in out]
    #print(out[0:2])
    return [out, len(out)]

def add_shelf(uid, name, descr):
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor();
    print([uid, name, descr])
    c.execute("INSERT INTO bookshelves (uid, title, description) VALUES (?, ?, ?);", (uid, name, descr))
    db.commit()
    db.close()

def add_book(shelfid, bookid):
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute("INSERT INTO shelfbooks (book_id, shelf_id) VALUES (?, ?);", (bookid, shelfid))
    db.commit()
    db.close()

def del_book(shelfid, bookid):
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute("DELETE FROM shelfbooks WHERE shelf_id=? AND book_id=?;",(shelfid, bookid))
    db.commit()
    db.close()

def get_my_shelves(userid):
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute('SELECT shelf_id, title, description FROM bookshelves WHERE uid=?;',(userid,))
    myshelves = c.fetchall()
    return myshelves

def get_shelf_info(shelf_id):
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute('SELECT title, description FROM bookshelves WHERE shelf_id=?;',(shelf_id,))
    shelfinfo = c.fetchall()
    return shelfinfo

def get_shelf_books(shelf_id):
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute('SELECT book_id FROM shelfbooks WHERE shelf_id=?;',(shelf_id,))
    mybooks = c.fetchall()
    #print(mybooks)
    return mybooks

def del_shelf(shelf_id):
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    c.execute("DELETE FROM bookshelves WHERE shelf_id=?;",(shelf_id,))
    db.commit()
    db.close()
    print("deleted")
    return True

# =============== STRING HELPER FUNCTIONS ===============
def capitalize_title(str):
    words = str.split(" ");
    for word in words:
        if (word != 'and' and word != 'the' and word != 'the' and word != "of"):
            word = word.capitalize()
    out = " ".join(words)
    return out

# =============== LIST HELPER FUNCTIONS ===============
def list_primer(list): #turns a list into a list lists with 3 elements
    new = []
    idx_old = 0
    idx_new = 0
    while(idx_old < len(list)):
        new.append([])
        new[idx_new].append(list[idx_old])
        idx_old += 1
        if(idx_old < len(list)):
            new[idx_new].append(list[idx_old])
        idx_old += 1
        if(idx_old < len(list)):
            new[idx_new].append(list[idx_old])
        idx_old += 1
        idx_new += 1
    return new
# =============== STARTUP FUNCTION CALLS ===============
init_tables()


# =============== TEST CODE ===============
# update_user(3000000001,'bobama','bobama@gmail.com','eifadkmaskmdfdxc')
# update_user('58689492321','bobama','barack@gmail.com','jlfkeskdldfj')
# print(get_token('3000000001'))
# print(get_userinfo(58689492321))
#info = searchfor_book("Disgrace")
#print(info)
#get_genres()
#book_finder("Science Fiction", 300, 400)
#print(list_primer([3, 2, 6, 87, 2]))
#print(searchfor_books("pride and prejudice"))
#book = searchfor_author("160")
#rint(book[0]["title"])
