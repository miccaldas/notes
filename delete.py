""" Module to update notes to database """

from mysql.connector import connect, Error
import click


def delete():
    ident = input(click.style(' ID to delete? » ', fg='magenta', bold=True))

    try:
        conn = connect(
                        host="localhost",
                        user="mic",
                        password="xxxx",
                        database="notes")
        cur = conn.cursor()
        query = " DELETE FROM notes WHERE ntid = " + ident
        cur.execute(query)
        conn.commit()

    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    delete()
