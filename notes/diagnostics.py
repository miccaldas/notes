"""
Module that'll do some housekeeping on the bookmarks db.
"""
# import snoop
from mysql.connector import Error, connect

# from snoop import pp

# import os
# import subprocess
from thefuzz import fuzz, process


# def type_watch(source, value):
#     return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])


class Diagnostics:
    """
    Here we'll house methods that'll analyze keywords that are
    too similar, repeated content and empty lines.
    """

    def __init__(self):
        pass

    # @snoop
    def kwd_lst(self):
        """
        Creates a set of keywords from bkmks, taken
        from k1, k2 and k3.
        """
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = "SELECT k1 FROM notes UNION DISTINCT SELECT k2 FROM notes UNION DISTINCT SELECT k3 FROM notes"
            cur.execute(query)
            records = cur.fetchall()
            recs = [i for t in records for i in t]
            rec = [i.strip() for i in recs]
        except Error as e:
            print("Error while connecting to db ", e)
        finally:
            if conn:
                conn.close()

        self.records = [i for i in rec if len(i) >= 2]

    # @snoop
    def kwd_similarity(self):
        """
        We analyze the keywords to find repeated values.
        I took the resulting list from the output because
        it took so long to run, and I don't want to run it
        again. I'll just clean the results in mycli.
        """
        val_lst = []
        for i in range(len(self.records)):
            vals = process.extract(self.records[i], self.records)
            values = [val for val in vals if val[1] >= 95 and val[1] <= 100]
            if len(values) > 1:
                val_lst.append(values)

        print(val_lst)


dgs = Diagnostics()
dgs.kwd_lst()
dgs.kwd_similarity()
