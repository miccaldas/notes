"""Module will aggregate disparate statisitcs about the app."""

from colr import color
from mysql.connector import connect, Error
from db_decorator.db_information import db_information


@db_information
def tag_list():
    """I'll join the three lists and order them by number of connections."""
    queries = [
        "SELECT k1, count(*) as links FROM notes GROUP BY k1",
        "SELECT k2, count(*) as links FROM notes GROUP BY k2",
        "SELECT k3, count(*) as links FROM notes GROUP BY k3",
    ]
    try:
        for q in queries:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = q
           
            cur.execute(
                query,
            )
        records = cur.fetchall()
        # Records is a list and row is a tuple with the tag name and number of connections.

        records.sort(
            key=lambda x: x[1]
        )  # This sorts the list by the value of the second element. https://tinyurl.com/yfn9alt7
        records = [i for t in records for i in t]
        it = iter(records)  # Solution to intercalate colorization, taken from here https://tinyurl.com/ygpwdrcl
        for x, y in zip(it, it):
            print(color("  " + x, fore="#acac87")), print(color("  " + str(y), fore="#f18892"))
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    tag_list()



def entries():
    """Returns the number of entries in the database"""
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT COUNT(*) FROM notes"
        cur.execute(
            query,
        )
        records = cur.fetchall()
        records = [i for t in records for i in t]
        records = str(records)
        records = records[1:-1]
        tag_num = int(records) * 3
        print("\n")
        print(color(f"  The number of database entries is {records}", fore="#a5a590"))
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    entries()



def tags():
    """Counts all keywords without duplications"""
    queryk1 = "SELECT COUNT(DISTINCT k1) FROM notes"
    queryk2 = "SELECT COUNT(DISTINCT k2) FROM notes"
    queryk3 = "SELECT COUNT(DISTINCT k3) FROM notes"
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = queryk1
        cur.execute(
            query,
        )
        recordk1 = cur.fetchone()

        query = queryk2
        cur.execute(
            query,
        )
        recordk2 = cur.fetchone()

        query = queryk3
        cur.execute(
            query,
        )
        recordk3 = cur.fetchone()

        soma = tuple(map(sum, zip(recordk1, recordk2, recordk3)))  # Taken from here: https://tinyurl.com/y35we4g7
        soma = str(soma)
        soma = soma[1:-2]
        print(color(f"  The number of tags in the database is {soma}", fore="a5a590"))

    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    tags()
