""" Module that prints the content of the databse."""
import sys
from mysql.connector import connect, Error
from colr import color
from loguru import logger


fmt = "{time} - {name} - {level} - {message}"
logger.add("spam.log", level="DEBUG", format=fmt)
logger.add(sys.stderr, level="ERROR", format=fmt)


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
            print(color("[0] ID » ", fore="#4c873a"), color(str(row[0]), fore="#fffb96"))
            print(
                color("[1] TITLE » ", fore="#4c873a"),
                color(str(row[1]), fore="#fffb96"),
            )
            print(
                color("[2] KEYWORD 1 » ", fore="#4c873a"),
                color(str(row[2]), fore="#fffb96"),
            )
            print(
                color("[3] KEYWORD 2 » ", fore="#4c873a"),
                color(str(row[3]), fore="#fffb96"),
            )
            print(
                color("[4] KEYWORD 3 » ", fore="#4c873a"),
                color(str(row[4]), fore="#fffb96"),
            )
            print(color("[5] NOTE : ", fore="#4c873a"), color(str(row[5]), fore="#ff6969"))
            print(color("[6] URL » ", fore="#4c873a"), color(str(row[6]), fore="#fffb96"))
            print(color("[7] TIME » ", fore="#4c873a"), color(str(row[7]), fore="#fffb96"))
            print("\n")
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    see()
