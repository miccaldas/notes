"""
Shows content of table 'favorites'.
"""

# import snoop
# from snoop import pp
from colr import color
from mysql.connector import Error, connect
from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import get_lexer_by_name
from db_decorator.db_information import db_information
# def type_watch(source, value):
#   return "type({})".format(source), type(value)


# @snoop
@db_information
def see_favorites():
    """
    Uses MySQL query that selects all in
    the 'favorites' table.
    """

    lexer = get_lexer_by_name("toml")
    formatter = TerminalTrueColorFormatter(linenos=False, style="zenburn")
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT * FROM favorites"
        cur.execute(
            query,
        )
        records = cur.fetchall()
        for row in records:
            print(
                color(" [0] ID » ", fore="#bfbfbf"), color(str(row[0]), fore="#ffffff")
            )
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
                color(" [5] NOTE : \n\n", fore="#bfbfbf"),
                highlight(row[5], lexer, formatter),
            )
            print("\n")
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    see_favorites()
