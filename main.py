from __future__ import unicode_literals
import sys
import questionary
from questionary import Style
from add import Add
from delete import del_md_html_pages, delete
from search import search
from update import update, update_md_html_page
from see import see
from stats import tag_list, entries, tags
from loguru import logger


fmt = "{time} - {name} - {level} - {message}"
logger.add("spam.log", level="DEBUG", format=fmt)
logger.add(sys.stderr, level="ERROR", format=fmt)

notes_style = Style(
    [
        ("qmark", "fg:#004c4c bold"),
        ("question", "fg:#acac87 bold"),
        ("answer", "fg:#ffffff bold"),
        ("pointer", "fg:#b5c51b"),
        ("highlighted", "fg:#494a65 bold"),
        ("separator", "fg:#fffffF"),
    ]
)

resposta = questionary.select(
    "What do you want to do?",
    choices=[
        "Add a Note",
        "Search for a Note",
        "See Notes ",
        "Update a Note",
        "Delete a Note",
        "See Stats",
        "Exit",
    ],
    style=notes_style,
).ask()


if resposta == "Add a Note":
    add = Add()
    add.input_data()
    add.taglst()
    add.issimilar()
    add.add_to_db()
    add.add_md_page()
    add.add_html_page()
if resposta == "Search for a Note":
    search()
if resposta == "See Notes ":
    see()
if resposta == "Update a Note":
    update()
    update_md_html_page()
if resposta == "Delete a Note":
    del_md_html_pages()
    delete()
if resposta == "See Stats":
    tag_list()
    entries()
    tags()
if resposta == "Exit":
    sys.exit()
