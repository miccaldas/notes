""" Module to see all of the database """
from mysql.connector import connect, Error
from colr import color
import fire


def search():
    try:
        busca = input(color(' What are you searching for? ', fore='#40afb8'))
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
            print(color(' [0] ID » ', fore='#40afb8'), color(str(row[0]), fore='#eadcc8'))
            print(color(' [1] TITLE » ', fore='#40afb8'), color(str(row[1]), fore='#eadcc8'))
            print(color(' [2] KEYWORD 1 » ', fore='#40afb8'), color(str(row[2]), fore='#eadcc8'))
            print(color(' [3] KEYWORD 2 » ', fore='#40afb8'), color(str(row[3]), fore='#eadcc8'))
            print(color(' [4] KEYWORD 3 » ', fore='#40afb8'), color(str(row[4]), fore='#eadcc8'))
            print(color(' [5] NOTE » ', fore='#40afb8'), color(str(row[5]), fore='#ffbca5'))
            print(color(' [6] TIME » ', fore='#40afb8'), color(str(row[6]), fore='#eadcc8'))
            print('\n')
    except Error as e:
        print("Error while connecting to db", e)
    finally:
        if(conn):
            conn.close()


if __name__ == '__main__':
    fire.Fire(search)
