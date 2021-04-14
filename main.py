from __future__ import unicode_literals
import sys
import questionary
from add import add
from delete import delete
from search import search
from update import update
from see import see


resposta = questionary.select(
    'What do you want to do?',
    choices=[
        'Add a Note',
        'Search for a Note',
        'See Notes ',
        'Update a Note',
        'Delete a Note',
        'Exit'
            ]).ask()

if resposta == 'Add a Note':
    add()
if resposta == 'Search for a Note':
    search()
if resposta == 'See Notes ':
    see()
if resposta == 'Update a Note':
    update()
if resposta == 'Delete a Note':
    delete()
if resposta == 'Exit':
    sys.exit()
