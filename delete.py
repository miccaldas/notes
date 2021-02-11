""" Module to update notes to database """

import sqlite3
from colr import color


def delete():
    ident = input(color(' ID to delete? » ', fore='#cf4647'))

    try:
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        query = " DELETE FROM notes WHERE ntid = " + ident
        cur.execute(query)
        conn.commit()

    except sqlite3.Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    delete()
