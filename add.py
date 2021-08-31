""" Module to insert notes to database, create a markdown and html page
    for the web version of app."""
import sys
import time
import click
import subprocess
from mysql.connector import connect, Error
from loguru import logger

fmt = "{time} - {name} - {level} - {message}"
logger.add("spam.log", level="DEBUG", format=fmt)
logger.add(sys.stderr, level="ERROR", format=fmt)


@logger.catch
def add():
    """Collects the inputs and sends it to the db as a SQL query"""
    add.titulo = input(click.style(" Title? » ", fg="magenta", bold=True))
    kwd1 = input(click.style(" Choose a keyword » ", fg="magenta", bold=True))
    kwd2 = input(click.style(" Choose another... » ", fg="magenta", bold=True))
    kwd3 = input(click.style(" And another... » ", fg="magenta", bold=True))
    print(click.style(" Write a note.", fg="magenta", bold=True))
    time.sleep(0.2)
    nota = click.edit().rstrip()
    add.tit = add.titulo.replace(" ", "_")
    add.md_path = "/srv/http/notes/pages/markdown/" + add.tit + ".md"
    add.url = "http://localhost/notes/pages/html/" + add.tit + ".html"
    answers = [add.titulo, kwd1, kwd2, kwd3, nota, add.url]
    logger.info(answers)

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = """INSERT INTO notes (title, k1, k2, k3, note, url)
                VALUES (%s, %s, %s, %s, %s, %s)"""
        logger.info(query)
        cur.execute(query, answers)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    add()


@logger.catch
def add_md_page():
    """We create a new markdown file in its folder and write to it, the content
    of the meta-data, and the note."""
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "select * from notes order by ntid desc limit 1"
        cur.execute(
            query,
        )
        records = cur.fetchall()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    for row in records:
        id = row[0]
        titulo = row[1]
        time = row[7]
        k1 = row[2]
        k2 = row[3]
        k3 = row[4]
        nota = row[5]

    with open(add.md_path, "w") as f:
        f.write("---")
        f.write("\n")
        f.write("id: " + str(id))
        f.write("\n")
        f.write("title: " + titulo)
        f.write("\n")
        f.write("author: mclds")
        f.write("\n")
        f.write("time: " + str(time))
        f.write("\n")
        f.write("tags: " + k1 + ", " + k2 + ", " + k3)
        f.write("\n")
        f.write("---")
        f.write("\n")
        f.write(nota)


if __name__ == "__main__":
    add_md_page()


@logger.catch
def add_html_page():
    """Where we create a html version of the markdown file.
    We just convert the md file into an html one, and
    put it in the html folder."""

    html_path = "/srv/http/notes/pages/html/" + add.tit + ".html"

    cmd = (
        "pandoc --highlight-style=zenburn --metadata title="
        + add.titulo
        + " -s '"
        + add.md_path
        + "' -o '"
        + html_path
        + "'"
    )

    logger.info(cmd)
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    add_html_page()
