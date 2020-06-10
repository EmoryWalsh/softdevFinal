# Flying Saucers
# Softdev2 pd9
# P05 -- The Bookshelf / CSV file parsing
# 2020-06-08

import csv
import sqlite3
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/'

DB_FILENAME=DIR+'../dat/saucer.db'
CSV_FILENAME=DIR+'../dat/book_data.csv'

def load_csv():
    db = sqlite3.connect(DB_FILENAME)
    c = db.cursor()
    try:
        with open(CSV_FILENAME) as csvfile:
            csvreader = csv.DictReader(csvfile)
            # c.executemany('INSERT INTO books (title,cover_url,description,rating,rating_count) VALUES (:book_title, :image_url, :book_desc, :book_rating, :book_rating_count)',csvreader)
            # the above code would work, but it wouldn't be possible to get the book_ids as they're generated!
            c.execute('DELETE FROM books;')
            c.execute('DELETE FROM genres;')
            for book_id,row in enumerate(csvreader,start=1):
                row['book_id'] = book_id

                c.execute('INSERT INTO books (book_id,title,cover_url,description,rating,rating_count,pages) VALUES (:book_id, :book_title, :image_url, :book_desc, :book_rating, :book_rating_count, :book_pages)',row)

                authors = row['book_authors'].split('|')
                genres = row['genres'].split('|')
                def couple_with_id(data):
                    return (book_id,data)
                c.executemany('INSERT INTO authors (book_id,author) VALUES (?, ?)',map(couple_with_id,authors))
                c.executemany('INSERT INTO genres (book_id,genre) VALUES (?, ?)',map(couple_with_id,genres))
    except FileNotFoundError:
        print('CSV file not found, leaving book database as is')

    db.commit()
    db.close()

load_csv()
