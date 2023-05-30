"""
Command line version of Notes' delete function.
"""
import os

import click

# import snoop
from dotenv import load_dotenv
from mysql.connector import Error, connect

# from snoop import pp


# def type_watch(source, value):
#     return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])
load_dotenv()


@click.command()
@click.argument("ntid")
def delete(ntid):
    """
    Function that deletes one, several or range of entries in the 'notes' database.\n
    You can call it with **ntdlt** in the following forms:\n
    1. **Delete non sequential entries**. Surround the ids with quotation
       marks and separate them with a comma::

           ntdlt '435,436'

    2. **Delete sequential entries**. Envelop first and last ids with quotation
       marks and separate them with a dash::

           ntdlt '437-439'

    3. **Delete single entry**::

           ntdlt 66
    """
    npth = os.getenv("NOTE_PATH")

    split_lst = []
    if "," in ntid:
        # When inputing id strings to delete as a sole string, as it is convenient, MySQL
        # creates an error, since it expects a tuple of strings in the query. First we have
        # to split the id's at the comma. Splitting with space or space + comma doesn't work.
        lst = ntid.split(",")
        # Splitting creates empty spaces inside the strings. This eliminates them.
        nlst = [i.strip() for i in lst]
        for n in nlst:
            if f"{npth}/{n}.txt":
                os.remove(f"{npth}/{n}.txt")
            else:
                print(f"There is no note file with the id {n}.")
        # Finally we turn the list to tuple, the desired format by MySQL.
        nt = tuple(nlst)
        query = f"DELETE FROM notes WHERE ntid IN {nt}"

    if "-" in ntid:
        if " - " in ntid:
            answers = ntid.replace(" ", "")
            split_lst = answers.split("-")
        else:
            split_lst = ntid.split("-")
        query = f"DELETE FROM notes WHERE ntid BETWEEN {split_lst[0]} AND {split_lst[1]}"
        # Now we have to find a list of the range of entries to erase, for the files.
        # First we turn it to ints.
        intlst = [int(i) for i in split_lst]
        # Then we create the range. Remmeber that range doesn't include its higher limit.
        rng = range(intlst[0], (intlst[1] + 1))
        # Now we create the list range.
        nlst = list(rng)
        for n in nlst:
            if f"{npth}/{n}.txt":
                os.remove(f"{npth}/{n}.txt")
            else:
                print(f"There is no note file with the id {n}")

    if "," not in ntid and "-" not in ntid:
        if f"{npth}/{ntid}.txt":
            os.remove(f"{npth}/{ntid}.txt")
        else:
            print("There is no note file with the id {n}.")

        query = f"DELETE FROM notes WHERE ntid = {ntid}"

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    delete()
