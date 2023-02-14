"""Module to delete notes from the database and connected files."""

from mysql.connector import connect, Error
from colr import color





def del_md_html_pages():
    """Deletes the markdown and html pages needed by the web version. It needs to go first
    because it must know the id field before its deleted."""



def delete():
    """After deleting the files, we can finally delete the database entry"""
    del_md_html_pages.ident = input("ID to delete? ")
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
