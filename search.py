""" Module to see all of the database """
from mysql.connector import connect, Error
import click
import fire


def search():
    try:
        busca = input(click.style(' What are you searching for? ', fg='magenta', bold=True))
        conn = connect(
            host="localhost",
            user="mic",
            password="xxxx",
            database="notes")
        cur = conn.cursor()
        query = " SELECT ntid, title, k1, k2, k3, note, time FROM notes WHERE MATCH(title, k1, k2, k3, note) AGAINST ('" + busca + "' IN NATURAL LANGUAGE MODE)"
        cur.execute(query)
        records = cur.fetchall()
        for row in records:
            print(click.style(' [0] ID » ', fg='cyan', bold=True), click.style(str(row[0]), fg='blue', bold=True))
            print(click.style(' [1] TITLE » ', fg='cyan', bold=True), click.style(str(row[1]), fg='blue', bold=True))
            print(click.style(' [2] KEYWORD 1 » ', fg='cyan', bold=True), click.style(str(row[2]), fg='blue', bold=True))
            print(click.style(' [3] KEYWORD 2 » ', fg='cyan', bold=True), click.style(str(row[3]), fg='blue', bold=True))
            print(click.style(' [4] KEYWORD 3 » ', fg='cyan', bold=True), click.style(str(row[4]), fg='blue', bold=True))
            print(click.style(' [5] NOTE » ', fg='cyan', bold=True), click.style(str(row[5]), fg='blue', bold=True))
            print(click.style(' [6] TIME » ', fg='cyan', bold=True), click.style(str(row[6]), fg='blue', bold=True))
            print('\n')
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    fire.Fire(search)
