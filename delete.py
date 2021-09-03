"""Module to delete notes from the database and connected files."""
from loguru import logger
import os
import subprocess
from mysql.connector import connect, Error
from colr import color

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch
def del_md_html_pages():
    """Deletes the markdown and html pages needed by the web version. It needs to go first
    because it must know the id field before its deleted."""
    del_md_html_pages.ident = input("ID to delete? ")

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT url FROM notes WHERE ntid = " + del_md_html_pages.ident
        cur.execute(query)
        record = cur.fetchone()
        path = record[0]
        filename = os.path.basename(path)
        file_short = filename[:-5]
        html_page = "/srv/http/notes/pages/html/" + file_short + ".html"
        md_page = "/srv/http/notes/pages/markdown/" + file_short + ".md'"
        cmd = "rm '" + html_page + "'; " + "rm '" + md_page
        subprocess.run(cmd, shell=True)
    except Error as e:
        print("Error while connecting to the db", e)
    finally:
        if conn:
            conn.close()
    print(color(f"Files related to the {file_short} title were deleted.", fore="#acac87"))


if __name__ == "__main__":
    del_md_html_pages()


@logger.catch
def delete():
    """After deleting the files, we can finally delete the database entry"""
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = " DELETE FROM notes WHERE ntid = " + del_md_html_pages.ident
        cur.execute(query)
        conn.commit()

    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()
    print(color(f"The database entry number {del_md_html_pages.ident} was deleted.", fore="#acac87"))


if __name__ == "__main__":
    delete()
