""" Module to delete notes to database """

import sys
from mysql.connector import connect, Error
import click
from loguru import logger


fmt = "{time} - {name} - {level} - {message}"
logger.add("delete.log", level="DEBUG", format=fmt)
logger.add("delete.log", level="ERROR", format=fmt)


@logger.catch
def delete():
    ident = input(click.style(" ID to delete? » ", fg="magenta", bold=True))
    logger.info(ident)

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = " DELETE FROM notes WHERE ntid = " + ident
        logger.info(query)
        cur.execute(query)
        conn.commit()

    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    delete()
