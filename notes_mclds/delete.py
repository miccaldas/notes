"""
Module to delete notes from the databases.
"""

import snoop
from colr import color
from db_decorator.db_information import db_information
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@db_information
# @snoop
def delete():
    """
    There are three ways in which you can delete:
    1. Delete multiple entries, specifying their ids.
    2. Delete range of ids.
    3. Delete just one id.
    """

    ident = input("ID to delete? ")

    # List declared here to avoid errors about being declared before assignment.
    split_lst = []
    if "," in ident:
        query = f"DELETE FROM notes WHERE ntid IN ({ident})"
    if "-" in ident:
        if " - " in ident:
            answers = ident.replace(" ", "")
            split_lst = answers.split("-")
        else:
            split_lst = ident.split("-")
        query = (
            f"DELETE FROM notes WHERE ntid BETWEEN {split_lst[0]} AND {split_lst[1]}"
        )
    if "," not in ident and "-" not in ident:
        query = f"DELETE FROM notes WHERE ntid = '{ident}'"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query
        cur.execute(query)
        conn.commit()
        conn.close()
    except Error as e:
        err_msg = "Error while connecting to db", e
        print("Error while connecting to db", e)
        if err_msg:
            return query, err_msg

    return query


if __name__ == "__main__":
    delete()
