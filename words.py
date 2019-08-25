'''Creates database'''

import sqlite3
import csv

def create_database(csv_file, database, execute_create, execute_insert):
    f = open(csv_file,'r', encoding='utf-8', errors= 'ignore')
    next(f, None)
    reader = csv.reader(f)

    sql = sqlite3.connect(database)
    cursor = sql.cursor()
    cursor.execute(execute_create)

    for row in reader:
        cursor.execute(execute_insert, row)

    f.close()
    sql.commit()
    sql.close()

def delete_database_all(database):
    sql = sqlite3.connect(database)
    cursor = sql.cursor()
    cursor.execute("DROP TABLE Word_table")

def delete_database_unread(database):
    sql = sqlite3.connect(database)
    cursor = sql.cursor()
    cursor.execute("DROP TABLE Word_table")

def delete_database_read(database):
    sql = sqlite3.connect(database)
    cursor = sql.cursor()
    cursor.execute("DROP TABLE Word_table")

create_database('words.csv', 'words_all.db', '''CREATE TABLE IF NOT EXISTS Word_table 
    (Word, Pronunciation, English, Read)''', "INSERT INTO Word_table VALUES (?,?,?,0)")

create_database('words.csv', 'words_unread.db', '''CREATE TABLE IF NOT EXISTS Word_table 
    (Word, Pronunciation, English, Read)''', "INSERT INTO Word_table VALUES (?,?,?,0)")

create_database('words_read.csv', 'words_read.db', '''CREATE TABLE IF NOT EXISTS Word_table 
    (Word, Pronunciation, English, Read)''', "INSERT INTO Word_table VALUES (?,?,?,0)")

create_database('words_favorites.csv', 'words_favorites.db', '''CREATE TABLE IF NOT EXISTS Word_table 
    (Word, Pronunciation, English, Read)''', "INSERT INTO Word_table VALUES (?,?,?,0)")