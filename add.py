""" Module to insert notes to database """
from mysql.connector import connect, Error
import time
import click
import fire


def add():
    titulo = input(click.style(' Title? » ', fg='magenta', bold=True))
    kwd1 = input(click.style(' Choose a keyword » ', fg='magenta', bold=True))
    kwd2 = input(click.style(' Choose another ... » ', fg='magenta', bold=True))
    kwd3 = input(click.style(' And another... » ', fg='magenta', bold=True))

    print(click.style(' Write a note.', fg='magenta', bold=True))
    time.sleep(0.2)
    nota = click.edit().rstrip()
    answers = [titulo, kwd1, kwd2, kwd3, nota]
    # Na apresentação da db, havia uma linha vazia entre os campos note e time. rstrip elimina essa linha.
    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="notes")
        cur = conn.cursor()
        query = """ INSERT INTO notes (title, k1, k2, k3, note) VALUES (%s, %s, %s, %s, %s) """
        cur.execute(query, answers)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    fire.Fire(add)
