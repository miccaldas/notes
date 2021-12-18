""" Module to see all of the database """
import fire
from colr import color
from loguru import logger
from mysql.connector import Error, connect

fmt = "{time} - {name} - {level} - {message}"
logger.add("../logs/search.log", level="INFO", format=fmt)
logger.add("../logs/search.log", level="ERROR", format=fmt)


def search():
    try:
        busca = input(color(" What are you searching for? ", fore="#40afb8"))
        logger.info(busca)
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = (
            " SELECT ntid, title, k1, k2, k3, note, url, time FROM notes WHERE MATCH(title, k1, k2, k3, note, url) AGAINST ('"
            + busca
            + "' )"
        )
        logger.info(query)
        cur.execute(query)
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
            print(
                color(" [5] NOTE » ", fore="#bfbfbf"),
                color(str(row[5]), fore="#9f9998"),
            )
            print(color(" [6] URL » ", fore="#bfbfbf"), color(str(row[6]), fore="#ffffff"))
            print(
                color(" [7] TIME » ", fore="#bfbfbf"),
                color(str(row[7]), fore="#ffffff"),
            )
            print("\n")
    except Error as e:
        print("Error while connecting to db", e)


if __name__ == "__main__":
    fire.Fire(search)
