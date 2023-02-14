""" Module to update notes to database """

import time

import click
from colr import color

from mysql.connector import Error, connect





def update():
    coluna = input(click.style(" Column? » ", fg="magenta", bold=True))
    update_ident = input(click.style(" ID? » ", fg="magenta", bold=True))
    print(click.style(" Write your update", fg="magenta", bold=True))
    time.sleep(0.3)
    updt = click.edit().rstrip()

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "UPDATE notes SET " + coluna + " = '" + updt + "' WHERE ntid = " + update_ident
        cur.execute(
            query,
        )
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()
    print(color(f'[*] - The update, "{updt}", was inserted on the database, with the id {update.ident}.', fore="#acac87"))


if __name__ == "__main__":
    update()
