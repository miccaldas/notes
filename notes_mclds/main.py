from __future__ import unicode_literals

import sys


import questionary
from questionary import Style


from add import Add
from delete import delete
from search import search
from see import see
from see_favorites import see_favorites
from stats import entries, tag_list, tags
from update import update


def main():
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
        style=notes_style,
        choices=[
            "Add a Note",
            "Search for a Note",
            "See Notes ",
            "Update a Note",
            "Delete a Note",
            "See Stats",
            "See Favorites",
            "Exit",
        ],
    ).ask()

    if resposta == "Add a Note":
        add = Add()
        add.input_data()
        add.suggest_tags()
        add.taglst()
        add.tag_links()
        add.new_tag()
        add.count_links()
        add.add_to_db()
        add.kwd_clean()
    if resposta == "Search for a Note":
        search()
    if resposta == "See Notes ":
        see()
    if resposta == "Update a Note":
        update()
    if resposta == "Delete a Note":
        delete()
    if resposta == "See Stats":
        tag_list()
        entries()
        tags()
    if resposta == "See Favorites":
        see_favorites()
    if resposta == "Exit":
        sys.exit()


if __name__ == "__main__":
    main()
