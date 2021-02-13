from mysql.connector import connect, Error
import click


def see():
    try:
        conn = connect(
                host="localhost",
                user="mic",
                password="xxxx",
                database="notes")
        cur = conn.cursor()
        query = 'SELECT * FROM notes'
        cur.execute(query,)
        records = cur.fetchall()
        for row in records:
            print(click.style('[0] ID » ', fg='cyan', bold=True), click.style(str(row[0]), fg='magenta', bold=True))
            print(click.style('[1] TITLE » ', fg='cyan', bold=True), click.style(str(row[1]), fg='magenta', bold=True))
            print(click.style('[2] KEYWORD 1 » ', fg='cyan', bold=True), click.style(str(row[2]), fg='magenta', bold=True))
            print(click.style('[3] KEYWORD 2 » ', fg='cyan', bold=True), click.style(str(row[3]), fg='magenta', bold=True))
            print(click.style('[4] KEYWORD 3 » ', fg='cyan', bold=True), click.style(str(row[4]), fg='magenta', bold=True))
            print(click.style('[5] NOTE : ', fg='cyan', bold=True), click.style(str(row[5]), fg='red', bold=True))
            print(click.style('[6] TIME » ', fg='cyan', bold=True), click.style(str(row[6]), fg='magenta', bold=True))
            print('\n')
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    see()
