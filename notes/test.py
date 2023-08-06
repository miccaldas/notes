"""
Module to do searches in db and present the notes from files.
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


@click.command()
@click.argument("qry")
@click.option("-bk", "--bkmk", is_flag=False, flag_value="bookmark", default="n")
@snoop
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

    time.sleep(0.5)
    if bkmk == "y":
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = "SELECT id, title, comment, link, k1, k2, k3, tempo FROM bkmks WHERE MATCH(title, comment, k1, k2, k3) AGAINST (%s) ORDER BY tempo"
            cur.execute(query, answers)
            recs = cur.fetchall()
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

        for rec in recs:
            rec = (
                term.bold_lemonchiffon2(str(rec[0])),
                term.bold_lemonchiffon2(rec[1]),
                term.bold_lemonchiffon2(rec[2]),
                term.bold_lemonchiffon2(rec[3]),
                term.bold_tan1("@")
                + term.bold_yellow4(f"{rec[4]}")
                + term.bold_tan1(" @")
                + term.bold_yellow4(f"{rec[5]}")
                + term.bold_tan1(" @")
                + term.bold_yellow4(f"{rec[6]}"),
                term.bold_lemonchiffon2(rec[7].strftime("%d-%m-%Y_%H:%M")),
            )
            # print(term.bold_bisque4("  ############# BOOKMARKS ###############"))
            for line in rec:
                print("\n".join(term.wrap(line, width=160)))
            subprocess.run(cmd, shell=True)
            print("\n")


if __name__ == "__main__":
    search()
