""" Module to update notes to database """
import time
from mysql.connector import connect, Error
import click


def update():
    coluna = input(click.style(' Column? » ', fg='magenta', bold=True))
    ident = input(click.style(' ID? » ', fg='magenta', bold=True))
    print(click.style(' Write your update', fg='magenta', bold=True))
    time.sleep(0.3)
    update = click.edit()
    vari = [coluna, update, ident]

    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="notes")
        cur = conn.cursor()
        query = """ UPDATE notes SET %s = %s WHERE id = %s """
        cur.execute(query, vari)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    update()
