"""
Coloring each entry with Pygmentyze was taking a long time.
This version is quicker. *Pygmentyze* will still be visible on
the other commands.
"""
import os
import time

# import snoop
from blessed import Terminal
from mysql.connector import Error, connect

# from snoop import pp


# def type_watch(source, value):
#     return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def nall():
    """
    Collects and shows the db's content.\n
    Called with *nall*.
    """

    npth = "/home/mic/python/notes/notes/notes"
    term = Terminal()

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
        with open(note, "r") as f:
            note = f.read()
        print(" ")
        print(term.bold_lightgoldenrod1(note))
        print("\n")


if __name__ == "__main__":
    nall()
