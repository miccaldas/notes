"""
Analyzes note text, looking for keywords. collects list.
Detects if the users' tags are very similar to pre-existing
ones. Suggests changing them to the old ones, or to the ones
it found now. This is here to avoid having tags in plural
and singular form or the same word written differently.
"""
import pickle

import click

# import snoop
from snoop import pp
from thefuzz import fuzz, process


# def type_watch(source, value):
#     return "type({})".format(source), type(value)


# snoop.install(watch_extras=[type_watch])


# @snoop
def similar_tags(key1, key2, key3):
    """
    Uses Thefuzz library to compare keyword strings.
    If similarity is above 95%, it prints a mesage
    asking the user if he wants to change it.
    """

    entries = []
    with open("/home/mic/python/notes/notes/add/taglst.bin", "rb") as f:
        while True:
            try:
                entries.append(pickle.load(f))
            except EOFError:
                break
    flat_entries = [i for sublst in entries for i in sublst]
    kws = [key1, key2, key3]
    for k in kws:
        value = process.extractOne(k, flat_entries)
        if 90 <= value[1] < 100:
            chgtag = input(
                click.style(
                    f"You entered the word '{k}', that's similar to the word '{value[0]}', which is already a keyword. Won't you use it instead? [y/n] ",
                    fg=(228, 147, 147),
                    bold=True,
                )
            )
            if chgtag == "y":
                if k == key1:
                    key1 = value[0]
                if k == key2:
                    key2 = value[0]
                if k == key3:
                    key3 = value[0]

    keywords = [key1, key2, key3]

    with open("/home/mic/python/notes/notes/add/keywords.bin", "wb") as f:
        pickle.dump(keywords, f)
