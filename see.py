""" Module that prints the content of the databse."""
import sys
from mysql.connector import connect, Error
from colr import color
from loguru import logger


fmt = "{time} - {name} - {level} - {message}"
logger.add("see.log", level="INFO", format=fmt)
logger.add("see.log", level="ERROR", format=fmt)


@logger.catch
def see():
    """Connect to db, get all the lines and present it with colr."""
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT * FROM notes"
        cur.execute(
            query,
        )
        records = cur.fetchall()
        for row in records:
            print(color(" [0] ID » ", fore="#bfbfbf"), color(str(row[0]), fore="#ffffff"))
            print(
                color(" [1] TITLE » ", fore="#bfbfbf"),
                color(str(row[1]), fore="#ffffff"),
            )
            print(
                color(" [2] KEYWORD 1 » ", fore="#bfbfbf"),
                color(str(row[2]), fore="#ffffff"),
            )
            print(
                color(" [3] KEYWORD 2 » ", fore="#bfbfbf"),
                color(str(row[3]), fore="#ffffff"),
            )
            print(
                color(" [4] KEYWORD 3 » ", fore="#bfbfbf"),
                color(str(row[4]), fore="#ffffff"),
            )
            print(color(" [5] NOTE : ", fore="#bfbfbf"), color(str(row[5]), fore="#9f9989"))
            print(color(" [6] URL » ", fore="#bfbfbf"), color(str(row[6]), fore="#ffffff"))
            print(color(" [7] TIME » ", fore="#bfbfbf"), color(str(row[7]), fore="#ffffff"))
            print("\n")
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    see()
