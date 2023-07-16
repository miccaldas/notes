"""
Command line version of the 'add' function in Notes.
Here, debloated and adapted to work with file notes.
"""
import os
import pickle

import click

# import snoop
from mysql.connector import Error, connect
from notes.add.similar_tags import similar_tags
from notes.add.tag_lst import tag_lst

# from snoop import pp


# def type_watch(source, value):
#     return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])


@click.command()
@click.option("-t", "--title")
@click.option("-k", "--keywords", nargs=3)
@click.option("-n", "--note", is_flag=False, flag_value="note", default="note")
# @snoop
def add(title, keywords, note):
    # sourcery skip: for-append-to-extend, move-assign-in-block, simplify-generator, use-named-expression
    """
    Gets information through command line, sends it to the db.\n
    **Options:**\n
    -t  Enter the title string for the note.\n
    -k  Accepts three keyword values as individual strings.\n
    -n  Opens Vim so as to write a note.\n
    Called with **ntadd**.
    """

    tag_lst()
    npth = "/home/mic/python/notes/notes/notes"
    tmp_title = f"{npth}/replace.txt"

    if note:
        entry = click.edit()
    # As it's difficult to know what number MySQL will use for the new id,
    # we'll use a temporary one, 'replace', and change it after.
    with open(tmp_title, "w") as f:
        f.write(entry)

    k1, k2, k3 = keywords
    similar_tags(k1, k2, k3)
    with open("/home/mic/python/notes/notes/add/keywords.bin", "rb") as f:
        kwds = pickle.load(f)

    answers = [title]
    for k in kwds:
        answers.append(k)

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "INSERT INTO notes (title, k1, k2, k3) VALUES (%s, %s, %s, %s)"
        cur.execute(query, answers)
        conn.commit()
        # Searches for the last, highest value of ntid in Notes.
        query1 = "SELECT ntid FROM notes ORDER BY ntid DESC LIMIT 0, 1"
        cur.execute(query1)
        record = cur.fetchone()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    # Update the file name with MySQL's id number.
    os.rename(
        tmp_title,
        f"{npth}/{record[0]}.txt",
    )

    tags = "/home/mic/python/notes/notes/add/taglst.bin"
    keys = "/home/mic/python/notes/notes/add/keywords.bin"

    if tags:
        os.remove(tags)
    if keys:
        os.remove(keys)


if __name__ == "__main__":
    add()
