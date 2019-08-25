from typing import List, Tuple
from utils.database_connection import DatabaseConnection

Word = Tuple[str, str, str]

def access_word_table(database) -> List[Word]:
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Word_table')
        words = cursor.fetchall()
    return words

def mark_as_read(database, Word):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE Word_table SET read=1 WHERE Word=?', (str(Word),))

def remove_word(database, Word):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Word_table WHERE Word=?', (str(Word),))

def add_word(database, Word, Pronunciation, English, Read):
    with DatabaseConnection(database) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Word_table VALUES (?,?,?,?)', (Word, Pronunciation, English, Read))

