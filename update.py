""" Module to update notes to database """
import sys
import time
import subprocess
from mysql.connector import connect, Error
import click
from colr import color
from loguru import logger


fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt)
logger.add("info.log", level="ERROR", format=fmt)


@logger.catch
def update():
    coluna = input(click.style(" Column? » ", fg="magenta", bold=True))
    update.ident = input(click.style(" ID? » ", fg="magenta", bold=True))
    print(click.style(" Write your update", fg="magenta", bold=True))
    time.sleep(0.3)
    updt = click.edit().rstrip()

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "UPDATE notes SET " + coluna + " = '" + updt + "' WHERE ntid = " + update.ident
        cur.execute(
            query,
        )
        conn.commit()
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()
    print(
        color(f'[*] - The update, "{updt}", was inserted on the database, with the id {update.ident}.', fore="#acac87")
    )


if __name__ == "__main__":
    update()


@logger.catch
def update_md_html_page():
    """We delete the current markdown page and create a new one with the
    updated content. We create a html page from the markdown, using pandoc."""

    try:
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = "SELECT * FROM notes WHERE ntid = " + update.ident
        cur.execute(
            query,
        )
        fields = cur.fetchall()

        for row in fields:
            id = row[0]
            titulo = row[1]
            time = row[7]
            k1 = row[2]
            k2 = row[3]
            k3 = row[4]
            nota = row[5]

            tit = titulo.replace(" ", "_")
            md_path = "/srv/http/notes/pages/markdown/" + tit + ".md"
            cmd = "rm " + md_path
            subprocess.run(cmd, shell=True)

            with open(md_path, "w") as f:
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

            html_path = "/srv/http/notes/pages/html/" + tit + ".html"

            cmd = (
                "pandoc --highlight-style=zenburn --metadata title='"
                + titulo
                + "' -s '"
                + md_path
                + "' -o '"
                + html_path
                + "'"
            )
            subprocess.run(cmd, shell=True)

    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if conn:
            conn.close()

    print(color(f"[*] - The files, markdown and html, with the {tit} title, were updated.", fore="#acac87"))


if __name__ == "__main__":
    update_md_html_page()
