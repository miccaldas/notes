"""Module that'll house all cleaning tasks needed."""

from loguru import logger
from get_tag_list import get_tag_list

fmt = "{time} - {name} - {level} - {message}"
logger.add("info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)
logger.add("error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)


@logger.catch
def clean_tag_list():
    """
    There is little to do here. Just doid a join operation so we have
    strings to work with, and we're set.
    """

    tags = list(get_tag_list())
    join_tags = []
    for i in range(0, len(tags)):
        join = "".join(tags[i])
        join_tags.append(join)
        # print(f"join_tag value is {join}")
    return join_tags


if __name__ == "__main__":
    clean_tag_list()
