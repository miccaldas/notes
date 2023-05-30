"""
Module to show content from the db, using note files.
"""
import os
import subprocess
import time

import click

# import snoop
from blessed import Terminal
from mysql.connector import Error, connect

# from snoop import pp


# def type_watch(source, value):
#     return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])


@click.command()
@click.option("-n", "--number", type=int)
# @snoop
def all(number):
    """
    When called without options, collects and shows the db's content.\n
    **Options:**\n
    -n  Integer defining how many of the more recent entries will be displayed. For example: **ntall -n 5**,
        returns the five latest entries in the database.\n
    Called with **ntall**.
    """

    npth = "/home/mic/python/notes/notes/notes"
    term = Terminal()

    if number:
        query = f"SELECT ntid, title, k1, k2, k3, time FROM notes ORDER BY ntid DESC LIMIT {number}"
    else:
        query = "SELECT ntid, title, k1, k2, k3, time FROM notes"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        cur.execute(query)
        records = cur.fetchall()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    for record in records:
        note = f"{npth}/{record[0]}.txt"
        cmd = f"pygmentize -l python -O style=zenburn {note}"
        record = (
            term.bold_lemonchiffon2(str(record[0])),
            term.bold_lemonchiffon2(record[1]),
            term.bold_tan1("@")
            + term.bold_yellow4(f"{record[2]}")
            + term.bold_tan1(" @")
            + term.bold_yellow4(f"{record[3]}")
            + term.bold_tan1(" @")
            + term.bold_yellow4(f"{record[4]}"),
            term.bold_lemonchiffon2(record[5].strftime("%d-%m-%Y_%H:%M")),
        )
        for line in record:
            print("\n".join(term.wrap(line, width=160)))
        subprocess.run(cmd, shell=True)
        print("\n")


if __name__ == "__main__":
    all()
