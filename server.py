"""Slack Slash Command TicTacToe"""

from flask import Flask, request, jsonify

import os

import requests

from Model import (connect_to_db, db, Game, Emoji, Player)

# ___________________________________________________________________________

app = Flask(__name__)

app.secret_key = os.environ['APP_SECRET_KEY']

slack_token = os.environ['SLACK_TOKEN']

# ___________________________________________________________________________

show_help = {"text": "*How to play OXO Emoji Tic-Tac-Toe:*\n-Challenge anyone on your team to a game by entering `/ttt` and your opponents username in any channel, e.g. `/ttt kenny`. There is one game per channel, at a time.\n- By default, your moves will show as :heavy_multiplication_x: and your opponents moves will show as :O:.  To change the emoji that represents your moves, type `/ttt` and the emoji you would like to use, e.g. `/ttt :alien:`. If the emoji you chose has aleady been chosen by another player, your emoji will not be updated.\n- Anyone can type `/ttt` at any time to show the game board and whose turn it is, but only the person whose turn it is can make a move.\n- To make your move, type `/ttt` and the number of the square you would like to claim, e.g. `/ttt 1`.\n- To end the game prematurely, type `/ttt catsgame`\n- To see this message again,type `/ttt help`\nThis:\n\n:one:|:two:|:three:\n:four:|:five:|:six:\n:seven:|:eight:|:nine:\n\n Quickly turns into this:\n\n :ghost:|:alien:|:three:\n:four:|:ghost:|:six:\n:alien:|:alien:|:ghost:"}


@app.route('/test', methods=['GET'])
def test():
    """Testing to see if this site is deployed on Heroku"""

    html = "<html><body>Testing testing, is this thing on?</body></html>"
    #  Pretty silly, but this is how I loaded my seed data for the emojis
    #  because I had trouble with the Heroku python CLI

    # for row in (open("valid_emojis.txt")):
    #     row = row.rstrip()
    #     this_emoji = Emoji(emoji=row)
    #     db.session.add(this_emoji)
    #     db.session.commit()

    return html


@app.route('/game.json', methods=['POST', 'GET'])
def new_game():
    '''Processes slash commands to play Tic-Tac-Toe'''

    cheese = requests.get_json(force=True)
    stuff = open("json.txt", "w")
    stuff.write(cheese)
    stuff.close()



    # token = request.data["token"]
    # if token == slack_token:
    #     text = request.data["text"]
    #     if text == "help":
    #         return jsonify(show_help)
    #     team_domain = request.data["team_domain"]
    #     domain = team_domain
    #     channel_id = request.data["channel_id"]
    #     channel_name = request.data["channel_name"]
    #     user_id = request.data["user_id"]
    #     user_name = request.data["user_name"]
    #     if text[0] == "@":
    #         domain = Game(player_one_user_name=user_name,
    #                   player_two_user_name=text,
    #                   channel_name=channel_name,
    #                   player_one_user_id=user_id,
    #                   )
    # elif text[0] ==":":


    #     print (token, text, team_domain,
    #            team_domain,
    #            domain,
    #            channel_name,
    #            user_id,
    #            user_name,
    #            command,
    #            text,
    #            response_url)

    #     url = response_url
    #     headers = {'Content-type': 'application/json'}
    #     payload = {'text': 'Slash command recieved. Cats rule!'}
    #     r = requests.post(url, headers=headers, data=payload)

    #     print r

    #     return jsonify(payload), status.HTTP_200_OK
    # else:
    #     payload = {'text': 'Not a valid token.'}
    #     return jsonify(payload), status.HTTP_400_BAD_REQUEST

    # token = "gIkuvaNzQIHg97ATvDxqgjtO"
    # team_id = "T0001"
    # team_domain = "example"
    # channel_id = "C2147483705"
    # channel_name = "test"
    # user_id = "U2147483697"
    # user_name = "Steve"
    # command = "/weather"
    # text = "94070"
    # response_url = "https://hooks.slack.com/commands/1234/5678"

        # execute the command

        # If you'd like to add HTTP headers to a request, simply pass in a dict to the headers parameter.

        # For example, we didn't specify our user-agent in the previous example:

        # >>> url = 'https://api.github.com/some/endpoint'
        # >>> headers = {'user-agent': 'my-app/0.0.1'}

        # >>> r = requests.get(url, headers=headers)
        # Note: Custom headers are given less precedence than more specific sources of information. For instance:

         # r = requests.post('http://httpbin.org/post', data = {'key':'value'})'

         # http://flask.pocoo.org/docs/0.11/quickstart/#about-responses

    #     pass

    # else:
    #     # error message or pass. The request did not come from Slack.
    #     # "Additionally, you can verify whether the team_id matches a
    #     # team that has approved your command for usage.
    #     # If the token or team are unknown to your application, you should
    #     # refuse to service the request and return an error instead."
    #     pass

# ___________________________________________________________________________


if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    app.debug = True

    DEBUG = "NO_DEBUG" not in os.environ

    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
