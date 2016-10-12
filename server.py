"""Slack Slash Command TicTacToe"""

from flask import Flask, request, make_response

import os

import json

import requests

from Model import (connect_to_db, db, Game, Emoji, Player)

# ___________________________________________________________________________

app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']

slack_token = os.environ['SLACK_TOKEN']

# ___________________________________________________________________________

# @app.route('/test', methods=['GET'])
# def test():
#     """Route to seed the database with valid emojis"""

    #     html = "<html><body>Testing testing, is this thing on?</body></html>"
    #  Pretty silly, but this is how I loaded my seed data into the Heroku 
    # database for the emojis because I was getting error messages from the 
    # Heroku python CLI

    # for row in (open("valid_emojis.txt")):
    #     row = row.rstrip()
    #     this_emoji = Emoji(emoji=row)
    #     db.session.add(this_emoji)
    #     db.session.commit()

    # return html

@app.route('/game.json', methods=['POST'])
def new_game():
    '''Processes slash commands to play Tic-Tac-Toe'''

    data = request.form
    token = data['token']
    query_text = data['text']
    team_id = data['team_id']
    channel_id = data['channel_id']
    token = data['token']
    team_domain = data['team_domain']
    user_id = data['user_id']
    username = data['user_name']
    if token != slack_token:
        return abort(403)
    elif query_text == "help":
        payload = {"text": "*How to play OXO Emoji Tic-Tac-Toe:*\n-Challenge anyone on your team to a game by entering `/ttt` and your opponents username in any channel, e.g. `/ttt @kenny`. There is one game per channel, at a time.\n- By default, your moves will show as :heavy_multiplication_x: and your opponents moves will show as :O:.  To change the emoji that represents your moves, type `/ttt` and the emoji you would like to use, e.g. `/ttt :alien:`. If the emoji you chose has aleady been chosen by another player, your emoji will not be updated.\n- Anyone can type `/ttt` at any time to show the game board and whose turn it is, but only the person whose turn it is can make a move.\n- To make your move, type `/ttt` and the number of the square you would like to claim, e.g. `/ttt 1`.\n- To end the game prematurely, type `/ttt catsgame`\n- To see this message again,type `/ttt help`\nThis:\n\n:one:|:two:|:three:\n:four:|:five:|:six:\n:seven:|:eight:|:nine:\n\n Quickly turns into this:\n\n :ghost:|:alien:|:three:\n:four:|:ghost:|:six:\n:alien:|:alien:|:ghost:"}
        json_payload = json.dumps(payload)
        response = make_response(json_payload)
        response.headers['content-type'] = 'application/json'
    elif query_text[0] == "@":
        return 'testing %s' % query_text

        # # return response
        # # query_text = data['text']
        # team_id = data['team_id']
        # channel_id = data['channel_id']
        # token = data['token']
        # team_domain = data['team_domain']
        # user_id = data['user_id']
        # username = data['user_name']

        # return 'query_text={0}, team_id={1}, channel_id={2}, channel_name={3}, token={4}, team_domain={5}, user_id={6}, username={7}'.format(query_text, team_id, channel_id, channel_name, token, team_domain, user_id, username)
    else:
        return 'I don\'t know that one. Enter \'/ttt help\' to see valid commands'


# ___________________________________________________________________________


if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    app.debug = True

    DEBUG = "NO_DEBUG" not in os.environ

    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
