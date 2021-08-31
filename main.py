from __future__ import unicode_literals
import sys
import questionary
from questionary import Style
from add import add
from delete import delete
from search import search
from update import update
from see import see
from add_md_page import add_md_page
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
        "Exit",
    ],
    style=notes_style,
).ask()


if resposta == "Add a Note":
    add()
    add_md_page()
if resposta == "Search for a Note":
    search()
if resposta == "See Notes ":
    see()
if resposta == "Update a Note":
    update()
if resposta == "Delete a Note":
    delete()
if resposta == "Exit":
    sys.exit()
