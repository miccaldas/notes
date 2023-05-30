"""
Command line implementation of the update funtion on Notes.
"""
import os
import subprocess

import click

# import snoop
from mysql.connector import Error, connect

# from snoop import pp


# def type_watch(source, value):
#     return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])


@click.command()
@click.option("-n", "--ntid", type=int)
@click.option("-c", "--column")
@click.option("-u", "--updt")
# @snoop
def update(ntid, column, updt):
    """
    Updates the value of some column in a given id.\n
    **Options:**\n
    -n  Integer of the ntid value.\n
    -c  Column to update.\n
    -u  String with the update. If you chosen 'note' in 'column', it'll open a Vim page for you to edit it.\n
    Called with **ntupdt**.
    """

    npth = "/home/mic/python/notes/notes/notes"
    note_file = f"{npth}/{ntid}.txt"

    if column == "note":
        if note_file:
            cmd = f"/usr/bin/vim {note_file}"
            subprocess.run(cmd, shell=True)
        else:
            print(f"There's no note file with the id {ntid}.")
    else:
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = f"UPDATE notes SET {column} = '{updt}' WHERE ntid = {ntid}"
            cur.execute(query)
            conn.commit()
            conn.close()
        except Error as e:
            print("Error while connecting to db", e)


if __name__ == "__main__":
    update()
