"""
Collects all tags in k1, k2, k3 with no duplicates.
"""
import pickle

# import snoop
from mysql.connector import Error, connect

# from snoop import pp


# def type_watch(source, value):
#     return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def tag_lst():
    """
    Union allows to combine two or more sets of results into one, but,
    the number and order of columns that appear in the SELECT statement
    must be the same, and the data types must be equal or compatible.
    Union removes duplicates.
    """
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
        cur.execute(query)
        records = cur.fetchall()  # Results come as one-element tuples. It's needed to turn it to list.
        records = [i for t in records for i in t]
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    with open("/home/mic/python/notes/notes/add/taglst.bin", "wb") as f:
        pickle.dump(records, f)
