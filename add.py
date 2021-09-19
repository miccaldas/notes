""" Module to insert notes to database, check for similar keyworda and create a markdown and html page
    for the web version of app."""
import sys
import time
import click
import subprocess
from colr import color
from loguru import logger
from thefuzz import fuzz
from thefuzz import process
from mysql.connector import connect, Error


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
    add.tit = add.titulo.replace(" ", "_").replace("'", "")  # Creates md and html title.
    add.md_path = "/srv/http/notes/pages/markdown/" + add.tit + ".md"
    add.url = "http://localhost/notes/pages/html/" + add.tit + ".html"

    answers = [add.titulo, kwd1, kwd2, kwd3, nota, add.url]
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = """INSERT INTO notes (title, k1, k2, k3, note, url)
                VALUES (%s, %s, %s, %s, %s, %s)"""
        cur.execute(query, answers)
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()
    print(color(f"[*] - The entry named: {add.titulo}, was added to the database.", fore="#acac87"))


if __name__ == "__main__":
    add()


def similar_kwd():
    """"""
    queries = [
        "SELECT k1, count(*) as links FROM notes GROUP BY k1",
        "SELECT k2, count(*) as links FROM notes GROUP BY k2",
        "SELECT k3, count(*) as links FROM notes GROUP BY k3",
    ]
    try:
        for q in queries:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = q
            cur.execute(
                query,
            )
        records = cur.fetchall()
        # Records is a list and row is a tuple with the tag name and number of connections.
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "select ntid, k1, k2, k3 from notes order by ntid desc limit 1"
        cur.execute(
            query,
        )
        tup_keys = cur.fetchall()
        keys = [i for t in tup_keys for i in t]  # Converts list of tuples to list.
        keys1 = keys[1:]  # Excludes the ntid value that is not needed and causes error messages.
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

        # Fuzzy string block.
        rec = [i for t in records for i in t]
        rec1 = rec[::2]  # It omits the integers relating to frequency. Otherwise generates an error.
        tup_process = []
        for k in keys1:
            tup_process.append(
                process.extract(k, rec1, limit=1)
            )  # Thefuzz command to run through lists. Shows only one result.
        tup_process = [i for sublist in tup_process for i in sublist]  # Flattens list of lists to a list.
        for i in tup_process:
            if i[1] > 80:
                chg_tag_decision = input(
                    color(
                        f"We have noticed that you inputed a word that is very similar to the word {i}, that we already have as a keyword. Won't you use it instead? [y/n] ",
                        fore="acac87",
                    )
                )
                if chg_tag_decision == "y":
                    for k in keys1:
                        if k == keys1[0]:
                            try:
                                conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
                                cur = conn.cursor()
                                query = "UPDATE notes SET k1 = '" + i[0] + "' WHERE ntid = " + str(keys[0])
                                cur.execute(
                                    query,
                                )
                                conn.commit()
                            except Error as e:
                                print("Error while connecting to db", e)
                            finally:
                                if conn:
                                    conn.close()
                        if k == keys1[1]:
                            try:
                                conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
                                cur = conn.cursor()
                                query = "UPDATE notes SET k2 = '" + i[0] + "' WHERE ntid = " + str(keys[0])
                                cur.execute(
                                    query,
                                )
                                conn.commit()
                            except Error as e:
                                print("Error while connecting to db", e)
                            finally:
                                if conn:
                                    conn.close()
                        if k == keys1[2]:
                            try:
                                conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
                                cur = conn.cursor()
                                query = "UPDATE notes SET k3 = '" + i[0] + "' WHERE ntid = " + str(keys[0])
                                cur.execute(
                                    query,
                                )
                                conn.commit()
                            except Error as e:
                                print("Error while connecting to db", e)
                            finally:
                                if conn:
                                    conn.close()

            else:
                pass


if __name__ == "__main__":
    similar_kwd()


@logger.catch
def add_md_page():
    """We create a new markdown file in its folder and write to it, the content
    of the meta-data, and the note."""
    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "select * from notes order by ntid desc limit 1"
        logger.info(query)
        cur.execute(
            query,
        )
        records = cur.fetchall()
        logger.info(records)
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
    print(color(f"[*] - It was created the markdown file named, {add.md_path}.", fore="#acac87"))


if __name__ == "__main__":
    add_md_page()


@logger.catch
def add_html_page():
    """Where we create a html version of the markdown file.
    We just convert the md file into an html one, and
    put it in the html folder."""

    html_path = "/srv/http/notes/pages/html/" + add.tit + ".html"
    cmd = "touch " + html_path
    subprocess.run(cmd, shell=True)

    cmd = (
        "pandoc --highlight-style=zenburn --metadata title='"
        + add.titulo
        + "' -s '"
        + add.md_path
        + "' -o '"
        + html_path
        + "'"
    )

    subprocess.run(cmd, shell=True)
    print(color(f"[*] - It was created the html file named, {add.url}.", fore="#acac87"))


if __name__ == "__main__":
    add_html_page()
