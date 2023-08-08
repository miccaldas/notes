"""
Module to do searches in db and, possibly, bookmarks.
"""
import os
import pickle
import subprocess
import time

import click
import snoop
from blessed import Terminal
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


# @snoop
def bks(qry):
    """
    In case the user chooses to add to the db's
    results those of 'bkmks', this function runs.
    """
    term = Terminal()
    query = "SELECT id, title, comment, link, k1, k2, k3, tempo FROM bkmks WHERE MATCH(title, comment, k1, k2, k3) AGAINST (%s) ORDER BY tempo"

    answers = [qry]
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
        cur = conn.cursor()
        cur.execute(query, answers)
        records = cur.fetchall()
    except Error as e:
        print(f"DB connection failed with error {e}")
    finally:
        if conn:
            conn.close()

    for record in records:
        record = (
            term.bold_lemonchiffon2(str(record[0])),
            term.bold_yellow4(record[1]),
            term.bold_lemonchiffon2(record[2]),
            term.bold_lightcoral(record[3]),
            term.bold_tan1("@")
            + term.bold_yellow4(f"{record[4]}")
            + term.bold_tan1(" @")
            + term.bold_yellow4(f"{record[5]}")
            + term.bold_tan1(" @")
            + term.bold_yellow4(f"{record[6]}"),
            term.bold_lemonchiffon2(record[7].strftime("%d-%m-%Y_%H:%M")),
        )
        for line in record:
            print("\n".join(term.wrap(line, width=160)))
        print("\n")


@click.command()
@click.argument("qry")
@click.option("-bk", "--bkmk", is_flag=False, flag_value="bookmark", default="y")
# @snoop
def search(qry, bkmk):
    """
    Receives search query, looks in db, and outputs to terminal with Blessed.\n
    Called with **ntsrch**.
    """

    records = []
    term = Terminal()
    answers = [qry]
    npth = "/home/mic/python/notes/notes/notes"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT ntid, title, k1, k2, k3, time FROM notes WHERE MATCH(title, k1, k2, k3) AGAINST (%s) ORDER BY time"
        cur.execute(query, answers)
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
    sep = "#" * 40
    print(term.bisque4(f"{sep} BOOKMARKS {sep}\n"))

    if bkmk == "y":
        bks(qry)


if __name__ == "__main__":
    search()
