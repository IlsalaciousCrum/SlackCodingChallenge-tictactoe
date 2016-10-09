"""Slack Slash Command TicTacToe"""

from flask import Flask, request, json

from Model import (Game)

import valid_emojis

import os

app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']

# ___________________________________________________________________________


@app.route('/hello')
def say_hello():
    html = "<html><body>Hello</body></html>"
    return html

# ___________________________________________________________________________


if __name__ == "__main__":

    app.debug = True

    app.run(host="0.0.0.0")
