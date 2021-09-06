"""Module to download all the keywords/tags from the database."""
from loguru import logger
from mysql.connector import connect, Error

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch
def get_tag_list():
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
        logger.info(query)
        cur.execute(query)
        records = cur.fetchall()
        return records
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    get_tag_list()
