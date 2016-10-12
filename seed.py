"""Utility file to seed Tic-Tac-Toe database with emojis"""

from Model import Emoji
from server import (app, db)

# "heroku run python manage.py shell" to access heroku's python shell to run this file


def load_emojis():
    """Loads the emojis that work on Slack and aren't being used"""

    print "Emojis:"

    for i, row in enumerate(open("valid_emojis.txt")):
        row = row.rstrip()
        this_emoji = Emoji(emoji=row)
        db.session.add(this_emoji)

    if i % 100 == 0:
        print i

    db.session.commit()
