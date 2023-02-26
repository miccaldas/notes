"""Collects user input, checks keywords for similarity, if they're new and their frequency.
Sends information to the database and creates the md and html pages."""
import time
from time import sleep

import click

# import snoop
import yake
from db_decorator.db_information import db_information
from mysql.connector import Error, connect
from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer  # noqa: F401

# from snoop import pp
from thefuzz import fuzz  # noqa: F401
from thefuzz import process

lexer = get_lexer_by_name("toml")
formatter = TerminalTrueColorFormatter(linenos=False, style="zenburn")


class Add:
    """The class starts with user input and a list with all tags in a string list.
    Having them separated will simplify processes. With this information collected,
    first we'll ask the keywords questions and run its processes, one by one.
    After this is done we'll send the information to the database and create the
    md and html files."""

    # @snoop
    def input_data(self):
        """All the user inputs needed to create a new entry are located here."""
        self.title = input(highlight(" Title? » ", lexer, formatter))
        print(highlight(" Write a note.", lexer, formatter))
        sleep(1)
        self.note = click.edit().rstrip()

    # @snoop
    def suggest_tags(self):
        """
        We'll use Yake to suggest keywords to the user. He may choose all, some
        or opt for writing them himself.
        """
        kw_extractor = yake.KeywordExtractor()
        text = self.note
        language = "en"
        max_ngram_size = 1
        deduplication_threshold = 0.9
        numOfKeywords = 10
        custom_kw_extractor = yake.KeywordExtractor(
            lan=language,
            n=max_ngram_size,
            dedupLim=deduplication_threshold,
            top=numOfKeywords,
            features=None,
        )
        keywords = custom_kw_extractor.extract_keywords(text)
        kwds = []
        for kw in keywords:
            kwds.append(kw[0])
        for idx, kwd in enumerate(kwds):
            print(highlight(f" {idx, kwd}", lexer, formatter))
        kwdcho = input(
            highlight(
                " If you want to keep any of three keywords, type their number. ",
                lexer,
                formatter,
            )
        )
        if kwdcho != "":
            kwdchoi = kwdcho.split(" ")
            kwd_choice = [int(i) for i in kwdchoi]
            choices = []
            for i in kwd_choice:
                choice = [(idx, val) for (idx, val) in enumerate(kwds) if idx == i]
                choices.append(choice)
            flatter_choices = [i for sublist in choices for i in sublist]
            kwd_names = [f[1] for f in flatter_choices]
            if len(kwd_names) == 1:
                self.k1 = kwd_names[0]
                self.k2 = input(highlight(" Choose a keyword » ", lexer, formatter))
                self.k3 = input(highlight(" Choose another... » ", lexer, formatter))
            if len(kwd_names) == 2:
                self.k1 = kwd_names[0]
                self.k2 = kwd_names[1]
                self.k3 = input(highlight(" Choose a keyword » ", lexer, formatter))
            if len(kwd_names) == 3:
                self.k1 = kwd_names[0]
                self.k2 = kwd_names[1]
                self.k3 = kwd_names[2]
        else:
            self.k1 = input(highlight(" Choose a keyword » ", lexer, formatter))
            self.k2 = input(highlight(" Choose another... » ", lexer, formatter))
            self.k3 = input(highlight(" And another... » ", lexer, formatter))

    @db_information
    # @snoop
    def taglst(self):
        """Union allows to combine two or more sets of results into one, but,
        the number and order of columns that appear in the SELECT statement
        must be the same, and the data types must be equal or compatible.
        Union removes duplicates.
        """
        try:
            conn = connect(
                host="localhost", user="mic", password="xxxx", database="notes"
            )
            cur = conn.cursor()
            query = "SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
            cur.execute(query)
            records = (
                cur.fetchall()
            )  # Results come as one-element tuples. It's needed to turn it to list.
            self.records = [i for t in records for i in t]
        except Error as e:
            err_msg = "Error while connecting to db", e
            print("Error while connecting to db", e)
            if err_msg:
                return query, err_msg
            return query, err_msg
        finally:
            if conn:
                conn.close()
            return query

    @db_information
    # @snoop
    def tag_links(self):
        """I'll join the three lists and order them by number of connections."""
        queries = [
            "SELECT k1, count(*) as links FROM notes GROUP BY k1",
            "SELECT k2, count(*) as links FROM notes GROUP BY k2",
            "SELECT k3, count(*) as links FROM notes GROUP BY k3",
        ]
        try:
            for q in queries:
                conn = connect(
                    host="localhost", user="mic", password="xxxx", database="notes"
                )
                cur = conn.cursor()
                query = q
                cur.execute(
                    query,
                )
            self.links = cur.fetchall()
            # Records is a list and row is a tuple with the tag name and number of connections.
            self.links.sort(
                key=lambda x: x[1]
            )  # This sorts the list by the value of the second element. https://tinyurl.com/yfn9alt7
        except Error as e:
            err_msg = "Error while connecting to db", e
            print("Error while connecting to db", e)
            if err_msg:
                return query, err_msg
        finally:
            if conn:
                conn.close()
            return query

    # @snoop
    def issimilar(self):
        """Uses Thefuzz library to compare keyword strings. If similarity is above 80%,
        it prints a mesage asking if the user wants to change it."""
        conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
        cur = conn.cursor()
        query = (
            "SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
        )
        cur.execute(query)
        records = (
            cur.fetchall()
        )  # Results come as one-element tuples. It's needed to turn it to list.
        self.records = [i for t in records for i in t]

        self.keywords = [self.k1, self.k2, self.k3]
        for k in self.keywords:
            value = process.extractOne(k, self.records)
            if (
                80 < value[1] < 100
            ):  # If we don't define it as less that 100, it will show message when inputing a old keyword.
                chg_tag_decision = input(
                    highlight(
                        f" You inputed the word {k}, that is similar to the word {value[0]}, that already is a keyword. Won't you use it instead? [y/n] ",
                        lexer,
                        formatter,
                    )
                )
                if chg_tag_decision == "y":
                    if k == self.k1:
                        self.k1 = value[0]
                    if k == self.k2:
                        self.k2 = value[0]
                    if k == self.k3:
                        self.k3 = value[0]
            else:
                pass

        return self.k1, self.k2, self.k3

    # @snoop
    def new_tag(self):
        """Will check the keyword names against the db records. If it doesn't find a
        match, it will produce a message saying the tag is new."""
        self.keywords = self.issimilar()
        for k in self.keywords:
            res = any(k in i for i in self.records)
            if not res:
                print(
                    highlight(
                        f" [*] - The keyword {k} is new in the database.",
                        lexer,
                        formatter,
                    )
                )
            else:
                pass

    @db_information
    # @snoop
    def count_links(self):
        try:
            """Will check the new keywords, see how many links they'll have, and return that
            information."""
            queries = [
                "SELECT k1, count(*) as links FROM notes GROUP BY k1",
                "SELECT k2, count(*) as links FROM notes GROUP BY k2",
                "SELECT k3, count(*) as links FROM notes GROUP BY k3",
            ]
            for q in queries:
                conn = connect(
                    host="localhost", user="mic", password="xxxx", database="notes"
                )
                cur = conn.cursor()
                query = q
                cur.execute(
                    query,
                )
            self.links = cur.fetchall()

            for i in self.links:
                if i[0] == self.k1:
                    new_i = list(i)
                    new_val = [new_i[0], (new_i[1] + 1)]
                    print(
                        highlight(
                            f" [*] - The updated value of the keyword links is {new_val}",
                            lexer,
                            formatter,
                        )
                    )
                if i[0] == self.k2:
                    new_i = list(i)
                    new_val = [new_i[0], (new_i[1] + 1)]
                    print(
                        highlight(
                            f" [*] - The updated value of the keyword links is {new_val}",
                            lexer,
                            formatter,
                        )
                    )
                if i[0] == self.k3:
                    new_i = list(i)
                    new_val = [new_i[0], (new_i[1] + 1)]
                    print(
                        highlight(
                            f" [*] - The updated value of the keyword links is {new_val}",
                            lexer,
                            formatter,
                        )
                    )
        except Error as e:
            err_msg = "Error while connecting to db", e
            print("Error while connecting to db", e)
            if err_msg:
                return queries, err_msg
        finally:
            if conn:
                conn.close()
            return queries

    @db_information
    # @snoop
    def add_to_db(self):
        """Sends the data to the database"""
        answers = [self.title, self.k1, self.k2, self.k3, self.note]
        try:
            conn = connect(
                host="localhost", user="mic", password="xxxx", database="notes"
            )
            cur = conn.cursor()
            query = "INSERT INTO notes (title, k1, k2, k3, note) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query, answers)
            conn.commit()
            # This was necessary because if I feed self.note directly to the query, MySQL will evaluate it as code not text.
            # Because 'db_information' can't decode '%s' contents, I needed to send query content in another way.
            nquery = f"INSERT INTO notes (title, k1, k2, k3, note) VALUES ({self.title}, {self.k1}, {self.k2}, {self.k3}, {self.note})"
        except Error as e:
            err_msg = "Error while connecting to db", e
            print("Error while connecting to db", e)
            if err_msg:
                return nquery, err_msg
        finally:
            if conn:
                conn.close()
            print(
                highlight(
                    f" [*] - The entry named: {self.title}, was added to the database.",
                    lexer,
                    formatter,
                )
            )
            return nquery

    # @snoop
    @db_information
    def kwd_clean(self):
        """
        Takes a list of all keywords, checks if there are
        plural versions of them, stores these cases in a
        list and updates them to the plural version.
        """
        try:
            conn = connect(
                host="localhost", user="mic", password="xxxx", database="notes"
            )
            cur = conn.cursor()
            query = "SELECT k1 FROM notes UNION SELECT k2 FROM notes UNION SELECT k3 FROM notes"
            cur.execute(query)
            records = (
                cur.fetchall()
            )  # Results come as one-element tuples. It's needed to turn it to list.
            records = [i for t in records for i in t]
            conn.close()
        except Error as e:
            err_msg = "Error while connecting to db", e
            print("Error while connecting to db", e)
            if err_msg:
                return query, err_msg

        records.sort()

        reps = []
        for i in records:
            plural = f"{i}s"
            if plural in records:
                reps.append((i, plural))

        if reps != []:
            try:
                conn = connect(
                    host="localhost", user="mic", password="xxxx", database="notes"
                )
                cur = conn.cursor()
                for rep in reps:
                    query1 = f"UPDATE notes SET k1 = '{rep[1]}' WHERE k1 = '{rep[0]}'"
                    cur.execute(query1)
                    conn.commit()
                    query2 = f"UPDATE notes SET k2 = '{rep[1]}' WHERE k2 = '{rep[0]}'"
                    cur.execute(query2)
                    conn.commit()
                    query3 = f"UPDATE notes SET k3 = '{rep[1]}' WHERE k3 = '{rep[0]}'"
                    cur.execute(query1)
                    conn.commit()
                conn.close()
            except Error as e:
                err_msg = "Error while connecting to db", e
                print("Error while connecting to db", e)
                if err_msg:
                    return query, err_msg

                return query
