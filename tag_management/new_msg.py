"""Module where we'll create a class with some functions who share outputs.."""
from mysql.connector import connect, Error
from loguru import logger
from colr import color
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from tag_management.get_tag_list import get_tag_list

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


class TagOutput:
    def __init__(self, k1, k2, k3):
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3

    @logger.catch
    def tag_list(self):
        """I'll join the three lists and order them by number of connections."""
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
                logger.info(query)
                cur.execute(
                    query,
                )
            self.records = cur.fetchall()
            records = cur.fetchall()
            # Records is a list and row is a tuple with the tag name and number of connections.

            self.records.sort(
                key=lambda x: x[1]
            )  # This sorts the list by the value of the second element. https://tinyurl.com/yfn9alt7
        except Error as e:
            print("Error while connecting to db", e)
        finally:
            if conn:
                conn.close()

    if __name__ == "__main__":
        tag_list()

    @logger.catch
    def new_msg(self):
        """Verifies if the tag was already present in database or not.
        Sends results to next method and builds a message with that
        information."""

        lnk_num = self.records
        id = [i for i in range(len(lnk_num))]

        self.cases = []
        for x in enumerate([self.k1, self.k2, self.k3]):
            for self.i in id:
                lnk = lnk_num[self.i][0]
                comp = x[1] == lnk
                if comp:
                    self.cases.append(x[1])
                else:
                    new = ""
        if new:
            print(f"the tag {x} is new.")

    @logger.catch
    def count_connections(self):
        """Gets information from the last method regarding what tags were
        repeated, looks for it in the database, and outputs the new
        connections value."""
        connections = self.records

        for i in self.cases:
            idx = [
                x for x, tup in enumerate(connections) if tup[0] == i
            ]  # Comprehension that returns the indexes of tuples.
            for x in range(len(idx)):
                connect = connections[x][1] + 1
            logger.info(connect)
            conn_answer = f"The tuple {i} has now {connect} connections."
            print(conn_answer)

    @logger.catch
    def string_closeness(self):
        """"""

        fuzz_lt = []
        for k in [self.k1, self.k2, self.k3]:
            for i in self.close:
                fuzz_lt.append((i[0], fuzz.ratio(k, i)))
        print(fuzz_lt)
        if fuzz.ratio(k, i) < 80:
            pass
        else:
            chg_tag_decision = input(
                f"We have noticed that you inputed the word {k}, that is very similar to the word {i},\
                that we already have as a keyword. Won't you use it instead? [y/n]"
            )
            if chg_tag_decision == "y":
                k = i
            else:
                pass


# to = TagOutput("tuple", "index", "indexes")
# to.tag_list()
# to.new_msg()
# to.count_connections()
# to.string_closeness()
