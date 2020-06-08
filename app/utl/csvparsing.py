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
    with open(CSV_FILENAME) as csvfile:
        csvreader = csv.DictReader(csvfile)
        c.executemany('INSERT INTO books (title,cover_url,description,rating,rating_count) VALUES (:book_title, :image_url, :book_desc, :book_rating, :book_rating_count)',csvreader)
            # print(row['book_authors'],row['book_rating'])
    db.commit()
    db.close()

load_csv()
