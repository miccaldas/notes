""" Module to update notes to database """
import time
import sqlite3
import click
from colr import color


def update():
    coluna = input(color(' Column? » ', fore='#cf4647'))
    ident = input(color(' ID? » ', fore='#cf4647'))
    print(color(' Write your update', fore='#cf4647'))
    time.sleep(0.3)
    update = click.edit()

    try:
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        query = " UPDATE notes SET " + coluna + " = " + update + " WHERE ntid = " + ident
        print(query)
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    update()
