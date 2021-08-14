""" Module to see all of the database """
import sys
from mysql.connector import connect, Error
from colr import color
import fire
from loguru import logger


fmt = "{time} - {name} - {level} - {message}"
logger.add("search.log", level="INFO", format=fmt)
logger.add("search.log", level="ERROR", format=fmt)


def search():
    try:
        busca = input(color(" What are you searching for? ", fore="#40afb8"))
        logger.info(busca)
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = (
            " SELECT ntid, title, k1, k2, k3, note, url, time FROM notes WHERE MATCH(title, k1, k2, k3, note) AGAINST ('"
            + busca
            + "' )"
        )
        logger.info(query)
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            print(color(" [0] ID » ", fore="#4c873a"), color(str(row[0]), fore="#fffb96"))
            print(
                color(" [1] TITLE » ", fore="#4c873a"),
                color(str(row[1]), fore="#fffb96"),
            )
            print(
                color(" [2] KEYWORD 1 » ", fore="#4c873a"),
                color(str(row[2]), fore="#fffb96"),
            )
            print(
                color(" [3] KEYWORD 2 » ", fore="#4c873a"),
                color(str(row[3]), fore="#fffb96"),
            )
            print(
                color(" [4] KEYWORD 3 » ", fore="#4c873a"),
                color(str(row[4]), fore="#fffb96"),
            )
            print(
                color(" [5] NOTE » ", fore="#4c873a"),
                color(str(row[5]), fore="#ff6969"),
            )
            print(color(" [6] URL » ", fore="#4c873a"), color(str(row[6]), fore="#fffb96"))
            print(
                color(" [7] TIME » ", fore="#4c873a"),
                color(str(row[7]), fore="#fffb96"),
            )
            print("\n")
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    fire.Fire(search)
