""" Module to see all of the database """

import sqlite3
from colr import color
import fire


def see():
    try:
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        query = """ SELECT * FROM notes """
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            print(color(' [0] ID » ', fore='#524656'), color(str(row[0]), fore='#e5ddcb'))
            print(color(' [1] TITLE » ', fore='#524656'), color(str(row[1]), fore='#e5ddcb'))
            print(color(' [2] KEYWORD 1 » ', fore='#524656'), color(str(row[2]), fore='#e5ddcb'))
            print(color(' [3] KEYWORD 2 » ', fore='#524656'), color(str(row[3]), fore='#e5ddcb'))
            print(color(' [4] KEYWORD 3 » ', fore='#524656'), color(str(row[4]), fore='#e5ddcb'))
            print(color(' [5] NOTE : ', fore='#524656'), color(str(row[5]), fore='#eb7b59'))
            print(color(' [6] TIME » ', fore='#524656'), color(str(row[6]), fore='#e5ddcb'))
            print('\n')
    except sqlite3.Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    fire.Fire(see)
