""" Module that prints the content of the databse."""
from colr import color
from db_decorator.db_information import db_information
from mysql.connector import Error, connect
from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer  # noqa: F401



@db_information
def see():
    """Connect to db, get all the lines and present it with colr."""

    lexer = get_lexer_by_name("toml")
    formatter = TerminalTrueColorFormatter(linenos=False, style="zenburn")
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
            print(color(" [5] NOTE : \n\n", fore="#bfbfbf"), highlight(row[5], lexer, formatter))
            print(color(" [6] URL » ", fore="#bfbfbf"), color(str(row[6]), fore="#ffffff"))
            print(color(" [7] TIME » ", fore="#bfbfbf"), color(str(row[7]), fore="#ffffff"))
            print("\n")
    except Error as e:
        print("Error while connecting to db", e)


if __name__ == "__main__":
    see()
