"""
Permits saving an entry in favorites table.
For ease of access.
"""
import click
from db_decorator.db_information import db_information
# import snoop
from mysql.connector import Error, connect
# from snoop import pp


"""def type_watch(source, value):
    return "type({})".format(source), type(value)"""



@click.command()
@click.option("-a", "--add", type=int)
@click.option("-d", "--delete", type=int)
@click.option("--delete_all/--no_delete_all", default=False)
# @snoop
@db_information
def favorites(add, delete, delete_all):
    """
    To create a favorite entry, the user inputs an id, and
    we copy the corresponding entry to the 'favorites' table.
    We use MySQL commands to delete one/some or all entries.
    """

    if add:
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = f"INSERT INTO favorites (ntid, title, k1, k2, k3, note) SELECT ntid, title, k1, k2, k3, note FROM notes WHERE ntid = {add}"
            cur.execute(query)
            conn.commit()
        except Error as e:
            print("Error while connecting to the db", e)
        finally:
            if conn:
                conn.close()
        print(click.style(f" [*] - The note with the id {add} was inserted in favorites.", fg="bright_white", bold=True))

    if delete:
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = f"DELETE FROM favorites WHERE ntid = {delete}"
            cur.execute(query)
            conn.commit()
        except Error as e:
            print("Error while connecting to the db", e)
        finally:
            if conn:
                conn.close()
        print(click.style(f" [*] - The note with the ntid {add} was deleted from favorites.", fg="bright_white", bold=True))

    if delete_all:
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = "DELETE FROM favorites"
            cur.execute(query)
            conn.commit()
        except Error as e:
            err_msg = "Error while connecting to the db", e
            print("Error while connecting to the db", e)
            if err_msg:
                return query, e
        finally:
            if conn:
                conn.close()
            print(click.style(" [*] - All notes in favorites were deleted.", fg="bright_white", bold=True))
            return query

if __name__ == "__main__":
    favorites()
