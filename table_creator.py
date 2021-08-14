""" This module creates a SQLite database and defines and uploads a new table for said database"""
from mysql.connector import connect, Error
import collections
import re
from colr import color
from icecream import ic
from loguru import logger

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("info.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)

db_name = input(color("What name do you want for the database? ", fore="#585a47"))


def create_db():
    """Where we use the database name to create one."""

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        ic("Database created and Successfully Connected to MySQL")
        conn.commit()
    except Error as e:
        ic("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_db()


def collect_data():
    """Here we ask the user the information needed to create a table, then we process the output until is fit to be a SQL query, and uploaded it to the db"""

    a = collections.OrderedDict()
    table_name = input(color("What name do you want for the table? ", fore="#585a47"))
    col_num = int(input(color("How many columns will you need? ", fore="#ff6f69")))
    for y in range(col_num):
        col_name = input(color("What is the name of your column? ", fore="#ff6f69"))
        key = col_name
        a.setdefault(key, [])
        att_num = int(input(color("How many attributes will you need? ", fore="#ff6f69")))
        for x in range(att_num):
            att_name = input(color("What is the name of your attribute? ", fore="#ff6f69"))
            a[key].append(att_name)

    new = []
    for i in a:
        b = (i, a[i])
        logger.info(b)
        c = list(b)
        logger.info(c)
        new.append(str(c[0]))
        logger.info(new)
        d = str(c[1])
        logger.info(d)
        e = d.replace(",", "")
        logger.info(e)
        new.append(e)
    logger.info(new)
    corda = str(new)
    logger.info(corda)
    cor1 = corda.translate({ord(i): None for i in '[]""'})
    logger.info(cor1)
    cor2 = cor1.translate({ord(i): None for i in "'"})
    logger.info(cor2)
    sub = ","
    matches = re.finditer(sub, cor2)
    logger.info(matches)
    matches_positions = [match.start() for match in matches]
    oc = matches_positions
    logger.info(oc)
    oc1 = oc[0::2]
    logger.info(oc1)
    logger.info("oc1 = ", oc1)
    cor3 = list(cor2)
    logger.info(cor3)
    for idx in oc1:
        cor3[idx] = ""
    cor4 = "".join(cor3)
    logger.info(cor4)
    query = "CREATE TABLE " + table_name + "(" + cor4 + ")"
    logger.info(query)

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
    collect_data()
