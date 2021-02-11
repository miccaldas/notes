""" Module to insert notes to database """
import time
import sqlite3
import click
from colr import color
import fire


def add():
    titulo = input(color(' Title? » ', fore='#cf4647'))
    kwd1 = input(color(' Choose a keyword » ', fore='#cf4647'))
    kwd2 = input(color(' Choose another ... » ', fore='#cf4647'))
    kwd3 = input(color(' And another... » ', fore='#cf4647'))
    print(color(' Write the note.', fore='#cf4647'))
    time.sleep(0.2)
    nota = click.edit(editor='vim').rstrip()
    # Na apresentação da db, havia uma linha vazia entre os campos note e time. rstrip elimina essa linha.

    answers = [titulo, kwd1, kwd2, kwd3, nota]

    try:
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        query = """ INSERT INTO notes (title, k1, k2, k3, note) VALUES (?, ?, ?, ?, ?) """
        cur.execute(query, answers)
        conn.commit()

    except sqlite3.Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    fire.Fire(add)
